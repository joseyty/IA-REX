from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap


def criar_personagem():
    personagem = QLabel()



    personagem.setPixmap(QPixmap("personagem/standby_kyara.png"))


    personagem.setPixmap(imagem)
    personagem.resize(imagem.size())

    personagem.setWindowFlags(
        Qt.FramelessWindowHint |
        Qt.WindowStaysOnTopHint |
        Qt.Tool

    )

    personagem.setAttribute(Qt.WA_TranslucentBackground)

    personagem.show()



    return personagem

