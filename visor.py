import os
import io
import time
import threading

import mss

from PIL import Image, ImageChops

from google import genai
from google.genai import types

from voz import falar


# ============================================================
# CONFIGURAÇÕES
# ============================================================

# Captura a tela a cada X segundos
INTERVALO_CAPTURA = 5

# Tempo mínimo entre duas análises da Gemini
INTERVALO_GEMINI = 5

# Porcentagem mínima de mudança visual
LIMIAR_MUDANCA = 0.05

# Diferença mínima entre pixels
LIMIAR_PIXEL = 35

# Modelo Gemini
MODELO_GEMINI = "gemini-3.8-flash"

# Limite de segurança desta execução
MAX_ANALISES = 80

# Qualidade da imagem enviada
QUALIDADE_JPEG = 65


# ============================================================
# API GEMINI
# ============================================================

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "\n"
        "ERRO: GEMINI_API_KEY não encontrada.\n\n"
        "Configure sua chave da Gemini como variável de ambiente "
        "e abra um novo terminal do VS Code.\n"
    )

client = genai.Client(api_key=API_KEY)


# ============================================================
# CONTROLE DA VOZ
# ============================================================

falando = False


# ============================================================
# CAPTURA DA TELA
# ============================================================

def capturar_tela(sct, monitor):

    """
    Captura a tela usando MSS.

    A imagem fica somente na memória.
    Nenhum arquivo é criado.
    """

    screenshot = sct.grab(monitor)

    imagem = Image.frombytes(
        "RGB",
        screenshot.size,
        screenshot.rgb
    )

    return imagem


# ============================================================
# REDUZIR IMAGEM PARA COMPARAÇÃO
# ============================================================

def preparar_comparacao(imagem):

    """
    Reduz a imagem para que a comparação seja leve.
    """

    imagem = imagem.resize(
        (128, 72),
        Image.Resampling.BILINEAR
    )

    imagem = imagem.convert("L")

    return imagem


# ============================================================
# VERIFICAR MUDANÇA NA TELA
# ============================================================

def tela_mudou_relevantemente(anterior, atual):

    """
    Verifica se uma quantidade relevante da tela mudou.
    """

    if anterior is None:
        return True

    anterior_reduzida = preparar_comparacao(anterior)
    atual_reduzida = preparar_comparacao(atual)

    diferenca = ImageChops.difference(
        anterior_reduzida,
        atual_reduzida
    )

    pixels = list(diferenca.getdata())

    pixels_diferentes = sum(
        1
        for pixel in pixels
        if pixel >= LIMIAR_PIXEL
    )

    porcentagem = (
        pixels_diferentes / len(pixels)
    )

    print(
        f"[VISOR] Mudança visual: "
        f"{porcentagem:.2%}"
    )

    return porcentagem >= LIMIAR_MUDANCA


# ============================================================
# CONVERTER IMAGEM PARA BYTES
# ============================================================

def imagem_para_bytes(imagem):

    """
    Converte a imagem diretamente da RAM para JPEG.

    Nenhum arquivo é criado.
    """

    buffer = io.BytesIO()

    imagem.save(
        buffer,
        format="JPEG",
        quality=QUALIDADE_JPEG,
        optimize=True
    )

    dados = buffer.getvalue()

    buffer.close()

    return dados


# ============================================================
# ANALISAR TELA COM GEMINI
# ============================================================
def analisar_tela(imagem):
    """
    Envia a imagem diretamente para a Gemini.

    Faz até 3 tentativas caso a API esteja temporariamente
    indisponível.
    """

    imagem_bytes = imagem_para_bytes(imagem)

    prompt = """
Você é a visão de uma assistente virtual de computador chamada Kyara.

Analise esta captura de tela.

Seu objetivo é perceber acontecimentos importantes na tela.

Observe principalmente:

- qual programa está aberto;
- qual jogo está sendo executado;
- qual site está aberto;
- erros;
- mensagens importantes;
- janelas novas;
- mudanças importantes;
- problemas visuais;
- informações que possam ajudar o usuário.

Ignore:

- movimento do mouse;
- pequenas animações;
- cursor;
- relógio;
- pequenas mudanças visuais.

Só diga para Kyara falar quando existir uma mudança
realmente relevante ou algo que mereça a atenção do usuário.

Não invente informações.

Responda EXATAMENTE neste formato:

FALAR: SIM

MENSAGEM: uma frase curta em português brasileiro.

OU:

FALAR: NAO

MENSAGEM: NADA

Se não houver algo importante, use FALAR: NAO.

Se houver algo importante, use FALAR: SIM.

Seja natural, curta e objetiva.
"""

    MAX_TENTATIVAS = 3

    for tentativa in range(1, MAX_TENTATIVAS + 1):

        try:

            print(
                f"[GEMINI] Tentativa "
                f"{tentativa}/{MAX_TENTATIVAS}..."
            )

            resposta = client.models.generate_content(
                model=MODELO_GEMINI,

                contents=[
                    types.Part.from_bytes(
                        data=imagem_bytes,
                        mime_type="image/jpeg"
                    ),

                    prompt
                ],

                config=types.GenerateContentConfig(
                    max_output_tokens=100,
                    temperature=0.2
                )
            )

            texto = resposta.text.strip()

            del imagem_bytes

            print("[GEMINI] Análise concluída.")

            return texto

        except Exception as erro:

            print(
                f"[GEMINI] Erro na tentativa "
                f"{tentativa}: {erro}"
            )

            # Se ainda houver tentativas,
            # espera antes de tentar novamente.
            if tentativa < MAX_TENTATIVAS:

                espera = tentativa * 3

                print(
                    f"[GEMINI] Aguardando "
                    f"{espera} segundos..."
                )

                time.sleep(espera)

            else:

                print(
                    "[GEMINI] Todas as tentativas "
                    "falharam."
                )

    del imagem_bytes

    return None


# ============================================================
# VERIFICAR SE GEMINI DEVE FALAR
# ============================================================

def processar_resposta(resposta, personagem):

    global falando

    if not resposta:
        return

    print()
    print("┌──────── GEMINI ────────")
    print(resposta)
    print("└────────────────────────")
    print()

    linhas = resposta.splitlines()

    deve_falar = False
    mensagem = ""

    for linha in linhas:

        linha_limpa = linha.strip()

        if linha_limpa.upper().startswith("FALAR:"):

            valor = linha_limpa.split(
                ":",
                1
            )[1].strip().upper()

            if valor == "SIM":
                deve_falar = True

        elif linha_limpa.upper().startswith("MENSAGEM:"):

            mensagem = linha_limpa.split(
                ":",
                1
            )[1].strip()

    if not deve_falar:
        print("[VISOR] Kyara decidiu não falar.")
        return

    if not mensagem:
        return

    if mensagem.upper() == "NADA":
        return

    if falando:
        print("[VISOR] Kyara já está falando.")
        return

    falando = True

    try:

        print(
            f"[KYARA] {mensagem}"
        )

        # Deixa a personagem diferente
        # enquanto estiver falando.
        if personagem is not None:
            personagem.falando()

        falar(mensagem)

    except Exception as erro:

        print(
            f"[VOZ] Erro ao falar: {erro}"
        )

    finally:

        if personagem is not None:
            personagem.parou_de_falar()

        falando = False


# ============================================================
# VISOR
# ============================================================

def iniciar_visor(personagem=None):

    print()
    print("=" * 55)
    print("              VISOR DO ASSISTENTE")
    print("=" * 55)
    print()

    print("MSS: OK")
    print("Gemini: OK")
    print()

    print(
        "A tela será verificada a cada "
        f"{INTERVALO_CAPTURA} segundos."
    )

    print(
        "A Gemini só será chamada quando houver "
        "uma mudança visual relevante."
    )

    print()
    print("Nenhum screenshot será salvo no computador.")
    print()
    print("Pressione CTRL+C para encerrar.")
    print()
    print("=" * 55)
    print()

    imagem_anterior = None

    ultima_analise = 0

    quantidade_analises = 0

    with mss.mss() as sct:

        # Monitor principal
        monitor = sct.monitors[1]

        while True:

            try:

                # =================================================
                # 1. CAPTURAR
                # =================================================

                imagem_atual = capturar_tela(
                    sct,
                    monitor
                )

                print(
                    "[VISOR] Tela capturada."
                )

                # =================================================
                # 2. VERIFICAR MUDANÇA
                # =================================================

                mudou = tela_mudou_relevantemente(
                    imagem_anterior,
                    imagem_atual
                )

                agora = time.time()

                tempo_desde_ultima = (
                    agora - ultima_analise
                )

                # =================================================
                # 3. VERIFICAR INTERVALO
                # =================================================

                intervalo_liberado = (
                    tempo_desde_ultima
                    >= INTERVALO_GEMINI
                )

                limite_liberado = (
                    quantidade_analises
                    < MAX_ANALISES
                )

                # =================================================
                # 4. ANALISAR
                # =================================================

                if mudou:

                    print(
                        "[VISOR] Mudança relevante detectada."
                    )

                    if not intervalo_liberado:

                        restante = (
                            INTERVALO_GEMINI
                            - tempo_desde_ultima
                        )

                        print(
                            "[VISOR] Gemini em espera."
                        )

                        print(
                            f"[VISOR] Aguarde "
                            f"{restante:.0f}s."
                        )

                    elif not limite_liberado:

                        print(
                            "[VISOR] Limite de segurança "
                            "da sessão atingido."
                        )

                    else:

                        print(
                            "[VISOR] Enviando para Gemini..."
                        )

                        resposta = analisar_tela(
                            imagem_atual
                        )

                        quantidade_analises += 1

                        ultima_analise = time.time()

                        processar_resposta(
                            resposta,
                            personagem
                        )

                        print(
                            f"[VISOR] Análises nesta sessão: "
                            f"{quantidade_analises}/"
                            f"{MAX_ANALISES}"
                        )

                else:

                    print(
                        "[VISOR] Nenhuma mudança "
                        "relevante."
                    )

                # =================================================
                # 5. ATUALIZAR MEMÓRIA
                # =================================================

                imagem_anterior = imagem_atual

                # =================================================
                # 6. ESPERAR
                # =================================================

                time.sleep(
                    INTERVALO_CAPTURA
                )

            except KeyboardInterrupt:

                print()
                print(
                    "[VISOR] Encerrado pelo usuário."
                )

                print(
                    f"[VISOR] Total de análises: "
                    f"{quantidade_analises}"
                )

                break

            except Exception as erro:

                print()
                print(
                    f"[VISOR] Erro: {erro}"
                )

                print(
                    "[VISOR] Tentando novamente "
                    "em 5 segundos..."
                )

                time.sleep(5)


# ============================================================
# THREAD DO VISOR
# ============================================================

def iniciar_visor_thread(personagem=None):

    thread = threading.Thread(
        target=iniciar_visor,
        args=(personagem,),
        daemon=True
    )

    thread.start()

    return thread


# ============================================================
# EXECUÇÃO DIRETA
# ============================================================

if __name__ == "__main__":

    iniciar_visor()