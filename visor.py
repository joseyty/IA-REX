import os
import io
import time

import mss
from PIL import Image, ImageChops, ImageStat
from google import genai
from google.genai import types


# ============================================================
# CONFIGURAÇÕES
# ============================================================

# Captura a tela a cada X segundos
INTERVALO_CAPTURA = 5

# Tempo mínimo entre duas análises da Gemini
INTERVALO_GEMINI = 30

# Quanto de mudança na tela é necessário para considerar
# que aconteceu algo relevante.
#
# 0.05 = aproximadamente 5% dos pixels mudaram
LIMIAR_MUDANCA = 0.05

# Diferença mínima de brilho entre pixels para considerar
# que aquele pixel realmente mudou.
LIMIAR_PIXEL = 35

# Modelo Gemini
MODELO_GEMINI = "gemini-3.8-flash"

# Limite de segurança desta execução.
# Sua cota mostrada no AI Studio é 100 RPD.
# Deixamos 20 chamadas de margem.
MAX_ANALISES = 80

# Qualidade JPEG enviada para a Gemini
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
# CAPTURA DA TELA
# ============================================================

def capturar_tela(sct, monitor):
    """
    Captura a tela usando MSS.

    A imagem fica somente na memória.
    Nenhum PNG/JPG é criado.
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

    Não altera a imagem original.
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

    Retorna:

        True  -> mudança relevante
        False -> mudança pequena
    """

    if anterior is None:
        return True

    anterior = preparar_comparacao(anterior)
    atual = preparar_comparacao(atual)

    diferenca = ImageChops.difference(
        anterior,
        atual
    )

    # --------------------------------------------------------
    # Calcula quantos pixels realmente mudaram.
    # --------------------------------------------------------

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
    """

    imagem_bytes = imagem_para_bytes(imagem)

    prompt = """
Você é o sistema de visão de um assistente virtual de computador.

Analise esta captura de tela.

Sua função é ajudar o usuário a entender o que está
acontecendo no computador.

Observe principalmente:

- qual programa está aberto;
- qual site está aberto;
- erros;
- mensagens importantes;
- janelas que apareceram;
- botões importantes;
- mudanças que possam exigir atenção;
- problemas visuais;
- informações que possam ajudar o usuário.

Não descreva cada detalhe da tela.

Se não houver nada importante, responda:

"A tela parece normal."

Se houver algo importante, seja curto e objetivo.

Responda sempre em português brasileiro.

Não invente informações que não estejam visíveis.
"""

    try:

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
                max_output_tokens=150,
                temperature=0.2
            )
        )

        texto = resposta.text

        # Libera os bytes da imagem
        del imagem_bytes

        return texto.strip()

    except Exception as erro:

        print(
            f"[GEMINI] Erro ao analisar tela: {erro}"
        )

        return None


# ============================================================
# VISOR
# ============================================================

def iniciar_visor():

    print()
    print("=" * 55)
    print("              VISOR DO ASSISTENTE")
    print("=" * 55)
    print()
    print("MSS: OK")
    print("Gemini: OK")
    print()
    print("A tela será verificada a cada 5 segundos.")
    print("A Gemini só será chamada quando houver")
    print("uma mudança visual relevante.")
    print()
    print("Nenhum screenshot será salvo no computador.")
    print()
    print("Pressione CTRL+C para encerrar.")
    print()
    print("=" * 55)
    print()

    # --------------------------------------------------------
    # Controle
    # --------------------------------------------------------

    imagem_anterior = None

    ultima_analise = 0

    quantidade_analises = 0

    # --------------------------------------------------------
    # MSS
    # --------------------------------------------------------

    with mss.mss() as sct:

        # Monitor 1 = tela principal
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
                # 3. VERIFICAR SE PODE CONSULTAR GEMINI
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

                        # -----------------------------------------
                        # RESPOSTA
                        # -----------------------------------------

                        if resposta:

                            print()
                            print(
                                "┌──────── ASSISTENTE ────────"
                            )

                            print(resposta)

                            print(
                                "└────────────────────────────"
                            )

                            print()

                        else:

                            print(
                                "[VISOR] Gemini não retornou "
                                "uma resposta."
                            )

                        print(
                            f"[VISOR] Análises nesta sessão: "
                            f"{quantidade_analises}/{MAX_ANALISES}"
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

            # =====================================================
            # CTRL+C
            # =====================================================

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

            # =====================================================
            # ERRO
            # =====================================================

            except Exception as erro:

                print()
                print(
                    f"[VISOR] Erro: {erro}"
                )

                print(
                    "[VISOR] Tentando novamente em 5 segundos..."
                )

                time.sleep(5)


# ============================================================
# INICIAR
# ============================================================

if __name__ == "__main__":
    iniciar_visor()