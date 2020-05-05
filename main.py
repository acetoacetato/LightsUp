import pygame, sys
from math import floor
from time import sleep


SCREEN_WIDTH = 700
SCREEN_HEIGHT = 600
filename = "input.txt"
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
    texto: pygame.font

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
        print(self.estado)
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
        print(pos)
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
                self.tablero[i][j].print()
            print('')

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
    
    pygame.display.update()

    while True:
        # Posibles entradas del teclado y mouse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


            
if __name__ == "__main__":
    main()