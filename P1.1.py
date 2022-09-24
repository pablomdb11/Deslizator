ruta= 'C:\\Users\\Javier\\Downloads\\examen1.txt'
f= open(ruta, 'r')

#PABLO MARTIN DE BENITO

matriz= [[0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0],
 [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0], 
 [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0], ]



simbol={
    'A':'###',
    'a':'###',
    'B':'$$$',
    'b':'$$$',
    ' ':'   ',
    0:'   '}
coordenada_f= {
    'A':0,
    'B':1,
    'C':2,
    'D':3,
    'E':4,
    'F':5,
    'G':6,
    'H':7,
    'I':8,
    'J':9,
    'K':10,
    'L':11,
    '-':0}

def imp_tablero(matriz):
    ncolumnas= range(11)

    letras= 'ABCDEFGHIJKL'
    cont_fil=0
    cont_col=0

    margen='\n  +---+---+---+---+---+---+---+---+---+---+'


    for i in range(26):
        cont_col=0

        if i%2==0:                                                                      #linea par imprime el margen
            if i<=24:
                print(margen)
        else:                                                                           #linea impar imprime las casillas
            for j in ncolumnas:
                if cont_fil==12 and cont_col<10:                                        #imprime los numeros indice
                    if cont_col==0:
                        print(' ', end='')
                    print('  ',cont_col, end='')

                if cont_fil<=11:
                    if cont_col==0:                                                      #imrpime las letras indice
                        print(letras[cont_fil], '', end='')

                    if cont_col<=9:                                                       #imprime lo que hay dentro de las casillas
                        if cont_fil==0:
                            matriz[cont_fil][j]= nueva_linea[j]

                        if matriz[cont_fil][j]== matriz[cont_fil][j-1] and matriz[cont_fil][j]!= ' ' and matriz[cont_fil][j]!=0:
                            print(simbol[matriz[cont_fil][j-1]][0], end='')
                        else:
                            print('|', end='')

                        print(simbol[matriz[cont_fil][j]], end='')
                    
                        
                cont_col+=1
            if cont_fil<12:
                print('|', end='')
            cont_fil+=1
    return ''
    
def bajada(matriz):
    
    ncolumnas=range(10)
    nfilas= range(12)
    test=0

    for i in nfilas: #pasa por todas las filas desde abajo, viendo cual es la linea vacia
        if test==10:
            continue
        for j in ncolumnas: #comprobar si en todas las casillas estan vacias
            fila=11-i
            if matriz[fila][j]==0:
                test+=1
            
    if test==10: #si encuentra una linea vacia guarda esa linea en la vacia
        for j in ncolumnas:
            matriz[fila][j]=matriz[0][j]
        
def jugada(matriz, instruccion):
    fil= coordenada_f[instruccion[0]]
    col= int(instruccion[1])
    mov= instruccion[2]
    memoria= matriz[fil][col]
    i=0

    if matriz[fil][col]==0 or matriz[fil][col]== ' ':
        return 0

    tamaño=1 #tamaño siempre va a ser 1 
    bloques_izq=0
    bloques_der=0

    #comprobar el tamaño de cada bloque, los bloques que tiene a la derecha y a la izquierda
    ncolumnas=range(col+1,10)
    for j in ncolumnas:
        if matriz[fil][j]==matriz[fil][col]:
            tamaño+=1
            bloques_der+=1
        else: #si encuentra una casilla seguida que no sea igual, para y queda establecido el tamaño
            break
    
    ncolumnas=range(-col+1,0)
    for j in ncolumnas:
        if matriz[fil][-j]==matriz[fil][col]:
            tamaño+=1
            bloques_izq+=1
        else:
            break

    #variables para saber donde empieza y termina el bloque
    empieza=col-bloques_izq
    termina=col+bloques_der
    
    if mov=='>': #jugada derecha
        ncolumnas=9-termina
        j=1
        while j<=ncolumnas:
            termina=col+bloques_der #donde termina el bloque se va moviendo tambien
            if matriz[fil][termina+j]==' ':
                while termina>=empieza:
                    matriz[fil][termina+j]=matriz[fil][termina+i]
                    matriz[fil][termina+i]=' '
                    termina+=-1
                i+=1
                j+=1
            else:
                break
            termina+=1
            
    if mov=='<': #jugada izquierda
        ncolumnas=0-empieza
        j=-1
        while j>=ncolumnas:
            empieza=col-bloques_izq
            if matriz[fil][empieza+j]==' ':
                while empieza<=termina:
                    matriz[fil][empieza+j]=matriz[fil][empieza+i]
                    matriz[fil][empieza+i]=' '
                    empieza+=1
                i+=-1
                j+=-1
            else:
                break
            empieza+=-1
    if matriz[fil][col]==memoria:
        return 0
            
def huecos(matriz):
    nfilas=2
    i=11
    ncolumnas=range(10)
    
    while i>=nfilas:
        
        ncolumnas=range(10)
        for j in ncolumnas:
            if matriz[i][j]==' ' or matriz[i][j]==0:
                tamaño=1#tamaño siempre va a ser 1 
                bloques_izq=0
                bloques_der=0
                fil=i
                col=j

                #comprobar el tamaño del hueco que ha detectado
                ncolumnas=range(col+1,10)
                for c in ncolumnas:
                    if matriz[fil][c]==matriz[fil][col]:
                        tamaño+=1
                        bloques_der+=1
                    else: #si encuentra una casilla seguida que no sea igual, para y queda establecido el tamaño
                        break
                
                ncolumnas=range(-col+1,0)
                for c in ncolumnas:
                    if matriz[fil][-c]==matriz[fil][col]:
                        tamaño+=1
                        bloques_izq+=1
                    else:
                        break
                
                if matriz[i-1][j]!=0 and matriz[i-1][j]!=' ':
                    tamaño_b=1 #tamaño siempre va a ser 1 
                    bloques_izq_b=0
                    bloques_der_b=0

                    #comprobar el tamaño del bloque situado arriba del hueco
                    ncolumnas=range(col+1,10)
                    for j in ncolumnas:
                        if matriz[fil-1][j]==matriz[fil-1][col]:
                            tamaño_b+=1
                            bloques_der_b+=1
                        else: #si encuentra una casilla seguida que no sea igual, para y queda establecido el tamaño
                            break
                    
                    ncolumnas=range(-col+1,0)
                    for j in ncolumnas:
                        if matriz[fil-1][-j]==matriz[fil-1][col]:
                            tamaño_b+=1
                            bloques_izq_b+=1
                        else:
                            break

                    if tamaño_b<=tamaño: #comprarar los tamaños del hueco y del bloque de arriba

                        empieza=col-bloques_izq_b
                        termina=col+bloques_der_b

                        
                        while empieza<=termina: #escribir el bloque de tamaño x una linea mas abajo
                            matriz[fil][empieza]=matriz[fil-1][empieza]
                            matriz[fil-1][empieza]=' '
                            empieza+=1
                        
                        empieza=col-bloques_izq_b
                        termina=col+bloques_der_b
                        if empieza>=1 and termina<=8:
                            if matriz[fil][empieza]==matriz[fil][empieza-1] or matriz[fil][termina]==matriz[fil][termina+1]:
                                while empieza<=termina:
                                    cambio(matriz, fil, empieza)
                                    empieza+=1
            
        i+=-1
    
def test(matriz):
    
    puntuacion=0
    nfilas= range(-11,-1)
    ncolumnas= range(10)

    for i in nfilas:
        test=0
        for j in ncolumnas:
            if matriz[-i][j]!=' ' and matriz[-i][j]!=0:
                test+=1
            else:
                continue
        if test==10:
            for j in ncolumnas:
                matriz[-i][j]=' '
            puntuacion+=10
    
    return puntuacion

def cambio(matriz, fil, empieza):
    if matriz[fil][empieza]=='a':
        matriz[fil][empieza]='A'
    if matriz[fil][empieza]=='A':
        matriz[fil][empieza]='a'

    if matriz[fil][empieza]=='b':
        matriz[fil][empieza]='B'
    if matriz[fil][empieza]=='B':
        matriz[fil][empieza]='b'
    return matriz


nueva_linea= f.readline()
print(imp_tablero(matriz))
puntos=0


while True:
    instruccion=input()
    if instruccion=='fin':
        print('PUNTUACION TOTAL: ',puntos)
        break
    #Empieza el programa
    linea=nueva_linea
    nueva_linea= f.readline()
    

    if instruccion!='---':
        try:
            jug=jugada(matriz, instruccion)
            if jug!=0:
                bajada(matriz)
                huecos(matriz)
                puntuacion_jug=test(matriz)
                puntos+=puntuacion_jug
                huecos(matriz)
                puntuacion_jug=test(matriz)
                puntos+=puntuacion_jug
                huecos(matriz)

                print(imp_tablero(matriz))
                puntos+=puntuacion_jug
                print('PUNTUACION: ',puntos)
            else: 
                print('ERROR DE JUGADA')
        except:
            print('INTRODUZCA UNA JUGADA')
        
    else:
        bajada(matriz)
        huecos(matriz)
        puntuacion_jug=test(matriz)
        puntos+=puntuacion_jug
        huecos(matriz)
        puntuacion_jug=test(matriz)
        puntos+=puntuacion_jug
        huecos(matriz)
        

        print(imp_tablero(matriz))
        puntos+=puntuacion_jug
        print('PUNTUACION:',puntos)

    


