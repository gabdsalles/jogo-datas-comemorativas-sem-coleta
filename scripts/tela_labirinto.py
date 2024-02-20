import pygame
from pygame.locals import *
import sys
from crianca import Crianca
import maze_maker
from robo import Robo
from labirinto.itens import Item, ListaItens
import random
import ia_labirinto
from logica_labirinto import pegar_coordenadas_personagem, pegar_coordenadas_robo, determinar_posicao_robo

DISTANCIA_X = 30
DISTANCIA_Y = 30
ESPESSURA_BORDA = 10
FPS = 60
X_INICIAL = 350
Y_INICIAL = 25

class TelaLabirinto:
    def __init__(self, largura, altura):
        pygame.init()

        # Configurações da tela
        self.LARGURA = largura
        self.ALTURA = altura
        self.tela = pygame.display.set_mode((self.LARGURA, self.ALTURA))
        pygame.display.set_caption('Fase 1 - Labirinto')
        self.relogio = pygame.time.Clock()

        self.GRID_ALTURA = 30
        self.GRID_LARGURA = 30
        self.ultima_geracao = 0

        # Imagens
        self.imagem_fundo = pygame.image.load("assets/imagens/natal_fundo.png").convert()
        self.arvore_jogador_1 = pygame.image.load("assets/imagens/natal/arvore_natal.png").convert_alpha()
        self.arvore_jogador_2 = pygame.image.load("assets/imagens/natal/arvore_natal.png").convert_alpha()
        self.arvore_robo_1 = pygame.image.load("assets/imagens/natal/arvore_natal.png").convert_alpha()
        self.arvore_robo_2 = pygame.image.load("assets/imagens/natal/arvore_natal.png").convert_alpha()

        # Cores
        self.BRANCO = (255, 255, 255)
        self.PRETO = (0, 0, 0)
        self.AMARELO = (255, 255, 0)
        self.VERMELHO = (255, 0, 0)
        self.AMARELO2 = (233, 255, 101)

        # Pontuação
        self.pontos_jogador = 0
        self.pontos_robo = 0
        self.pontos_totais = 10

        # Jogadores (robô e criança)
        self.robo = Robo((0, 0))
        self.todas_sprites = pygame.sprite.Group()
        self.todas_sprites.add(self.robo)

        self.crianca = Crianca((0, 0))
        self.todas_sprites.add(self.crianca)

        # Textos
        self.fonte = pygame.font.Font(None, 36)
        self.fonte_maior = pygame.font.Font('assets/fonts/archivo_black.ttf', 48)
        self.fonte_menor = pygame.font.Font('assets/fonts/archivo_black.ttf', 30)
        self.fundo_rect = pygame.rect.Rect(0, 0, 300, 720)

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

        # Labirinto
        self.tabuleiro = maze_maker.make_maze()
        self.lista_rect_tabuleiro = [] # lista de retangulos do labirinto, que serão desenhados
        for row in self.tabuleiro:
            print(''.join(row))

        self.lista_posicoes_imagens_jogador = [(30, 260), (80, 260), (35, 220), (70, 220), (55, 180), (180, 260), 
        (230, 260), (185, 220), (220, 220), (205, 180)]

        self.lista_posicoes_imagens_robo = [(x, y + 325) for x, y in self.lista_posicoes_imagens_jogador]
        self.cont_lista_jogador = 0

        self.novos_itens_jogador = []
        self.novas_imagens_jogador = []

        self.novos_itens_robo = []
        self.novas_imagens_robo = []

        self.caminho = []

        self.lista_itens = ListaItens().lista_itens
        self.posicoes_itens_matriz = [(i, j) for i, linha in enumerate(self.tabuleiro) for j, celula in enumerate(linha) if celula == 'i']
        # print(self.posicoes_itens_matriz)

        self.lista_imagens = [pygame.image.load(item.imagem) for item in self.lista_itens]

        self.posicao_crianca_matriz = (1, 1)
        self.posicao_robo_matriz = (len(self.tabuleiro) - 2, len(self.tabuleiro[0]) - 2)

    def desenhar_labirinto(self):
        x, y = X_INICIAL, Y_INICIAL  # Posição inicial
        cont_itens = 0

        for i in range(len(self.tabuleiro)):

            linha = self.tabuleiro[i]

            for j, caractere in enumerate(linha):
                
                if i % 2 == 0:
                    if j % 2 == 0: #coluna de bordas verticais
                        if caractere == '+':
                            retangulo = (pygame.rect.Rect(x, y, ESPESSURA_BORDA, ESPESSURA_BORDA), self.PRETO)
                            pygame.draw.rect(self.tela, self.PRETO, retangulo[0])
                            self.lista_rect_tabuleiro.append(retangulo)
                        elif caractere == ' ':
                            retangulo = (pygame.rect.Rect(x, y, DISTANCIA_X, ESPESSURA_BORDA), self.BRANCO)
                            pygame.draw.rect(self.tela, self.BRANCO, retangulo[0])
                            self.lista_rect_tabuleiro.append(retangulo)
                        x += ESPESSURA_BORDA
                    else: #coluna de espaços
                        if caractere == "-":
                            retangulo = (pygame.rect.Rect(x, y, DISTANCIA_X, ESPESSURA_BORDA), self.PRETO)
                            pygame.draw.rect(self.tela, self.PRETO, retangulo[0])
                            self.lista_rect_tabuleiro.append(retangulo)
                        elif caractere == ' ':
                            retangulo = (pygame.rect.Rect(x, y, DISTANCIA_X, ESPESSURA_BORDA), self.BRANCO)
                            pygame.draw.rect(self.tela, self.BRANCO, retangulo[0])
                            self.lista_rect_tabuleiro.append(retangulo)
                        x += DISTANCIA_X

                else:
                    
                    if j % 2 == 0: #coluna de bordas verticais
                        if caractere == '|':
                            retangulo = (pygame.rect.Rect(x, y, ESPESSURA_BORDA, DISTANCIA_Y), self.PRETO)
                            pygame.draw.rect(self.tela, self.PRETO, retangulo[0])
                            self.lista_rect_tabuleiro.append(retangulo)
                        elif caractere == " ":
                            retangulo = (pygame.rect.Rect(x, y, ESPESSURA_BORDA, DISTANCIA_Y), self.BRANCO)
                            pygame.draw.rect(self.tela, self.BRANCO, retangulo[0])
                            self.lista_rect_tabuleiro.append(retangulo)
                        x += ESPESSURA_BORDA
                    
                    else: # coluna de espaços
                        if caractere == ' ':
                            retangulo = (pygame.rect.Rect(x, y, DISTANCIA_X, DISTANCIA_Y), self.BRANCO)
                            self.lista_rect_tabuleiro.append(retangulo)
                            pygame.draw.rect(self.tela, self.BRANCO, retangulo[0])
                        elif caractere == "i":
                            retangulo = (pygame.Rect(x, y, DISTANCIA_X, DISTANCIA_Y), self.BRANCO)
                            imagem_rect = self.lista_imagens[cont_itens].get_rect()

                            pygame.draw.rect(self.tela, self.BRANCO, retangulo[0])
                            if self.lista_itens[cont_itens].passou == False:
                                self.tela.blit(self.lista_imagens[cont_itens], (x, y))
                            self.lista_itens[cont_itens].posicao = (x, y)
                            self.lista_itens[cont_itens].posicao_matriz = (i, j)
                            #print(len(self.lista_itens))

                            self.lista_rect_tabuleiro.append(retangulo)
                            cont_itens += 1
                        x += DISTANCIA_X  # Avança horizontalmente

            x = 350  # Volta para a posição inicial na próxima linha
            if i % 2 == 0:
                y += ESPESSURA_BORDA
            else:
                y += DISTANCIA_Y

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

    def direcao_valida_crianca(self, key):
    
        if key == K_a or key == K_LEFT:
            x = self.posicao_crianca_matriz[0] - 1
            y = self.posicao_crianca_matriz[1]
        elif key == K_d or key == K_RIGHT:
            x = self.posicao_crianca_matriz[0] + 1
            y = self.posicao_crianca_matriz[1]
        elif key == K_w or key == K_UP:
            x = self.posicao_crianca_matriz[0]
            y = self.posicao_crianca_matriz[1] - 1
        elif key == K_s or key == K_DOWN:
            x = self.posicao_crianca_matriz[0]
            y = self.posicao_crianca_matriz[1] + 1

        if self.tabuleiro[y][x] not in ["+", "-", "|"]:
            if key == K_a or key == K_LEFT:
                x_novo = self.posicao_crianca_matriz[0] - 2
                y_novo = self.posicao_crianca_matriz[1]
            elif key == K_d or key == K_RIGHT:
                x_novo = self.posicao_crianca_matriz[0] + 2
                y_novo = self.posicao_crianca_matriz[1]
            elif key == K_w or key == K_UP:
                x_novo = self.posicao_crianca_matriz[0]
                y_novo = self.posicao_crianca_matriz[1] - 2
            elif key == K_s or key == K_DOWN:
                x_novo = self.posicao_crianca_matriz[0]
                y_novo = self.posicao_crianca_matriz[1] + 2

            self.posicao_crianca_matriz = (x_novo, y_novo)
            return True
        else:
            return False
        
    def direcao_valida_robo(self, key):
    
        if key == "left":
            x = self.posicao_robo_matriz[0] - 1
            y = self.posicao_robo_matriz[1]
        elif key == "right":
            x = self.posicao_robo_matriz[0] + 1
            y = self.posicao_robo_matriz[1]
        elif key == "up":
            x = self.posicao_robo_matriz[0]
            y = self.posicao_robo_matriz[1] - 1
        elif key == "down":
            x = self.posicao_robo_matriz[0]
            y = self.posicao_robo_matriz[1] + 1

        if self.tabuleiro[y][x] not in ["+", "-", "|"]:
            if key == "left":
                x_novo = self.posicao_robo_matriz[0] - 2
                y_novo = self.posicao_robo_matriz[1]
            elif key == "right":
                x_novo = self.posicao_robo_matriz[0] + 2
                y_novo = self.posicao_robo_matriz[1]
            elif key == "up":
                x_novo = self.posicao_robo_matriz[0]
                y_novo = self.posicao_robo_matriz[1] - 2
            elif key == "down":
                x_novo = self.posicao_robo_matriz[0]
                y_novo = self.posicao_robo_matriz[1] + 2

            self.posicao_robo_matriz = (x_novo, y_novo)
            return True
        else:
            return False

        

    def desenhar_tela(self):

        self.relogio.tick(FPS)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == K_a or event.key == K_LEFT:
                    nova_posicao = (self.crianca.xcor - DISTANCIA_X - ESPESSURA_BORDA, self.crianca.ycor)
                    if self.direcao_valida_crianca(event.key):
                        self.crianca.atualizar(nova_posicao)
                if event.key == K_d or event.key == K_RIGHT:
                    nova_posicao = (self.crianca.xcor + DISTANCIA_X + ESPESSURA_BORDA, self.crianca.ycor)
                    if self.direcao_valida_crianca(event.key):
                        self.crianca.atualizar(nova_posicao)
                if event.key == K_w or event.key == K_UP:
                    nova_posicao = (self.crianca.xcor, self.crianca.ycor - DISTANCIA_Y - ESPESSURA_BORDA)
                    if self.direcao_valida_crianca(event.key):
                        self.crianca.atualizar(nova_posicao)
                if event.key == K_s or event.key == K_DOWN:
                    nova_posicao = (self.crianca.xcor, self.crianca.ycor + DISTANCIA_Y + ESPESSURA_BORDA)
                    if self.direcao_valida_crianca(event.key):
                        self.crianca.atualizar(nova_posicao)

            if event.type == MOUSEBUTTONDOWN:
                pass          

        posicao_jogador = self.crianca.rect.topleft
        posicao_robo = self.robo.rect.topleft

        for item in self.lista_itens:
            if posicao_jogador == item.posicao and item.passou == False:
                item.passou = True
                self.pontos_jogador += 1 #aumentar pontuação do jogador
                self.itens_jogador_texto = self.fonte.render(f"Jogador: {self.pontos_jogador}/{self.pontos_totais}", True, self.PRETO)
                item.dono = "jogador"
                print(item.nome, item.dono, item.passou, item.posicao)
                self.novos_itens_jogador.append(item)
                posicao_matriz = item.posicao_matriz
                self.posicoes_itens_matriz.remove(posicao_matriz)
                self.novas_imagens_jogador.append(pygame.image.load(item.imagem))
            
            if posicao_robo == item.posicao and item.passou == False:
                item.passou = True
                self.pontos_robo += 1
                self.itens_robo_texto = self.fonte.render(f"Robô: {self.pontos_robo}/{self.pontos_totais}", True, self.PRETO)
                item.dono = "robô"
                print(item.nome, item.dono, item.passou, item.posicao)
                self.novos_itens_robo.append(item)
                self.novas_imagens_robo.append(pygame.image.load(item.imagem))
                posicao_matriz = item.posicao_matriz
                self.posicoes_itens_matriz.remove(posicao_matriz)
                self.caminho = ia_labirinto.encontrar_caminho_para_item(self.tabuleiro, self.posicao_robo_matriz, self.posicoes_itens_matriz)
                
 
        self.tela.fill(self.PRETO)
        self.tela.blit(self.imagem_fundo, (0, 0))
        pygame.draw.rect(self.tela, self.AMARELO2, self.fundo_rect)

        self.desenhar_labirinto()

        if self.robo.xcor == 0 and self.robo.ycor == 0:
            robo_x, robo_y = pegar_coordenadas_robo(self.lista_rect_tabuleiro)
            #print(robo_x, robo_y)
            self.robo.xcor = robo_x
            self.robo.ycor = robo_y
            self.robo.rect.topleft = robo_x, robo_y

        if self.crianca.xcor == 0 and self.crianca.ycor == 0:
            crianca_x, crianca_y = pegar_coordenadas_personagem(self.lista_rect_tabuleiro)
            self.crianca.xcor = crianca_x
            self.crianca.ycor = crianca_y
            self.crianca.rect.topleft = crianca_x, crianca_y
            #print(crianca_x, crianca_y)

        self.tempo_decorrido += 1
        segundos = self.tempo_decorrido // 60
        minutos = segundos // 60
        tempo_formatado = f"{minutos:02}:{segundos % 60:02}"
        self.tempo = self.fonte.render(tempo_formatado, True, self.PRETO)

        if self.tempo_decorrido % 300 == 0 or self.caminho is None:

            self.caminho = ia_labirinto.encontrar_caminho_para_item(self.tabuleiro, self.posicao_robo_matriz, self.posicoes_itens_matriz)
        
        if self.tempo_decorrido % 60 == 0 and self.caminho is not None and len(self.caminho) > 0:

            x_novo = 0
            y_novo = 0
            direcao = determinar_posicao_robo(self.caminho)
            self.caminho.pop(0)
            if direcao == 'left':
                nova_posicao = (self.robo.xcor - DISTANCIA_X - ESPESSURA_BORDA, self.robo.ycor)
                self.robo.atualizar(nova_posicao)
                x_novo = self.posicao_robo_matriz[0]
                y_novo = self.posicao_robo_matriz[1] - 2
            if direcao == 'right':
                nova_posicao = (self.robo.xcor + DISTANCIA_X + ESPESSURA_BORDA, self.robo.ycor)
                self.robo.atualizar(nova_posicao)
                x_novo = self.posicao_robo_matriz[0]
                y_novo = self.posicao_robo_matriz[1] + 2
            if direcao == "up":
                nova_posicao = (self.robo.xcor, self.robo.ycor - DISTANCIA_Y - ESPESSURA_BORDA)
                self.robo.atualizar(nova_posicao)
                x_novo = self.posicao_robo_matriz[0] - 2
                y_novo = self.posicao_robo_matriz[1]
            if direcao == "down":
                nova_posicao = (self.robo.xcor, self.robo.ycor + DISTANCIA_Y + ESPESSURA_BORDA)
                self.robo.atualizar(nova_posicao)
                x_novo = self.posicao_robo_matriz[0] + 2
                y_novo = self.posicao_robo_matriz[1]

            self.posicao_robo_matriz = (x_novo, y_novo)
            

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

        cont = 0
        for item in self.novos_itens_robo:
            self.tela.blit(self.novas_imagens_robo[cont], self.lista_posicoes_imagens_robo[cont])
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

