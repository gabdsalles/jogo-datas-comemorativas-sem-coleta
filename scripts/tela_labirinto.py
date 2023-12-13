import pygame
from pygame.locals import *
import sys
from crianca import Crianca
import maze_maker
from robo import Robo
from labirinto.itens import Item, ListaItens
import random

DISTANCIA_X = 30
DISTANCIA_Y = 30
ESPESSURA_BORDA = 10
FPS = 60
X_INICIAL = 350
Y_INICIAL = 25

class TelaLabirinto:
    def __init__(self, largura, altura):
        pygame.init()

        self.LARGURA = largura
        self.ALTURA = altura
        self.tela = pygame.display.set_mode((self.LARGURA, self.ALTURA))
        pygame.display.set_caption('Fase 1 - Labirinto')
        self.relogio = pygame.time.Clock()

        self.GRID_ALTURA = 30
        self.GRID_LARGURA = 30
        self.ultima_geracao = 0


        self.imagem_fundo = pygame.image.load("assets/imagens/natal_fundo.png").convert()
        self.arvore_jogador_1 = pygame.image.load("assets/imagens/natal/arvore_natal.png").convert_alpha()
        self.arvore_jogador_2 = pygame.image.load("assets/imagens/natal/arvore_natal.png").convert_alpha()
        self.arvore_robo_1 = pygame.image.load("assets/imagens/natal/arvore_natal.png").convert_alpha()
        self.arvore_robo_2 = pygame.image.load("assets/imagens/natal/arvore_natal.png").convert_alpha()

        self.BRANCO = (255, 255, 255)
        self.PRETO = (0, 0, 0)
        self.AMARELO = (255, 255, 0)
        self.VERMELHO = (255, 0, 0)
        self.AMARELO2 = (233, 255, 101)

        self.pontos_jogador = 0
        self.pontos_robo = 0
        self.pontos_totais = 10

        self.robo = Robo((0, 0))
        self.todas_sprites = pygame.sprite.Group()
        self.todas_sprites.add(self.robo)

        self.crianca = Crianca((0, 0))
        self.todas_sprites.add(self.crianca)

        self.fonte = pygame.font.Font(None, 36)
        self.fonte_maior = pygame.font.Font('assets/fonts/archivo_black.ttf', 48)
        self.fonte_menor = pygame.font.Font('assets/fonts/archivo_black.ttf', 30)
        self.fundo_rect = pygame.rect.Rect(0, 0, 300, 720)
        self.tabuleiro = maze_maker.make_maze()
        self.lista_rect_tabuleiro = [] # lista de retangulos do labirinto, que serão desenhados
        print(self.tabuleiro)

        self.titulo_fase_texto = self.fonte_maior.render("Natal", True, self.PRETO)
        self.titulo_fase_x = 75
        self.titulo_fase_y = 20

        self.itens_jogador_texto = self.fonte.render(f"Jogador: {self.pontos_jogador}/{self.pontos_totais}", True, self.PRETO)
        self.itens_jogador_x = 75
        self.itens_jogador_y = 100

        self.tempo_texto = self.fonte.render("Tempo: ", True, self.PRETO)
        self.tempo_texto_x = 10
        self.tempo_texto_y = 675

        self.itens_robo_texto = self.fonte.render(f"Robô: {self.pontos_robo}/{self.pontos_totais}", True, self.PRETO)
        self.itens_robo_x = 90
        self.itens_robo_y = 430

        self.tempo = self.fonte.render("00:00", True, self.PRETO)
        self.tempo_x = 100
        self.tempo_y = 675

        self.tempo_decorrido = 0

        self.lista_posicoes_imagens_jogador = [(30, 260), (80, 260), (35, 220), (70, 220), (55, 180), (180, 260), 
        (230, 260), (185, 220), (220, 220), (205, 180)]
        self.cont_lista_jogador = 0

        self.novos_itens_jogador = []
        self.novas_imagens_jogador = []

        self.novos_itens_robo = []
        self.novas_imagens_robo = []

        self.lista_itens = ListaItens().lista_itens

        self.lista_imagens = [pygame.image.load(item.imagem) for item in self.lista_itens]

    def desenhar_labirinto(self):

        x, y = X_INICIAL, Y_INICIAL # Posição inicial
        cont_itens = 0
        linhas_tabuleiro = self.tabuleiro.splitlines()

        for i in range(len(linhas_tabuleiro)):

            linha = linhas_tabuleiro[i]
            for caractere in linha:
                if caractere == ' ':
                    retangulo = (pygame.rect.Rect(x, y, DISTANCIA_X, DISTANCIA_Y), self.BRANCO)
                    self.lista_rect_tabuleiro.append(retangulo)
                    pygame.draw.rect(self.tela, self.BRANCO, retangulo[0])
                elif caractere == '+':
                    retangulo = (pygame.rect.Rect(x, y, DISTANCIA_X, DISTANCIA_Y), self.PRETO)
                    self.lista_rect_tabuleiro.append(retangulo)
                    pygame.draw.rect(self.tela, self.PRETO, retangulo[0])
                elif caractere == '|':
                    retangulo = (pygame.rect.Rect(x, y, DISTANCIA_X, DISTANCIA_Y), self.PRETO)
                    self.lista_rect_tabuleiro.append(retangulo)
                    pygame.draw.rect(self.tela, self.PRETO, retangulo[0])
                elif caractere == '-':
                    retangulo = (pygame.rect.Rect(x, y, DISTANCIA_X, DISTANCIA_Y), self.PRETO)
                    self.lista_rect_tabuleiro.append(retangulo)
                    pygame.draw.rect(self.tela, self.PRETO, retangulo[0]) 
                elif caractere == "i":
                    retangulo = pygame.Rect(x, y, DISTANCIA_X, DISTANCIA_Y)
                    imagem_rect = self.lista_imagens[cont_itens].get_rect()

                    pygame.draw.rect(self.tela, self.BRANCO, retangulo)
                    if self.lista_itens[cont_itens].passou == False:
                        self.tela.blit(self.lista_imagens[cont_itens], (x, y))
                    #print(len(self.lista_itens))
                    self.lista_itens[cont_itens].posicao = (x, y)

                    self.lista_rect_tabuleiro.append((retangulo, self.BRANCO))
                    cont_itens += 1

                x += DISTANCIA_X # Avança horizontalmente
            x = 350  # Volta para a posição inicial na próxima linha
            y += DISTANCIA_Y
    
    def pegar_coordenadas_robo(self): #coordenadas: x = 1140, y = 625
        
        for retangulo, cor in reversed(self.lista_rect_tabuleiro):
            if cor == self.BRANCO:
                x, y, _, _ = retangulo
                return x, y
        
        return None
    
    def pegar_coordenadas_personagem(self): #x = 480, y = 65

        for retangulo, cor in self.lista_rect_tabuleiro:
            if cor == self.BRANCO:
                x, y, _, _ = retangulo
                return x, y

    def direcao_valida(self, posicao):
        x, y = posicao

        for retangulo, cor in self.lista_rect_tabuleiro:
            rect_x, rect_y, _, _ = retangulo
            if x == rect_x and y == rect_y:
                if cor == self.PRETO:
                    return False
                else:
                    return True

    def gerar_item_aleatorio(self, segundos):
        if segundos % 10 == 0: #and segundos != 0
            item_novo = random.choice(ListaItens().lista_possibilidades_itens)
            # self.atualizar_labirinto()



    def desenhar_grid(self, tela, largura_tela, altura_tela, grid_largura, grid_altura):

        # Desenhe as linhas horizontais do grid
        for y in range(0, altura_tela, grid_altura):
            pygame.draw.line(tela, (100, 100, 100), (0, y), (largura_tela, y))

        # Desenhe as linhas verticais do grid
        for x in range(0, largura_tela, grid_largura):
            pygame.draw.line(tela, (100, 100, 100), (x, 0), (x, altura_tela))

    def desenhar_tela(self):

        self.relogio.tick(FPS)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == K_a or event.key == K_LEFT:
                    nova_posicao = (self.crianca.xcor - DISTANCIA_X, self.crianca.ycor)
                    if self.direcao_valida(nova_posicao):
                        self.crianca.atualizar(nova_posicao)
                if event.key == K_d or event.key == K_RIGHT:
                    nova_posicao = (self.crianca.xcor + DISTANCIA_X, self.crianca.ycor)
                    if self.direcao_valida(nova_posicao):
                        self.crianca.atualizar(nova_posicao)
                if event.key == K_w or event.key == K_UP:
                    nova_posicao = (self.crianca.xcor, self.crianca.ycor - DISTANCIA_Y)
                    if self.direcao_valida(nova_posicao):
                        self.crianca.atualizar(nova_posicao)
                if event.key == K_s or event.key == K_DOWN:
                    nova_posicao = (self.crianca.xcor, self.crianca.ycor + DISTANCIA_Y)
                    if self.direcao_valida(nova_posicao):
                        self.crianca.atualizar(nova_posicao)

            if event.type == MOUSEBUTTONDOWN:
                pass          

        posicao_jogador = self.crianca.rect.topleft
        novos_itens = []
        novas_imagens = []

        for item in self.lista_itens:
            if posicao_jogador == item.posicao and item.passou == False:
                item.passou = True
                self.pontos_jogador += 1 #aumentar pontuação do jogador
                self.itens_jogador_texto = self.fonte.render(f"Jogador: {self.pontos_jogador}/{self.pontos_totais}", True, self.PRETO)
                item.dono = "jogador"
                print(item.nome, item.dono, item.passou, item.posicao)
                self.novos_itens_jogador.append(item)
                self.novas_imagens_jogador.append(pygame.image.load(item.imagem))
                

        self.tela.fill(self.PRETO)
        self.tela.blit(self.imagem_fundo, (0, 0))
        pygame.draw.rect(self.tela, self.AMARELO2, self.fundo_rect)

        self.desenhar_labirinto()

        if self.robo.xcor == 0 and self.robo.ycor == 0:
            robo_x, robo_y = self.pegar_coordenadas_robo()
            #print(robo_x, robo_y)
            self.robo.xcor = robo_x
            self.robo.ycor = robo_y
            self.robo.rect.topleft = robo_x, robo_y

        if self.crianca.xcor == 0 and self.crianca.ycor == 0:
            crianca_x, crianca_y = self.pegar_coordenadas_personagem()
            self.crianca.xcor = crianca_x
            self.crianca.ycor = crianca_y
            self.crianca.rect.topleft = crianca_x, crianca_y
            #print(crianca_x, crianca_y)

        self.tempo_decorrido += 1
        segundos = self.tempo_decorrido // 60
        minutos = segundos // 60
        tempo_formatado = f"{minutos:02}:{segundos % 60:02}"
        self.tempo = self.fonte.render(tempo_formatado, True, self.PRETO)

        self.todas_sprites.draw(self.tela)
        
        self.tela.blit(self.titulo_fase_texto, (self.titulo_fase_x, self.titulo_fase_y))
        self.tela.blit(self.itens_jogador_texto, (self.itens_jogador_x, self.itens_jogador_y))
        self.tela.blit(self.itens_robo_texto, (self.itens_robo_x, self.itens_robo_y))
        self.tela.blit(self.tempo_texto, (self.tempo_texto_x, self.tempo_texto_y))
        self.tela.blit(self.tempo, (self.tempo_x, self.tempo_y))
        self.tela.blit(self.arvore_jogador_1, (-30, 130))
        self.tela.blit(self.arvore_jogador_2, (120, 130))
        self.tela.blit(self.arvore_robo_1, (-30, 460))
        self.tela.blit(self.arvore_robo_2, (120, 460))

        # virar função depois
        cont = 0
        for item in self.novos_itens_jogador:
            self.tela.blit(self.novas_imagens_jogador[cont], self.lista_posicoes_imagens_jogador[cont])
            cont += 1

        #self.desenhar_grid(self.tela, self.LARGURA, self.ALTURA, self.GRID_LARGURA, self.GRID_ALTURA)

        pygame.display.flip()


    def executar(self):
        while True:
            self.desenhar_tela()
            segundos_atual = self.tempo_decorrido // 60

            if segundos_atual - self.ultima_geracao >= 10:
                self.gerar_item_aleatorio(segundos_atual)
                self.ultima_geracao = segundos_atual

tela = TelaLabirinto(1280, 720)
tela.executar()

#TO-DO:
# 1. Implementar algoritmo de IA no robô
# 2. Colocar música + efeitos sonoros quando alguém pega um item
# 3. Deixar a interface mais intuitiva (quando alguém ganha ou perde, avisar para o jogador)
# 4. Resolver problema de não poder mover o jogador sem ter que apertar a tecla mais vezes

