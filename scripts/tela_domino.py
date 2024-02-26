import random
import pygame
from pygame.locals import *
from collections import deque
import sys

from domino.pecas import Pecas
from domino.posicoes_pecas import posicoes_retangulos_jogador, Posicao

LARGURA = 1280
ALTURA = 720
FPS = 60
QTD_INICIAL_PECAS = 6
POSICAO_INICIAL = Posicao((760, 307, 70, 5), (760, 245, 70, 130), (760, 245), "dupla")

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
        self.AZUL_CLARO = (175, 217, 232)

        self.fonte = pygame.font.Font(None, 36)
        self.fundo_rect = pygame.rect.Rect(0, 0, 280, 720)
        self.tabuleiro_rect = pygame.rect.Rect(310, 100, 940, 440)

        self.lista_pecas = Pecas().lista_pecas
        self.pecas_jogador = []
        self.pecas_robo = []
        self.pecas_tabuleiro = deque()
        self.posicao_pecas_tabuleiro = deque()
        self.posicao_pecas_tabuleiro.append(POSICAO_INICIAL)

        self.titulo_fase_texto = self.fonte.render("Páscoa", True, self.PRETO)
        self.titulo_fase_x = 100
        self.titulo_fase_y = 20

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

        self.qtd_pecas_jogador = QTD_INICIAL_PECAS
        self.qtd_pecas_robo = QTD_INICIAL_PECAS

        self.itens_jogador_texto = self.fonte.render(f"Peças do jogador: {self.qtd_pecas_jogador}", True, self.PRETO)
        self.itens_jogador_x = 20
        self.itens_jogador_y = 100

        self.itens_robo_texto = self.fonte.render(f"Peças do robô: {self.qtd_pecas_robo}", True, self.PRETO)
        self.itens_robo_x = 45
        self.itens_robo_y = 550

        self.lista_rect_jogador = []

        for i in range(QTD_INICIAL_PECAS):
            peca = random.choice(self.lista_pecas)
            self.pecas_jogador.append(peca)
            self.lista_pecas.remove(peca)

            peca = random.choice(self.lista_pecas)
            self.pecas_robo.append(peca)
            self.lista_pecas.remove(peca)
        
        self.vez_jogador = False
        self.vez_robo = False

        self.compras_texto = self.fonte.render(f"Pilha de compras: {len(self.lista_pecas)} ", True, self.PRETO)
        self.compras_texto_x = 20
        self.compras_texto_y = 150

        self.fundo_carta = pygame.image.load("assets/imagens/pascoa/fundo_carta.png")
        self.fundo_carta = pygame.transform.scale(self.fundo_carta, (167, 250))

        self.tempo_jogada = None
        
        self.qtd_jogadas_jogador = 0
        self.qtd_jogadas_robo = 0

        self.esquerda_tabuleiro = None
        self.direita_tabuleiro = None
        self.pos_extremidade_esquerda = POSICAO_INICIAL
        self.pos_extremidade_direita = POSICAO_INICIAL
        self.pecas_pra_esquerda = 0
        self.pecas_pra_direita = 0
        self.puxar_pecas_pra_cima = False

    def desenhar_grid(self, tela, largura_tela, altura_tela, grid_largura, grid_altura):

        # Desenhe as linhas horizontais do grid
        for y in range(0, altura_tela, grid_altura):
            pygame.draw.line(tela, (100, 100, 100), (0, y), (largura_tela, y))

        # Desenhe as linhas verticais do grid
        for x in range(0, largura_tela, grid_largura):
            pygame.draw.line(tela, (100, 100, 100), (x, 0), (x, altura_tela))
    
    def checar_colisao(self, posicao_mouse):
            
        for i, rect in enumerate(self.lista_rect_jogador):
            if rect.collidepoint(posicao_mouse):
                return i
                        
        return None
    
    def checar_jogada_jogador(self, peca_clicada):

        peca = self.pecas_jogador[peca_clicada]
        # print(peca.nome1, peca.nome2)
        if peca.nome1 == self.esquerda_tabuleiro:
            if self.pecas_pra_esquerda <= 3:
                aux_imagem1 = peca.imagem1
                peca.imagem1 = peca.imagem2
                peca.imagem2 = aux_imagem1
                aux_cor = peca.cor1
                peca.cor1 = peca.cor2
                peca.cor2 = aux_cor
            self.pecas_tabuleiro.appendleft(peca)
            self.pecas_jogador.remove(peca)
            self.qtd_pecas_jogador -= 1
            self.esquerda_tabuleiro = peca.nome2
            self.vez_jogador = False
            self.vez_robo = True
            self.texto_jogador = self.fonte.render("É a vez do robô jogar!", True, self.PRETO)
            self.rect_texto_jogador = self.texto_jogador.get_rect()
            self.itens_jogador_texto = self.fonte.render(f"Peças do jogador: {self.qtd_pecas_jogador}", True, self.PRETO)
            self.qtd_jogadas_jogador += 1
            self.pecas_pra_esquerda += 1
            self.calcular_posicao_peca_tabuleiro("esquerda")
        
        elif peca.nome1 == self.direita_tabuleiro:
            if self.pecas_pra_direita >= 4:
                aux_imagem1 = peca.imagem1
                peca.imagem1 = peca.imagem2
                peca.imagem2 = aux_imagem1
                aux_cor = peca.cor1
                peca.cor1 = peca.cor2
                peca.cor2 = aux_cor
            self.pecas_tabuleiro.append(peca)
            self.pecas_jogador.remove(peca)
            self.qtd_pecas_jogador -= 1
            self.direita_tabuleiro = peca.nome2
            self.vez_jogador = False
            self.vez_robo = True
            self.texto_jogador = self.fonte.render("É a vez do robô jogar!", True, self.PRETO)
            self.rect_texto_jogador = self.texto_jogador.get_rect()
            self.itens_jogador_texto = self.fonte.render(f"Peças do jogador: {self.qtd_pecas_jogador}", True, self.PRETO)
            self.qtd_jogadas_jogador += 1
            self.pecas_pra_direita += 1
            self.calcular_posicao_peca_tabuleiro("direita")
        
        elif peca.nome2 == self.esquerda_tabuleiro:
            if self.pecas_pra_esquerda >= 3:
                aux_imagem1 = peca.imagem1
                peca.imagem1 = peca.imagem2
                peca.imagem2 = aux_imagem1
                aux_cor = peca.cor1
                peca.cor1 = peca.cor2
                peca.cor2 = aux_cor
            self.pecas_tabuleiro.appendleft(peca)
            self.pecas_jogador.remove(peca)
            self.qtd_pecas_jogador -= 1
            self.esquerda_tabuleiro = peca.nome1
            self.vez_jogador = False
            self.vez_robo = True
            self.texto_jogador = self.fonte.render("É a vez do robô jogar!", True, self.PRETO)
            self.rect_texto_jogador = self.texto_jogador.get_rect()
            self.itens_jogador_texto = self.fonte.render(f"Peças do jogador: {self.qtd_pecas_jogador}", True, self.PRETO)
            self.qtd_jogadas_jogador += 1
            self.pecas_pra_esquerda += 1
            self.calcular_posicao_peca_tabuleiro("esquerda")
        
        elif peca.nome2 == self.direita_tabuleiro:
            if self.pecas_pra_direita <= 3:
                aux_imagem = peca.imagem1
                peca.imagem1 = peca.imagem2
                peca.imagem2 = aux_imagem
                aux_cor = peca.cor1
                peca.cor1 = peca.cor2
                peca.cor2 = aux_cor
            self.pecas_tabuleiro.append(peca)
            self.pecas_jogador.remove(peca)
            self.qtd_pecas_jogador -= 1
            self.direita_tabuleiro = peca.nome1
            self.vez_jogador = False
            self.vez_robo = True
            self.texto_jogador = self.fonte.render("É a vez do robô jogar!", True, self.PRETO)
            self.rect_texto_jogador = self.texto_jogador.get_rect()
            self.itens_jogador_texto = self.fonte.render(f"Peças do jogador: {self.qtd_pecas_jogador}", True, self.PRETO)
            self.qtd_jogadas_jogador += 1
            self.pecas_pra_direita += 1
            self.calcular_posicao_peca_tabuleiro("direita")

    def calcular_posicao_peca_tabuleiro(self, lado):

        if self.pecas_pra_direita <= 3 and self.pecas_pra_esquerda <= 3:
            if lado == "esquerda" and self.pos_extremidade_esquerda == POSICAO_INICIAL:
                pos_borda = (self.pos_extremidade_esquerda.posicao_borda[0] - 65, self.pos_extremidade_esquerda.posicao_borda[1] - 32, 5, 70)
                pos_retangulo = (self.pos_extremidade_esquerda.posicao_retangulo[0] - 130, self.pos_extremidade_esquerda.posicao_retangulo[1] + 30, 130, 70)
                pos_imagem = (pos_retangulo[0], pos_retangulo[1])
                nova_posicao = Posicao(pos_borda, pos_retangulo, pos_imagem)
                self.pos_extremidade_esquerda = nova_posicao
                self.posicao_pecas_tabuleiro.appendleft(nova_posicao)
            elif lado == "direita" and self.pos_extremidade_direita == POSICAO_INICIAL:
                pos_borda = (self.pos_extremidade_direita.posicao_borda[0] + 130, self.pos_extremidade_direita.posicao_borda[1] - 32, 5, 70)
                pos_retangulo = (self.pos_extremidade_direita.posicao_retangulo[0] + 65, self.pos_extremidade_direita.posicao_retangulo[1] + 30, 130, 70)
                pos_imagem = (pos_retangulo[0], pos_retangulo[1])
                nova_posicao = Posicao(pos_borda, pos_retangulo, pos_imagem)
                self.pos_extremidade_direita = nova_posicao
                self.posicao_pecas_tabuleiro.append(nova_posicao)
            elif lado == "esquerda" and self.pos_extremidade_esquerda != POSICAO_INICIAL:
                pos_borda = (self.pos_extremidade_esquerda.posicao_borda[0] - 130, self.pos_extremidade_esquerda.posicao_borda[1], 5, 70)
                pos_retangulo = (self.pos_extremidade_esquerda.posicao_retangulo[0] - 130, self.pos_extremidade_esquerda.posicao_retangulo[1], 130, 70)
                pos_imagem = (pos_retangulo[0], pos_retangulo[1])
                nova_posicao = Posicao(pos_borda, pos_retangulo, pos_imagem)
                self.pos_extremidade_esquerda = nova_posicao
                self.posicao_pecas_tabuleiro.appendleft(nova_posicao)
            elif lado == "direita" and self.pos_extremidade_direita != POSICAO_INICIAL:
                pos_borda = (self.pos_extremidade_direita.posicao_borda[0] + 65, self.pos_extremidade_direita.posicao_borda[1], 5, 70)
                pos_retangulo = (self.pos_extremidade_direita.posicao_retangulo[0] + 130, self.pos_extremidade_direita.posicao_retangulo[1], 130, 70)
                pos_imagem = (pos_retangulo[0], pos_retangulo[1])
                nova_posicao = Posicao(pos_borda, pos_retangulo, pos_imagem)
                self.pos_extremidade_direita = nova_posicao
                self.posicao_pecas_tabuleiro.append(nova_posicao)
        
        else: #se passar de 3 peças pra cada lado, vamos desenhar a peça na vertical
            if self.puxar_pecas_pra_cima == False:
                self.puxar_todas_pecas_pra_cima()
                self.puxar_pecas_pra_cima = True
            if lado == "esquerda" and self.pecas_pra_esquerda == 4:
                pos_borda = (self.pos_extremidade_esquerda.posicao_borda[0] - 65, self.pos_extremidade_esquerda.posicao_borda[1] + 130, 70, 5)
                pos_retangulo = (self.pos_extremidade_esquerda.posicao_retangulo[0], self.pos_extremidade_esquerda.posicao_retangulo[1] + 65, 70, 130)
                pos_imagem = (pos_retangulo[0], pos_retangulo[1])
                nova_posicao = Posicao(pos_borda, pos_retangulo, pos_imagem, "vertical")
                self.pos_extremidade_esquerda = nova_posicao
                self.posicao_pecas_tabuleiro.appendleft(nova_posicao)
            elif lado == "direita" and self.pecas_pra_esquerda > 3:
                pos_borda = (self.pos_extremidade_direita.posicao_borda[0], self.pos_extremidade_direita.posicao_borda[1], 5, 130)
                pos_retangulo = (self.pos_extremidade_direita.posicao_retangulo[0], self.pos_extremidade_direita.posicao_retangulo[1], 130, 130)
                pos_imagem = (pos_retangulo[0], pos_retangulo[1])
                nova_posicao = Posicao(pos_borda, pos_retangulo, pos_imagem, "vertical")
                self.pos_extremidade_direita = nova_posicao
                self.posicao_pecas_tabuleiro.append(nova_posicao)

    def puxar_todas_pecas_pra_cima(self):
        for pos in self.posicao_pecas_tabuleiro:
            nova_posicao_borda = (pos.posicao_borda[0], pos.posicao_borda[1] - 130, pos.posicao_borda[2], pos.posicao_borda[3])
            nova_posicao_retangulo = (pos.posicao_retangulo[0], pos.posicao_retangulo[1] - 130, pos.posicao_retangulo[2], pos.posicao_retangulo[3])
            nova_posicao_imagem = (pos.posicao_imagem[0], pos.posicao_imagem[1] - 130)
            
            pos.posicao_borda = nova_posicao_borda
            pos.posicao_retangulo = nova_posicao_retangulo
            pos.posicao_imagem = nova_posicao_imagem

    
    def desenhar_pecas_jogador(self, tela, pecas_jogador):

        # desenhar retangulos
        for i in range(self.qtd_pecas_jogador):
            
            rect_peca = pygame.rect.Rect(posicoes_retangulos_jogador[QTD_INICIAL_PECAS][i])
            pygame.draw.rect(tela, self.AZUL_CLARO, posicoes_retangulos_jogador[QTD_INICIAL_PECAS][i])
        
        #desenhar bordas
            pygame.draw.rect(tela, self.AMARELO, posicoes_retangulos_jogador[QTD_INICIAL_PECAS][i], 5)
            pygame.draw.rect(tela, self.BRANCO, (posicoes_retangulos_jogador[QTD_INICIAL_PECAS][i][0], posicoes_retangulos_jogador[QTD_INICIAL_PECAS][i][1] + 90, 90, 5), 5)

        # desenhar imagem 1 das peças
            imagem1 = pygame.image.load(pecas_jogador[i].imagem1)
            pygame.draw.rect(tela, pecas_jogador[i].cor1, (posicoes_retangulos_jogador[QTD_INICIAL_PECAS][i][0] + 5, posicoes_retangulos_jogador[QTD_INICIAL_PECAS][i][1] + 5, 80, 85))
            tela.blit(imagem1, (posicoes_retangulos_jogador[QTD_INICIAL_PECAS][i][0] + 10, posicoes_retangulos_jogador[QTD_INICIAL_PECAS][i][1] + 10))
        # desenhar imagem 2 das peças
            imagem2 = pygame.image.load(pecas_jogador[i].imagem2)
            pygame.draw.rect(tela, pecas_jogador[i].cor2, (posicoes_retangulos_jogador[QTD_INICIAL_PECAS][i][0] + 5, posicoes_retangulos_jogador[QTD_INICIAL_PECAS][i][1] + 95, 80, 85))
            tela.blit(imagem2, (posicoes_retangulos_jogador[QTD_INICIAL_PECAS][i][0] + 10, posicoes_retangulos_jogador[QTD_INICIAL_PECAS][i][1] + 100))

            if rect_peca not in self.lista_rect_jogador:
                self.lista_rect_jogador.append(rect_peca)
    
    def desenhar_pecas_robo(self, tela):

        for i in range(self.qtd_pecas_robo):
            pygame.draw.rect(tela, self.AZUL_CLARO, (posicoes_retangulos_jogador[QTD_INICIAL_PECAS][i][0], 0, posicoes_retangulos_jogador[QTD_INICIAL_PECAS][i][2], 90))
            pygame.draw.rect(tela, self.AMARELO, (posicoes_retangulos_jogador[QTD_INICIAL_PECAS][i][0], 0, posicoes_retangulos_jogador[QTD_INICIAL_PECAS][i][2], 90), 5)
    
    def desenhar_tabuleiro(self, tela):

        if len(self.pecas_tabuleiro) > 0:
            for i in range(len(self.pecas_tabuleiro)):
                
                pos = self.posicao_pecas_tabuleiro[i]
                if pos == POSICAO_INICIAL or pos.tipo == "vertical":
                    
                    imagem1 = pygame.image.load(self.pecas_tabuleiro[i].imagem1)
                    imagem1 = pygame.transform.scale(imagem1, (60, 60))
                    #imagem1 = pygame.transform.rotate(imagem1, 270)
                    imagem2 = pygame.image.load(self.pecas_tabuleiro[i].imagem2)
                    imagem2 = pygame.transform.scale(imagem2, (60, 60))
                    # imagem2 = pygame.transform.rotate(imagem2, 270)
                    pygame.draw.rect(tela, self.pecas_tabuleiro[i].cor1, (pos.posicao_imagem[0], pos.posicao_imagem[1], 70, 65))
                    tela.blit(imagem1, pos.posicao_imagem)
                    pygame.draw.rect(tela, self.pecas_tabuleiro[i].cor2, (pos.posicao_imagem[0], pos.posicao_imagem[1]+65, 70, 65))
                    tela.blit(imagem2, (pos.posicao_imagem[0], pos.posicao_imagem[1]+70))
                    pygame.draw.rect(tela, self.AMARELO, pos.posicao_retangulo, 5)
                    pygame.draw.rect(tela, self.BRANCO, pos.posicao_borda, 5)

                else:
                    pygame.draw.rect(tela, self.AZUL_CLARO, pos.posicao_retangulo)
                    imagem1 = pygame.image.load(self.pecas_tabuleiro[i].imagem1)
                    imagem1 = pygame.transform.scale(imagem1, (60, 60))
                    imagem1 = pygame.transform.rotate(imagem1, 270)
                    imagem2 = pygame.image.load(self.pecas_tabuleiro[i].imagem2)
                    imagem2 = pygame.transform.scale(imagem2, (60, 60))
                    imagem2 = pygame.transform.rotate(imagem2, 270)
                    pygame.draw.rect(tela, self.pecas_tabuleiro[i].cor1, (pos.posicao_imagem[0], pos.posicao_imagem[1], 70, 65))
                    tela.blit(imagem1, pos.posicao_imagem)
                    pygame.draw.rect(tela, self.pecas_tabuleiro[i].cor2, (pos.posicao_imagem[0] + 65, pos.posicao_imagem[1], 70, 65))
                    tela.blit(imagem2, (pos.posicao_imagem[0] + 65, pos.posicao_imagem[1]))
                    pygame.draw.rect(tela, self.AMARELO, pos.posicao_retangulo, 5)
                    pygame.draw.rect(tela, self.BRANCO, pos.posicao_borda, 5)

    def escolher_quem_joga_primeiro(self):

        duplas_jogador = sum(1 for peca in self.pecas_jogador if peca.tipo == "dupla")
        duplas_robo = sum(1 for peca in self.pecas_robo if peca.tipo == "dupla")

        if duplas_jogador == duplas_robo == 0:
            peca_inicial = random.choice([peca for peca in self.lista_pecas if peca.tipo == "dupla"])
            peca_inicial.dono = None
            self.pecas_tabuleiro.append(peca_inicial)
            self.lista_pecas.remove(peca_inicial)
        
        if duplas_jogador >= duplas_robo:
            self.texto_jogador = self.fonte.render("É a vez do robô jogar!", True, self.PRETO)
            self.rect_texto_jogador = self.texto_jogador.get_rect()
            peca_inicial = random.choice([peca for peca in self.pecas_jogador if peca.tipo == "dupla"])
            peca_inicial.dono = None
            self.pecas_tabuleiro.append(peca_inicial)
            self.pecas_jogador.remove(peca_inicial)
            self.esquerda_tabuleiro = peca_inicial.nome1
            self.direita_tabuleiro = peca_inicial.nome2
            self.qtd_pecas_jogador -= 1
            self.itens_jogador_texto = self.fonte.render(f"Peças do jogador: {self.qtd_pecas_jogador}", True, self.PRETO)
            self.vez_robo = True
            self.vez_jogador = False
        
        else:
            self.texto_jogador = self.fonte.render("É a sua vez de jogar!", True, self.PRETO)
            self.rect_texto_jogador = self.texto_jogador.get_rect()
            peca_inicial = random.choice([peca for peca in self.pecas_robo if peca.tipo == "dupla"])
            peca_inicial.dono = None
            peca_inicial.posicao = POSICAO_INICIAL
            self.pecas_tabuleiro.append(peca_inicial)
            self.pecas_robo.remove(peca_inicial)
            self.esquerda_tabuleiro = peca_inicial.nome1
            self.direita_tabuleiro = peca_inicial.nome2
            self.qtd_pecas_robo -= 1
            self.itens_robo_texto = self.fonte.render(f"Peças do robô: {self.qtd_pecas_robo}", True, self.PRETO)
            self.vez_jogador = True
            self.vez_robo = False
        
        # print(duplas_jogador, duplas_robo)
    
    def desenhar_tela(self):

        self.relogio.tick(FPS)

        for event in pygame.event.get():

            if event.type == QUIT:
                for pos in self.posicao_pecas_tabuleiro:
                    print(pos.posicao_borda, pos.posicao_retangulo, pos.posicao_imagem)
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN: #and self.vez_jogador:
                posicao_mouse = pygame.mouse.get_pos()

                peca_clicada = self.checar_colisao(posicao_mouse)
                if peca_clicada is not None:
                    self.checar_jogada_jogador(peca_clicada)

        self.tela.fill(self.PRETO)
        self.tela.blit(self.imagem_fundo, (0, 0))
        pygame.draw.rect(self.tela, self.AMARELO2, self.fundo_rect)
        pygame.draw.rect(self.tela, self.AZUL_FUNDO, self.tabuleiro_rect)

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
        pygame.draw.rect(self.tela, self.AZUL_FUNDO, (40, 220, 187, 270))
        self.tela.blit(self.fundo_carta, (50, 230), (0, 0, 200, 300))
        
        pygame.draw.rect(self.tela, self.AMARELO, (self.texto_jogador_x-10, self.texto_jogador_y-10, self.rect_texto_jogador.width+20, self.rect_texto_jogador.height+20), border_radius=20)
        self.tela.blit(self.texto_jogador, (self.texto_jogador_x, self.texto_jogador_y))

        self.desenhar_pecas_jogador(self.tela, self.pecas_jogador)
        self.desenhar_pecas_robo(self.tela)

        if self.vez_jogador == False and self.vez_robo == False:
            self.escolher_quem_joga_primeiro()

        self.desenhar_tabuleiro(self.tela)

        # self.desenhar_grid(self.tela, self.LARGURA, self.ALTURA, 50, 100)

        pygame.display.flip()


    def executar(self):
        while True:
            self.desenhar_tela()


tela = TelaDomino(1280, 720)

tela.executar()
