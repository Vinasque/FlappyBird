import pygame
from pygame.locals import *
from pygame.sprite import Group

pygame.init()

reloj = pygame.time.Clock()
fps = 60

pantalla_ancho = 684
pantalla_altura = 702

pantalla = pygame.display.set_mode((pantalla_ancho, pantalla_altura))
pygame.display.set_caption("Flappy Bird")

# Cargando las imágenes
fondo = pygame.image.load("img/fondo.png")
suelo = pygame.image.load("img/suelo.png")

# Variables del juego
suelo_desplazamiento = 0
desplazamiento_velocidad = 4

class Pajaro(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.imagenes = []
        self.indice = 0
        self.contador = 0
        for num in range(1, 4):
            img = pygame.image.load(f"img/pajaro{num}.png")
            self.imagenes.append(img)
        self.image = self.imagenes[self.indice]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        # Manejar la animación
        self.contador += 1
        calmar_vuelos = 5

        if self.contador > calmar_vuelos:
            self.contador = 0
            self.indice += 1
            if self.indice >= len(self.imagenes):
                self.indice = 0
        self.image = self.imagenes[self.indice]

grupo_pajaros = pygame.sprite.Group()

flappy = Pajaro(75, int(pantalla_ancho / 2))

grupo_pajaros.add(flappy)

correr = True
while correr:

    reloj.tick(fps)

    pantalla.blit(fondo, (0, 0)) # Diseño del fonde
    grupo_pajaros.draw(pantalla)
    grupo_pajaros.update()

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