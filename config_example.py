openAI = dict(
    api_key='',
    organization='',
    language='german',  # Request answer in this language

    model='gpt-4-0125-preview', # gpt-3.5-turbo-1106
    base_url='https://api.openai.com/v1/chat/completions'
)

paperless = dict(
    title_pattern='',  # Skip update if current title does _not_ match this pattern.
    api_key='',
    base_url='https://your-paperless:1234',
    generate_titel_tag=''   # If provided, only documents with this tag id will be processed and the tag will then be removed.
)
