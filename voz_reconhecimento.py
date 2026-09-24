import json
import queue
import time

import sounddevice as sd
from vosk import Model, KaldiRecognizer

from comandos import executar

# ==============================
# CONFIGURAÇÕES
# ==============================

CAMINHO_MODELO = r"C:\Users\lmelo\Downloads\vosk-model-small-pt-0.3\vosk-model-small-pt-0.3"

DEVICE = 15
SAMPLE_RATE = 48000
BLOCK_SIZE = 24000

fila_audio = queue.Queue()

# ==============================
# CALLBACK DO MICROFONE
# ==============================

def callback(indata, frames, time_info, status):
    if status:
        print("Áudio:", status)

    fila_audio.put(bytes(indata))

# ==============================
# OUVIR
# ==============================

def ouvir():
    print("🎤 Ouvindo...")

    modelo = Model(CAMINHO_MODELO)
    reconhecedor = KaldiRecognizer(modelo, 16000)

    with sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        blocksize=BLOCK_SIZE,
        device=DEVICE,
        dtype="int16",
        channels=1,
        callback=callback,
    ):
        while True:
            dados = fila_audio.get()
            if not dados:
                continue

            audio = bytearray(dados)

            # 48 kHz → aproximadamente 16 kHz
            audio_16k = audio[::3]

            if reconhecedor.AcceptWaveform(bytes(audio_16k)):
                resultado = json.loads(reconhecedor.Result())
                texto = resultado.get("text", "").strip()

                if texto:
                    print("Você:", texto)
                    return texto

# ==============================
# ASSISTENTE
# ==============================

def iniciar_assistente():
    print("=" * 40)
    print("             IA REX")
    print("       Assistente iniciado")
    print("=" * 40)

    while True:
        try:
            texto = ouvir()

            if not texto:
                continue

            if texto in [
                "sair",
                "encerrar",
                "fechar assistente",
                "desligar assistente",
            ]:
                print("REX: Encerrando assistente.")
                break

            resposta = executar(texto)
            print("REX:", resposta)

        except KeyboardInterrupt:
            print("\nREX: Assistente encerrado.")
            break

        except Exception as erro:
            print("Erro:", erro)
            time.sleep(1)

# ==============================
# INICIAR PROGRAMA
# ==============================

if __name__ == "__main__":
    iniciar_assistente()