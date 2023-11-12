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
volando = False
fin_del_juego = False

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
        self.vel = 0
        self.hizo_clic = False

    def update(self):
        if volando == True:
            # Gravedad
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 576:
                self.rect.y += int(self.vel)

        if fin_del_juego == False:
            # Volar
            if pygame.mouse.get_pressed()[0] == 1 and self.hizo_clic == False:
                self.hizo_clic = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.hizo_clic = False

            # Manejar la animación
            self.contador += 1
            calmar_vuelo = 5

            if self.contador > calmar_vuelo:
                self.contador = 0
                self.indice += 1
                if self.indice >= len(self.imagenes):
                    self.indice = 0
            self.image = self.imagenes[self.indice]

            # Rotacionar el pájaro
            self.image = pygame.transform.rotate(self.imagenes[self.indice], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.imagenes[self.indice], -90)

grupo_pajaros = pygame.sprite.Group()

flappy = Pajaro(75, int(pantalla_ancho / 2))

grupo_pajaros.add(flappy)

correr = True
while correr:

    reloj.tick(fps)

    pantalla.blit(fondo, (0, 0)) # Diseño del fonde
    grupo_pajaros.draw(pantalla)
    grupo_pajaros.update()

    # Dibuja el suelo
    pantalla.blit(suelo, (suelo_desplazamiento, 576))

    # Mira si el pájaro ha tocado el suelo
    if flappy.rect.bottom > 576:
        fin_del_juego = True
        volando = False

    if fin_del_juego == False:
        # Desplazando el suelo
        suelo_desplazamiento -= desplazamiento_velocidad
        if abs(suelo_desplazamiento) > 35:
            suelo_desplazamiento = 0

    for acto in pygame.event.get():
        if acto.type == pygame.QUIT:
            correr = False
        if acto.type == pygame.MOUSEBUTTONDOWN and volando == False and fin_del_juego == False:
            volando = True

    pygame.display.update()

pygame.quit()