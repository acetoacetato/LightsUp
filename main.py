import pygame, sys
from math import floor
from time import sleep


SCREEN_WIDTH = 700
SCREEN_HEIGHT = 600
filename = "input.txt"
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Clase que guarda los gráficos usados en la interfaz
class Imagenes:
    imagenes = {}
    def __init__(self, ancho, largo):
        
        ampolleta = pygame.image.load("./img/bulb.jpg")
        ampolleta = pygame.transform.scale(ampolleta, (floor(ancho-2), floor(largo-2)))
        Imagenes.imagenes['s-2'] = ampolleta

        cruz = pygame.image.load("./img/x.png")
        cruz = pygame.transform.scale(cruz, (floor(ancho-2), floor(largo-2)))
        Imagenes.imagenes['s-1'] = cruz

        # Se guardan las paredes con números
        for i in range(5):
            aux = pygame.image.load("./img/pared/" + str(i) + ".jpg")
            aux = pygame.transform.scale(aux, (floor(ancho-2), floor(largo-2)))
            Imagenes.imagenes[str(i)] = aux


# Clase que representa un espacio junto con su enlace a la interfaz gráfica
class Espacio:
    estado: int
    iluminado: bool

    def __init__(self, estado=0, iluminado=False):
        self.estado = estado
        self.iluminado = iluminado

    def print(self):
        if self.iluminado:
            print('_', end='')
        if self.estado == 0:
            print('_', end='')

    def draw(self, pos, ancho, largo):
        
        # Calcula las posiciones en x e y de la interfaz gráfica para colocar la imagen
        pos_x = 150 + floor(ancho+2)*pos[0]+2
        pos_y = 100 + floor(largo+2)*pos[1]+2

        #Primero se ilumina
        if self.iluminado:
            color = (255,255,0)
        else:
            color=(255,255,255)
        pygame.draw.rect(screen, color, pygame.Rect(pos_x, pos_y,ancho,largo))

        #Luego se dibuja la imagen
        ## Estado 0 es espacio vacío, así que se omite
        if self.estado == 0:
            return

        screen.blit(Imagenes.imagenes['s-' + str(self.estado)], ((pos_x, pos_y)))
        pygame.display.update()



class Pared:
    numero: int

    def __init__(self, numero):
        self.numero = numero

    def print(self):
        print('[', end='')
        if self.numero != -1:
            print(self.numero, end='')
        print(']', end='')
    
    def draw(self, pos, ancho, largo):
        # Calcula las posiciones en la interfaz gráfica
        pos_x = 150 + floor(ancho+2)*pos[0]+2
        pos_y = 100 + floor(largo+2)*pos[1]+2
        if self.numero == -1:
            # Dibuja una pared vacía en caso de necesitarlo
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(pos_x, pos_y,ancho,largo))
        else:
            # Dibuja una copia de la pared con el número
            screen.blit(Imagenes.imagenes[str(self.numero)], ((pos_x, pos_y)))
        # Actualiza la pantalla
        pygame.display.update()

# Clase que representa el tablero completo, guardando la matriz con los elementos, largo, ancho y la máxima dimensión
class Tablero:
    tablero : [[]]
    largo: int
    ancho: int
    max_dim: int
    def __init__(self, filename):
        f = open(filename, 'r')

        # Se guardan las dimensiones
        dim = f.readline().strip().split(' ')
        self.largo, self.ancho = [int(i) for i in dim]
 
        # Se inicializa el arreglo con 0
        self.tablero = [[0 for x in range(self.ancho)] for y in range(self.largo)] 
        if self.ancho > self.largo:
            self.max_dim = self.ancho
        else:
            self.max_dim = self.largo
        lineas = f.readlines()
        x, y = [0,0]

        # Se recorre cada linea del archivo, creando un espacio o una pared según corresponda
        for linea in lineas:
            datos = linea.strip().split(' ')
            for dato in datos:

                if dato == '-':
                    aux = Espacio()
                else:
                    aux = Pared(int(dato))

                self.tablero[x][y] = aux
                x = x + 1
                
            x = 0
            y = y + 1

        # Se imprime el tablero para confirmar
        for i in range(self.largo):
            for j in range(self.ancho):
                #print(type(self.tablero[i][j]), end='')
                #print(' (' + str(i) + ',' + str(j) + ')')
                self.tablero[i][j].print()
            print('')



    """
        Coloca una ampolleta en el tablero, 
        dibujándola además en la interfaz gráfica 
        pero sin actualizarla
    """
    def coloca_ampolleta(self, x, y):

        # Se calcula el ancho y largo de la imagen
        ancho = 400/self.ancho
        largo = 400/self.largo

        # Si las coordenadas entregadas se salen de 
        #  los límites del tablero, se omite la inserción
        if x > self.ancho or x < 0:
            return False
        if y > self.largo or y < 0:
            return False

        # Se guarda una referencia al espacio en las coordenadas
        espacio = self.tablero[x][y]

        #TODO: Cambiar esto por excepciones
            # Si es una pared
        if isinstance(espacio, Pared):
            return False
            # Si es un espacio iluminado (o contiene una ampolleta)
        elif espacio.iluminado == True:
            return False

            # Si está bloqueado
        elif espacio.estado == 1:
            return False

        else:
            espacio.estado = 2
            espacio.iluminado = True
            #FIXME: mal hecho, optimizar
            # Se recorre hacia arriba
            for i in range(y, -1, -1):
                espacio = self.tablero[x][i]
                if isinstance(espacio, Pared):
                    break;
                else:
                    espacio.iluminado = True

            # Esto va iluminando las casillas en la misma columna/fila que la ampolleta colocada.
            #   Esto va alejandose en cada dirección de 1 a 1 unidad, 
            #       acabando la expansión en c/u cuando hay una pared o se alcanza el final del tablero
            flag_up, flag_down, flag_left, flag_right = [True, True, True, True]
            for i in range(1, self.max_dim):

                # Si aún no alcanza el final del tablero o una pared
                #   la posición en y es positiva (porque python permite underflow por alguna razón)
                #   y el tablero en esa posición tiene un espacio, entonces se ilumina
                if flag_up and (y-i) >= 0 and isinstance(self.tablero[x][y-i], Espacio):
                    self.tablero[x][y-i].iluminado = True
                else:
                    # En caso contrario se cambia el flag para detener la iluminación hacia arriba
                    flag_up = False
                
                # Si aún no alcanza el final del tablero o una pared
                #   la posición en y está dentro del tamaño del tablero
                #   y el tablero en esa posición tiene un espacio, entonces se ilumina
                if flag_down and  (y+i) < self.largo and isinstance(self.tablero[x][y+i], Espacio):   
                    self.tablero[x][y+i].iluminado = True
                else:
                    # En caso contrario se cambia el flag para detener la iluminación hacia abajo
                    flag_down = False

                # Si aún no alcanza el final del tablero o una pared
                #   la posición en x es positiva (porque python permite underflow por alguna razón)
                #   y el tablero en esa posición tiene un espacio, entonces se ilumina
                if flag_left and (x-i) >= 0 and isinstance(self.tablero[x-i][y], Espacio):
                    self.tablero[x-i][y].iluminado = True
                else:
                    flag_left = False

                # Si aún no alcanza el final del tablero o una pared
                #   la posición en x está dentro del tamaño del tablero
                #   y el tablero en esa posición tiene un espacio, entonces se ilumina
                if flag_right and (x+i) < self.ancho and isinstance(self.tablero[x+i][y], Espacio):
                        self.tablero[x+i][y].iluminado = True
                else:
                    flag_right = False

    """
    Marca una casilla como bloqueada (con una X)
    """
    def bloquea(self, x, y):
        if x > self.ancho or x < 0:
            return False
        if y > self.largo or y < 0:
            return False
        
        if isinstance(self.tablero[x][y], Pared):
            return False
        
        if self.tablero[x][y].estado ==2:
            return False
        self.tablero[x][y].estado = 1
        return True
        #self.update()


    """
    Verifica que todas las casillas del tablero están iluminadas.
    Retorna false en caso contrario
    """
    def verifica_tablero(self) -> bool:
        for i in range(self.largo):
            for j in range(self.ancho):
                if isinstance(self.tablero[i][j], Espacio):
                    if self.tablero[i][j].iluminado == False:
                        return False
        return True

    """
    Actualiza la interfaz gráfica del tablero, mandando a dibujar cada casilla.
    """
    def update(self):
        ancho = 400/self.ancho
        largo = 400/self.largo
        for i in range(self.largo):
            for j in range(self.ancho):
                self.tablero[i][j].draw((i,j), ancho-2, largo-2)
        pygame.display.update()



def main():
    
    # Se le pone titulo a la pantalla y se llena el fondo de color blanco
    pygame.display.set_caption("IA light up")
    screen.fill([255,255,255])


    # Se carga los datos del tablero desde archivo
    tablero = Tablero(filename)

    # Se dibuja el contorno del tablero vacío
    pygame.draw.rect(screen, (230,30,30), pygame.Rect(150,100,400,400), 4)
    pygame.display.update()


    # Se calcula el largo y el ancho de cada casilla del tablero
    #   dada la dimensión del contorno y la cantidad de filas y columnas que tiene.
    ancho = 400/tablero.ancho
    largo = 400/tablero.largo

    # Se inicializa la clase que contiene las instancias de las imagenes 
    Imagenes(ancho, largo)

    # Para líneas horizontales
    for i in range(1, tablero.largo):
        pygame.draw.line(screen, (230, 30, 30), (150,100 + i*largo), (400+150,100 +  i*largo), 4)

    # Para líneas verticales
    for i in range(1, tablero.largo):
        pygame.draw.line(screen, (230, 30, 30), (150 + i*ancho, 100), (150 +  i*ancho, 100 + 400), 4)
    tablero.update()


    sleep(1)

    # Se separan los espacios de las paredes, para optimizar el recorrido
    espacios = []
    paredes = []
    for i in range(tablero.largo):
            for j in range(tablero.ancho):
                if isinstance(tablero.tablero[i][j], Espacio):
                    espacios.append((i,j))
                else:
                    paredes.append((i,j))


    # Loop principal de la IA.
    #   Realiza un recorrido de los espacios y las paredes hasta que el puzle esté completo
    while not tablero.verifica_tablero():
        
        # Se recorren los espacios
        for tupla in espacios:
            espacio = tablero.tablero[tupla[0]][tupla[1]]

            # Si el espacio está iluminado, se omite la comprobación de las reglas.
            if espacio.iluminado:
                continue

            # Si el espacio está bloqueado (con una X) y no está iluminado, 
            #   entonces es un candidato a la regla 4
            elif espacio.estado == 1:
                regla_4(tablero, tupla[0], tupla[1])

            # Si es un espacio, no bloqueado y no iluminado, 
            #   entonces es un candidato a la regla 5
            else:
                regla_5(tablero, tupla[0], tupla[1])


        # Se recorren las paredes
        for tupla in paredes:
            pared = tablero.tablero[tupla[0]][tupla[1]]

            # Si la pared contiene un número, 
            #   entonces es un candidato para las reglas 1, 2 y 3
            if pared.numero != -1:
                regla_1(tablero, tupla[0], tupla[1]) # pared
                regla_2(tablero, tupla[0], tupla[1]) # 
                regla_3(tablero, tupla[0], tupla[1])
        
        # Luego de que se apliquen todas las reglas posibles en un recorrido, 
        #   se actualiza la interfaz gráfica (para que sea más rápido).
        # Luego de esto se vuelve a iterar sobre todos los espacios
        tablero.update()

    print("Resuelto!!");
 

    # Un loop que evita cerrar la interfaz
    while True:
        # Posibles entradas del teclado y mouse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


"""
Primera regla para resolver el puzle.
Si el número en una pared es igual a la cantidad de espacios blancos disponibles adyacentes a este,
 entonces se inserta una ampolleta en cada uno de estos.
"""
def regla_1(tablero, x, y):

    # Se confirma primero que la posición ingresada es una pared
    if isinstance(tablero.tablero[x][y], Pared):
        cont = 0

        # Se verifican las posiciones adyacentes, una arriba, una abajo, una izq y una derecha
        for i in [(x,y+1), (x,y-1), (x+1,y), (x-1,y)]:

            # Si la posición está fuera del tablero, se omite
            if i[0] >= tablero.ancho or i[0] < 0:
                continue
            if i[1] >= tablero.largo or i[1] < 0:
                continue
            aux = tablero.tablero[i[0]][i[1]]

            # Si es un espacio y no está bloqueado, se cuenta
            #   ya que puede ser tmbn una ampolleta
            if isinstance(aux, Espacio) and ((aux.estado != 1 and aux.iluminado == False) or aux.estado == 2):
                cont = cont+1
        
        # Si se cumple la condicional de la regla
        if cont == tablero.tablero[x][y].numero:
            for i in [(x,y+1), (x,y-1), (x+1,y), (x-1,y)]:
                # Se vuelve a confirmar que no se excede el rango permitido
                if i[0] >= tablero.ancho or i[0] < 0:
                    continue
                if i[1] >= tablero.largo or i[1] < 0:
                    continue

                tablero.coloca_ampolleta(i[0], i[1])
                


"""
Segunda regla para resolver el puzle:
Si la cantidad de ampolletas adyacentes a una pared es igual al número que tiene dentro de esta,
 entonces el resto de espacios se llenan con una x, 
 bloqueando la posibilidad de colocar una ampolleta dentro de estos
"""
def regla_2(tablero, x, y):

    # Se confirma primero que la posición ingresada es una pared
    if isinstance(tablero.tablero[x][y], Pared):
        cont = 0
        # Se verifican las posiciones adyacentes, una arriba, una abajo, una izq y una derecha
        for i in [(x,y+1), (x,y-1), (x+1,y), (x-1,y)]:
            # Si la posición está fuera del tablero, se omite
            if i[0] >= tablero.ancho or i[0] < 0:
                continue
            if i[1] >= tablero.largo or i[1] < 0:
                continue
            aux = tablero.tablero[i[0]][i[1]]

            # Si es un espacio y tiene una ampolleta, se contabiliza
            if isinstance(aux, Espacio) and aux.estado == 2:
                cont = cont+1

        # La condición de la regla
        if cont == tablero.tablero[x][y].numero:
            for i in [(x,y+1), (x,y-1), (x+1,y), (x-1,y)]:
                # Se vuelve a confirmar que no se pasa del rango
                if i[0] >= tablero.ancho or i[0] < 0:
                    continue
                if i[1] >= tablero.largo or i[1] < 0:
                    continue
                aux = tablero.tablero[i[0]][i[1]]

                # Si es un espacio sin ampolleta, se bloquea
                if isinstance(aux, Espacio) and aux.estado != 2:
                    tablero.bloquea(i[0], i[1])

"""
Tercera regla para resolver el puzle
Si una pared contiene un 3, entonces se llenan con una x los 4 espacios diagonales a esta.
"""
def regla_3(tablero, x, y):
    # Se confirma que es una pared y contiene el número tres
    if isinstance(tablero.tablero[x][y], Pared) and tablero.tablero[x][y].numero == 3:
        # Se bloquean las diagonales, el método "bloquea" de Tablero confirma que están dentro del rango
        for i in [(x-1,y-1), (x+1,y-1), (x-1,y+1), (x+1,y+1)]:
            tablero.bloquea(i[0], i[1])


"""
Cuarta regla para resolver el puzle.
Si un espacio marcado con una x no está iluminado y sólo tiene disponible un espacio (horizontal o vertical)
 para colocar una ampolleta, en ese espacio se debe colocar una. Cabe destacar que la posición de este espacio 
 puede ser en cualquier distancia, pero no debe estar bloqueado por una pared.
"""
def regla_4(tablero, x, y):
    espacio = tablero.tablero[x][y]
    # Lista que guarda las posiciones de los espacios vacíos en la fila/columna del espacio ingresado
    espacios_vacios = []

    # Se verifica que es un espacio bloqueado no liuminado
    if isinstance(espacio, Espacio) and espacio.estado == 1 and espacio.iluminado == False:

        # Se inicializan los flags para cada dirección
        flag_up, flag_down, flag_left, flag_right = [True, True, True, True]

        # Esto va verificando las casillas en la misma columna/fila que el espacio candidato.
        #   Esto va alejandose en cada dirección de 1 a 1 unidad, 
        #       acabando el recorrido en c/u cuando hay una pared o se alcanza el final del tablero
        for i in range(1, tablero.max_dim):
            try:
                # Si el espacio en la posición(x, y+i) no está iluminado y es un espacio vacío, 
                #  entonces se agrega a la lista
                if flag_up and tablero.tablero[x][y+i].iluminado == False and tablero.tablero[x][y+i].estado == 0:
                    espacios_vacios.append((x, y+i))

            # Si en la posición(x, y+i) hay una pared o se excede el rango del tablero, 
            #   entonces lanzará una excepción que se resuelve cambiando el flag, 
            #   deteniendo la búsqueda en esta dirección
            except:
                flag_up = False

            # Verificación porque python permite underflow por alguna razón
            if y-i >= 0:
                try:
                    # Si el espacio en la posición(x, y-i) no está iluminado y es un espacio vacío, 
                    #  entonces se agrega a la lista
                    if flag_down and tablero.tablero[x][y-i].iluminado == False and tablero.tablero[x][y-i].estado == 0:
                        espacios_vacios.append((x, y-i))
                except:
                    flag_down = False

            # Verificación porque python permite underflow por alguna razón
            if x-i >= 0:
                try:
                    # Si el espacio en la posición(x-i, y) no está iluminado y es un espacio vacío, 
                    #  entonces se agrega a la lista
                    if flag_left and tablero.tablero[x-i][y].iluminado == False and tablero.tablero[x-i][y].estado == 0:
                        espacios_vacios.append((x-i, y))
                except:
                    # Si en la posición(x-i, y) hay una pared, 
                    #   entonces lanzará una excepción que se resuelve cambiando el flag, 
                    #   deteniendo la búsqueda en esta dirección
                    flag_left = False

            try:
                # Si el espacio en la posición(x, yi) no está iluminado y es un espacio vacío, 
                #  entonces se agrega a la lista
                if flag_right and tablero.tablero[x+i][y].iluminado == False and tablero.tablero[x+i][y].estado == 0:
                    espacios_vacios.append((x+i, y))
            except:
                # Si en la posición(x, y+i) hay una pared o se excede el rango del tablero, 
                #   entonces lanzará una excepción que se resuelve cambiando el flag, 
                #   deteniendo la búsqueda en esta dirección
                flag_right = False
            


        # Verificación de la regla
        if len(espacios_vacios) == 1:
            # Se obtiene el único espacio vacío encontrado y se inserta una ampolleta ahí
            coord = espacios_vacios[0]
            tablero.coloca_ampolleta(coord[0], coord[1])

"""
Quinta regla para resolver el puzle.
Si un espacio está vacío, no iluminado y todas los demás espacios en su fila y columna están iluminados, 
    son una pared o están bloqueados, entonces se coloca una ampolleta en este espacio.
"""
def regla_5(tablero, x, y):
    espacio = tablero.tablero[x][y]
    espacios_vacios = 0

    # Se verifica que es un espacio vacío no iluminado
    if isinstance(espacio, Pared) or espacio.estado != 0 or espacio.iluminado == True:
        return False

    # Se inicializan los flags para cada dirección
    flag_up, flag_down, flag_left, flag_right = [True, True, True, True]

    # Esto va verificando las casillas en la misma columna/fila que el espacio candidato.
    #   Esto va alejandose en cada dirección de 1 a 1 unidad, 
    #       acabando el recorrido en c/u cuando hay una pared o se alcanza el final del tablero
    for i in range(1, tablero.max_dim):

        try:
            # Si el espacio en la posición(x, y+i) no está iluminado y es un espacio vacío, 
            #  entonces ya no se cumple la regla
            if flag_up and tablero.tablero[x][y+i].iluminado == False and tablero.tablero[x][y+i].estado == 0:
                return False
        except:
            # Si en la posición(x, y+i) hay una pared o se excede el rango del tablero, 
            #   entonces lanzará una excepción que se resuelve cambiando el flag, 
            #   deteniendo la búsqueda en esta dirección
            flag_up = False

        # Verificación porque python permite underflow por alguna razón
        if y-i >= 0:
            try:
                # Si el espacio en la posición(x, y-i) no está iluminado y es un espacio vacío, 
                #  entonces ya no se cumple la regla
                if flag_down and tablero.tablero[x][y-i].iluminado == False and tablero.tablero[x][y-i].estado == 0:
                    return False
            except:
                # Si en la posición(x, y-i) hay una pared, 
                #   entonces lanzará una excepción que se resuelve cambiando el flag, 
                #   deteniendo la búsqueda en esta dirección
                flag_down = False

        # Verificación porque python permite underflow por alguna razón
        if x-i >= 0:
            try:
                # Si el espacio en la posición(x-i, y) no está iluminado y es un espacio vacío, 
                #  entonces ya no se cumple la regla 
                if flag_left and tablero.tablero[x-i][y].iluminado == False and tablero.tablero[x-i][y].estado == 0:
                    return False
            except:
                # Si en la posición(x-i, y) hay una pared, 
                #   entonces lanzará una excepción que se resuelve cambiando el flag, 
                #   deteniendo la búsqueda en esta dirección
                flag_left = False

        try:
            # Si el espacio en la posición(x+i, y) no está iluminado y es un espacio vacío, 
            #  entonces ya no se cumple la regla
            if flag_right and tablero.tablero[x+i][y].iluminado == False and tablero.tablero[x+i][y].estado == 0:
                return False
        except:
            # Si en la posición(x+i, y) hay una pared o se excede el rango del tablero, 
            #   entonces lanzará una excepción que se resuelve cambiando el flag, 
            #   deteniendo la búsqueda en esta dirección
            flag_right = False


    # Si no hay espacios, entonces se coloca una ampolleta en la posición ingresada
    return tablero.coloca_ampolleta(x, y)
            
if __name__ == "__main__":
    main()