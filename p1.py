


# Código de referencia para la segunda práctica de Paradigmas de Programación
# Grado en Ingeniería Informática, Grado en Estadística
# Universidad de Valladolid © 2021
#
# Autor: César Vaca Rodríguez (cvaca@infor.uva.es)

# ************** CONSTANTES ********************
CH_PANT = ord('#')  # Inicio secuencia caracteres pantalla
CH_FICH = ord('A')  # Inicio secuencia caracteres fichero (mayúsculas)
CH_FIL = ord('A')   # Inicio secuencia caracteres que representan filas
CH_COL = ord('0')   # Inicio secuencia caracteres que representan columnas


# Ejemplo de corutina/generador: Devuelve de forma cíclica los elementos
# de la lista que se pasa por parámetro (nunca termina)
# Ver https://docs.python.org/3/tutorial/classes.html#generators
def ciclo(lis):
    while True:
        for elem in lis:
            yield elem


class Bloque(object):
    """ Representa un bloque. Propiedades: fila, columna inicial, final y valor (color) """
    def __init__(self, fil, col0, col1, val):
        self.fil = fil
        self.col0 = col0
        self.col1 = col1
        self.val = val            # Es un entero positivo (0, 1, ...)
        self.n = col1 - col0 + 1  # Tamaño del bloque

    # Desplazamiento de un bloque
    def desplazar(self, dx, dy):
        self.fil += dy
        self.col0 += dx
        self.col1 += dx

    # Para depuración
    def __repr__(self):
        return f"{self.col0}-{self.col1},{self.fil}:{self.val}"

    # Ver https://docs.python.org/3/reference/datamodel.html#object.__str__
    def __str__(self):
        return chr(self.val+CH_PANT)*(4*self.n-1)


class Tablero(object):
    """ Representa el estado del Tablero en un momento dado """

    # Se pasa como parámetros el nombre de ficheros de filas entrantes
    # y el número de filas del tablero (las columnas son siempre 10)
    def __init__(self, nomfich, numfil):
        # Lectura de fichero de filas entrantes
        with open(nomfich) as fich:
            self.entrada = ciclo(fich.read().splitlines())
        # Propiedades/Atributos: Tamaño del tablero y puntuación
        self.nfil = numfil
        self.ncol = 10
        self.ptos = 0
        # El tablero se representa como una lista de filas,
        # cada fila es una lista de Bloques. Usamos compresión de listas
        # Ver https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
        self.dat = [[] for _ in range(numfil)]

    # ************** OPERACIONES PRINCIPALES ********************

    # Comprueba si hay bloques en la primera fila (fin de partida)
    def lleno(self):
        return len(self.dat[0]) > 0

    # Asigna una nueva fila de bloques en la parte superior del tablero
    def ins_fila(self):
        # Nueva linea de texto (formato fichero) que indica los bloques
        # Ver https://docs.python.org/3/library/functions.html#next
        # Ver https://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do
        linea = next(self.entrada)
        # Ver https://docs.python.org/3/tutorial/datastructures.html sección 5.1.3
        self.dat[0] = [Bloque(0, c0, c1, val) for (c0, c1, val) in self.bloques_en_linea(linea)]

    # Traduce jugada (string) y la efectúa si es correcta. Valores devueltos:
    # -3 -> Sintaxis errónea
    # -2 -> El bloque no puede desplazarse
    # -1 -> No hay bloque en esa posición
    #  0 -> Jugada válida
    def jugada(self, jug):
        if len(jug) != 3:
            return -3
        # No hace movimiento
        if jug == '---':
            return 0
        # Obtener fila y columna
        fil = ord(jug[0]) - CH_FIL
        col = ord(jug[1]) - CH_COL
        # Fuera de rango
        if fil < 0 or fil >= self.nfil or col < 0 or col >= self.ncol:
            return -3
        # Indice del bloque en esa columna
        i = self.index_bloque(self.dat[fil], col)
        # No es una posición de bloque
        if i < 0:
            return -1
        b = self.dat[fil][i]
        # Comprobar si se puede desplazar
        if jug[2] == '<':            
            if i == 0:
                # Caso de bloque situado más a la izquierda
                if b.col0 == 0:  # Pegado a borde
                    return -2
                # Lo movemos al borde
                b.desplazar(-b.col0, 0)
            else:
                ba = self.dat[fil][i - 1]  # Bloque anterior
                db = b.col0 - ba.col1 - 1    # Espacio entre bloques
                if db == 0:  # Pegado a nuestro bloque
                    return -2
                # Lo movemos de forma que se "pegue" al bloque anterior
                b.desplazar(-db, 0)
        elif jug[2] == '>':
            if i == len(self.dat[fil])-1:
                # Caso de bloque situado más a la derecha
                if b.col1 == self.ncol-1:  # Pegado a borde
                    return -2
                # Lo movemos al borde
                b.desplazar(self.ncol-b.col1-1, 0)
            else:
                bs = self.dat[fil][i + 1]  # Bloque siguiente
                db = bs.col0 - b.col1 - 1    # Espacio entre bloques
                if db == 0:  # Pegado a nuestro bloque
                    return -2
                # Lo movemos de forma que se "pegue" al bloque siguiente
                b.desplazar(db, 0)
        else:
            return -3
        return 0

    # Se hacen caer los bloques recorriendo las filas desde la penúltima
    # a la primera (de "abajo" a "arriba")
    def caida(self):
        for fil_ori in range(self.nfil-2, -1, -1):
            # Se recorren los bloques de la fila
            # Cuidado: Como es posible que durante el bucle modifiquemos la composición
            # de la fila, el bucle trabaja sobre una copia de la fila ([:])
            for b in self.dat[fil_ori][:]:
                # Se comprueban huecos en filas inferiores
                fil_des = pos_hueco = -1
                for i in range(fil_ori+1, self.nfil):
                    ph = self.pos_ins_bloque(self.dat[i], b)
                    if ph == -1:
                        break
                    pos_hueco = ph
                    fil_des = i
                # Si hay descenso, mover el bloque
                if fil_des > -1:
                    self.dat[fil_ori].remove(b)
                    self.dat[fil_des].insert(pos_hueco, b)
                    b.desplazar(0, fil_des - fil_ori)

    # Elimina las filas completas, detectando si se produce una "reacción en cadena"
    # Devuelve la lista de bloques borrados
    def eliminacion(self):
        lis = []
        reaccion_cadena = False
        inc_ptos = 0
        for fil in range(self.nfil):
            if self.fila_completa(self.dat[fil], self.ncol):
                if self.fila_mismo_color(self.dat[fil]):
                    reaccion_cadena = True
                    break
                lis += self.borra_fila(fil)
                hay_borrado = True
                inc_ptos += self.ncol
        if reaccion_cadena:
            for fil in range(self.nfil):
                # Suma de las longitudes de todos los bloques de la fila,
                # usando una enumeración mediante la sintaxis (.. for .. in ..)
                # Ver https://docs.python.org/3/tutorial/classes.html#generator-expressions
                inc_ptos += sum((b.n for b in self.dat[fil]))
                lis += self.borra_fila(fil)
        self.ptos += inc_ptos
        return lis

    # Ver https://docs.python.org/3/reference/datamodel.html#basic-customization
    def __str__(self):
        return self.tab2txt()

    def __repr__(self):
        return self.tab2txt()

    # ************** OPERACIONES AUXILIARES ********************

    # Se define como método aparte para que pueda sobrescribirse en clases derivadas
    # Devuelve la lista de bloques borrados
    def borra_fila(self, fil):
        lis = self.dat[fil]
        self.dat[fil] = []
        return lis

    # Iterador sobre todos los bloques del tablero, implementado mediante corutina/generador
    def iter_bloques(self):
        for fila in self.dat:
            for b in fila:
                yield b

    # Devuelve una tupla (columna inicial, final y valor/color) por cada bloque que
    # aparece en la línea de texto (formato fichero). Implementado mediante corutina/generador
    # Ver https://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do
    @staticmethod
    def bloques_en_linea(lin):
        i, n, c_ant = 0, 0, ' '
        for c in lin:
            if c != c_ant:
                if c_ant != ' ':
                    yield (i-n, i-1, ord(c_ant.upper())-CH_FICH)
                c_ant = c
                n = 1
            else:
                n += 1
            i += 1
        if c_ant != ' ':
            yield (i-n, i-1, ord(c_ant.upper())-CH_FICH)

    # Busca en la lista el bloque que contiene esa columna
    # Devuelve su índice en la lista o -1 si no existe
    @staticmethod
    def index_bloque(lis, col):
        i = 0
        for b in lis:
            if b.col0 <= col <= b.col1:
                return i
            i += 1
        return -1

    # Devuelve la posición donde se debería insertar un bloque
    # si existe un hueco para él (o -1 si no se puede insertar)
    @staticmethod    
    def pos_ins_bloque(lis, blo):
        # Búsqueda del primer bloque totalmente posterior al nuestro
        i = 0
        for b in lis:
            if b.col0 > blo.col1:
                break
            i += 1
        # Si existe colisión, es con el bloque anterior al posterior
        return i if i == 0 or lis[i-1].col1 < blo.col0 else -1

    # Comprueba si una fila está completa
    @staticmethod
    def fila_completa(fila, numcol):
        if len(fila) == 0:
            return False
        # Comprobación de que los bloques inicial y final cubren los extremos 
        if fila[0].col0 != 0 or fila[-1].col1 != numcol-1:
            return False
        # Comprobación de que todos los bloques están "pegados"
        # Ver https://docs.python.org/3/library/functions.html#zip
        for (b1, b2) in zip(fila, fila[1:]):
            if b1.col1+1 != b2.col0:
                return False
        return True

    # Comprueba si en una fila completa todos los bloques son del mismo color
    # Ver https://docs.python.org/3/library/functions.html#all
    # Ver https://docs.python.org/3/library/functions.html#map
    # Ver https://docs.python.org/3/tutorial/controlflow.html#lambda-expressions
    @staticmethod
    def fila_mismo_color(fila):
        return all(map(lambda b: b.val == fila[0].val, fila[1:]))

    # Traducción de fila a texto
    def fil2txt(self, letra, fila):
        ca = 0
        lin = letra+' '
        for b in fila:
            lin += '|   '*(b.col0-ca) + '|' + str(b)
            ca = b.col1+1
        lin += '|   '*(self.ncol-ca) + '|\n'
        return lin
            
    # Traducción de tablero a texto
    # Ver https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
    # Ver https://docs.python.org/3/library/functions.html#zip
    # Ver https://docs.python.org/3/library/stdtypes.html?highlight=join#str.join
    def tab2txt(self):
        sep = '  ' + '---'.join(['+']*(self.ncol+1)) + '\n'
        ejey = [chr(i+CH_FIL) for i in range(self.nfil)]
        ejex = '    ' + '   '.join([chr(i+CH_COL) for i in range(self.ncol)]) + '\n'
        return sep + sep.join([self.fil2txt(*p) for p in zip(ejey, self.dat)]) + sep + ejex


def main():
    print("*** PRACTICA DE PARADIGMAS 2020-21 ***\n")
    nomfich = input("Fichero de filas iniciales: ")
    tab = Tablero(nomfich, 12)
    while not tab.lleno():
        # Insertar fila
        tab.ins_fila()
        print("1. INSERCIÓN FILA")
        print(tab)
        print(f"Puntuación: {tab.ptos}\n")
        # Obtener y realizar jugada
        error = True
        while error:
            jug = input("Introduzca jugada o --- o FIN: ")
            if jug == "FIN":
                return
            res = tab.jugada(jug)
            if res == -3:
                print("Error de sintaxis en jugada")
            elif res == -2:
                print("El bloque no puede moverse en esa dirección")
            elif res == -1:
                print("No hay ningún bloque en esa celda")
            else:
                error = False
        print("2. MOVIMIENTO")
        print(tab)
        # Caída de bloques y borrado de filas
        seguir = True
        while seguir:
            tab.caida()
            print("3. CAÍDA")
            print(tab)
            lis = tab.eliminacion()
            seguir = len(lis) > 0
            if seguir:
                print("4. ELIMINACIÓN")
                print(tab)


if __name__ == '__main__':
    main()
