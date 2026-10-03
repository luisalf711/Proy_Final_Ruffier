# result.py
# Ventana 3: muestra el resultado final de la prueba.

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from config import *

class ResultWindow(QWidget):
    def __init__(self, indice, rendimiento):
        super().__init__()

        # Guarda los datos que recibe desde test.py
        self.indice = indice
        self.rendimiento = rendimiento

        self.crear_widgets()
        self.armar_layout()
        self.configurar_ventana()
        self.show()

    # =====================================================
    # 1) CREAR LOS WIDGETS
    # =====================================================
    def crear_widgets(self):
        # Si el índice es un número entero (ej: 5.0), lo muestra sin decimales.
        if self.indice == int(self.indice):
            indice_a_mostrar = int(self.indice)
        else:
            indice_a_mostrar = self.indice

        # Etiquetas con los resultados
        self.label_indice = QLabel(f'{TXT_INDEX}{indice_a_mostrar}')
        self.label_rendimiento = QLabel(f'{TXT_WORKOUT}{self.rendimiento}')

        # Agrego estilos a las etiquetas
        self.label_indice.setStyleSheet('font-size: 16px;')
        self.label_rendimiento.setStyleSheet('font-size: 16px;')

    # =====================================================
    # 2) DISTRIBUCION EN LA VENTANA (etiquetas centradas)
    # =====================================================
    def armar_layout(self):
        layout = QVBoxLayout()

        layout.addStretch()                     # Distribuye el espacio vacío arriba
        layout.addWidget(self.label_indice, alignment=Qt.AlignCenter)
        layout.addStretch()                     # espacio vacío en el medio
        layout.addWidget(self.label_rendimiento, alignment=Qt.AlignCenter)
        layout.addStretch()                     # Distribuye el espacio vacío abajo

        self.setLayout(layout)

    # =====================================================
    # 3) CONFIGURCION DE LA VENTANA
    # =====================================================
    def configurar_ventana(self):
        self.setWindowTitle(TXT_RESULT_TITLE)
        self.resize(WIN_WIDTH, WIN_HEIGHT)
        self.move(WIN_X, WIN_Y)
