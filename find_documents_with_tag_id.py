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


# Check if the tag to be removed is set in the config
generate_titel_tag_config = config.paperless.get('generate_titel_tag')
generate_titel_tag = int(generate_titel_tag_config) if generate_titel_tag_config else None

# Check if the tag is in the configuration
if generate_titel_tag is not None:
    # Find documents with the specified tag
    documents = find_documents_with_tag_id(generate_titel_tag)
    if documents:
        # Print the number of documents found with the tag
        print(f"Found: {len(documents)} documents with tag: {generate_titel_tag}")
        # Start editing the documents
        print('Begin editing the documents.')
        total_documents = len(documents)
        # Iterate through the documents
        for index, doc_id in enumerate(documents, start=1):
            print('#############################')
            # Print the current document being processed
            print(f'Start processing document {index} of {total_documents}.')
            process_document(str(doc_id))
    else:
        # If no documents are retrieved
        print("No documents retrieved.")
else:
    # If generate_titel_tag is not specified in the configuration
    print("No generate_titel_tag specified in the configuration.")