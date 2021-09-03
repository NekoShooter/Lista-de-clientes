from QtAgregar import QAgregar
from QtBusqueda import QBusqueda
from QtEditar import QEditar
from QtEliminar import QEliminar
from QtMostrar import QMostrar
from QtMultiplesIndices import QMultiplesIndices
from QtOpciones import QOpciones

from cliente import CLIENTES, AbrirBase_Declientes,GuardarBase_DeClientes
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication,\
                            QWidget,\
                            QLabel,\
                            QHBoxLayout,\
                            QVBoxLayout

class Ventana_principal(QWidget):
    def __init__(self,lista = None):
        super(QWidget,self).__init__()
        self.propiedades_de_ventana()
        self.iniciador(lista)
        self.interfaz()
        self.conexiones()

    def propiedades_de_ventana(self):
        self.setMinimumWidth(750)


    def iniciador(self,lista):
        self.LISTA_CLIENTES = lista
        self.lista_de_widgets = []
        self.boton_pulsado = None

        self.menu_principal = QOpciones()
        self.tabla_de_clientes = QMostrar()
        self.menu_de_busqueda = QBusqueda()
        self.editar = QEditar()
        self.agregar = QAgregar()
        self.eliminar = QEliminar()
        self.elegir_cliente = QMultiplesIndices()

        imagen = QtGui.QPixmap('./iconos/Python Qt5.png')
        imagen.scaled(50,100)
        self.Imagen = QLabel()
        self.Imagen.setPixmap(imagen)

        self.lista_de_widgets.append(self.menu_de_busqueda)
        self.lista_de_widgets.append(self.editar)
        self.lista_de_widgets.append(self.agregar)
        self.lista_de_widgets.append(self.eliminar)
        self.lista_de_widgets.append(self.Imagen)
        self.lista_de_widgets.append(self.elegir_cliente)
        self.__bloquear(4)


    def __bloquear(self,exepcion = None):
        if exepcion != None:
            self.lista_de_widgets[exepcion].setHidden(False)

        for ind, widget in enumerate(self.lista_de_widgets):
            if ind != exepcion:
                widget.setHidden(True)


    def interfaz(self):
        encabezado = QHBoxLayout()
        encabezado.addWidget(self.menu_principal)

        lateral_izq = QVBoxLayout()
        lateral_izq.addWidget(self.menu_de_busqueda)
        lateral_izq.addWidget(self.elegir_cliente)
        lateral_izq.addWidget(self.editar)
        lateral_izq.addWidget(self.agregar)
        lateral_izq.addWidget(self.eliminar)
        lateral_izq.addWidget(self.Imagen)
        lateral_izq.setAlignment(QtCore.Qt.AlignTop)

        lateral_der = QHBoxLayout()
        lateral_der.addWidget(self.tabla_de_clientes)

        centro = QHBoxLayout()
        centro.addLayout(lateral_izq)
        centro.addLayout(lateral_der)

        self.CUERPO = QVBoxLayout(self)
        self.CUERPO.addLayout(encabezado)
        self.CUERPO.addLayout(centro)

    def conexiones(self):
        self.menu_principal.click[int].connect(self.__activar_funciones)
        self.menu_principal.cancelar.connect(self.__restablecer_funciones)

        self.menu_de_busqueda.click_busqueda[list].connect(self.__encontrado)
        self.menu_de_busqueda.click_cancelar.connect(lambda: self.menu_principal.cancelar.emit(self.boton_pulsado))

        self.elegir_cliente.indice_elegido[int].connect(self.__modificar_eliminar)
        self.elegir_cliente.cancelar.connect(lambda: self.menu_principal.cancelar.emit(self.boton_pulsado))

        self.eliminar.eliminar.connect(self.__mostrar)
        self.eliminar.cancelar.connect(lambda: self.menu_principal.cancelar.emit(self.boton_pulsado))

        self.editar.cambioHecho.connect(self.__mostrar)
        self.editar.cancelar.connect(lambda: self.menu_principal.cancelar.emit(self.boton_pulsado))

        self.agregar.Agregado[dict].connect(self.__agregar)
        self.agregar.Cancelar.connect(lambda: self.menu_principal.cancelar.emit(self.boton_pulsado))

    def __activar_funciones(self, ind = 4):
        self.boton_pulsado = ind
        if ind == 0 or ind == 1 or ind == 3:
            self.__bloquear(0)
            self.menu_de_busqueda.cargar(self.LISTA_CLIENTES)
        elif ind == 2:
            self.__bloquear(ind)
        if ind == 4:
            self.__mostrar()

    def __mostrar(self):
        self.__bloquear(4)
        self.menu_principal._desbloquear(self.boton_pulsado)
        self.tabla_de_clientes.ReCargar(self.LISTA_CLIENTES)
        if self.boton_pulsado != 4:
            GuardarBase_DeClientes()
        


    def __encontrado(self, lista_de_informacion):
        lista_de_diccionarios = lista_de_informacion[1]
        self.tabla_de_clientes.ReCargar(lista_de_diccionarios)
        if self.boton_pulsado == 0: # buscar
            self.menu_principal.cancelar.emit(0)
        else:
            if len(lista_de_informacion[0]) > 1:
                self.__bloquear(5)
                self.elegir_cliente.cargar(lista_de_informacion[0])
            else:
                self.__modificar_eliminar(lista_de_informacion[0][0])

    def __modificar_eliminar(self,ind):
        print(ind)
        self.__bloquear(self.boton_pulsado)
        if self.boton_pulsado == 1: # editar
            self.editar.cargar(self.LISTA_CLIENTES[ind])
        if self.boton_pulsado == 3: # eliminar
            self.eliminar.cargar(self.LISTA_CLIENTES,ind)

    def __agregar(self, diccionario_nuevo):
        self.LISTA_CLIENTES.append(diccionario_nuevo)
        self.__mostrar()


    def __restablecer_funciones(self):
        self.__bloquear()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    AbrirBase_Declientes()
    v = Ventana_principal(CLIENTES)
    v.show()
    sys.exit(app.exec_())
