import pygame, sys, random
from pygame.locals import *
from  random import  randint


class Room (object):
    def __init__(self, x1, y1, ancho, alto ):
        self.ancho = ancho
        self.alto = alto
      #  self.centro = centro
        self.x1 = x1
        self.x2= x1+ancho
        self.y1= y1
        self.y2=y1+alto

    def comprobarOberlaupin (self, room):
        if (self.x1-1 <= room.x2 and self.x2+1 >= room.x1 and self.y1-1 <= room.y2 and self.y2+1 >= room.y1):
            return True; # Hay solapamiento
        return False; # No hay solapamiento

    def puedeSerConstruido(self, listaDeHabitaciones):
        for x in range (0, len(listaDeHabitaciones)):
            if self.comprobarOberlaupin(listaDeHabitaciones[x]):
                return False

        return True


def crearPuerta (x1, x2 ,y1,y2):

    xPuerta=0
    yPuerta=0
    cordPuerta=[0,0]
    if (bool(random.getrandbits(1))):
        xPuerta=randint(x1+1,x2-1)
        if (bool(random.getrandbits(1))):
            yPuerta=y1
        else : yPuerta=y2
    else:
        yPuerta=randint (y1+1,y2-1)
        if (bool(random.getrandbits(1))):
            xPuerta=x1
        else: xPuerta=x2

    cordPuerta[0]=xPuerta
    cordPuerta[1]=yPuerta
    return cordPuerta


def crearHabitaciones(tamaño_mapa_x, tamaño_mapa_y):

    ROOM_MIN_SIZE = 4
    ROOM_MAX_SIZE = 6

    listaDeHabitaciones = []
    mapa = [[0 for x in range(tamaño_mapa_x)] for y in range(tamaño_mapa_y)]

    for a in range(0, tamaño_mapa_x):
        for b in range(0, tamaño_mapa_y):
            mapa[a][b] = 0
    for y in range(0, 100000):
        roomB = Room(randint(0, tamaño_mapa_x - ROOM_MAX_SIZE - 1), randint(0, tamaño_mapa_y - ROOM_MAX_SIZE - 1), randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE), randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE))

        if roomB.puedeSerConstruido(listaDeHabitaciones):
            listaDeHabitaciones.append(roomB)


    for j in range (0, len(listaDeHabitaciones)):
        for k in range(listaDeHabitaciones[j].x1, listaDeHabitaciones[j].x2+1 ):
            mapa[k][listaDeHabitaciones[j].y1] = 1
            mapa[k][listaDeHabitaciones[j].y2] = 1
        for l in range(listaDeHabitaciones[j].y1, listaDeHabitaciones[j].y2+1):
            mapa[listaDeHabitaciones[j].x1] [l] = 1
            mapa[listaDeHabitaciones[j].x2] [l] = 1

        cordPuerta=crearPuerta(listaDeHabitaciones[j].x1, listaDeHabitaciones[j].x2, listaDeHabitaciones[j].y1, listaDeHabitaciones[j].y2 )

        mapa[cordPuerta[0]][cordPuerta[1]] = 0

    for x in range(tamaño_mapa_x):
        mapa[x][0] = 1
        mapa[x][tamaño_mapa_y - 1] = 1
    for y in range(tamaño_mapa_y):
        mapa[0][y] = 1
        mapa[tamaño_mapa_x - 1][y] = 1


    return (mapa)

