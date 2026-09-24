import sys

from PySide6.QtWidgets import QApplication
from dispositivos import dispositivos
from usuarios import usuarios
from voz import falar
import comandos
from personagem import criar_personagem

app = QApplication(sys.argv)
personagem = criar_personagem()

id_dispositivo = input("Digite o ID do dispositivo: ")

if id_dispositivo in dispositivos:
    dispositivo = dispositivos[id_dispositivo]

    nome_usuario= dispositivo["usuario"]
    voz_usuario = dispositivo["voz"]

    usuario = usuarios[nome_usuario]


    print("\n--- Dispositivo identificado ---")
    print("Usuario:", usuario["nome"])
    print("Voz:", voz_usuario)
    while True:
        # 1. Pede o comando
        meu_comando = input("Digite o que quer fazer: ")
        
        # 2. Manda para o comandos.py trabalhar
        resposta = comandos.executar(meu_comando)
        
        # 3. Faz o REX falar o que o comandos.py devolveu
        falar(resposta)

else:
    print("Dispositivo não cadastrado,cadastre.")
