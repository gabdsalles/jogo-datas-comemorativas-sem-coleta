import pygame
from pygame.locals import *
import sys
from crianca import Crianca
import maze_maker
from robo import Robo

DISTANCIA_X = 30
DISTANCIA_Y = 40

class TelaLabirinto:
    def __init__(self, largura, altura):
        pygame.init()

        self.LARGURA = largura
        self.ALTURA = altura
        self.tela = pygame.display.set_mode((self.LARGURA, self.ALTURA))
        pygame.display.set_caption('Fase 1 - Labirinto')

        self.imagem_fundo = pygame.image.load("assets/imagens/natal_fundo.jpeg").convert()

        self.BRANCO = (255, 255, 255)
        self.PRETO = (0, 0, 0)
        self.AMARELO = (255, 255, 0)
        self.VERMELHO = (255, 0, 0)

        self.flag = [False, False, False, False, False]
        self.cont_flag = 0

        self.pontos_jogador = 0
        self.pontos_robo = 0
        self.pontos_totais = 5

        self.robo = Robo((0, 0))
        self.todas_sprites = pygame.sprite.Group()
        self.todas_sprites.add(self.robo)

        self.crianca = Crianca((0, 0))
        self.todas_sprites.add(self.crianca)

        self.fonte = pygame.font.Font('assets/fonts/archivo_black.ttf', 36)
        self.fundo_rect = pygame.rect.Rect(0, 0, 400, 720)
        self.tabuleiro = maze_maker.make_maze(8, 8)
        self.lista_rect_tabuleiro = [] # lista de retangulos do labirinto, que serão desenhados
        #print(self.tabuleiro)

        self.titulo_fase_texto = self.fonte.render("Natal", True, self.BRANCO)
        self.titulo_fase_x = 150
        self.titulo_fase_y = 50

        self.itens_jogador_texto = self.fonte.render("Itens do jogador", True, self.BRANCO)
        self.itens_jogador_x = 50
        self.itens_jogador_y = 200

        self.pontuacao_jogador_texto = self.fonte.render(f"{self.pontos_jogador}/{self.pontos_totais}", True, self.BRANCO)
        self.pontos_jogador_x = 50
        self.pontos_jogador_y = 250

        self.tempo_texto = self.fonte.render("Tempo", True, self.BRANCO)
        self.tempo_texto_x = 50
        self.tempo_texto_y = 350

        self.tempo = self.fonte.render("00:00", True, self.BRANCO)
        self.tempo_x = 50
        self.tempo_y = 400

        self.itens_robo_texto = self.fonte.render("Itens do robô", True, self.BRANCO)
        self.itens_robo_x = 50
        self.itens_robo_y = 500

        self.pontuacao_robo_texto = self.fonte.render(f"{self.pontos_robo}/{self.pontos_totais}", True, self.BRANCO)
        self.pontos_robo_x = 50
        self.pontos_robo_y = 550

        self.lista_posicoes_itens = []

        self.lista_itens = [pygame.image.load("assets/imagens/natal/santa.png"),
         pygame.image.load("assets/imagens/natal/tree.png"), 
         pygame.image.load("assets/imagens/natal/giftbox.png"),
         pygame.image.load("assets/imagens/natal/bell.png"),
         pygame.image.load("assets/imagens/natal/bengala.png")]

    def desenhar_labirinto(self):

        x, y = 450, 25 # Posição inicial
        cont_itens = 0
        for linha in self.tabuleiro.splitlines():
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
                    imagem_rect = self.lista_itens[cont_itens].get_rect()
                    pygame.draw.rect(self.tela, self.AMARELO, retangulo)
                    self.lista_posicoes_itens.append((x, y))

                    self.tela.blit(self.lista_itens[cont_itens], (x, y))
                    self.lista_rect_tabuleiro.append((retangulo, self.AMARELO))
                    cont_itens += 1

                x += DISTANCIA_X # Avança horizontalmente
            x = 450  # Volta para a posição inicial na próxima linha
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


    
    def desenhar_tela(self):

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
        if posicao_jogador in self.lista_posicoes_itens and self.flag[self.cont_flag] == False:
            self.pontos_jogador += 1 #aumentar pontuação do jogador
            self.pontuacao_jogador_texto = self.fonte.render(f"{self.pontos_jogador}/{self.pontos_totais}", True, self.BRANCO)
            self.lista_posicoes_itens.remove(posicao_jogador) #remover posição do item da lista de posições
            #tirar item da tela
            #ter controle de vários itens
        
        self.tela.fill(self.PRETO)
        self.tela.blit(self.imagem_fundo, (0, 0))
        pygame.draw.rect(self.tela, self.VERMELHO, self.fundo_rect)

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

        self.todas_sprites.draw(self.tela)
        
        self.tela.blit(self.titulo_fase_texto, (self.titulo_fase_x, self.titulo_fase_y))
        self.tela.blit(self.itens_jogador_texto, (self.itens_jogador_x, self.itens_jogador_y))
        self.tela.blit(self.pontuacao_jogador_texto, (self.pontos_jogador_x, self.pontos_jogador_y))
        self.tela.blit(self.tempo_texto, (self.tempo_texto_x, self.tempo_texto_y))
        self.tela.blit(self.tempo, (self.tempo_x, self.tempo_y))
        self.tela.blit(self.itens_robo_texto, (self.itens_robo_x, self.itens_robo_y))
        self.tela.blit(self.pontuacao_robo_texto, (self.pontos_robo_x, self.pontos_robo_y))
        pygame.display.flip()

    def executar(self):
        while True:
            self.desenhar_tela()

tela = TelaLabirinto(1280, 720)
tela.executar()

#TO-DO:
# 1. Fazer com que os textos de tempo e pontuação mudem
# 2. Checar colisões com o labirinto (direções possíveis)
# 3. Checar colisões com os itens
# 4. Implementar algoritmo de IA no robô
# 5. Colocar música + efeitos sonoros quando alguém pega um item

