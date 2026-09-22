import edge_tts
import asyncio
import os
import time

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame

VOZ = "pt-BR-AntonioNeural"

pygame.mixer.init()


async def gerar_audio(texto):
    comunicacao = edge_tts.Communicate(texto, VOZ)
    await comunicacao.save("resposta.mp3")


def falar(texto):
    asyncio.run(gerar_audio(texto))

    pygame.mixer.music.load("resposta.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    pygame.mixer.music.unload()
