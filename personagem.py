from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtGui import QPixmap





def criar_personagem():
personagem = QLabel()

personagem.setPixmap(QPixmap("personagem/standby_kyara.png"))
personagem.show()
return personagem

