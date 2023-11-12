import pygame
from pygame.locals import *

pygame.init()

reloj = pygame.time.Clock()
fps = 60

pantalla_ancho = 684
pantalla_altura = 702

pantalla = pygame.display.set_mode((pantalla_ancho, pantalla_altura))
pygame.display.set_caption("Flappy Bird")

# Cargando las imágenes
fondo = pygame.image.load("imagenes/fondo.png")
suelo = pygame.image.load("imagenes/suelo.png")

# Variables del juego
suelo_desplazamiento = 0
desplazamiento_velocidad = 4

correr = True
while correr:

    reloj.tick(fps)

    pantalla.blit(fondo, (0, 0)) # Diseño del fonde

    # Dibujando y desplazando el suelo
    pantalla.blit(suelo, (suelo_desplazamiento, 576))
    suelo_desplazamiento -= desplazamiento_velocidad
    if abs(suelo_desplazamiento) > 35:
        suelo_desplazamiento = 0

    for acto in pygame.event.get():
        if acto.type == pygame.QUIT:
            correr = False

    pygame.display.update()

pygame.quit()