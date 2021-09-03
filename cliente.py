import sys
import os


CLIENTES = []

MENU_DICCIONARIO = {'N':'NOMBRE',
                    'P':'POSICION', 
                    'C':'COMPANIA',
                    'E':'EMAIL'}

BASE_TXT = './lista_de_clientes.txt'
BASE_TEMP = 'lista_de_clientes.temp'

def AbrirBase_Declientes():
    global BASE_TXT, CLIENTES

    try:
        with open(BASE_TXT,'r',encoding='utf-8') as __ARCHIVO__:
            base_de_clientes = __ARCHIVO__.read()

            limite = 0
            un_cliente = dict()

            un_dato_del_cliente = base_de_clientes.split(',')

            for index, dato in enumerate(un_dato_del_cliente):
                if index % 2 != 0:
                    un_cliente[un_dato_del_cliente[index - 1]] = dato
                    limite += 1
                if limite == 4:
                    CLIENTES.append(un_cliente)
                    un_cliente = dict()
                    limite = 0
    except FileNotFoundError:
        with open(BASE_TXT,'w',encoding='utf-8') as __ARCHIVO__:
            return

def GuardarBase_DeClientes():
    global BASE_TXT, CLIENTES

    with open('lista_de_clientes.temp','w', encoding='utf-8') as __ARCHIVO__:
        for cliente in CLIENTES:
            for llave, valor in cliente.items():
                __ARCHIVO__.write(f'{llave},{valor},')

    os.remove(BASE_TXT)
    os.rename(BASE_TEMP, BASE_TXT)



def Agrega_Cliente():
    global CLIENTES
    cliente = dict()
    print('por favor agrega:')
    for valor in MENU_DICCIONARIO.values():
        cliente[valor] = input(f'{valor} :')
    CLIENTES.append(cliente)
    Mostrar_Clientes()
    GuardarBase_DeClientes()


def Elimina_Cliente():
    print('Como desea localizar a su cliente a eliminar: ')
    cliente = busqueda_de_cliente()
    if cliente:
        accion =__Dame_comando(texto = 'deseas continuar [S]i / [TECLA] no : ')
        if accion == 'S':
            indice = cliente[0]
            if len(cliente) > 1:
                indice = __Dame_comando(cliente,'Elige el indice de quien deseas eliminar : ')

            CLIENTES.pop(indice)
            GuardarBase_DeClientes()


def Actualiza_Cliente():
    print('Localize su cliente para actualizar: ')
    cliente = busqueda_de_cliente()
    if cliente:
        accion = __Dame_comando(texto ="deseas hacer una actualizacion [S]i / [TECLA] no : ")
        indice = -1
        while accion == 'S':
            if indice == -1 and len(cliente) == 1:
                indice = cliente[0]
            elif indice == -1:
                indice = __Dame_comando(cliente,"Elige el indice de quien deseas actualizar : ")

            llave = __Dame_comando(MENU_DICCIONARIO,'que deseas actualizar :')
            CLIENTES[indice][llave] = input(f'actualiza {llave} : ')
            print('¿Quieres continuar ACTUALIZANDO a')
            Mostrar_Clientes([indice])
            GuardarBase_DeClientes()
            accion = __Dame_comando(texto='[S]i /[TECLA] no : ')


def busqueda_de_cliente():
     llave = __Dame_comando(MENU_DICCIONARIO,'Buscar por: ')
     valor = input(f'ingresa el {llave} : ')
     return Busca_Cliente(llave,valor,CLIENTES)

def Busca_Cliente(llave,valor,lista_de_diccionarios):
    print(f'{llave} : {valor}')
    cliente_localizado = []
    cliente_localizado = __localiza_por_medio_de(llave,valor,lista_de_diccionarios)
    if cliente_localizado:
        print('mostrando informacion: ')
        Mostrar_Clientes(cliente_localizado)
    else:
        print('el cliente no ha sido localizado')

    return cliente_localizado



def __localiza_por_medio_de(llave,valor,lista_de_diccionarios):
    objeto = valor.lower()
    indice = []
    for i , cliente in enumerate(lista_de_diccionarios):
        if cliente[llave] == objeto:
            indice.append(i)
    return indice
        

def Mostrar_Clientes(indice = None):
    global CLIENTES
    if indice == None:
        for ind, cliente in enumerate(CLIENTES):
            print(f'[{ind}] : ',end='')
            for llave, valor in cliente.items():
                print(f'[{llave} = {valor}]', end=' ')
            print("")
    else:
        for i in indice:
            print(f'[{i}] : ',end='')
            for llave, valor in CLIENTES[i].items():
                print(f'[{llave} = {valor}]',end=' ')
            print('')


MENU = '''
            BIENVENIDO
            ********************
            ¿Que desea realizar?
            [I]ngresar cliente
            [B]uscar cliente
            [E]liminar cliente
            [A]ctualizar cliente
            [M]ostrar clientes
            [TECLA] para salir
            '''


def Interfaz():
    AbrirBase_Declientes()
    while True:
        print('')
        comando = __Dame_comando(texto=MENU)
        if comando == 'I':
            Agrega_Cliente()
        elif comando == 'B':
            busqueda_de_cliente()
        elif comando == 'E':
            Elimina_Cliente()
        elif comando == 'A':
            Actualiza_Cliente()
        elif comando == 'M':
            Mostrar_Clientes()
        else:
            break


def __Dame_comando(menu_de_intercion = None, texto = ''):
    while True:
        print(texto)
        if type(menu_de_intercion) == dict:
            for llave , valor in menu_de_intercion.items():
                print(f'[{llave}] : [{valor}] ')
        comando = input().upper()
        if type(menu_de_intercion) == dict:
            try:
                return menu_de_intercion[comando]
            except KeyError:
                pass
        elif menu_de_intercion == None:
            if len(comando) == 1:
                return comando.upper()
        elif type(menu_de_intercion) == list:
            try:
                if int(comando) in menu_de_intercion:
                    return int(comando)
            except ValueError:
                pass
        print('intentalo de nuevo ')


if __name__ == "__main__":
    Interfaz()
