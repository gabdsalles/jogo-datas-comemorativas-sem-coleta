import pygame
from pygame.locals import *
import sys
from tela_inicial import TelaInicial
from scripts.tela_labirinto import TelaLabirinto

pygame.init()

tela = TelaInicial(1280, 720)
tela.executar()
