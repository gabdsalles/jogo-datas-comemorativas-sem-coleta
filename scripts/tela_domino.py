import random
import pygame
from pygame.locals import *
from collections import deque
import sys
import copy
import domino.ia_domino as ia

from domino.pecas import Pecas
from domino.posicoes_pecas import posicoes_retangulos_jogador, Posicao, posicoes_borda_esquerda, posicoes_borda_direita, posicoes_imagem_esquerda, posicoes_imagem_direita, posicoes_retangulo_esquerda, posicoes_retangulo_direita

LARGURA = 1280
ALTURA = 720
FPS = 60
QTD_INICIAL_PECAS = 6
POSICAO_INICIAL = Posicao((760, 177, 70, 5), (760, 115, 70, 130), (760, 115), (760, 180), "dupla")

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
        self.cores = Pecas().cores

        self.lista_retangulos_tabuleiro = deque()
        self.lista_retangulos_tabuleiro.append(POSICAO_INICIAL.posicao_retangulo)
        self.lista_imagens_tabuleiro = deque()
        self.lista_imagens_tabuleiro.append(POSICAO_INICIAL.posicao_imagem1)
        self.lista_imagens_tabuleiro.append(POSICAO_INICIAL.posicao_imagem2)
        self.lista_bordas_tabuleiro = deque()
        self.lista_bordas_tabuleiro.append(POSICAO_INICIAL.posicao_borda)
        self.nomes_pecas_tabuleiro = deque()

        self.posicoes_retangulos_jogador = copy.deepcopy(posicoes_retangulos_jogador)
        self.posicoes_borda_esquerda = copy.deepcopy(posicoes_borda_esquerda)
        self.posicoes_borda_direita = copy.deepcopy(posicoes_borda_direita)
        self.posicoes_imagem_esquerda = copy.deepcopy(posicoes_imagem_esquerda)
        self.posicoes_imagem_direita = copy.deepcopy(posicoes_imagem_direita)
        self.posicoes_retangulo_esquerda = copy.deepcopy(posicoes_retangulo_esquerda)
        self.posicoes_retangulo_direita = copy.deepcopy(posicoes_retangulo_direita)

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
        self.pecas_pra_esquerda = 0
        self.pecas_pra_direita = 0

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
        if peca.nome1 == self.esquerda_tabuleiro or peca.nome2 == self.esquerda_tabuleiro:
            
            if peca.nome1 == self.esquerda_tabuleiro:
                self.nomes_pecas_tabuleiro.appendleft(peca.nome1)
                self.esquerda_tabuleiro = peca.nome2
                self.nomes_pecas_tabuleiro.appendleft(peca.nome2)
                # print("nome1")
            elif peca.nome2 == self.esquerda_tabuleiro:
                self.nomes_pecas_tabuleiro.appendleft(peca.nome2)
                self.esquerda_tabuleiro = peca.nome1
                self.nomes_pecas_tabuleiro.appendleft(peca.nome1)
                # print("nome2")
            
            self.pecas_tabuleiro.appendleft(peca)
            self.pecas_jogador.remove(peca)
            self.qtd_pecas_jogador -= 1
            self.vez_jogador = False
            self.vez_robo = True
            self.texto_jogador = self.fonte.render("É a vez do robô jogar!", True, self.PRETO)
            self.rect_texto_jogador = self.texto_jogador.get_rect()
            self.itens_jogador_texto = self.fonte.render(f"Peças do jogador: {self.qtd_pecas_jogador}", True, self.PRETO)
            self.qtd_jogadas_jogador += 1
            self.pecas_pra_esquerda += 1
            self.incluir_peca_tabuleiro(peca, "esquerda")
        
        elif peca.nome1 == self.direita_tabuleiro or peca.nome2 == self.direita_tabuleiro:
            
            if peca.nome1 == self.direita_tabuleiro:
                self.nomes_pecas_tabuleiro.append(peca.nome1)
                self.direita_tabuleiro = peca.nome2
                self.nomes_pecas_tabuleiro.append(peca.nome2)
            else:
                self.nomes_pecas_tabuleiro.append(peca.nome2)
                self.direita_tabuleiro = peca.nome1
                self.nomes_pecas_tabuleiro.append(peca.nome1)
            
            self.pecas_tabuleiro.append(peca)
            self.pecas_jogador.remove(peca)
            self.qtd_pecas_jogador -= 1
            self.vez_jogador = False
            self.vez_robo = True
            self.texto_jogador = self.fonte.render("É a vez do robô jogar!", True, self.PRETO)
            self.rect_texto_jogador = self.texto_jogador.get_rect()
            self.itens_jogador_texto = self.fonte.render(f"Peças do jogador: {self.qtd_pecas_jogador}", True, self.PRETO)
            self.qtd_jogadas_jogador += 1
            self.pecas_pra_direita += 1
            self.incluir_peca_tabuleiro(peca, "direita")   
    
    def limpar_tabuleiro(self, peca):

        self.posicoes_retangulo_esquerda = copy.deepcopy(posicoes_retangulo_esquerda)
        self.posicoes_retangulo_direita = copy.deepcopy(posicoes_retangulo_direita)
        self.posicoes_imagem_esquerda = copy.deepcopy(posicoes_imagem_esquerda)
        self.posicoes_imagem_direita = copy.deepcopy(posicoes_imagem_direita)
        self.posicoes_borda_esquerda = copy.deepcopy(posicoes_borda_esquerda)
        self.posicoes_borda_direita = copy.deepcopy(posicoes_borda_direita)
        self.lista_retangulos_tabuleiro = deque()
        self.lista_retangulos_tabuleiro.append(POSICAO_INICIAL.posicao_retangulo)
        self.lista_imagens_tabuleiro = deque()
        self.lista_imagens_tabuleiro.append(POSICAO_INICIAL.posicao_imagem1)
        self.lista_imagens_tabuleiro.append(POSICAO_INICIAL.posicao_imagem2)
        self.lista_bordas_tabuleiro = deque()
        self.lista_bordas_tabuleiro.append(POSICAO_INICIAL.posicao_borda)
        self.nomes_pecas_tabuleiro = deque()
        self.esquerda_tabuleiro = peca.nome1
        self.direita_tabuleiro = peca.nome2
        self.nomes_pecas_tabuleiro.append(peca.nome1)
        self.nomes_pecas_tabuleiro.append(peca.nome2)
        self.lista_pecas.extend(self.pecas_tabuleiro)
        self.lista_pecas.remove(peca)
        self.pecas_tabuleiro = deque()
        self.compras_texto = self.fonte.render(f"Pilha de compras: {len(self.lista_pecas)} ", True, self.PRETO)


    def incluir_peca_tabuleiro(self, peca, posicao):

        if self.pecas_pra_esquerda == 9 or self.pecas_pra_direita == 9: #acabou as posições
            self.limpar_tabuleiro(peca)
            self.pecas_pra_esquerda = 0
            self.pecas_pra_direita = 0
            return None
        
        if posicao == "esquerda":

            self.lista_retangulos_tabuleiro.appendleft(self.posicoes_retangulo_esquerda[0])

            self.posicoes_retangulo_esquerda.pop(0)

            self.lista_imagens_tabuleiro.appendleft(self.posicoes_imagem_esquerda[0])
            self.lista_imagens_tabuleiro.appendleft(self.posicoes_imagem_esquerda[1])
            self.posicoes_imagem_esquerda.pop(0)
            self.posicoes_imagem_esquerda.pop(0)

            self.lista_bordas_tabuleiro.appendleft(self.posicoes_borda_esquerda[0])
            self.posicoes_borda_esquerda.pop(0)

        elif posicao == "direita":
            self.lista_retangulos_tabuleiro.append(self.posicoes_retangulo_direita[0])
            self.posicoes_retangulo_direita.pop(0)

            self.lista_imagens_tabuleiro.append(self.posicoes_imagem_direita[0])
            self.lista_imagens_tabuleiro.append(self.posicoes_imagem_direita[1])
            self.posicoes_imagem_direita.pop(0)
            self.posicoes_imagem_direita.pop(0)

            self.lista_bordas_tabuleiro.append(self.posicoes_borda_direita[0])
            self.posicoes_borda_direita.pop(0)
    
    def desenhar_pecas_jogador(self, tela, pecas_jogador):

        self.lista_rect_jogador = []
        
        # desenhar retangulos
        for i in range(self.qtd_pecas_jogador):
            
            rect_peca = pygame.rect.Rect(posicoes_retangulos_jogador[self.qtd_pecas_jogador][i])
            pygame.draw.rect(tela, self.AZUL_CLARO, posicoes_retangulos_jogador[self.qtd_pecas_jogador][i])
        
        #desenhar bordas
            pygame.draw.rect(tela, self.AMARELO, posicoes_retangulos_jogador[self.qtd_pecas_jogador][i], 5)
            pygame.draw.rect(tela, self.BRANCO, (posicoes_retangulos_jogador[self.qtd_pecas_jogador][i][0], posicoes_retangulos_jogador[self.qtd_pecas_jogador][i][1] + 90, 90, 5), 5)

        # desenhar imagem 1 das peças
            imagem1 = pygame.image.load(pecas_jogador[i].imagem1)
            pygame.draw.rect(tela, pecas_jogador[i].cor1, (posicoes_retangulos_jogador[self.qtd_pecas_jogador][i][0] + 5, posicoes_retangulos_jogador[self.qtd_pecas_jogador][i][1] + 5, 80, 85))
            tela.blit(imagem1, (posicoes_retangulos_jogador[self.qtd_pecas_jogador][i][0] + 10, posicoes_retangulos_jogador[self.qtd_pecas_jogador][i][1] + 10))
        # desenhar imagem 2 das peças
            imagem2 = pygame.image.load(pecas_jogador[i].imagem2)
            pygame.draw.rect(tela, pecas_jogador[i].cor2, (posicoes_retangulos_jogador[self.qtd_pecas_jogador][i][0] + 5, posicoes_retangulos_jogador[self.qtd_pecas_jogador][i][1] + 95, 80, 85))
            tela.blit(imagem2, (posicoes_retangulos_jogador[self.qtd_pecas_jogador][i][0] + 10, posicoes_retangulos_jogador[self.qtd_pecas_jogador][i][1] + 100))

            self.lista_rect_jogador.append(rect_peca)
    
    def desenhar_pecas_robo(self, tela):

        for i in range(self.qtd_pecas_robo):
            pygame.draw.rect(tela, self.AZUL_CLARO, (posicoes_retangulos_jogador[self.qtd_pecas_robo][i][0], 0, posicoes_retangulos_jogador[self.qtd_pecas_robo][i][2], 90))
            pygame.draw.rect(tela, self.AMARELO, (posicoes_retangulos_jogador[self.qtd_pecas_robo][i][0], 0, posicoes_retangulos_jogador[self.qtd_pecas_robo][i][2], 90), 5)

    def desenhar_tabuleiro(self, tela):

        for i, nome in enumerate(self.nomes_pecas_tabuleiro):
            cor = self.cores[nome.split()[0]]
            pygame.draw.rect(tela, cor, (self.lista_imagens_tabuleiro[i][0], self.lista_imagens_tabuleiro[i][1], 65, 65))
            imagem = pygame.image.load(f"assets/imagens/pascoa_horizontal/{nome}.png")
            imagem = pygame.transform.scale(imagem, (60, 60))
            tela.blit(imagem, self.lista_imagens_tabuleiro[i])

        for rect in self.lista_bordas_tabuleiro:
            pygame.draw.rect(tela, self.BRANCO, rect, 5)

        for rect in self.lista_retangulos_tabuleiro:
            pygame.draw.rect(tela, self.AMARELO, rect, 5)

    
    def checar_compra(self, pecas):

        esquerda = sum(1 for peca in pecas if peca.nome1 == self.esquerda_tabuleiro or peca.nome2 == self.esquerda_tabuleiro)
        direita = sum(1 for peca in pecas if peca.nome1 == self.direita_tabuleiro or peca.nome2 == self.direita_tabuleiro)
        # print("Possibilidades à esquerda: ", esquerda)
        # print("Possibilidades à direita: ", direita)
        if esquerda == 0 and direita == 0:
            return True
        else:
            return False
        
    def comprar_peca(self, pecas, quem_joga):
            
            if self.lista_pecas == []: # se não tiver mais peças pra comprar
                peca = random.choice(self.pecas_tabuleiro)
                self.limpar_tabuleiro(peca)
            
            peca = random.choice(self.lista_pecas)
            pecas.append(peca)
            self.lista_pecas.remove(peca)
            self.compras_texto = self.fonte.render(f"Pilha de compras: {len(self.lista_pecas)} ", True, self.PRETO)

            if quem_joga == "jogador":
                self.qtd_pecas_jogador += 1
                self.itens_jogador_texto = self.fonte.render(f"Peças do jogador: {self.qtd_pecas_jogador}", True, self.PRETO)
                self.vez_jogador = False
                self.vez_robo = True
                self.texto_jogador = self.fonte.render("É a vez do robô jogar!", True, self.PRETO)

            elif quem_joga == "robo":
                self.qtd_pecas_robo += 1
                self.itens_robo_texto = self.fonte.render(f"Peças do robô: {self.qtd_pecas_robo}", True, self.PRETO)
                self.vez_jogador = True
                self.vez_robo = False
                self.texto_jogador = self.fonte.render("É a sua vez de jogar!", True, self.PRETO)
            
            # print(f"{quem_joga} comprou uma peça!")

    def escolher_quem_joga_primeiro(self):

        duplas_jogador = sum(1 for peca in self.pecas_jogador if peca.tipo == "dupla")
        duplas_robo = sum(1 for peca in self.pecas_robo if peca.tipo == "dupla")

        if duplas_jogador == duplas_robo == 0:
            duplas_tabuleiro = [peca for peca in self.lista_pecas if peca.tipo == "dupla"]
            peca_inicial = random.choice(duplas_tabuleiro)
            peca_inicial.dono = None
            self.nomes_pecas_tabuleiro.append(peca_inicial.nome1)
            self.nomes_pecas_tabuleiro.append(peca_inicial.nome2)
            self.pecas_tabuleiro.append(peca_inicial)
            self.lista_pecas.remove(peca_inicial)
        
        if duplas_jogador >= duplas_robo and duplas_jogador > 0:
            self.texto_jogador = self.fonte.render("É a vez do robô jogar!", True, self.PRETO)
            self.rect_texto_jogador = self.texto_jogador.get_rect()
            peca_inicial = random.choice([peca for peca in self.pecas_jogador if peca.tipo == "dupla"])
            peca_inicial.dono = None
            self.pecas_tabuleiro.append(peca_inicial)
            self.pecas_jogador.remove(peca_inicial)
            self.esquerda_tabuleiro = peca_inicial.nome1
            self.direita_tabuleiro = peca_inicial.nome2
            self.nomes_pecas_tabuleiro.append(peca_inicial.nome1)
            self.nomes_pecas_tabuleiro.append(peca_inicial.nome2)
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
            self.nomes_pecas_tabuleiro.append(peca_inicial.nome1)
            self.nomes_pecas_tabuleiro.append(peca_inicial.nome2)
            self.qtd_pecas_robo -= 1
            self.itens_robo_texto = self.fonte.render(f"Peças do robô: {self.qtd_pecas_robo}", True, self.PRETO)
            self.vez_jogador = True
            self.vez_robo = False
        
        # print(duplas_jogador, duplas_robo)
    
    def escolher_peca_robo(self):
        peca = ia.escolher_peca(self.pecas_robo, self.esquerda_tabuleiro, self.direita_tabuleiro)
        # print(peca.nome1, peca.nome2)
        if peca.nome1 == self.esquerda_tabuleiro or peca.nome2 == self.esquerda_tabuleiro:
                
                if peca.nome1 == self.esquerda_tabuleiro:
                    self.nomes_pecas_tabuleiro.appendleft(peca.nome1)
                    self.esquerda_tabuleiro = peca.nome2
                    self.nomes_pecas_tabuleiro.appendleft(peca.nome2)
                elif peca.nome2 == self.esquerda_tabuleiro:
                    self.nomes_pecas_tabuleiro.appendleft(peca.nome2)
                    self.esquerda_tabuleiro = peca.nome1
                    self.nomes_pecas_tabuleiro.appendleft(peca.nome1)
                
                self.pecas_tabuleiro.appendleft(peca)
                self.pecas_robo.remove(peca)
                self.qtd_pecas_robo -= 1
                self.vez_jogador = True
                self.vez_robo = False
                self.texto_jogador = self.fonte.render("É a sua vez de jogar!", True, self.PRETO)
                self.rect_texto_jogador = self.texto_jogador.get_rect()
                self.itens_robo_texto = self.fonte.render(f"Peças do robô: {self.qtd_pecas_robo}", True, self.PRETO)
                self.qtd_jogadas_robo += 1
                self.pecas_pra_esquerda += 1
                self.incluir_peca_tabuleiro(peca, "esquerda")
        
        elif peca.nome1 == self.direita_tabuleiro or peca.nome2 == self.direita_tabuleiro:

            if peca.nome1 == self.direita_tabuleiro:
                self.nomes_pecas_tabuleiro.append(peca.nome1)
                self.direita_tabuleiro = peca.nome2
                self.nomes_pecas_tabuleiro.append(peca.nome2)
            
            elif peca.nome2 == self.direita_tabuleiro:
                self.nomes_pecas_tabuleiro.append(peca.nome2)
                self.direita_tabuleiro = peca.nome1
                self.nomes_pecas_tabuleiro.append(peca.nome1)
            
            self.pecas_tabuleiro.append(peca)
            self.pecas_robo.remove(peca)
            self.qtd_pecas_robo -= 1
            self.vez_jogador = True
            self.vez_robo = False
            self.texto_jogador = self.fonte.render("É a sua vez de jogar!", True, self.PRETO)
            self.rect_texto_jogador = self.texto_jogador.get_rect()
            self.itens_robo_texto = self.fonte.render(f"Peças do robô: {self.qtd_pecas_robo}", True, self.PRETO)
            self.qtd_jogadas_robo += 1
            self.pecas_pra_direita += 1
            self.incluir_peca_tabuleiro(peca, "direita")
    
    def desenhar_tela(self):

        self.relogio.tick(FPS)

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            
            if event.type == MOUSEBUTTONDOWN:
                posicao_mouse = pygame.mouse.get_pos()

                peca_clicada = self.checar_colisao(posicao_mouse)
                if peca_clicada is not None and self.vez_jogador:
                    self.checar_jogada_jogador(peca_clicada)

            if self.vez_jogador:
                precisa_comprar = self.checar_compra(self.pecas_jogador)
                if precisa_comprar:
                    self.comprar_peca(self.pecas_jogador, "jogador")
                    pass

            if self.vez_robo:
                precisa_comprar = self.checar_compra(self.pecas_robo)
                if precisa_comprar:
                    self.comprar_peca(self.pecas_robo, "robo")
                else:
                    self.escolher_peca_robo()

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
