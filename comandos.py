import os
import time
import webbrowser
from urllib.parse import quote_plus

import pyautogui


# =========================================================
# CONFIGURAÇÃO
# =========================================================

pyautogui.PAUSE = 0.3


# =========================================================
# APLICATIVOS
# =========================================================

def abrir_aplicativo(nome):
    pyautogui.press("win")
    time.sleep(0.5)

    pyautogui.write(nome)
    time.sleep(0.8)

    pyautogui.press("enter")
    time.sleep(2)


def abrir_youtube(comando=""):
    print("Abrindo YouTube...")

    pesquisa = ""

    palavras = comando.lower().split()

    if "youtube" in palavras:
        posicao = palavras.index("youtube")
        pesquisa = " ".join(palavras[posicao + 1:])

    if pesquisa:
        url = "https://www.youtube.com/results?search_query=" + quote_plus(pesquisa)
        webbrowser.open(url)
        return f"Pesquisando {pesquisa} no YouTube."

    webbrowser.open("https://www.youtube.com")
    return "YouTube aberto. Bom vídeo!"


def abrir_google(comando=""):
    print("Abrindo Google...")

    pesquisa = ""

    palavras = comando.lower().split()

    if "google" in palavras:
        posicao = palavras.index("google")
        pesquisa = " ".join(palavras[posicao + 1:])

    if pesquisa:
        url = "https://www.google.com/search?q=" + quote_plus(pesquisa)
        webbrowser.open(url)
        return f"Pesquisando {pesquisa} no Google."

    webbrowser.open("https://www.google.com")
    return "Google aberto. Boa busca!"


def abrir_spotify():
    print("Abrindo Spotify...")
    abrir_aplicativo("spotify")
    return "Spotify aberto. Solta o som, DJ!"


def abrir_vscode():
    print("Abrindo VS Code...")
    abrir_aplicativo("Visual Studio Code")
    return "Boa programação!"


def abrir_fortnite():
    print("Abrindo Fortnite...")

    try:
        abrir_aplicativo("Epic Games")
        time.sleep(5)
        return "Epic Games aberta. Cuidado com o Geno, boa sorte looper."
    except Exception as e:
        return f"Erro ao abrir a Epic Games: {e}"


def abrir_chrome():
    abrir_aplicativo("Google Chrome")
    return "Chrome aberto."


def abrir_edge():
    abrir_aplicativo("Microsoft Edge")
    return "Edge aberto."


def abrir_discord():
    abrir_aplicativo("Discord")
    return "Discord aberto."


def abrir_steam():
    abrir_aplicativo("Steam")
    return "Steam aberto."


def abrir_minecraft():
    abrir_aplicativo("Minecraft")
    return "Minecraft aberto."


def abrir_valorant():
    abrir_aplicativo("Riot Client")
    return "Riot Client aberto."


# =========================================================
# FERRAMENTAS DO WINDOWS
# =========================================================

def abrir_explorador():
    pyautogui.hotkey("win", "e")
    return "Explorador de arquivos aberto."


def abrir_configuracoes():
    pyautogui.hotkey("win", "i")
    return "Configurações abertas."


def abrir_gerenciador():
    pyautogui.hotkey("ctrl", "shift", "esc")
    return "Gerenciador de tarefas aberto."


def abrir_downloads():
    caminho = os.path.join(os.path.expanduser("~"), "Downloads")
    os.startfile(caminho)
    return "Downloads aberto."


def abrir_documentos():
    caminho = os.path.join(os.path.expanduser("~"), "Documents")
    os.startfile(caminho)
    return "Documentos aberto."


def abrir_bloco_notas():
    abrir_aplicativo("Bloco de Notas")
    return "Bloco de notas aberto."


# =========================================================
# VOLUME E MÍDIA
# =========================================================

def aumentar_volume():
    pyautogui.press("volumeup", presses=3)
    return "Volume aumentado."


def diminuir_volume():
    pyautogui.press("volumedown", presses=3)
    return "Volume diminuído."


def silenciar():
    pyautogui.press("volumemute")
    return "Volume alterado."


def pausar_musica():
    pyautogui.press("playpause")
    return "Música pausada."


def proxima_musica():
    pyautogui.press("nexttrack")
    return "Próxima música."


def musica_anterior():
    pyautogui.press("prevtrack")
    return "Voltando para a música anterior."


# =========================================================
# CONTROLE DO WINDOWS
# =========================================================

def bloquear_pc():
    os.system("rundll32.exe user32.dll,LockWorkStation")
    return "Computador bloqueado."


def desligar_pc():
    os.system("shutdown /s /t 10")
    return "O computador será desligado em 10 segundos."


def reiniciar_pc():
    os.system("shutdown /r /t 10")
    return "O computador será reiniciado em 10 segundos."


def cancelar_desligamento():
    os.system("shutdown /a")
    return "Desligamento cancelado."


# =========================================================
# ARQUIVOS E PASTAS
# =========================================================

def criar_pasta():
    nome = input("Nome da pasta: ")
    caminho = os.path.join(os.path.expanduser("~"), "Desktop", nome)
    os.makedirs(caminho, exist_ok=True)
    return f"Pasta {nome} criada na área de trabalho."


def criar_arquivo():
    nome = input("Nome do arquivo: ")

    if not nome.endswith(".txt"):
        nome += ".txt"

    caminho = os.path.join(os.path.expanduser("~"), "Desktop", nome)

    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write("")

    return f"Arquivo {nome} criado."


def bloco_de_notas():
    texto = input("O que gostaria de escrever? ")

    abrir_bloco_notas()
    time.sleep(1)

    pyautogui.write(texto)
    return "Texto escrito no bloco de notas."


# =========================================================
# INTERNET
# =========================================================

def abrir_github():
    webbrowser.open("https://github.com")
    return "GitHub aberto."


def abrir_chatgpt():
    webbrowser.open("https://chatgpt.com")
    return "ChatGPT aberto."


def abrir_email():
    webbrowser.open("https://mail.google.com")
    return "E-mail aberto."


# =========================================================
# PESQUISA
# =========================================================

def pesquisar_google(comando):
    palavras = comando.lower().split()

    palavras_remover = [
        "pesquise",
        "pesquisar",
        "procure",
        "buscar",
        "busque",
        "no",
        "na",
        "google",
    ]

    pesquisa = " ".join(
        palavra for palavra in palavras if palavra not in palavras_remover
    )

    if not pesquisa:
        return "O que você quer pesquisar?"

    url = "https://www.google.com/search?q=" + quote_plus(pesquisa)
    webbrowser.open(url)
    return f"Pesquisando {pesquisa}."


def pesquisar_youtube(comando):
    palavras = comando.lower().split()

    palavras_remover = [
        "pesquise",
        "pesquisar",
        "procure",
        "buscar",
        "busque",
        "no",
        "na",
        "youtube",
    ]

    pesquisa = " ".join(
        palavra for palavra in palavras if palavra not in palavras_remover
    )

    if not pesquisa:
        return "O que você quer procurar no YouTube?"

    url = "https://www.youtube.com/results?search_query=" + quote_plus(pesquisa)
    webbrowser.open(url)
    return f"Pesquisando {pesquisa} no YouTube."


# =========================================================
# EXECUTOR PRINCIPAL
# =========================================================

def executar(comando):
    comando = comando.lower().strip()
    print(f"Comando recebido: {comando}")

    # YOUTUBE
    if "youtube" in comando:
        if any(palavra in comando for palavra in [
            "pesquise", "pesquisar", "procure", "buscar", "busque"
        ]):
            return pesquisar_youtube(comando)
        return abrir_youtube(comando)

    # GOOGLE
    elif "google" in comando:
        if any(palavra in comando for palavra in [
            "pesquise", "pesquisar", "procure", "buscar", "busque"
        ]):
            return pesquisar_google(comando)
        return abrir_google(comando)

    # SPOTIFY
    elif "spotify" in comando:
        return abrir_spotify()

    # VS CODE
    elif "vscode" in comando or "vs code" in comando:
        return abrir_vscode()

    # FORTNITE
    elif "fortnite" in comando:
        return abrir_fortnite()

    # CHROME
    elif "chrome" in comando:
        return abrir_chrome()

    # EDGE
    elif "edge" in comando:
        return abrir_edge()

    # DISCORD
    elif "discord" in comando:
        return abrir_discord()

    # STEAM
    elif "steam" in comando:
        return abrir_steam()

    # MINECRAFT
    elif "minecraft" in comando:
        return abrir_minecraft()

    # VALORANT
    elif "valorant" in comando:
        return abrir_valorant()

    # EXPLORADOR
    elif "explorador de arquivos" in comando or "explorador" in comando:
        return abrir_explorador()

    # CONFIGURAÇÕES
    elif "configurações" in comando or "configuracoes" in comando:
        return abrir_configuracoes()

    # GERENCIADOR DE TAREFAS
    elif "gerenciador de tarefas" in comando or "gerenciador" in comando:
        return abrir_gerenciador()

    # BLOCO DE NOTAS
    elif "bloco de notas" in comando or "notas" in comando:
        return bloco_de_notas()

    # DOWNLOADS
    elif "downloads" in comando:
        return abrir_downloads()

    # DOCUMENTOS
    elif "documentos" in comando:
        return abrir_documentos()

    # GITHUB
    elif "github" in comando:
        return abrir_github()

    # CHATGPT
    elif "chatgpt" in comando:
        return abrir_chatgpt()

    # E-MAIL
    elif "email" in comando or "e-mail" in comando:
        return abrir_email()

    # VOLUME
    elif "aumente o volume" in comando or "aumentar o volume" in comando or "volume para cima" in comando:
        return aumentar_volume()

    elif "diminua o volume" in comando or "diminuir o volume" in comando or "volume para baixo" in comando:
        return diminuir_volume()

    elif "silencioso" in comando or "silencie" in comando or "mudo" in comando or "mutar" in comando:
        return silenciar()

    # MÚSICA
    elif "pause a música" in comando or "pausar música" in comando or "pausar a música" in comando or "pause a musica" in comando:
        return pausar_musica()

    elif "próxima música" in comando or "proxima musica" in comando or comando == "próxima" or comando == "proxima":
        return proxima_musica()

    elif "música anterior" in comando or "musica anterior" in comando or "volte a música" in comando or "volte a musica" in comando:
        return musica_anterior()

    # SISTEMA
    elif "bloqueie o computador" in comando or "bloquear computador" in comando or "bloqueie o pc" in comando or "bloquear o pc" in comando:
        return bloquear_pc()

    elif "desligue o computador" in comando or "desligar computador" in comando or "desligue o pc" in comando or "desligar o pc" in comando:
        return desligar_pc()

    elif "reinicie o computador" in comando or "reiniciar computador" in comando or "reinicie o pc" in comando or "reiniciar o pc" in comando:
        return reiniciar_pc()

    elif "cancele o desligamento" in comando or "cancelar desligamento" in comando:
        return cancelar_desligamento()

    # ARQUIVOS
    elif "crie uma pasta" in comando:
        return criar_pasta()

    elif "crie um arquivo" in comando:
        return criar_arquivo()

    # PESQUISA GENÉRICA
    elif (
        comando.startswith("pesquise ")
        or comando.startswith("pesquisar ")
        or comando.startswith("procure ")
        or comando.startswith("buscar ")
        or comando.startswith("busque ")
    ):
        return pesquisar_google(comando)

    # NÃO RECONHECIDO
    else:
        return "Comando não reconhecido. Tente novamente."