import sys
import threading

from PySide6.QtWidgets import QApplication

from dispositivos import dispositivos
from usuarios import usuarios
from voz import falar
import comandos

from personagem import criar_personagem
from visor import iniciar_visor_thread


# ============================================================
# APLICAÇÃO QT
# ============================================================

app = QApplication(sys.argv)


# ============================================================
# CRIAR PERSONAGEM
# ============================================================

personagem = criar_personagem()


# ============================================================
# INICIAR VISOR
# ============================================================

iniciar_visor_thread(personagem)


# ============================================================
# LOOP PRINCIPAL DO ASSISTENTE
# ============================================================

def loop_assistente():

    id_dispositivo = input(
        "Digite o ID do dispositivo: "
    )

    if id_dispositivo in dispositivos:

        dispositivo = dispositivos[id_dispositivo]

        nome_usuario = dispositivo["usuario"]
        voz_usuario = dispositivo["voz"]

        usuario = usuarios[nome_usuario]

        print("\n--- Dispositivo identificado ---")
        print(
            "Usuario:",
            usuario["nome"]
        )

        print(
            "Voz:",
            voz_usuario
        )

        while True:

            meu_comando = input(
                "Digite o que quer fazer: "
            )

            if not meu_comando.strip():
                continue

            try:

                resposta = comandos.executar(
                    meu_comando
                )

                personagem.falando()

                falar(resposta)

                personagem.parou_de_falar()

            except Exception as erro:

                print(
                    "[ASSISTENTE] Erro:",
                    erro
                )

                personagem.parou_de_falar()

    else:

        print(
            "Dispositivo não cadastrado, cadastre."
        )


# ============================================================
# THREAD DO ASSISTENTE
# ============================================================

thread = threading.Thread(
    target=loop_assistente,
    daemon=True
)

thread.start()


# ============================================================
# INICIAR QT
# ============================================================

sys.exit(app.exec())