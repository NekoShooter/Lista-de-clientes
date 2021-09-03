from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QApplication,\
                            QPushButton, \
                            QHBoxLayout, \
                            QVBoxLayout, \
                            QLabel,\
                            QSpinBox


class QMultiplesIndices(QtWidgets.QWidget):

    indice_elegido = QtCore.pyqtSignal(int)
    cancelar = QtCore.pyqtSignal(bool)

    def __init__(self):
        super(QtWidgets.QWidget,self).__init__()
        self.iniciador()
        self.interfaz()
        self.conexiones()

    def cargar(self,lista):
        if type(lista) != list or not lista:
            return
        self.lista_de_indices = lista
        self.seleccion_indice.setMaximum(len(lista) - 1)


    def iniciador(self):
        self.lista_de_indices = list()
        self.etiqueta_mensaje = QLabel('Hay multiples resultados:')
        self.etiqueta_eleccion = QLabel('seleciona el indice')
        self.seleccion_indice = QSpinBox()
        self.boton_ok = QPushButton('OK')
        self.boton_cancelar = QPushButton('cancelar')

    def interfaz(self):
        derecha = QVBoxLayout()
        derecha.setAlignment(QtCore.Qt.AlignBottom)
        derecha.addWidget(self.boton_cancelar)
        derecha.addWidget(self.boton_ok)
        

        izquierda = QVBoxLayout()
        izquierda.setAlignment(QtCore.Qt.AlignBottom)
        izquierda.addWidget(self.etiqueta_mensaje)

        izquierda_inferior = QHBoxLayout()
        izquierda_inferior.addWidget(self.etiqueta_eleccion)
        izquierda_inferior.addWidget(self.seleccion_indice)

        izquierda.addLayout(izquierda_inferior)

        self.CUERPO = QHBoxLayout(self)
        self.CUERPO.addLayout(izquierda)
        self.CUERPO.addLayout(derecha)


    def conexiones(self):
        self.boton_ok.clicked.connect(self._indice_elegido)
        self.boton_cancelar.clicked.connect(lambda:self.cancelar.emit(True))

    def _indice_elegido(self):
        if not self.lista_de_indices:
            return
        self.indice_elegido.emit(self.lista_de_indices[self.seleccion_indice.value()])


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    lista = [1,2,4]
    v = QMultiplesIndices()
    v.cargar(lista)
    v.show()
    sys.exit(app.exec_())