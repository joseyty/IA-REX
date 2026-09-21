import edge_tts
import asyncio

async def teste():
    voz = "pt-BR-AntonioNeural"
    texto = "Olá Igor, está funcionando"

    comunicacao = edge_tts.Communicate(texto, voz)
    await comunicacao.save("teste.mp3")

    print("Áudio criado!")

asyncio.run(teste())
