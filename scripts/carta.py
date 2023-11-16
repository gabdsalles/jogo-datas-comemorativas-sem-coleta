import pygame
from pygame.locals import *
import random

VERMELHO = (255, 0, 0)
AMARELO = (255, 255, 0)
AZUL = (0, 0, 255)
LARANJA = (255, 165, 0)
VERDE = (0, 128, 0)

class Carta:

    def __init__(self, imagem, nome, posicao, cor):

        self.imagem = pygame.image.load(imagem)
        self.nome = nome
        self.posicao = posicao
        self.cor = cor
        self.virada = False
        self.dono = None


class Tabuleiro:

    def __init__(self):

        #tamanho das cartas: 130x200
        self.lista_posicoes = [(475, 125), (625, 125), (775, 125), (925, 125), (1075, 125), (475, 350), (625, 350), (775, 350), (925, 350), (1075, 350)]
        self.lista_cartas = []
        self.lista_viradas = []
        self.inicializar_cartas()
        self.cartas_viradas = 0

    def inicializar_cartas(self):
        nomes_cartas = ["fogueira", "fogueira", "bandeira", "bandeira", "balao", "balao", "chapeu", "chapeu", "comidas", "comidas"]
        cores_cartas = [VERMELHO, VERMELHO, AMARELO, AMARELO, AZUL, AZUL, LARANJA, LARANJA, VERDE, VERDE] 

        for i in range(10):
            nome = nomes_cartas[i]
            cor = cores_cartas[i]

            # Escolher uma posição aleatória da lista
            posicao = random.choice(self.lista_posicoes)
            
            # Remover a posição escolhida da lista
            self.lista_posicoes.remove(posicao)

            caminho_imagem = f"assets/imagens/cartas/{nome}.png"
            carta = Carta(caminho_imagem, nome, posicao, cor)
            self.lista_cartas.append(carta)
