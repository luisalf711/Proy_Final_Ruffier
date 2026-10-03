from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout)

from config import *
from test import * # Importa TestWindow correctamente

class MainWindow(QWidget):
    def __init__(self, title=TXT_TITLE):
        self.title = title
        super().__init__()
        self.set_ui()
        self.config_window()
        self.connections()
        self.show()

    def set_ui(self):
        # ESTABLECER WIDGETS 
        self.welcome_label = QLabel(TXT_HELLO)
        self.instructions_label = QLabel(TXT_INSTRUCTION)
        self.btn_next = QPushButton(TXT_NEXT, self)
        # LAYOUT
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.welcome_label, alignment=Qt.AlignLeft)
        self.main_layout.addWidget(self.instructions_label, alignment=Qt.AlignLeft)
        self.main_layout.addWidget(self.btn_next, alignment=Qt.AlignCenter)

        self.setLayout(self.main_layout)

    def config_window(self):
        self.resize(WIN_WIDTH, WIN_HEIGHT)
        self.move(WIN_X, WIN_Y)
        # self.setStyleSheet(STYLES)

    def connections(self):
        self.btn_next.clicked.connect(self.next_click)

    def next_click(self):
        self.hide()
        self.test = TestWindow() # Al quitar el '#', la ventana dos se crea y se muestra en pantalla     

app = QApplication([])
main_window = MainWindow()
app.exec_()
