import openai
from api_secrets import API_KEY_OPENAI


def ask_chatbot(prompt):
    
    client = openai.OpenAI(api_key=API_KEY_OPENAI)

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": prompt}
        ]
    )
    response = completion.choices[0].message.content
    return response
