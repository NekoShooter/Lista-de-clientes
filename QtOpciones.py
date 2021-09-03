from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QApplication




def _crear_boton(titulo,icono):
    boton = QPushButton()
    boton.setFlat(True)
    boton.setToolTip(titulo)
    boton.setIcon(QtGui.QIcon(icono))
    boton.setIconSize(QtCore.QSize(50,50))
    return boton


class QOpciones(QWidget):
    click = QtCore.pyqtSignal(int)

    cancelar = QtCore.pyqtSignal(int)


    def __init__(self):
        super(QWidget,self).__init__()
        self.inicializador()
        self.interfaz()
        self.conexiones()



    def inicializador(self):
        self.H1 = QtWidgets.QLabel('¿Que desea realizar?')

        self.boton_buscar = _crear_boton('Buscar','./iconos/buscar.png')
        self.boton_mostrar = _crear_boton('mostrar','./iconos/lista.png')
        self.boton_editar = _crear_boton('editar','./iconos/editar.png')
        self.boton_agregar = _crear_boton('agregar','./iconos/agregar.png')
        self.boton_eliminar = _crear_boton('eliminar','./iconos/eliminar.png')

        self.opciones = QtWidgets.QButtonGroup()
        self.opciones.addButton(self.boton_buscar,0)
        self.opciones.addButton(self.boton_editar,1)
        self.opciones.addButton(self.boton_agregar,2)
        self.opciones.addButton(self.boton_eliminar,3)
        self.opciones.addButton(self.boton_mostrar,4)



    def interfaz(self):
        contenedor_opciones = QHBoxLayout()
        self.CUERPO = QVBoxLayout(self)

        contenedor_opciones.addWidget(self.boton_buscar)
        contenedor_opciones.addWidget(self.boton_mostrar)
        contenedor_opciones.addWidget(self.boton_editar)
        contenedor_opciones.addWidget(self.boton_agregar)
        contenedor_opciones.addWidget(self.boton_eliminar)

        self.CUERPO.addWidget(self.H1)
        self.CUERPO.addLayout(contenedor_opciones)



    def conexiones(self):
        self.opciones.buttonClicked[int].connect(self._opcion_elegida)
        self.cancelar.connect(self._desbloquear)



    def _opcion_elegida(self,_id):
        opcion_elegida = _id

        if self._verificar_bloqueo():
                self.cancelar.emit(opcion_elegida)
                return

        self._desbloquear(opcion_elegida,False)
        self.click.emit(opcion_elegida)
            

                
    def _desbloquear(self,boton_id,Enable = True):
        if boton_id == 4:
            return
        for i in range(0,5):
            if i != boton_id:
                self.opciones.button(i).setEnabled(Enable)



    def _verificar_bloqueo(self):
        for i in range(0,5):
            if not self.opciones.button(i).isEnabled():
                return True

        return False


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)

    v = QOpciones()
    v.show()

    sys.exit(app.exec_())