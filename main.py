import pygame, sys
from math import floor
from time import sleep


SCREEN_WIDTH = 700
SCREEN_HEIGHT = 600
filename = "input4.txt"
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class Imagenes:
    imagenes = {}
    def __init__(self, ancho, largo):
        
        ampolleta = pygame.image.load("./img/bulb.jpg")
        ampolleta = pygame.transform.scale(ampolleta, (floor(ancho-2), floor(largo-2)))
        Imagenes.imagenes['s-2'] = ampolleta

        ampolleta = pygame.image.load("./img/x.png")
        ampolleta = pygame.transform.scale(ampolleta, (floor(ancho-2), floor(largo-2)))
        Imagenes.imagenes['s-1'] = ampolleta

        
        for i in range(5):
            aux = pygame.image.load("./img/pared/" + str(i) + ".jpg")
            aux = pygame.transform.scale(aux, (floor(ancho-2), floor(largo-2)))
            Imagenes.imagenes[str(i)] = aux



class Espacio:
    estado: int
    iluminado: bool

    def __init__(self, estado=0, iluminado=False):
        self.estado = estado
        self.iluminado = iluminado
        self.font = pygame.font.SysFont('Arial', 25)

    def print(self):
        if self.iluminado:
            print('_', end='')
        if self.estado == 0:
            print('_', end='')

    def draw(self, pos, ancho, largo):
        #pygame.draw.rect(screen, (255,255,255), pygame.Rect(pos[0], pos[1],ancho,largo))
        
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
    texto: pygame.font

    def __init__(self, numero):
        self.numero = numero
        self.font = pygame.font.SysFont('Arial', 25)

    def print(self):
        print('[', end='')
        if self.numero != -1:
            print(self.numero, end='')
        print(']', end='')
    
    def draw(self, pos, ancho, largo):
        pos_x = 150 + floor(ancho+2)*pos[0]+2
        pos_y = 100 + floor(largo+2)*pos[1]+2
        if self.numero == -1:
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(pos_x, pos_y,ancho,largo))
        else:
            screen.blit(Imagenes.imagenes[str(self.numero)], ((pos_x, pos_y)))
        pygame.display.update()


class Tablero:
    tablero : [[]]
    largo: int
    ancho: int
    def __init__(self, filename):
        f = open(filename, 'r')

        # Se guardan las dimensiones
        dim = f.readline().strip().split(' ')
        self.largo, self.ancho = [int(i) for i in dim]
 
        # Se inicializa el arreglo con 0
        self.tablero = [[0 for x in range(self.ancho)] for y in range(self.largo)] 

        lineas = f.readlines()
        x, y = [0,0]
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

    def coloca_ampolleta(self, x, y):
        ancho = 400/self.ancho
        largo = 400/self.largo
        if x > self.ancho or x < 0:
            return
        if y > self.largo or y < 0:
            return
        espacio = self.tablero[x][y]

        #TODO: Cambiar esto por excepciones
            # Si es una pared
        if isinstance(espacio, Pared):
            return
            # Si es un espacio iluminado (o contiene una ampolleta)
        elif espacio.iluminado == True:
            return

            # Si está bloqueado
        elif espacio.estado == 1:
            return

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
            # Se recorre hacia abajo
            for i in range(y, self.largo):
                espacio = self.tablero[x][i]
                if isinstance(espacio, Pared):
                    break;
                else:
                    espacio.iluminado = True
            # Se recorre hacia la izquierda
            for i in range(x, -1, -1):
                espacio = self.tablero[i][y]
                if isinstance(espacio, Pared):
                    break
                else:
                    espacio.iluminado = True

            # Se recorre hacia la derecha
            for i in range(x, self.ancho):
                espacio = self.tablero[i][y]
                if isinstance(espacio, Pared):
                    break
                else:
                    espacio.iluminado = True

        #self.update()
    def bloquea(self, x, y):
        if x > self.ancho or x < 0:
            return
        if y > self.largo or y < 0:
            return
        
        if isinstance(self.tablero[x][y], Pared):
            return
        
        if self.tablero[x][y].estado ==2:
            return
        self.tablero[x][y].estado = 1
        #self.update()

    def verifica_tablero(self) -> bool:
        for i in range(self.largo):
            for j in range(self.ancho):
                if isinstance(self.tablero[i][j], Espacio):
                    if self.tablero[i][j].iluminado == False:
                        return False
        return True

    def update(self):
        ancho = 400/self.ancho
        largo = 400/self.largo
        for i in range(self.largo):
            for j in range(self.ancho):
                self.tablero[i][j].draw((i,j), ancho-2, largo-2)
        pygame.display.update()



def main():
    
    
    pygame.display.set_caption("IA light up")
    screen.fill([255,255,255])
    # el bucle principal del juego

    # Se carga los datos del tablero desde archivo
    tablero = Tablero(filename)

    # Se crea el tablero vacío
    pygame.draw.rect(screen, (230,30,30), pygame.Rect(150,100,400,400), 4)
    pygame.display.update()


    # Se crean las líneas del tablero
    ancho = 400/tablero.ancho
    largo = 400/tablero.largo

    #Se inicializa la clase que contiene las instancias de las imagenes
    Imagenes(ancho, largo)
    # Para líneas horizontales
    for i in range(1, tablero.largo):
        pygame.draw.line(screen, (230, 30, 30), (150,100 + i*largo), (400+150,100 +  i*largo), 4)

    # Para líneas verticales
    for i in range(1, tablero.largo):
        pygame.draw.line(screen, (230, 30, 30), (150 + i*ancho, 100), (150 +  i*ancho, 100 + 400), 4)
    tablero.update()
    sleep(1)
    while not tablero.verifica_tablero():
        for i in range(tablero.largo):
            for j in range(tablero.ancho):
                aux = tablero.tablero[i][j]
                if isinstance(aux, Espacio) and tablero.tablero[i][j].iluminado == True:
                    continue
                if isinstance(aux, Pared):
                    if aux.numero != -1:
                        regla_1(tablero, i, j) # pared
                        regla_2(tablero, i, j) # 
                        regla_3(tablero, i, j)
                    else:
                        continue
                else:
                    if aux.estado == 1:
                        regla_4(tablero, i, j)
                    else:
                        regla_5(tablero, i, j)
            tablero.update()

    print("Resuelto!!");
    #sleep(1)
    #tablero.coloca_ampolleta(1,5)
    #tablero.coloca_ampolleta(2,4)
    #tablero.coloca_ampolleta(3,5)
    #tablero.coloca_ampolleta(2,6)
    #if tablero.verifica_tablero():
    #    print("RESUELTO!!")
    #sleep(1)
    #tablero.coloca_ampolleta(2,0)
    #tablero.coloca_ampolleta(1,1)
    #if tablero.verifica_tablero():
    #    print("RESUELTO!!")
    #sleep(1)
    #tablero.bloquea(0,2)
    #tablero.bloquea(1,3)
    #tablero.bloquea(2,2)
    #tablero.bloquea(5,5)
    #if tablero.verifica_tablero():
    #    print("RESUELTO!!")
    #sleep(1)
    #tablero.coloca_ampolleta(6,5)
    #if tablero.verifica_tablero():
    #    print("RESUELTO!!")
    #sleep(1)
    #tablero.coloca_ampolleta(5,1)
    #tablero.coloca_ampolleta(5,3)
    #tablero.coloca_ampolleta(4,2)
    #if tablero.verifica_tablero():
    #    print("RESUELTO!!")
    #sleep(1)
    #tablero.coloca_ampolleta(0,4)
    #if tablero.verifica_tablero():
    #    print("RESUELTO!!")

    while True:
        # Posibles entradas del teclado y mouse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()



def regla_1(tablero, x, y):
    if isinstance(tablero.tablero[x][y], Pared):
        cont = 0
        for i in [(x,y+1), (x,y-1), (x+1,y), (x-1,y)]:
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
                if i[0] >= tablero.ancho or i[0] < 0:
                    continue
                if i[1] >= tablero.largo or i[1] < 0:
                    continue
                tablero.coloca_ampolleta(i[0], i[1])
                
def regla_2(tablero, x, y):
    if isinstance(tablero.tablero[x][y], Pared):
        cont = 0
        for i in [(x,y+1), (x,y-1), (x+1,y), (x-1,y)]:
            if i[0] >= tablero.ancho or i[0] < 0:
                continue
            if i[1] >= tablero.largo or i[1] < 0:
                continue
            aux = tablero.tablero[i[0]][i[1]]
            if isinstance(aux, Espacio) and aux.estado == 2:
                cont = cont+1
        if cont == tablero.tablero[x][y].numero:
            for i in [(x,y+1), (x,y-1), (x+1,y), (x-1,y)]:
                if i[0] >= tablero.ancho or i[0] < 0:
                    continue
                if i[1] >= tablero.largo or i[1] < 0:
                    continue
                aux = tablero.tablero[i[0]][i[1]]
                if isinstance(aux, Espacio) and aux.estado != 2:
                    tablero.bloquea(i[0], i[1])

def regla_3(tablero, x, y):
    if isinstance(tablero.tablero[x][y], Pared) and tablero.tablero[x][y].numero == 3:
        for i in [(x-1,y-1), (x+1,y-1), (x-1,y+1), (x+1,y+1)]:
            tablero.bloquea(i[0], i[1])



def regla_4(tablero, x, y):
    espacio = tablero.tablero[x][y]
    espacios_vacios = []
    if isinstance(espacio, Espacio) and espacio.estado == 1 and espacio.iluminado == False:
        for i in range(y,-1,-1):
            espacio = tablero.tablero[x][i]
            if isinstance(espacio, Pared):
                break
            if espacio.estado != 1 and espacio.estado != 2 and espacio.iluminado == False:
                espacios_vacios.append((x,i))
        for i in range(y,tablero.largo):
            espacio = tablero.tablero[x][i]
            if isinstance(espacio, Pared):
                break
            if espacio.estado != 1 and espacio.iluminado == False:
                espacios_vacios.append((x,i))

        for i in range(x,-1,-1):
            espacio = tablero.tablero[i][y]
            if isinstance(espacio, Pared):
                break
            if espacio.estado != 1 and espacio.iluminado == False:
                espacios_vacios.append((i,y))

        for i in range(x,tablero.ancho):
            espacio = tablero.tablero[i][y]
            if isinstance(espacio, Pared):
                break
            if espacio.estado != 1 and espacio.iluminado == False:
                espacios_vacios.append((i,y))
    
        if len(espacios_vacios) == 1:
            coord = espacios_vacios[0]
            tablero.coloca_ampolleta(coord[0], coord[1])


def regla_5(tablero, x, y):
    espacio = tablero.tablero[x][y]
    espacios_vacios = 0
    if isinstance(espacio, Pared) or espacio.estado != 0 or espacio.iluminado == True:
        return
    
    for i in range(x-1,-1,-1):
            espacio = tablero.tablero[i][y]
            if isinstance(espacio, Pared):
                break
            if espacio.estado == 0 and espacio.iluminado == False:
                espacios_vacios = espacios_vacios + 1

    for i in range(x+1, tablero.ancho):
            espacio = tablero.tablero[i][y]
            if isinstance(espacio, Pared):
                break
            if espacio.estado == 0 and espacio.iluminado == False:
                espacios_vacios = espacios_vacios + 1


    for i in range(y-1,-1,-1):
            espacio = tablero.tablero[x][i]
            if isinstance(espacio, Pared):
                break
            if espacio.estado == 0 and espacio.iluminado == False:
                espacios_vacios = espacios_vacios + 1

    for i in range(y+1,tablero.largo):
            espacio = tablero.tablero[x][i]
            if isinstance(espacio, Pared):
                break
            if espacio.estado == 0 and espacio.iluminado == False:
                espacios_vacios = espacios_vacios + 1

    if espacios_vacios == 0:
        tablero.coloca_ampolleta(x, y)

            
if __name__ == "__main__":
    main()