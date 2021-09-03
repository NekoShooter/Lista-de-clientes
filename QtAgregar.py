from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtWidgets import  QApplication


def _crear_boton(titulo,icono):
    boton = QtWidgets.QPushButton()
    boton.setFlat(True)
    boton.setToolTip(titulo)
    boton.setIcon(QtGui.QIcon(icono))
    #boton.setIconSize(QtCore.QSize(50,50))
    return boton


class QAgregar(QtWidgets.QWidget):

    Agregado = QtCore.pyqtSignal(dict)
    Cancelar = QtCore.pyqtSignal(bool)


    def __init__(self):
        
        super(QtWidgets.QWidget,self).__init__()
        self.llaves = ['NOMBRE','COMPANIA','POSICION','EMAIL']
        self.inicializador()
        self.interfaz()
        self.conexiones()
        

    def inicializador(self):
        self.H1 = QtWidgets.QLabel(self.llaves[0])
        self.caja_de_texto = QtWidgets.QLineEdit()
        self.caja_de_texto.setPlaceholderText('ingresa texto')

        self.boton_siguiente = _crear_boton('siguiente', './iconos/siguiente.png')
        self.boton_anterior = _crear_boton('anterior', './iconos/anterior.png')
        self.boton_anterior.setEnabled(False)
        self.boton_cancelar = _crear_boton('cancelar','./iconos/cancelar')

        self.indice_actual = 0
        self.un_Cliente = dict()

    def reiniciar(self):
        self.indice_actual = 0
        self.un_Cliente = dict()
        self.boton_siguiente.setIcon(QtGui.QIcon('./iconos/siguiente.png'))
        self.H1.setText(self.llaves[0])


    def interfaz(self):
        barra_de_introducion_de_datos = QtWidgets.QHBoxLayout()
        barra_de_introducion_de_datos.addWidget(self.boton_anterior)
        barra_de_introducion_de_datos.addWidget(self.caja_de_texto)
        barra_de_introducion_de_datos.addWidget(self.boton_siguiente)
        barra_de_introducion_de_datos.addWidget(self.boton_cancelar)

        self.CUERPO = QtWidgets.QVBoxLayout(self)
        self.CUERPO.setAlignment(QtCore.Qt.AlignBottom)

        self.CUERPO.addWidget(self.H1)
        self.CUERPO.addLayout(barra_de_introducion_de_datos)

    def conexiones(self):
        self.caja_de_texto.returnPressed.connect(self._introducir_texto)
        self.boton_siguiente.clicked.connect(self._introducir_texto)
        self.boton_anterior.clicked.connect(self._editar_texto_anterior)
        self.boton_cancelar.clicked.connect(self._cancelar)
        self.Agregado.connect(self._imprimir)

    def _introducir_texto(self):
        texto = ''
        hay_valor_almacenado_previamente = False
        num_elementos = len(self.llaves)

        if self.indice_actual + 1 < num_elementos:
            try:
                texto = self.un_Cliente[self.llaves[self.indice_actual + 1]]
                self.caja_de_texto.setText(texto)
                hay_valor_almacenado_previamente = True
            except KeyError:
                texto = self.caja_de_texto.text()

        if texto != self.caja_de_texto.text():
            texto = self.caja_de_texto.text()

        if not hay_valor_almacenado_previamente:
            self.caja_de_texto.clear()

        if texto:
            i = 0
            if hay_valor_almacenado_previamente:
                i = 1
            self.un_Cliente[self.llaves[self.indice_actual + i]] = texto
            self.indice_actual += 1
            try:
                self.H1.setText(self.llaves[self.indice_actual])
            except IndexError:
                self.Agregado.emit(self.un_Cliente)
                self.reiniciar()

        if self.indice_actual == 1:
            self.boton_anterior.setEnabled(True)

        if self.indice_actual > 2:
            self.boton_siguiente.setIcon(QtGui.QIcon('./iconos/listo.png'))

    
    def _editar_texto_anterior(self):
        self.caja_de_texto.clear()
        self.indice_actual -= 1
        self.H1.setText(self.llaves[self.indice_actual])
        if self.indice_actual <= 0:
            self.indice_actual = 0
            self.boton_anterior.setEnabled(False)

        if self.indice_actual == 2:
            self.boton_siguiente.setIcon(QtGui.QIcon('./iconos/siguiente.png'))

        self.caja_de_texto.setText(self.un_Cliente[self.llaves[self.indice_actual]])
        
            
    
    def _cancelar(self):
        self.Cancelar.emit(True)

    def _imprimir(self, diccionario):
        print(diccionario)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    app.setStyle('fusion')

    v = QAgregar()
    v.show()

    sys.exit(app.exec_())