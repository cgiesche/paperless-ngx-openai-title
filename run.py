import requests
import config

from generate_title import process_document


def find_documents_with_tag_id(tag_id):
    paperless_base_url = config.paperless['base_url']
    paperless_auth_header = {'Authorization': 'Token ' + config.paperless['api_key']}
    
    # Start URL
    documents_url = f"{paperless_base_url}/api/documents/?is_tagged=true&tags__id__all={tag_id}&fields=id"

    all_document_ids = []

    while documents_url:
        # Make a GET request to the Paperless API
        response = requests.get(documents_url, headers=paperless_auth_header)


        # Check for successful response
        if response.status_code == 200:
            data = response.json()
            document_ids = [doc['id'] for doc in data['results']]
            all_document_ids.extend(document_ids)
            
            
            # Update the URL for the next page, if it exists
            documents_url = data.get('next', None)

        elif response.status_code == 404:
            print("No documents found for the specified tag.")
            return None
        else:
            print(f"Error: Received status code {response.status_code}")
            return None

    return all_document_ids



generate_titel_tag = config.paperless['generate_titel_tag']

# check if tag is given
if generate_titel_tag:
    documents = find_documents_with_tag_id(generate_titel_tag)
    if documents:
        print(f"Found: {len(documents)} documents with tag: {generate_titel_tag}")
        for doc_id in documents:
            process_document(str(doc_id))
    else:
        print("No documents retrieved.")
else:
    print("No generate_titel_tag specified in the configuration.")


