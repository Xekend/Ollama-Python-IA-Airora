import ollama

messages=[
    {
    'role': 'user', 
    'content': 'Hola, puedes presentarte? con un limite de 200 palabras'
     },
    ]


stream = ollama.chat(model='Xekend/Chat:latest', messages=messages, stream=True)


for chunk in stream:
    print(chunk['message']['content'], end='', flush=True)

