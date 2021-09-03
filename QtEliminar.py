from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QApplication,\
                            QPushButton, \
                            QHBoxLayout, \
                            QVBoxLayout, \
                            QLabel

from cliente import CLIENTES, AbrirBase_Declientes


class QEliminar(QtWidgets.QWidget):

    cancelar = QtCore.pyqtSignal(bool)
    eliminar = QtCore.pyqtSignal(bool)

    def __init__(self):
        super(QtWidgets.QWidget, self).__init__()
        self.iniciador()
        self.interfaz()
        self.conexiones()

    def cargar(self, lista_general, indice):
        if type(lista_general) != list or not lista_general\
        or len(lista_general) - 1 < indice or indice < 0:
            return
        self.lista_principal = lista_general
        self.indice = indice

        self.nombre.setText(self.lista_principal[self.indice]['NOMBRE'])
        self.posicion.setText(self.lista_principal[self.indice]['POSICION'])
        self.compania.setText(self.lista_principal[self.indice]['COMPANIA'])
        self.email.setText(self.lista_principal[self.indice]['EMAIL'])
        

    def iniciador(self):
        self.lista_principal = list()
        self.indice = None

        self.nombre = QLabel()
        self.posicion = QLabel()
        self.compania = QLabel()
        self.email = QLabel()

        self.etiqueta_nombre = QLabel('NOMBRE')
        self.etiqueta_posicion = QLabel('POSICION')
        self.etiqueta_compania = QLabel('COMPANIA')
        self.etiqueta_email = QLabel('EMAIL')

        self.boton_eliminar = QPushButton('eliminar')
        self.boton_cancelar = QPushButton('cancelar')


    def interfaz(self):
        columna_etiquetas = QVBoxLayout()
        columna_etiquetas.addWidget(self.etiqueta_nombre)
        columna_etiquetas.addWidget(self.etiqueta_compania)
        columna_etiquetas.addWidget(self.etiqueta_posicion)
        columna_etiquetas.addWidget(self.etiqueta_email)

        columna_info = QVBoxLayout()
        columna_info.addWidget(self.nombre)
        columna_info.addWidget(self.compania)
        columna_info.addWidget(self.posicion)
        columna_info.addWidget(self.email)
        
        div = QHBoxLayout()
        div.addLayout(columna_etiquetas)
        div.addLayout(columna_info)
        footer = QHBoxLayout()
        footer.addWidget(self.boton_eliminar)
        footer.addWidget(self.boton_cancelar)

        self.CUERPO = QVBoxLayout(self)
        self.CUERPO.addLayout(div)
        self.CUERPO.addLayout(footer)

    def conexiones(self):
        self.boton_eliminar.clicked.connect(self._eliminar)
        self.boton_cancelar.clicked.connect(lambda :self.cancelar.emit(True))

    def _eliminar(self):
        if not self.lista_principal or self.indice == None:
            return
            
        self.lista_principal.pop(self.indice)
        self.indice = None

        self.nombre.clear()
        self.posicion.clear()
        self.compania.clear()
        self.email.clear()

        self.eliminar.emit(True)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    AbrirBase_Declientes()
    v = QEliminar()
    v.cargar(CLIENTES,1)
    v.show()
    sys.exit(app.exec_())