import ollama

def Airorav2():
    print("Bienvenido a Airora, el asistente de vuelo virtual. Escribe Bye para Salir")
    print("Por favor, Escribe Que necesitas_:")

    while True:
        user_input = input('Tu: ')
        if user_input.lower== "bye":
            print("Hasta luego")
            break

        response = ollama.generate(model='Xekend/Chat:latest', prompt=user_input,)
            
        print('Airora: ', response['response'])

Airorav2()