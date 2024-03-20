import pygame
from pygame.locals import *
import random

VERMELHO = (255, 0, 0)
AMARELO = (255, 255, 0)
AZUL = (0, 0, 255)
LARANJA = (255, 165, 0)
VERDE = (0, 128, 0)

class Carta:

    """A classe Carta define um objeto que representa uma carta do jogo. Cada carta tem uma imagem, um nome, uma posição
    e uma cor. A posição é uma tupla que representa a posição da carta na tela. A cor é uma tupla que representa a cor
    da carta, em RGB. A carta também tem um atributo virada, que indica se a carta está virada ou não. Por padrão, a carta
    começa virada para baixo. A carta também tem um atributo dono, que indica se a carta já foi virada e, se sim, quem é o
    dono dela, jogador ou robô."""
    
    def __init__(self, imagem, nome, posicao, cor):

        self.imagem = pygame.image.load(imagem)
        self.nome = nome
        self.posicao = posicao
        self.cor = cor
        self.virada = False
        self.dono = None


class Tabuleiro:

    """A classe Tabuleiro define um objeto que representa o tabuleiro do jogo. O tabuleiro tem uma lista de posições
    e uma lista de cartas. A lista de posições é uma lista de tuplas que representa as posições das cartas no tabuleiro.
    A lista de cartas é uma lista de objetos da classe Carta. O tabuleiro também tem um atributo cartas_viradas, que
    indica quantas cartas já foram viradas. O tabuleiro começa com todas as cartas viradas para baixo."""
    
    def __init__(self):

        #tamanho das cartas: 130x200
        self.lista_posicoes = [(475, 125), (625, 125), (775, 125), (925, 125), (1075, 125), (475, 350), (625, 350), (775, 350), (925, 350), (1075, 350)]
        self.lista_cartas = []
        self.lista_viradas = []
        self.inicializar_cartas()
        self.cartas_viradas = 0

    def inicializar_cartas(self):
        
        """Nessa função, as cartas são inicializadas, com nomes e cores fixas. O que muda é a posição de cada carta,
        que é escolhida aleatoriamente da lista de posições. A função escolhe uma posição aleatória da lista, remove
        essa posição da lista e cria uma carta com essa posição. A função faz isso para cada carta."""        
        
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
