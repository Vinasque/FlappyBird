import pygame
from pygame.locals import *
import random

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
velocidad_desplazamiento = 4
volando = False
fin_del_juego = False
tubo_brecha = 150
tubo_frecuencia = 1500
ultimo_tubo = pygame.time.get_ticks() - tubo_frecuencia

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

class Tubo(pygame.sprite.Sprite):
    def __init__(self, x, y, posicion):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/tubo.png")
        self.rect = self.image.get_rect()
        # Posición 1 para el de cima, -1 para el debajo
        if posicion == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(tubo_brecha / 2)]
        if posicion == -1:
            self.rect.topleft = [x, y + int(tubo_brecha / 2)]

    def update(self):
        self.rect.x -= velocidad_desplazamiento
        if self.rect.right < 0:
            self.kill()


grupo_pajaros = pygame.sprite.Group()
grupo_tubos = pygame.sprite.Group()

pajarito = Pajaro(75, int(pantalla_altura / 2))
grupo_pajaros.add(pajarito)

correr = True
while correr:

    reloj.tick(fps)

    pantalla.blit(fondo, (0, 0)) # Diseño del fonde
    grupo_pajaros.draw(pantalla)
    grupo_pajaros.update()
    grupo_tubos.draw(pantalla)

    # Dibuja el suelo
    pantalla.blit(suelo, (suelo_desplazamiento, 576))

    # Mirando por colisión
    if pygame.sprite.groupcollide(grupo_pajaros, grupo_tubos, False, False) or pajarito.rect.top < 0:
        fin_del_juego = True

    # Mira si el pájaro ha tocado el suelo
    if pajarito.rect.bottom >= 576:
        fin_del_juego = True
        volando = False

    if fin_del_juego == False and volando == True:
        # Generando nuevos tubos
        tiempo_ahora = pygame.time.get_ticks()
        tubo_altura = random.randint(-100, 100)
        if tiempo_ahora - ultimo_tubo > tubo_frecuencia:
            inf_tubo = Tubo(pantalla_ancho, int(pantalla_altura / 2) + tubo_altura, -1)
            sup_tubo = Tubo(pantalla_ancho, int(pantalla_altura / 2) + tubo_altura, 1)
            grupo_tubos.add(inf_tubo)
            grupo_tubos.add(sup_tubo)
            ultimo_tubo = tiempo_ahora

        # Desplazando el suelo
        suelo_desplazamiento -= velocidad_desplazamiento
        if abs(suelo_desplazamiento) > 35:
            suelo_desplazamiento = 0

        grupo_tubos.update()

    for acto in pygame.event.get():
        if acto.type == pygame.QUIT:
            correr = False
        if acto.type == pygame.MOUSEBUTTONDOWN and volando == False and fin_del_juego == False:
            volando = True

    pygame.display.update()

pygame.quit()