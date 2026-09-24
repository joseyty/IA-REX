import sys
import threading

from PySide6.QtWidgets import QApplication

from personagem import criar_personagem
from dispositivos import dispositivos
from usuarios import usuarios
from voz import falar
from voz_reconhecimento import ouvir
from ia import perguntar

import comandos


def falar_kyara(personagem, mensagem):
    print("Kyara:", mensagem)

    try:
        personagem.falando()
        falar(mensagem)

    except Exception as erro:
        print("[VOZ] Erro:", erro)

    finally:
        personagem.parou_de_falar()


def processar_mensagem(mensagem, personagem):

    mensagem = mensagem.strip()

    if not mensagem:
        return

    print("\nVocê:", mensagem)

    # Primeiro tenta executar um comando do computador
    try:

        resposta = comandos.executar(mensagem)

        if resposta:
            falar_kyara(personagem, resposta)
            return

    except Exception as erro:

        print("[COMANDOS] Erro:", erro)

    # Se não for um comando, manda para a IA
    try:

        resposta = perguntar(mensagem)

        if resposta:
            falar_kyara(personagem, resposta)

    except Exception as erro:

        print("[OLLAMA] Erro:", erro)

        falar_kyara(
            personagem,
            "Tive um problema para pensar nessa resposta."
        )


def loop_assistente(personagem):

    print()
    print("==============================")
    print("       KYARA INICIADA")
    print("==============================")
    print()

    # Identificação do dispositivo
    id_dispositivo = input("Digite o ID do dispositivo: ")

    if id_dispositivo not in dispositivos:

        print("Dispositivo não cadastrado.")
        return

    dispositivo = dispositivos[id_dispositivo]

    nome_usuario = dispositivo["usuario"]
    voz_usuario = dispositivo["voz"]

    usuario = usuarios[nome_usuario]

    print()
    print("--- Dispositivo identificado ---")
    print("Usuário:", usuario["nome"])
    print("Voz:", voz_usuario)
    print()

    falar_kyara(
        personagem,
        f"Olá {usuario['nome']}. Eu sou a Kyara."
    )

    while True:

        try:

            # Agora a entrada vem do microfone
            mensagem = ouvir()

            if not mensagem:
                continue

            mensagem_minuscula = mensagem.lower()

            if mensagem_minuscula in [
                "sair",
                "encerrar",
                "fechar kyara"
            ]:

                falar_kyara(
                    personagem,
                    "Até mais!"
                )

                break

            processar_mensagem(
                mensagem,
                personagem
            )

        except KeyboardInterrupt:

            print("\n[KYARA] Encerrando...")
            break

        except Exception as erro:

            print("[ASSISTENTE] Erro:", erro)


app = QApplication(sys.argv)

personagem = criar_personagem()


thread = threading.Thread(
    target=loop_assistente,
    args=(personagem,),
    daemon=True
)

thread.start()


sys.exit(app.exec())