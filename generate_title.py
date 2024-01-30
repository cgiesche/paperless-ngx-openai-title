import os
import re

import requests

import config

def process_document(document_id):
    print(f'Document ID {document_id}: Processing document')

    paperless_base_url = config.paperless['base_url']
    paperless_auth_header = {'Authorization': 'Token ' + config.paperless['api_key']}

    # Collect document information from paperless
    print(f'Document ID {document_id}: Reading document details from paperless.')
    document_url_template = paperless_base_url + '/api/documents/{document_id}/'
    document_url = document_url_template.format(document_id=document_id)
    document_response = requests.get(document_url, headers=paperless_auth_header)
    if document_response.status_code == 404:
        print(f'Document ID {document_id}: Document does not exist!')
        exit(0)

    document_json = document_response.json()

    original_document_content = document_json['content']
    original_document_title = document_json['title']
    original_document_tags = document_json['tags']

    # Check if title matches filter
    title_pattern = config.paperless['title_pattern']
    if not re.match(title_pattern, original_document_title):
        print(f'Document ID {document_id}: Current title "{original_document_title}" does not match pattern "{title_pattern}". Skipping.')
        exit(0)

    # Send content to GPT and ask for title
    openai_api_key = config.openAI['api_key']
    openai_organization = config.openAI['organization']

    openai_auth_headers = {
        'Authorization': f'Bearer {openai_api_key}',
        'Content-Type': 'application/json',
        'OpenAI-Organization': openai_organization
    }
    openai_model = config.openAI['model']
    openai_language = config.openAI['language']
    system_role_message = "You are an expert in analyzing texts. Your task is to create a title for " \
                        "the text provided by the user. Be aware that the text may result from an OCR " \
                        "process and contain imprecise segments. Avoid mentioning dates, any form of " \
                        "monetary values or specific names (such as individuals or organizations) in the " \
                        "title. Ensure the title does never exceed 128 characters." \
                        "Do not add or insert any special characters at the beginning and end of the title." \
                        "A bad example is 'title' or '/title/'." \
                        "Most importantly, generate the title in " + openai_language + "."

    request = {
        "model": openai_model,
        "messages": [
            {"role": "system", "content": system_role_message},
            {"role": "user", "content": original_document_content}
        ],
        "temperature": 0.7
    }
    openai_response = requests.post(config.openAI['base_url'], headers=openai_auth_headers, json=request)
    openai_response_json = openai_response.json()

    open_ai_response_content = openai_response_json['choices'][0]['message']['content']
    print(f'Document ID {document_id}: OpenAI title suggestion: ' + open_ai_response_content)

    # Update Title and add note
    print(f'Document ID {document_id}: Saving original title of document as note.')
    document_original_title_note_request = {
        'note': f'Original title: {original_document_title}'
    }
    result = requests.post(document_url + "notes/", json=document_original_title_note_request, headers=paperless_auth_header)
    if not result.ok:
        raise AssertionError("Adding original title as note failed.")

    # print(f'Document ID {document_id}: Updating title and tags of document')

    # Check if the tag to be removed is set in the config
    tag_id_to_remove_config = config.paperless.get('generate_titel_tag')
    tag_id_to_remove = int(tag_id_to_remove_config) if tag_id_to_remove_config else None

    # Only update tags if the tag to be removed is set
    if tag_id_to_remove is not None:
        # Remove the specific tag from the list
        updated_tags = [tag for tag in original_document_tags if tag != tag_id_to_remove]
        
        # Prepare the data for the update (both title and tags)
        patch_data = {
            'title': open_ai_response_content,  # New title
            'tags': updated_tags  # Updated tag list
        }
    else:
        # Prepare the data for the update (title only)
        patch_data = {
            'title': open_ai_response_content  # New title
        }

    # Perform the PATCH request
    update_response = requests.patch(document_url, json=patch_data, headers=paperless_auth_header)

    # Check the result of the request
    if update_response.status_code == 200:
        if tag_id_to_remove is not None:
            print(f'Document ID {document_id}: Successfully updated title and tags.')
        else:
            print(f'Document ID {document_id}: Successfully updated title.')
    else:
        print(f'Document ID {document_id}: Error updating the document! Status code {update_response.status_code}')


    print(f'Document ID {document_id}: Finished')

if __name__ == "__main__":
    DOCUMENT_ID = os.getenv('DOCUMENT_ID')
    if DOCUMENT_ID:
        process_document(DOCUMENT_ID)
    else:
        print("No document ID provided.")

