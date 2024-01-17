import json
import os

import requests

import config_local as config

paperless_base_url = config.paperless['base_url']
paperless_auth_header = {'Authorization': 'Token ' + config.paperless['api_key']}

DOCUMENT_ID = os.getenv('DOCUMENT_ID')
print('Processing document with ID ' + DOCUMENT_ID)

# Read Correspondents
correspondents_url = paperless_base_url + '/api/correspondents/?&page_size=300'
correspondents = requests.get(correspondents_url, headers=paperless_auth_header)
correspondent_names = [{"id": obj['id'], "name": obj['name']} for obj in correspondents.json()['results']]
print(json.dumps(correspondent_names))

# Collect document information from paperless
print('Reading document details for document ' + DOCUMENT_ID + " from paperless.")
document_url_template = paperless_base_url + '/api/documents/{document_id}/'
document_url = document_url_template.format(document_id=DOCUMENT_ID)
document_response = requests.get(document_url, headers=paperless_auth_header)
document_json = document_response.json()

original_document_content = document_json['content']
original_document_title = document_json['title']

# Send content to GPT and ask for title
print('Asking OpenAI model ' + config.openAI['model'] + ' for a title.')
openai_auth_headers = {
    'Authorization': 'Bearer ' + config.openAI['api_key'],
    'Content-Type': 'application/json',
    'OpenAI-Organization': config.openAI['organization']
}
request = {
    "model": config.openAI['model'],
    "messages": [
        {
            "role": "system",
            "content": "You are specialized on analyzing text and are able to extract a title and a correspondent."
        },
        {
            "role": "system",
            "content": "You always answer with valid JSON."
        }
        , {
            "role": "system",
            "content": "You return the ID of the item that matches the correspondent of the text. If no item matches, you return -1 as correspondent and optional a suggestion in the correspondent_suggestion field. Here the list of known correspondents as JSON array:\n" + json.dumps(correspondent_names)
        },
        {
            "role": "system",
            "content": "You do not mention dates, amounts of money or correspondents in the title."
        },
        {
            "role": "system",
            "content": "The title must not be longer than 128 characters."
        },
        {
            "role": "system",
            "content": "You return titles in the same language as the text was in."
        },
        {
            "role": "user",
            "content": original_document_content
        }
    ],
    "temperature": 0.7
}
openai_response = requests.post(config.openAI['base_url'], headers=openai_auth_headers, json=request)
openai_response_json = openai_response.json()

open_ai_response_content = openai_response_json['choices'][0]['message']['content']
print("OpenAI title suggestion: " + open_ai_response_content)

# # Update Title and add note
# print('Saving original title of document with ID ' + DOCUMENT_ID + ' as note.')
# document_original_title_note_request = {
#     'note': 'Original title: ' + original_document_title
# }
# result = requests.post(document_url + "notes/", json=document_original_title_note_request, headers=paperless_auth_header)
# if not result.ok:
#     raise AssertionError("Adding original title as note failed.")
#
# print('Updating title of document with ID ' + DOCUMENT_ID )
# document_title_request = {
#     'title': open_ai_response_content
# }
# result = requests.patch(document_url, json=document_title_request, headers=paperless_auth_header)
# if not result.ok:
#     raise AssertionError("Updating title failed.")
#
# print('Finished')
#
