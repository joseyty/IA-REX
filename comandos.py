import pyautogui
import time


def abrir_youtube():
    musica = input("qual musica gostaria? ").lower()
    pyautogui.press("win")
    time.sleep(5)
    pyautogui.write("edga")
    time.sleep(5)
    pyautogui.press("enter")


    time.sleep(2)
    pyautogui.hotkey("crtl", "l")
    time.sleep(0.5)
    pyautogui.write("youtube.com")
    pyautogui.press("enter")

    time.sleep(4)

    pyautogui.press('tab')
    time.sleep(1)
    pyautogui.press('tab')
    time.sleep(1)
    pyautogui.press('tab')
    time.sleep(1)
    pyautogui.press('tab')
    time.sleep(1)
    pyautogui.press('tab')

    time.sleep(3)

    pyautogui.press("enter")
    time.sleep(1)

    pyautogui.write(video)
    time.sleep(1)
    pyautogui.press('enter')

    time.sleep(3)
    pyautogui.press('tab')
    time.sleep(1)
    pyautogui.press('enter')
    return "Video iniciado com sucesso!,bom video!"
   


def abrir_google():
    pesquisa = input("qual pesquisa você quer fazer?").lower()
    print("abrindo google...")
    pyautogui.PAUSE = 0.5
    pyautogui.press('win')
    pyautogui.write("chrome")
    pyautogui.press('enter')

    time.sleep(3)

    pyautogui.hotkey("ctrl", "l")
    pyautogui.write("https://www.google.com")
    pyautogui.press('enter')
    return" google aberto,boa busca."


def abrir_spotify():
    musica = input("qual musica você quer ouvir?").lower()
    print("abrindo spotify...")
    pyautogui.PAUSE = 0.5
    pyautogui.press("win")
    pyautogui.write("spotify")
    pyautogui.press('enter')

    time.sleep(10)

    pyautogui.hotkey("ctrl", "l")

    time.sleep(1)
    pyautogui.write(musica)

    time.sleep(3)

    pyautogui.press('enter')
    time.sleep(2)

    pyautogui.press('tab')
    time.sleep(0.5)

    pyautogui.press('down')
    time.sleep(0.5)
    pyautogui.press('enter')

    return"solta o som dj"


def abrir_vscode():
    pyautogui.PAUSE = 0.5
    pyautogui.press('win')
    pyautogui.write("vscode")
    pyautogui.press('enter')
    return "boa programação"


def abrir_fortnite():
    try:
        pyautogui.press("win")
        pyautogui.write("epic games")
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(5)

        for _ in range(40):
            pyautogui.press('tab')
            time.sleep(0.1)

        pyautogui.press("enter")
        return "cuidado com o geno,boa sorte looper."
    except Exception as e:
        return "erro ao abrir a epic games: {e}"

def bloco_de_notas():
    texto_para_digitar = input("o que gostaria de escrever?")
    pyautogui.press("win")
    time.sleep(0.5)
    pyautogui.write("bloco de notas")
    time.sleep(0.2)
    pyautogui.press("enter")
    time.sleep(0.5)
    pyautogui.write(texto_para_digitar)

    return "texto escrito."

    


def executar(comando):
    if "youtube" in comando:
        return abrir_youtube()
    elif "google" in comando:
        return abrir_google()
    elif "spotify" in comando:
        return abrir_spotify()
    elif "vscode" in comando:
        return abrir_vscode()
    elif "fortnite" in comando:
        return abrir_fortnite()
    elif "notas" in comando:
        return bloco_de_notas()
    else:
        return "Comando não reconhecido. Por favor, tente novamente."
