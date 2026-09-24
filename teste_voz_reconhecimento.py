from voz_reconhecimento import ouvir


while True:

    texto = ouvir()

    if texto.lower() in ["sair", "encerrar"]:
        break