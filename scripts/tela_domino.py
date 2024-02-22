import random
import pygame
from pygame.locals import *
import sys

from domino.pecas import Pecas
from domino.posicoes_pecas import posicoes_retangulos

LARGURA = 1280
ALTURA = 720
FPS = 60
QTD_INICIAL_PECAS = 6

class TelaDomino:

    def __init__(self, largura, altura):

        pygame.init()

        self.LARGURA = largura
        self.ALTURA = altura
        self.tela = pygame.display.set_mode((self.LARGURA, self.ALTURA))
        pygame.display.set_caption('Fase 3 - Dominó')
        self.relogio = pygame.time.Clock()

        self.imagem_fundo = pygame.image.load("assets/imagens/pascoa_fundo.png").convert()

        self.BRANCO = (255, 255, 255)
        self.PRETO = (0, 0, 0)
        self.AMARELO = (255, 255, 0)
        self.VERMELHO = (255, 0, 0)
        self.AZUL_FUNDO = (0, 61, 80)
        self.AMARELO2 = (233, 255, 101)

        self.pecas_jogador = 0
        self.pecas_robo = 0

        self.fonte = pygame.font.Font(None, 36)
        self.fundo_rect = pygame.rect.Rect(0, 0, 300, 720)

        self.titulo_fase_texto = self.fonte.render("Páscoa", True, self.PRETO)
        self.titulo_fase_x = 100
        self.titulo_fase_y = 20

        self.itens_jogador_texto = self.fonte.render(f"Peças do jogador: {self.pecas_jogador}", True, self.PRETO)
        self.itens_jogador_x = 30
        self.itens_jogador_y = 100

        self.itens_robo_texto = self.fonte.render(f"Peças do robô: {self.pecas_robo}", True, self.PRETO)
        self.itens_robo_x = 45
        self.itens_robo_y = 550

        self.compras_texto = self.fonte.render(f"Pilha de compras: ", True, self.PRETO)
        self.compras_texto_x = 40
        self.compras_texto_y = 150

        self.tempo_texto = self.fonte.render("Tempo: ", True, self.PRETO)
        self.tempo_texto_x = 10
        self.tempo_texto_y = 675

        self.tempo = self.fonte.render("00:00", True, self.PRETO)
        self.tempo_x = 100
        self.tempo_y = 675

        self.tempo_decorrido = 0

        self.texto_jogador = self.fonte.render("É sua vez de jogar!", True, self.PRETO)
        self.texto_jogador_x = 15
        self.texto_jogador_y = 600
        self.rect_texto_jogador = self.texto_jogador.get_rect()

        self.lista_pecas = Pecas().lista_pecas
        self.pecas_jogador = []
        self.pecas_robo = []

        for i in range(QTD_INICIAL_PECAS):
            peca = random.choice(self.lista_pecas)
            self.pecas_jogador.append(peca)
            self.lista_pecas.remove(peca)

            peca = random.choice(self.lista_pecas)
            self.pecas_robo.append(peca)
            self.lista_pecas.remove(peca)

        self.vez_jogador = True
        self.vez_robo = False

        self.fundo_carta = pygame.image.load("assets/imagens/pascoa/fundo_carta.png")
        self.fundo_carta = pygame.transform.scale(self.fundo_carta, (167, 250))

        self.tempo_jogada = None
        
        self.qtd_jogadas_jogador = 0
        self.qtd_jogadas_robo = 0

    def desenhar_grid(self, tela, largura_tela, altura_tela, grid_largura, grid_altura):

        # Desenhe as linhas horizontais do grid
        for y in range(0, altura_tela, grid_altura):
            pygame.draw.line(tela, (100, 100, 100), (0, y), (largura_tela, y))

        # Desenhe as linhas verticais do grid
        for x in range(0, largura_tela, grid_largura):
            pygame.draw.line(tela, (100, 100, 100), (x, 0), (x, altura_tela))
    
    def desenhar_pecas_jogador(self, tela, pecas_jogador):

        # desenhar retangulos
        largura_retangulo = 120
        altura_retangulo = 180

        for i in range(QTD_INICIAL_PECAS):
            
            pygame.draw.rect(tela, self.AZUL_FUNDO, posicoes_retangulos[QTD_INICIAL_PECAS][i], border_radius=40)
        # desenhar imagem 1 das peças
        # desenhar imagem 2 das peças
    
    def desenhar_tela(self):

        self.relogio.tick(FPS)

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN and self.vez_jogador:
                posicao_mouse = pygame.mouse.get_pos()

                # self.checar_colisao(posicao_mouse)

        self.tela.fill(self.PRETO)
        self.tela.blit(self.imagem_fundo, (0, 0))
        pygame.draw.rect(self.tela, self.AMARELO2, self.fundo_rect)

        self.tempo_decorrido += 1
        segundos = self.tempo_decorrido // 60
        minutos = segundos // 60
        tempo_formatado = f"{minutos:02}:{segundos % 60:02}"

        self.tempo = self.fonte.render(tempo_formatado, True, self.PRETO)

        self.tela.blit(self.titulo_fase_texto, (self.titulo_fase_x, self.titulo_fase_y))
        self.tela.blit(self.itens_jogador_texto, (self.itens_jogador_x, self.itens_jogador_y))
        self.tela.blit(self.compras_texto, (self.compras_texto_x, self.compras_texto_y))
        self.tela.blit(self.tempo_texto, (self.tempo_texto_x, self.tempo_texto_y))
        self.tela.blit(self.tempo, (self.tempo_x, self.tempo_y))
        self.tela.blit(self.itens_robo_texto, (self.itens_robo_x, self.itens_robo_y))
        pygame.draw.rect(self.tela, self.AZUL_FUNDO, (60, 215, 187, 270))
        self.tela.blit(self.fundo_carta, (70, 225), (0, 0, 200, 300))
        
        pygame.draw.rect(self.tela, self.AMARELO, (self.texto_jogador_x-10, self.texto_jogador_y-10, self.rect_texto_jogador.width+70, self.rect_texto_jogador.height+20), border_radius=20)
        self.tela.blit(self.texto_jogador, (self.texto_jogador_x, self.texto_jogador_y))

        self.desenhar_pecas_jogador(self.tela, self.pecas_jogador)

        # self.desenhar_grid(self.tela, self.LARGURA, self.ALTURA, 30, 30)

        pygame.display.flip()


    def executar(self):
        while True:
            self.desenhar_tela()


tela = TelaDomino(1280, 720)

tela.executar()
