import pygame, sys

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 600
filename = "input.txt"

class Espacio:
    estado: int
    iluminado: bool

    def __init__(self, estado=0, iluminado=False):
        self.estado = estado
        self.iluminado = iluminado

    def print(self):
        if self.iluminado:
            print('\033[1;33;40m', end='')
        if self.estado == 0:
            print('_', end='')


class Pared:
    numero: int
    def __init__(self, numero):
        self.numero = numero

    def print(self):
        print('[', end='')
        if self.numero != -1:
            print(self.numero, end='')
        print(']', end='')

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


    def leer_pukamones(self, filename: str) -> list:
        lista = []
        f = open(filename, 'r')
        lineas = f.readlines()
        for linea in lineas:
            datos = linea.strip().split(';')
            lista.append(tuple([datos[0], float(datos[1]), float(datos[2])]))
        return lista

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("IA light up")
    # el bucle principal del juego

    # Se crea el tablero vacío
    pygame.draw.line(screen, (230,30,30), (0,0), (600,600), 4)
    pygame.display.update()

    # Se carga los datos del tablero desde archivo
    tablero = Tablero(filename)

    while True:
        # Posibles entradas del teclado y mouse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            
if __name__ == "__main__":
    main()