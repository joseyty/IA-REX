import sys
import threading

from PySide6.QtWidgets import QApplication

from dispositivos import dispositivos
from usuarios import usuarios
from voz import falar
import comandos
from personagem import criar_personagem


app = QApplication(sys.argv)

personagem = criar_personagem()


def loop_assistente():

    id_dispositivo = input("Digite o ID do dispositivo: ")

    if id_dispositivo in dispositivos:

        dispositivo = dispositivos[id_dispositivo]

        nome_usuario = dispositivo["usuario"]
        voz_usuario = dispositivo["voz"]

        usuario = usuarios[nome_usuario]

        print("\n--- Dispositivo identificado ---")
        print("Usuario:", usuario["nome"])
        print("Voz:", voz_usuario)

        while True:

            meu_comando = input("Digite o que quer fazer: ")

            resposta = comandos.executar(meu_comando)

            personagem.falando()

            falar(resposta)

            personagem.parou_de_falar()

    else:

        print("Dispositivo não cadastrado, cadastre.")


thread = threading.Thread(
    target=loop_assistente,
    daemon=True
)

thread.start()

sys.exit(app.exec())