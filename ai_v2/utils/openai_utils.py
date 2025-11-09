def chatgpt_response(client, messages):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=300,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()
