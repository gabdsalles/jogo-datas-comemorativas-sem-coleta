import pygame
from pygame.locals import *
import sys
from tela_inicial import TelaInicial
from tela_labirinto import TelaLabirinto

pygame.init()

tela = TelaLabirinto(1280, 720)
tela.executar()
