import os

from PySide6.QtWidgets import QLabel, QGraphicsOpacityEffect
from PySide6.QtGui import QPixmap, QTransform
from PySide6.QtCore import Qt, QPoint


class Personagem(QLabel):

    def __init__(self):
        super().__init__()

        caminho = os.path.join(
            os.path.dirname(__file__),
            "img",
            "standby_kyara.png"
        )

        imagem = QPixmap(caminho)

        if imagem.isNull():
            print("ERRO: imagem não foi carregada:", caminho)
            return

        imagem = imagem.scaled(
            250,
            250,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        imagem = imagem.transformed(
            QTransform().scale(-1, 1)
        )

        self.setPixmap(imagem)
        self.resize(imagem.size())

        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )

        self.setAttribute(Qt.WA_TranslucentBackground)

        tela = self.screen().availableGeometry()

        x = tela.width() - self.width() - 20
        y = tela.height() - self.height() - 20

        self.move(x, y)

        self.efeito_fala = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.efeito_fala)

        self.efeito_fala.setOpacity(1.0)

        self.posicao_mouse = QPoint()

    def falando(self):
        self.efeito_fala.setOpacity(0.65)


    def parou_de_falar(self):
        self.efeito_fala.setOpacity(1.0)

    def mousePressEvent(self, evento):

        if evento.button() == Qt.LeftButton:
            self.posicao_mouse = evento.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, evento):

        if evento.buttons() & Qt.LeftButton:
            nova_posicao = evento.globalPosition().toPoint() - self.posicao_mouse
            self.move(nova_posicao)


def criar_personagem():

    personagem = Personagem()
    personagem.show()

    return personagem