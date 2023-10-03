import pygame
from pygame.locals import *

class Crianca(pygame.sprite.Sprite):

    def __init__(self, posicao):
        self.xcor, self.ycor = posicao  # Desempacote a tupla de posição
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/sprites/kid.png')
        #self.image = pygame.transform.scale(self.image, (32*10, 32*10))

        self.rect = self.image.get_rect()
        self.rect.topleft = self.xcor, self.ycor

    def atualizar(self, posicao):
        self.xcor, self.ycor = posicao
        self.rect.topleft = self.xcor, self.ycor
