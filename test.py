# test.py
# Ventana 2: aquí se hace la prueba de Ruffier paso a paso.
# Contiene las 3 mediciones del pulso, el temporizador, el calculo el indice de Ruffier y la clasificación por la edad.

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox)

from config import *
from result import ResultWindow

# =====================================================
# ESTILOS DEL CRONÓMETRO
# =====================================================
# Verde: se usa cuando se mide el pulso.
# Negro: se usa cuando hay descanso o test normales.
ESTILO_CRONOMETRO_VERDE = "font-size: 60px; font-weight: bold; color: green;"
ESTILO_CRONOMETRO_NEGRO = "font-size: 60px; font-weight: bold; color: black;"

class TestWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Variables para controlar el cronómetro
        self.segundos = 0     # mide cuántos segundos le quedan al cronómetro
        self.fase = ""        # señala cuál es el test que está realizando: "test1", "test2" o "test_final"

        # Paso a paso para construir la ventana.
        self.crear_widgets()
        self.armar_layout()
        self.configurar_ventana()
        self.conectar_botones()
        self.crear_cronometro()
        self.show()

    # =====================================================
    # 1) CREAR TODOS LOS WIDGETS
    # =====================================================
    def crear_widgets(self):
        # --- Datos personales ---
        self.label_nombre = QLabel(TXT_NOMBRE)
        self.input_nombre = QLineEdit()            # para colocar el nombre
        self.input_nombre.setPlaceholderText("Nombre completo")
        self.input_nombre.setMaxLength(80)         # máximo 80 caracteres
        self.input_nombre.setFixedWidth(300)       # ancho visual acorde a 80 caracteres

        self.label_edad = QLabel(TXT_AGE)
        self.input_edad = QLineEdit()              # para colocar la edad
        self.input_edad.setPlaceholderText("0")    # visible en el campo de la edad
        self.input_edad.setMaxLength(3)            # máximo 3 dígitos
        self.input_edad.setFixedWidth(60)          # ancho visual acorde a 3 dígitos
        self.input_edad.setAlignment(Qt.AlignCenter)  # centra el valor

        # --- Test 1: para medir el pulso P1 ---
        self.label_test1 = QLabel(TXT_TEST1)
        self.boton_test1 = QPushButton(TXT_START_TEST1) 
        self.input_p1 = QLineEdit()                # para colocar el valor del pulso 1
        self.input_p1.setPlaceholderText("0")      # visible en el campo de P1
        self.input_p1.setMaxLength(2)              # máximo 2 dígitos
        self.input_p1.setFixedWidth(60)            # ancho igual al de la edad
        self.input_p1.setAlignment(Qt.AlignCenter) # centra el valor

        # --- Test 2: hacer las sentadillas ---
        self.label_test2 = QLabel(TXT_TEST2)
        self.boton_test2 = QPushButton(TXT_START_TEST2) # boton que contiene texto
        self.boton_test2.setEnabled(False)   # al inicio está deshabilitado

        # --- Test 3: test final ---
        self.label_test3 = QLabel(TXT_TEST3)
        self.boton_test3 = QPushButton(TXT_START_TEST3)
        self.boton_test3.setEnabled(False)         # al inicio está deshabilitado

        self.input_p2 = QLineEdit()                # para colocar el valor del pulso 2
        self.input_p2.setPlaceholderText("0")      # visible en el campo de P2
        self.input_p2.setMaxLength(2)              # máximo 2 dígitos
        self.input_p2.setFixedWidth(60)            # ancho igual al de la edad
        self.input_p2.setAlignment(Qt.AlignCenter) # centra el valor
        self.input_p3 = QLineEdit()                # para colocar el valor del pulso 3
        self.input_p3.setPlaceholderText("0")      # visible en el campo de P3
        self.input_p3.setMaxLength(2)              # máximo 2 dígitos
        self.input_p3.setFixedWidth(60)            # ancho igual al de la edad
        self.input_p3.setAlignment(Qt.AlignCenter) # centra el valor

        # --- Botón para enviar los resultados para que aparezcan en la ventana 3 ---
        self.boton_enviar = QPushButton(TXT_SEND_RESULTS)
        self.boton_enviar.setEnabled(False)        # al inicio está deshabilitado

        # --- Cronómetro (aparece en la columna derecha) ---
        self.label_cronometro = QLabel("00:00:00")
        self.label_cronometro.setAlignment(Qt.AlignCenter)  # alineado en el centro de la columna
        self.label_cronometro.setStyleSheet(ESTILO_CRONOMETRO_NEGRO)  # color inicial
        self.label_cronometro.setFixedWidth(350)   # ancho fijo del cronómero

    # =====================================================
    # 2) ARMAR EL LAYOUT o DISTRIBUIR LOS OBJETOS EN LA VENTANA: se vincula cadaobjeto a la columna (columna izquierda + columna derecha)
    # =====================================================
    def armar_layout(self):
        # ==========================================
        # COLUMNA IZQUIERDA: el formulario completo
        # ==========================================
        columna = QVBoxLayout()                    # Línea vertical a la izquierda

        columna.addStretch()                       # empuja todo hacia abajo
        
        # Bloque 1: datos personales
        columna.addWidget(self.label_nombre)
        columna.addWidget(self.input_nombre)
        columna.addWidget(self.label_edad)
        columna.addWidget(self.input_edad)

        # Bloque 2: Test 1
        columna.addWidget(self.label_test1)
        columna.addWidget(self.boton_test1, alignment=Qt.AlignLeft)   # ajustado al texto
        columna.addWidget(self.input_p1)

        # Bloque 3: Test 2
        columna.addWidget(self.label_test2)
        columna.addWidget(self.boton_test2, alignment=Qt.AlignLeft)   # ajustado al texto

        # Bloque 4: Test 3
        columna.addWidget(self.label_test3)
        columna.addWidget(self.boton_test3, alignment=Qt.AlignLeft)   # ajustado al texto
        columna.addWidget(self.input_p2)
        columna.addWidget(self.input_p3)

        # Bloque 5: botón enviar
        columna.addWidget(self.boton_enviar, alignment=Qt.AlignLeft)  # ajustado al texto

        columna.addStretch()                        # empuja todo hacia arriba

        # ==========================================
        # COLUMNA DERECHA: el cronómetro
        # ==========================================
        columna_derecha = QVBoxLayout()
        
        columna_derecha.addStretch()                # empuja todo hacia abajo para centrar verticalmente
        columna_derecha.addWidget(self.label_cronometro, alignment=Qt.AlignCenter)
        columna_derecha.addStretch()                # empuja todo hacia arriba para centrar verticalmente

        # ==========================================
        # LAYOUT PRINCIPAL: une las dos columnas
        # ==========================================
        layout_principal = QHBoxLayout()
        layout_principal.addLayout(columna, 3)          # 3/4 para el formulario
        layout_principal.addLayout(columna_derecha, 1)  # 1/4 para el cronómetro

        self.setLayout(layout_principal)

    # =====================================================
    # 3) CONFIGURAR LA VENTANA
    # =====================================================
    def configurar_ventana(self):
        self.setWindowTitle(TXT_TEST_TITLE)
        self.resize(WIN_WIDTH, WIN_HEIGHT)
        self.move(WIN_X, WIN_Y)

    # =====================================================
    # 4) CREAR EL CRONÓMETRO
    # =====================================================
    def crear_cronometro(self):
        # QTimer es un reloj que dispara una señal cada cierto tiempo.
        # Cada 1000 ms (1 segundo) llamará a "cada_segundo".
        self.timer = QTimer()
        self.timer.timeout.connect(self.cada_segundo)

    # =====================================================
    # 5) CONECTAR LOS BOTONES CON LAS FUNCIONES
    # =====================================================
    def conectar_botones(self):
        self.boton_test1.clicked.connect(self.iniciar_test1)
        self.boton_test2.clicked.connect(self.iniciar_test2)
        self.boton_test3.clicked.connect(self.iniciar_test3)
        self.boton_enviar.clicked.connect(self.enviar_resultados)

    # =====================================================
    # 6) FUNCIONES QUE ARRANCAN CADA TEST
    # =====================================================
    def iniciar_test1(self):
        self.fase = "test1"                  # recordamos qué test empezamos
        self.segundos = 15                   # dura 15 segundos
        self.boton_test1.setEnabled(False)   # ya no se puede pulsar de nuevo
        self.label_cronometro.setStyleSheet(ESTILO_CRONOMETRO_NEGRO)  # negro
        self.timer.start(1000)               # inicia el cronómetro

    def iniciar_test2(self):
        self.fase = "test2"
        self.segundos = 45
        self.boton_test2.setEnabled(False)
        self.label_cronometro.setStyleSheet(ESTILO_CRONOMETRO_NEGRO)  # negro
        self.timer.start(1000)

    def iniciar_test3(self):
        self.fase = "test_final"
        self.segundos = 60
        self.boton_test3.setEnabled(False)
        # El test final inica en color verde: los primeros 15 segundos son de medición
        self.label_cronometro.setStyleSheet(ESTILO_CRONOMETRO_VERDE)
        self.timer.start(1000)

    # =====================================================
    # 7) LO QUE PASA CADA SEGUNDO
    # =====================================================
    def cada_segundo(self):
        self.segundos = self.segundos - 1           # Resta 1 segundo
        self.actualizar_cronometro()                # Actualiza el número y el color en pantalla

        # Cuando elcronómetro llegue a cero, se detiene y termina la fase
        if self.segundos <= 0:
            self.timer.stop()
            self.terminar_fase()

    def actualizar_cronometro(self):
        # 1) Convierte los segundos al formato 00:MM:SS
        minutos = self.segundos // 60
        segundos = self.segundos % 60
        self.label_cronometro.setText(f"00:{minutos:02d}:{segundos:02d}")

        # 2) Cambia el color segun la fase y el tiempo restante
        if self.fase == "test_final":
            # Test 3: verde en los primeros y últimos 15 s,
            # negro en los 30 s intermedios
            if self.segundos > 45:
                self.label_cronometro.setStyleSheet(ESTILO_CRONOMETRO_VERDE)
            elif self.segundos > 15:
                self.label_cronometro.setStyleSheet(ESTILO_CRONOMETRO_NEGRO)
            else:
                self.label_cronometro.setStyleSheet(ESTILO_CRONOMETRO_VERDE)
        else:
            # Test 1 y Test 2: siempre negro
            self.label_cronometro.setStyleSheet(ESTILO_CRONOMETRO_NEGRO)

    def terminar_fase(self):
        # Según qué test acabamos de terminar, habilitamos el siguiente botón
        if self.fase == "test1":
            self.boton_test2.setEnabled(True)
        elif self.fase == "test2":
            self.boton_test3.setEnabled(True)
        elif self.fase == "test_final":
            self.boton_enviar.setEnabled(True)

        # Limpiamos la fase para que no quede activa
        self.fase = ""

    # =====================================================
    # 8) ENVIAR RESULTADOS Y CALCULAR EL ÍNDICE
    # =====================================================
    def enviar_resultados(self):
        # 1. Intentar leer los números que escribió el usuario
        try:
            p1 = int(self.input_p1.text())
            p2 = int(self.input_p2.text())
            p3 = int(self.input_p3.text())
            edad = int(self.input_edad.text())
        except ValueError:
            QMessageBox.warning(self, "Error, por favor, ingrese números en todos los campos.")
            return

        # 2. Calcular el índice de Ruffier
        indice = (4 * (p1 + p2 + p3) - 200) / 10

        # 3. Ver qué rendimiento le corresponde según su edad
        rendimiento = self.calcular_rendimiento(edad, indice)

        # 4. Abrir la Ventana 3 y ocultar la Ventana2
        self.resultado = ResultWindow(indice, rendimiento)
        self.hide()

    # =====================================================
    # 9) CALCULA EL RENDIMIENTO SEGÚN EDAD E ÍNDICE
    # =====================================================
    def calcular_rendimiento(self, edad, indice):
        if edad >= 15:
            if indice >= 15:
                return 'Bajo'
            elif indice >= 11:
                return 'Satisfactorio'
            elif indice >= 6:
                return 'Promedio'
            elif indice >= 0.5:
                return 'Por encima del promedio'
            else:
                return 'Alto'
        elif edad >= 13 and edad <= 14:
            if indice >= 16.5:
                return 'Bajo'
            elif indice >= 12.5:
                return 'Satisfactorio'
            elif indice >= 7.5:
                return 'Promedio'
            elif indice >= 2:
                return 'Por encima del promedio'
            else:
                return 'Alto'
        elif edad >= 11 and edad <= 12:
            if indice >= 18:
                return 'Bajo'
            elif indice >= 14:
                return 'Satisfactorio'
            elif indice >= 9:
                return 'Promedio'
            elif indice >= 3.5:
                return 'Por encima del promedio'
            else:
                return 'Alto'
        elif edad >= 9 and edad <= 10:
            if indice >= 19.5:
                return 'Bajo'
            elif indice >= 15.5:
                return 'Satisfactorio'
            elif indice >= 10.5:
                return 'Promedio'
            elif indice >= 5:
                return 'Por encima del promedio'
            else:
                return 'Alto'
        elif edad >= 7 and edad <= 8:
            if indice >= 21:
                return 'Bajo'
            elif indice >= 17:
                return 'Satisfactorio'
            elif indice >= 12:
                return 'Promedio'
            elif indice >= 6.5:
                return 'Por encima del promedio'
            else:
                return 'Alto'
        else:
            return 'No hay datos para esta edad'
