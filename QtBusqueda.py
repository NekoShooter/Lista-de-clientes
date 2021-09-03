from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QApplication
import cliente

class QBusqueda(QWidget):

    click_busqueda = QtCore.pyqtSignal(list)
    click_cancelar = QtCore.pyqtSignal(bool)

    def __init__(self):
        super(QWidget, self).__init__()
        self._inicializador()
        self._interfaz()
        self._senyales()


    def cargar(self,lista_de_diccionarios):
        if not lista_de_diccionarios or type(lista_de_diccionarios) != list:
            return
        self.lista_de_diccionarios = lista_de_diccionarios
        for llave in self.lista_de_diccionarios[0].keys():
            self.llaves_principales.append(llave)

    def _inicializador(self):
        self.lista_de_diccionarios = list()
        self.llaves_principales = list()

        self.H1 = QtWidgets.QLabel('Buscar Por:')

        self.opciones = QtWidgets.QButtonGroup()

        self.casilla_nombre = QtWidgets.QRadioButton('Nombre')
        self.casilla_compania = QtWidgets.QRadioButton('Compania')
        self.casilla_puesto = QtWidgets.QRadioButton('Pocision')
        self.casilla_email = QtWidgets.QRadioButton('Email')

        self.opciones.addButton(self.casilla_nombre,1)
        self.opciones.addButton(self.casilla_compania,2)
        self.opciones.addButton(self.casilla_puesto,3)
        self.opciones.addButton(self.casilla_email,4)

        self.barra_de_busqueda = QtWidgets.QLineEdit(self)
        self.barra_de_busqueda.setEnabled(False)

        self.boton_buscar = QPushButton()
        self.boton_buscar.setFlat(True)
        self.boton_buscar.setIcon(QtGui.QIcon('./iconos/lupa.png'))
        self.boton_buscar.setEnabled(False)
        self.buscar = True

        self.boton_cancelar = QPushButton(' Cancelar')
        self.boton_cancelar.setFlat(True)
        self.boton_cancelar.setIcon(QtGui.QIcon('./iconos/x.png'))

        self.parametro_de_busqueda = ''
        self.llave_de_busqueda = ''

    def _interfaz(self):
        self.cabecera = QVBoxLayout()
        self.nevegador = QHBoxLayout()
        self.buscador = QHBoxLayout()

        self.CUERPO = QVBoxLayout(self)

        self.cabecera.addWidget(self.H1)
        self.cabecera.setAlignment(QtCore.Qt.AlignBottom)

        self.nevegador.addWidget(self.casilla_nombre)
        self.nevegador.addWidget(self.casilla_compania)
        self.nevegador.addWidget(self.casilla_puesto)
        self.nevegador.addWidget(self.casilla_email)

        self.buscador.addWidget(self.barra_de_busqueda)
        self.buscador.addWidget(self.boton_buscar)
        self.buscador.addWidget(self.boton_cancelar)

        self.CUERPO.addLayout(self.cabecera)
        self.CUERPO.addLayout(self.nevegador)
        self.CUERPO.addLayout(self.buscador)


    def _senyales(self):
        self.opciones.buttonClicked[int].connect(self.habilitar_barra_de_busqueda)
        self.barra_de_busqueda.returnPressed.connect(self.enviar_datos_de_busqueda)
        
        self.boton_buscar.clicked.connect(self.enviar_datos_de_busqueda)
        self.boton_cancelar.clicked.connect(lambda : self.click_cancelar.emit(True))


    def habilitar_barra_de_busqueda(self,_id):

        if not self.llaves_principales:
            return
        self.llave_de_busqueda = self.llaves_principales[_id - 1]

        self.barra_de_busqueda.setEnabled(True)
        self.boton_buscar.setEnabled(True)



    def enviar_datos_de_busqueda(self):
        
        if not self.lista_de_diccionarios:
            return

        self.parametro_de_busqueda = self.barra_de_busqueda.text()
        lista_de_encontrados = list()

        if self.parametro_de_busqueda:
            indice = cliente.Busca_Cliente(self.llave_de_busqueda,self.parametro_de_busqueda,self.lista_de_diccionarios)
            if indice:
                lista_de_encontrados.append(indice)
                lista_de_diccionarios = []
                for i in indice:
                    lista_de_diccionarios.append(self.lista_de_diccionarios[i])
                lista_de_encontrados.append(lista_de_diccionarios)

                self.click_busqueda.emit(lista_de_encontrados)
            else:
                self.barra_de_busqueda.setPlaceholderText('-- No Encontrado --')
                self.barra_de_busqueda.clear()

        

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    #cliente.AbrirBase_Declientes()

    v = QBusqueda()
    v.cargar(cliente.CLIENTES)
    v.show()

    sys.exit(app.exec_())
