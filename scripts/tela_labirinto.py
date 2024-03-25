import pygame
from pygame.locals import *
import sys, json
from scripts.sprites.crianca import Crianca
import scripts.maze_maker as maze_maker
from scripts.sprites.robo import Robo
from scripts.labirinto.itens import ListaItens
import scripts.labirinto.ia_labirinto as ia
import scripts.labirinto.logica_labirinto as logica

# -*- coding: utf-8 -*-

DISTANCIA_X = 30
DISTANCIA_Y = 30
ESPESSURA_BORDA = 10
FPS = 60
X_INICIAL = 350
Y_INICIAL = 25

class TelaLabirinto:
    
    """A tela do labirinto tem como data comemorativa o Natal. O jogador deve coletar 10 itens antes do robô.
    O jogador e o robô se movem pelo labirinto e coletam os itens. O jogador pode clicar nas setas do teclado
    para mover a criança e o robô se move automaticamente. O jogador pode clicar no botão de voltar para voltar
    para a seleção de fases."""
    
    def __init__(self, largura, altura):
        
        """Inicializa os componentes da tela do labirinto."""
        
        pygame.init()

        with open("./data/game_data.json", "r", encoding='utf-8') as arquivo:
            self.configuracoes = json.load(arquivo)

        self.sons = self.configuracoes["sons"]
        self.texto_narracao = self.configuracoes["textos_fases"]["natal"]
        
        pygame.mixer.music.set_volume(self.sons["volume_jogador"])
        self.musica_de_fundo = pygame.mixer.music.load(self.configuracoes["narracoes"]["natal"])
        pygame.mixer.music.play()

        self.som_pontuacao_jogador = pygame.mixer.Sound('./assets/sons/ponto_jogador.wav')
        self.som_pontuacao_robo = pygame.mixer.Sound('./assets/sons/ponto_robo_labirinto.wav')

        self.narracao = True
        self.jogando = False
        self.perdeu = False
        self.ganhou = False
        
        # Configurações da tela
        self.LARGURA = largura
        self.ALTURA = altura
        self.tela = pygame.display.set_mode((self.LARGURA, self.ALTURA))
        pygame.display.set_caption('Labirinto')
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
        self.lista_imagens_narracao = [pygame.image.load("assets/imagens/natal_narracao/arvore_natal.png"), pygame.image.load("assets/imagens/natal_narracao/papai_noel.png"), 
                                       pygame.image.load("assets/imagens/natal_narracao/presepio_natal.png")]

        # Cores
        self.BRANCO = (255, 255, 255)
        self.PRETO = (0, 0, 0)
        self.AMARELO = (255, 255, 0)
        self.VERMELHO = (255, 0, 0)
        self.AMARELO2 = (233, 255, 101)
        self.cor_botoes = (106, 224, 97)

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
        self.fonte_narracao = pygame.font.SysFont("calibri", 30, bold=True, italic=True)
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
        self.itens_robo_y = 380

        self.tempo = self.fonte.render("00:00", True, self.PRETO)
        self.tempo_x = 100
        self.tempo_y = 675

        self.tempo_decorrido = 0

        self.imagem_voltar = pygame.image.load("assets/imagens/voltar.png")
        self.botao_voltar = pygame.rect.Rect(10, 10, 30, 30)

        # Labirinto
        self.tabuleiro = maze_maker.make_maze()
        self.lista_rect_tabuleiro = [] # lista de retangulos do labirinto, que serão desenhados
        # for row in self.tabuleiro:
        #     print(''.join(row))

        self.lista_posicoes_imagens_jogador = [(30, 260), (80, 260), (35, 220), (70, 220), (55, 180), (180, 260), 
        (230, 260), (185, 220), (220, 220), (205, 180)]

        self.lista_posicoes_imagens_robo = [(x, y + 275) for x, y in self.lista_posicoes_imagens_jogador]
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
        
        """Função que desenha o labirinto na tela. A partir do self.tabuleiro, desenha-se os retângulos
        que representam as paredes e os espaços do labirinto. Também desenha as imagens dos itens nos
        retângulos correspondentes."""
        
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
                            if self.lista_itens[cont_itens].passou == False and self.lista_itens[cont_itens].dono == None:
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
    
    def desenhar_grid(self, tela, largura_tela, altura_tela, grid_largura, grid_altura):

        """Função auxiliar, não é desenhada na versão final do jogo. Desenha um grid na tela para facilitar
         a disposição dos componentes da tela. O grid é desenhado com linhas horizontais e verticais."""
        
        # Desenhe as linhas horizontais do grid
        for y in range(0, altura_tela, grid_altura):
            pygame.draw.line(tela, (100, 100, 100), (0, y), (largura_tela, y))

        # Desenhe as linhas verticais do grid
        for x in range(0, largura_tela, grid_largura):
            pygame.draw.line(tela, (100, 100, 100), (x, 0), (x, altura_tela))

    def direcao_valida_crianca(self, key):
    
        """Recebe a tecla pressionada pelo jogador e verifica se a criança (jogador) pode se mover na direção.
        Retorna True se a direção é válida e False caso contrário."""
        
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
    
        """Similar à função direcao_valida_crianca, mas para o robô. Recebe a direção que o robô quer seguir
        e verifica se é possível. Retorna True se a direção é válida e False caso contrário."""
        
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

        """Desenha todos os componentes da tela. Também é responsável por verificar os cliques e teclas pressionadas
        pelo jogador. Retorna "selecao_fases" se o jogador clicar no botão de voltar. A lógica de jogo é executada
        aqui."""
        
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
                if self.botao_voltar.collidepoint(pygame.mouse.get_pos()):
                    return "selecao_fases"          

        posicao_jogador = self.crianca.rect.topleft
        posicao_robo = self.robo.rect.topleft

        for item in self.lista_itens:
            if posicao_jogador == item.posicao and item.passou == False and item.dono == None:
                item.passou = True
                pygame.mixer.music.set_volume(self.sons["volume_jogador"])
                self.som_pontuacao_jogador.play()
                pygame.mixer.music.set_volume(self.sons["volume_musica"])
                self.pontos_jogador += 1 #aumentar pontuação do jogador
                self.itens_jogador_texto = self.fonte.render(f"Jogador: {self.pontos_jogador}/{self.pontos_totais}", True, self.PRETO)
                item.dono = "jogador"
                #print(item.nome, item.dono, item.passou, item.posicao)
                self.novos_itens_jogador.append(item)
                posicao_matriz = item.posicao_matriz
                if posicao_matriz in self.posicoes_itens_matriz:
                    self.posicoes_itens_matriz.remove(posicao_matriz)
                self.novas_imagens_jogador.append(pygame.image.load(item.imagem))
            
            if posicao_robo == item.posicao and item.passou == False and item.dono == None:
                item.passou = True
                self.som_pontuacao_robo.play()
                pygame.mixer.music.set_volume(self.sons["volume_musica"])
                self.pontos_robo += 1
                self.itens_robo_texto = self.fonte.render(f"Robô: {self.pontos_robo}/{self.pontos_totais}", True, self.PRETO)
                item.dono = "robô"
                #print(item.nome, item.dono, item.passou, item.posicao)
                self.novos_itens_robo.append(item)
                self.novas_imagens_robo.append(pygame.image.load(item.imagem))
                posicao_matriz = item.posicao_matriz
                if posicao_matriz in self.posicoes_itens_matriz:
                    self.posicoes_itens_matriz.remove(posicao_matriz)
                self.caminho = ia.encontrar_caminho_para_item(self.tabuleiro, self.posicao_robo_matriz, self.posicoes_itens_matriz)
                
        self.tela.fill(self.PRETO)
        self.tela.blit(self.imagem_fundo, (0, 0))
        pygame.draw.rect(self.tela, self.AMARELO2, self.fundo_rect)

        self.desenhar_labirinto()

        if self.robo.xcor == 0 and self.robo.ycor == 0:
            robo_x, robo_y = logica.pegar_coordenadas_robo(self.lista_rect_tabuleiro)
            #print(robo_x, robo_y)
            self.robo.xcor = robo_x
            self.robo.ycor = robo_y
            self.robo.rect.topleft = robo_x, robo_y

        if self.crianca.xcor == 0 and self.crianca.ycor == 0:
            crianca_x, crianca_y = logica.pegar_coordenadas_personagem(self.lista_rect_tabuleiro)
            self.crianca.xcor = crianca_x
            self.crianca.ycor = crianca_y
            self.crianca.rect.topleft = crianca_x, crianca_y
            #print(crianca_x, crianca_y)

        self.tempo_decorrido += 1
        segundos = self.tempo_decorrido // 60
        minutos = segundos // 60
        tempo_formatado = f"{minutos:02}:{segundos % 60:02}"
        self.tempo = self.fonte.render(tempo_formatado, True, self.PRETO)

        if self.tempo_decorrido % 300 == 0 or self.caminho is None or self.tempo_decorrido == 0 or len(self.caminho) == 0:

            self.caminho = ia.encontrar_caminho_para_item(self.tabuleiro, self.posicao_robo_matriz, self.posicoes_itens_matriz)
        
        if self.tempo_decorrido % 60 == 0 and self.caminho is not None and len(self.caminho) > 0:

            x_novo = 0
            y_novo = 0
            direcao = logica.determinar_posicao_robo(self.caminho)
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
        
        pygame.draw.rect(self.tela, self.PRETO, self.botao_voltar)
        self.tela.blit(self.imagem_voltar, (10, 10))
        self.tela.blit(self.titulo_fase_texto, (self.titulo_fase_x, self.titulo_fase_y))
        self.tela.blit(self.itens_jogador_texto, (self.itens_jogador_x, self.itens_jogador_y))
        self.tela.blit(self.itens_robo_texto, (self.itens_robo_x, self.itens_robo_y))
        self.tela.blit(self.tempo_texto, (self.tempo_texto_x, self.tempo_texto_y))
        self.tela.blit(self.tempo, (self.tempo_x, self.tempo_y))
        self.tela.blit(self.arvore_jogador_1, (-30, 130))
        self.tela.blit(self.arvore_jogador_2, (120, 130))
        self.tela.blit(self.arvore_robo_1, (-30, 410))
        self.tela.blit(self.arvore_robo_2, (120, 410))

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

        if self.pontos_jogador == 10:
            self.jogando = False
            self.ganhou = True
            return None
        
        if self.pontos_robo == 10:
            self.jogando = False
            self.perdeu = True
            return None

    def desenhar_perdeu(self):
        
        """Desenha a tela de perdeu. O jogador perdeu se o robô coletou 10 itens antes dele. O jogador pode clicar
        no botão de voltar para voltar para a seleção de fases ou no botão de jogar novamente para recomeçar o jogo."""
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                pos_mouse = pygame.mouse.get_pos()
                if self.botao_voltar.collidepoint(pos_mouse):
                    #limpar variáveis de tempo, pontuação, etc e recomeçar o jogo
                    #print("Clicou no Sim!")
                    return "natal"
                if self.botao_nao.collidepoint(pos_mouse):
                    # voltar para a seleção de fases
                    #print("Clicou no Não!")
                    return "selecao_fases"

        self.tela.blit(self.imagem_fundo, (0, 0))
        pygame.draw.rect(self.tela, self.AMARELO2, self.fundo_rect)

        self.tela.blit(self.titulo_fase_texto, (self.titulo_fase_x, self.titulo_fase_y))
        self.tela.blit(self.itens_jogador_texto, (self.itens_jogador_x, self.itens_jogador_y))
        self.tela.blit(self.itens_robo_texto, (self.itens_robo_x, self.itens_robo_y))
        self.tela.blit(self.tempo_texto, (self.tempo_texto_x, self.tempo_texto_y))
        self.tela.blit(self.tempo, (self.tempo_x, self.tempo_y))
        self.tela.blit(self.arvore_jogador_1, (-30, 130))
        self.tela.blit(self.arvore_jogador_2, (120, 130))
        self.tela.blit(self.arvore_robo_1, (-30, 410))
        self.tela.blit(self.arvore_robo_2, (120, 410))

        cont = 0
        for item in self.novos_itens_jogador:
            self.tela.blit(self.novas_imagens_jogador[cont], self.lista_posicoes_imagens_jogador[cont])
            cont += 1

        cont = 0
        for item in self.novos_itens_robo:
            self.tela.blit(self.novas_imagens_robo[cont], self.lista_posicoes_imagens_robo[cont])
            cont += 1

        pygame.draw.rect(self.tela, self.AMARELO2, (400, 100, 780, 520), border_radius=40)
        self.imagem_robo = pygame.image.load("assets/imagens/robo_maior.png")
        self.tela.blit(self.imagem_robo, (450, 200))

        texto_perdeu = self.fonte_maior.render("Você perdeu! :(", True, self.PRETO)
        self.tela.blit(texto_perdeu, (740, 170))
        texto_jogar_novamente = self.fonte_menor.render("Quer jogar novamente?", True, self.PRETO)
        self.tela.blit(texto_jogar_novamente, (760, 300))

        self.botao_voltar = pygame.draw.rect(self.tela, self.cor_botoes, (810, 400, 100, 50), border_radius=20)
        texto_sim = self.fonte.render("Sim", True, self.PRETO)
        self.tela.blit(texto_sim, (830, 410))

        self.botao_nao = pygame.draw.rect(self.tela, self.cor_botoes, (1010, 400, 100, 50), border_radius=20)
        texto_nao = self.fonte.render("Não", True, self.PRETO)
        self.tela.blit(texto_nao, (1030, 410))

        #self.desenhar_grid(self.tela, self.LARGURA, self.ALTURA, self.GRID_LARGURA, self.GRID_ALTURA)

        pygame.display.flip()
    
    def desenhar_ganhou(self):

        """Desenha a tela de ganhou. O jogador ganhou se coletou 10 itens antes do robô. O jogador pode clicar
        no botão de voltar para voltar para a seleção de fases."""
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                pos_mouse = pygame.mouse.get_pos()
                if self.botao_voltar.collidepoint(pos_mouse):
                    return "selecao_fases"
        
        self.tela.blit(self.imagem_fundo, (0, 0))
        pygame.draw.rect(self.tela, self.AMARELO2, self.fundo_rect)

        self.tela.blit(self.titulo_fase_texto, (self.titulo_fase_x, self.titulo_fase_y))
        self.tela.blit(self.itens_jogador_texto, (self.itens_jogador_x, self.itens_jogador_y))
        self.tela.blit(self.itens_robo_texto, (self.itens_robo_x, self.itens_robo_y))
        self.tela.blit(self.tempo_texto, (self.tempo_texto_x, self.tempo_texto_y))
        self.tela.blit(self.tempo, (self.tempo_x, self.tempo_y))
        self.tela.blit(self.arvore_jogador_1, (-30, 130))
        self.tela.blit(self.arvore_jogador_2, (120, 130))
        self.tela.blit(self.arvore_robo_1, (-30, 410))
        self.tela.blit(self.arvore_robo_2, (120, 410))

        cont = 0
        for item in self.novos_itens_jogador:
            self.tela.blit(self.novas_imagens_jogador[cont], self.lista_posicoes_imagens_jogador[cont])
            cont += 1

        cont = 0
        for item in self.novos_itens_robo:
            self.tela.blit(self.novas_imagens_robo[cont], self.lista_posicoes_imagens_robo[cont])
            cont += 1

        pygame.draw.rect(self.tela, self.AMARELO2, (400, 100, 780, 520), border_radius=40)
        self.imagem_robo = pygame.image.load("assets/imagens/robo_maior.png")
        self.tela.blit(self.imagem_robo, (450, 200))

        texto_ganhou = self.fonte_maior.render("Você ganhou! :)", True, self.PRETO)
        self.tela.blit(texto_ganhou, (740, 200))
        texto_voltar = self.fonte_menor.render("Volte para a seleção", True, self.PRETO)
        texto_voltar2 = self.fonte_menor.render("de fases", True, self.PRETO)
        self.tela.blit(texto_voltar, (800, 330))
        self.tela.blit(texto_voltar2, (900, 360))

        cor_botoes = (106, 224, 97)
        self.botao_voltar = pygame.draw.rect(self.tela, cor_botoes, (910, 430, 100, 50), border_radius=20)
        texto_voltar = self.fonte.render("Voltar", True, self.PRETO)
        self.tela.blit(texto_voltar, (920, 440))

        #self.desenhar_grid(self.tela, self.LARGURA, self.ALTURA, self.GRID_LARGURA, self.GRID_ALTURA)

        pygame.display.flip()

    def box_text(self, surface, font, x_start, x_end, y_start, text):
        
        """Função auxiliar chamada na função desenhar_narracao, que desenha a tela e o texto de narração.
        Essa função quebra o texto em linhas para que ele caiba na tela. Também desenha o texto na tela"""
        
        x = x_start
        y = y_start
        words = text.split(' ')
        
        line_width = 0
        space_width = font.render(' ', True, self.PRETO).get_width() * 1.1

        for word in words:
            word_t = font.render(word, True, self.PRETO)
            word_width = word_t.get_width()
            
            if line_width + word_width <= x_end - x_start:
                surface.blit(word_t, (x, y))
                x += word_width + space_width
                line_width += word_width + space_width
            else:
                y += word_t.get_height() * 1.25
                x = x_start
                line_width = 0
                surface.blit(word_t, (x, y))
                x += word_width + space_width
                line_width += word_width + space_width

    def desenhar_narracao(self):
        
        """Desenha a tela, os textos e as imagens de narração daquela fase. O jogador pode pular a narração
        no botão "Pular", no canto inferior direito da tela."""
        
        if pygame.mixer.get_busy():
            self.musica_de_fundo = pygame.mixer.music.load(self.configuracoes["musicas"]["pascoa"])
            pygame.mixer.music.set_volume(self.sons["volume_musica"])
            self.narracao = False
            self.jogando = True
            pygame.mixer.music.play(-1)
            return None
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                pos_mouse = pygame.mouse.get_pos()
                if self.botao_pular.collidepoint(pos_mouse):
                    self.musica_de_fundo = pygame.mixer.music.load(self.configuracoes["musicas"]["natal"])
                    pygame.mixer.music.set_volume(self.sons["volume_musica"])
                    self.narracao = False
                    self.jogando = True
                    pygame.mixer.music.play(-1)
                    return None
                elif self.botao_voltar.collidepoint(pos_mouse):
                    return "selecao_fases"

        self.tela.fill(self.PRETO)
        self.tela.blit(self.imagem_fundo, (0, 0))
        pygame.draw.rect(self.tela, self.AMARELO2, self.fundo_rect)

        pygame.draw.rect(self.tela, self.PRETO, self.botao_voltar)
        self.tela.blit(self.imagem_voltar, (10, 10))
        
        self.tela.blit(self.titulo_fase_texto, (self.titulo_fase_x, self.titulo_fase_y))

        y_imagem = 100
        for imagem in self.lista_imagens_narracao:
            self.tela.blit(imagem, (25, y_imagem))
            y_imagem += 200
        
        pygame.draw.rect(self.tela, self.AMARELO2, (350, 50, 880, 620), border_radius=40)
        self.box_text(self.tela, self.fonte_narracao, 700, 1200, 150, self.texto_narracao)

        self.imagem_robo = pygame.image.load("assets/imagens/robo_maior.png")
        self.tela.blit(self.imagem_robo, (350, 200))

        self.botao_pular = pygame.rect.Rect(1100, 600, 100, 50)
        pygame.draw.rect(self.tela, self.cor_botoes, self.botao_pular, border_radius=20)
        texto_pular = self.fonte.render("Pular", True, self.PRETO)
        self.tela.blit(texto_pular, (1120, 615))
        
        pygame.display.flip()
    
    def executar(self):
        
        """Função principal que chama as outras funções de desenho e controle do jogo. As variáveis booleanas
        self.narracao, self.jogando, self.ganhou e self.perdeu controlam o que é desenhado na tela."""
        
        while True:
            
            if self.narracao:
                retorno = self.desenhar_narracao()
            
            if self.jogando:
                retorno = self.desenhar_tela()

            if self.perdeu:
                retorno = self.desenhar_perdeu()

            if self.ganhou:
                retorno = self.desenhar_ganhou()

            if retorno != None:
                pygame.mixer.music.stop()
                if retorno == "selecao_fases":
                    self.musica_de_fundo = pygame.mixer.music.load("./assets/sons/musica_fundo.wav")
                    pygame.mixer.music.play()
                return retorno