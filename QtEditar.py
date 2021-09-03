from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QApplication,\
                            QPushButton, \
                            QHBoxLayout, \
                            QVBoxLayout, \
                            QLabel,\
                            QLineEdit
from cliente import CLIENTES, AbrirBase_Declientes

class QEditar(QtWidgets.QWidget):

    cancelar = QtCore.pyqtSignal(bool)
    cambioHecho =  QtCore.pyqtSignal(bool)

    def __init__(self):
        super(QtWidgets.QWidget,self).__init__()
        self.iniciador()
        self.interfaz()
        self.conexiones()

    def cargar(self,diccionario):
        
        if type(diccionario) != dict or not diccionario:
            return
        self.dict_original = diccionario
        self.dict_temp = self.dict_original.copy()

        self.nombre.setText(self.dict_original['NOMBRE'])
        self.posicion.setText(self.dict_original['POSICION']) 
        self.compania.setText(self.dict_original['COMPANIA']) 
        self.email.setText(self.dict_original['EMAIL'])

    def iniciador(self):
        self.dict_original = dict()
        self.dict_temp = dict()

        self.nombre = QLineEdit()
        self.posicion = QLineEdit()
        self.compania = QLineEdit()
        self.email = QLineEdit()

        self.etiqueta_nombre = QLabel('Nombre :')
        self.etiqueta_posicion = QLabel('Posicion :')
        self.etiqueta_compania = QLabel('Compania :')
        self.etiqueta_email = QLabel('Email :')

        self.boton_guardar_cambios = QPushButton('guardar cambios')
        self.boton_cancelar = QPushButton('cancelar')


    def interfaz(self):
        columna_etiquetas = QVBoxLayout()
        columna_etiquetas.addWidget(self.etiqueta_nombre)
        columna_etiquetas.addWidget(self.etiqueta_compania)
        columna_etiquetas.addWidget(self.etiqueta_posicion)
        columna_etiquetas.addWidget(self.etiqueta_email)

        columna_caja_de_texto = QVBoxLayout()
        columna_caja_de_texto.addWidget(self.nombre)
        columna_caja_de_texto.addWidget(self.compania)
        columna_caja_de_texto.addWidget(self.posicion)
        columna_caja_de_texto.addWidget(self.email)
        
        div = QHBoxLayout()
        div.addLayout(columna_etiquetas)
        div.addLayout(columna_caja_de_texto)
        footer = QHBoxLayout()
        footer.addWidget(self.boton_guardar_cambios)
        footer.addWidget(self.boton_cancelar)

        self.CUERPO = QVBoxLayout(self)
        self.CUERPO.addLayout(div)
        self.CUERPO.addLayout(footer)

    def conexiones(self):
        self.nombre.returnPressed.connect(self._hacer_cambios)
        self.compania.returnPressed.connect(self._hacer_cambios)
        self.posicion.returnPressed.connect(self._hacer_cambios)
        self.email.returnPressed.connect(self._hacer_cambios)

        self.boton_guardar_cambios.clicked.connect(self._hacer_cambios)
        self.boton_cancelar.clicked.connect(lambda :self.cancelar.emit(True))


    def _hacer_cambios(self):
        if not self.dict_temp:
            return
        self.dict_temp['NOMBRE'] = (self.nombre.text())
        self.dict_temp['COMPANIA'] = (self.compania.text())
        self.dict_temp['POSICION'] = (self.posicion.text())
        self.dict_temp['EMAIL'] = (self.email.text())
        for valor in self.dict_temp.values():
            if not valor:
                self.dict_temp.clear()
                return
        for llave, valor in self.dict_temp.items():
            self.dict_original[llave] = valor
        self.dict_temp.clear()
        self.cambioHecho.emit(True)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    AbrirBase_Declientes()
    v = QEditar()
    v.cargar(CLIENTES[1])
    v.show()
    sys.exit(app.exec_())