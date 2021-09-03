from cliente import CLIENTES,AbrirBase_Declientes
from PyQt5 import QtWidgets, QtGui,QtCore
from PyQt5.QtWidgets import QApplication

class QMostrar(QtWidgets.QWidget):

    def __init__(self):
        super(QtWidgets.QWidget,self).__init__()
        self.iniciador()
        self.interfaz()

    def iniciador(self):
        self.area_de_texto = QtWidgets.QTextEdit()
        self.area_de_texto.setReadOnly(True)
        self.area_de_texto.setStyleSheet("background-color:#00000000;")
        


    def interfaz(self):
        self.area = QtWidgets.QVBoxLayout(self)
        self.area.addWidget(self.area_de_texto)



    def _limite_de_informacion(self,lista_general):
            self.lista_de_LLaves = []
            try:
                for llave in lista_general[0].keys():
                    self.lista_de_LLaves.append(llave)
            except AttributeError:
                return None

            return ( len(lista_general) + 1,len(self.lista_de_LLaves) + 1)



    def Cargar(self,lista):
        if not lista:
            return
        self.tabla = self.area_de_texto.textCursor()

        self.formato_de_tabla = QtGui.QTextTableFormat()
        self.formato_de_tabla.setAlignment(QtCore.Qt.AlignCenter)
        self.formato_de_tabla.setCellPadding(50)
        self.formato_de_tabla.setCellPadding(5)

        fila_columna = self._limite_de_informacion(lista)
        if not fila_columna:
            self.area_de_texto.clear()
            return
        self.tabla.insertTable(fila_columna[0],fila_columna[1],self.formato_de_tabla)
        self._imprimir_informacion(lista)



    def ReCargar(self,lista):
        self.area_de_texto.clear()
        self.Cargar(lista)



    def _imprimir_informacion(self,lista_general):
        self.tabla.insertText('[ ]')
        self.tabla.movePosition(QtGui.QTextCursor.NextCell)

        for elemento in self.lista_de_LLaves:
            self.tabla.insertText(elemento)
            self.tabla.movePosition(QtGui.QTextCursor.NextCell)

        for ind, Diccionario in enumerate(lista_general):
            if type(Diccionario) != dict:
                continue
            self.tabla.insertText(str(ind))
            self.tabla.movePosition(QtGui.QTextCursor.NextCell)
            for valor in Diccionario.values():
                self.tabla.insertText(valor)
                self.tabla.movePosition(QtGui.QTextCursor.NextCell)
            

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    AbrirBase_Declientes()
    v = QMostrar()
    v.Cargar(CLIENTES)
    v.show()
    sys.exit(app.exec_())