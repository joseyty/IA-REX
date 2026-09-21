import edge_tts
import asyncio
import os

VOZ = "pt-BR-AntonioNeural"

async def gerar_audio(texto):
    comunicacao = edge_tts.Communicate(texto, VOZ)
    await comunicacao.save("resposta.mp3")


def falar(texto):
    asyncio.run(gerar_audio(texto))
    os.startfile("resposta.mp3")