import requests
import os
import config

DOCUMENT_ID = os.getenv('DOCUMENT_ID')
print('Processing document with ID ' + DOCUMENT_ID)

# Collect document information from paperless
print('Reading document details for document ' + DOCUMENT_ID + " from paperless.")
url_template = config.paperless['base_url'] + config.paperless['document_path']
document_url = url_template.format(document_id=DOCUMENT_ID)

paperless_auth_header = {'Authorization': 'Token ' + config.paperless['api_key']}
document_response = requests.get(document_url, headers=paperless_auth_header)
document_json = document_response.json()

original_document_content = document_json['content']
original_document_title = document_json['title']

# # Send content to GPT and ask for title
print('Asking OpenAI model ' + config.openAI['model'] + ' for a title.')
headers = {
    'Authorization': 'Bearer ' + config.openAI['api_key'],
    'Content-Type': 'application/json',
    'OpenAI-Organization': config.openAI['organization']
}
request = {
    "model": config.openAI['model'],
    "messages": [
        {
            "role": "system",
            "content": "You are specialized on reading text and returning a title for it."
        },
        {
            "role": "system",
            "content": "You do not mention dates, amounts of money or correspondents in the title."
        },
        {
            "role": "system",
            "content": "You never answer with titles that are longer than 128 characters."
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
openai_response = requests.post(config.openAI['base_url'], headers=headers, json=request)
openai_response_json = openai_response.json()

open_ai_title = openai_response_json['choices'][0]['message']['content']
print("OpenAI title suggestion: " + open_ai_title)

# Update Title and add note
print('Saving original title of document with ID ' + DOCUMENT_ID + ' as note.')
document_original_title_note_request = {
    'note': 'Original title: ' + original_document_title
}
result = requests.post(document_url + "notes/", json=document_original_title_note_request, headers=paperless_auth_header)
if not result.ok:
    raise AssertionError("Adding original title as note failed.")

print('Updating title of document with ID ' + DOCUMENT_ID )
document_title_request = {
    'title': open_ai_title
}
result = requests.patch(document_url, json=document_title_request, headers=paperless_auth_header)
if not result.ok:
    raise AssertionError("Updating title failed.")

print('Finished')

