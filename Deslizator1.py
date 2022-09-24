


# Clase Bloque que implementara la funcionalidad de un solo bloque
class Bloque(object):
    # propiedades: coordenadas (fila, columna), color
    def __init__(self, fila, col0,col1, col):
        self.fil = fila
        self.colI = col0
        self.colF = col1
        self.color = col

class Tablero(object):
    def __init__(self, nomfich, numfil):
        self.numfil = numfil
        self.numcol = 10


def main():
    tab = Tablero(12,10)

if '__name__':
    main()