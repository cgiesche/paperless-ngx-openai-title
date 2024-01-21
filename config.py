openAI = dict(
    api_key='',
    organization='',
    language='german',  # Request answer in this language

    model='gpt-3.5-turbo-1106',
    base_url='https://api.openai.com/v1/chat/completions'
)

paperless = dict(
    title_pattern='',  # Skip update if current title does _not_ match this pattern.
    api_key='',
    base_url='https://your-paperless:1234'
)
