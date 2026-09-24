from ia import perguntar

while True:

    mensagem = input("Você: ")

    if mensagem.lower() in ["sair", "exit", "quit"]:
        break

    resposta = perguntar(mensagem)

    print("Kyara:", resposta)