import pygame
from pygame.locals import *
import sys
from robo import Robo
from crianca import Crianca
from carta import Tabuleiro, Carta
import ia_jogo_memoria

LARGURA = 1280
ALTURA = 720
FPS = 60

carta1, carta2 = None, None

class TelaJogoMemoria:

    def __init__(self, largura, altura):

        pygame.init()

        self.LARGURA = largura
        self.ALTURA = altura
        self.tela = pygame.display.set_mode((self.LARGURA, self.ALTURA))
        pygame.display.set_caption('Fase 2 - Jogo da Memória')
        self.relogio = pygame.time.Clock()

        self.imagem_fundo = pygame.image.load("assets/imagens/festa_junina/festajunina_fundo.jpg").convert()

        self.BRANCO = (255, 255, 255)
        self.PRETO = (0, 0, 0)
        self.AMARELO = (255, 255, 0)
        self.VERMELHO = (255, 0, 0)
        self.AZUL_FUNDO = (0, 61, 80)
        self.AMARELO2 = (233, 255, 101)

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

        self.fonte = pygame.font.Font(None, 36)
        self.fundo_rect = pygame.rect.Rect(0, 0, 300, 720)

        self.titulo_fase_texto = self.fonte.render("Festa Junina", True, self.PRETO)
        self.titulo_fase_x = 75
        self.titulo_fase_y = 20

        self.itens_jogador_texto = self.fonte.render(f"Jogador: {self.pontos_jogador}/{self.pontos_totais}", True, self.PRETO)
        self.itens_jogador_x = 75
        self.itens_jogador_y = 100

        self.tempo_texto = self.fonte.render("Tempo: ", True, self.PRETO)
        self.tempo_texto_x = 10
        self.tempo_texto_y = 675

        self.tempo = self.fonte.render("00:00", True, self.PRETO)
        self.tempo_x = 100
        self.tempo_y = 675

        self.tempo_decorrido = 0

        self.itens_robo_texto = self.fonte.render(f"Robô: {self.pontos_robo}/{self.pontos_totais}", True, self.PRETO)
        self.itens_robo_x = 90
        self.itens_robo_y = 430

        self.texto_jogador = self.fonte.render("É sua vez de jogar!", True, self.PRETO)
        self.texto_jogador_x = 500
        self.texto_jogador_y = 630
        self.rect_texto_jogador = self.texto_jogador.get_rect()

        self.vez_jogador = True
        self.vez_robo = False

        self.retangulo_background = pygame.rect.Rect(450, 100, 775, 500)
        self.lista_retangulos = []

        self.fundo_carta = pygame.image.load("assets/imagens/cartas/fundo_carta.png")

        self.tabuleiro = Tabuleiro()

        self.tempo_jogada = None
        
        self.qtd_jogadas_jogador = 0
        self.qtd_jogadas_robo = 0

    def desenhar_cartas(self):

            for carta in self.tabuleiro.lista_cartas:
                
                if carta.virada == False:
                    rect = pygame.draw.rect(self.tela, self.AZUL_FUNDO, (carta.posicao[0], carta.posicao[1], 140, 210), border_radius=50) #borda
                    self.lista_retangulos.append(rect)
                    self.tela.blit(self.fundo_carta, carta.posicao)
                else:
                    # pygame.draw.rect(self.tela, self.PRETO, (carta.posicao[0], carta.posicao[1], 140, 210), border_radius=50) #borda
                    rect = pygame.draw.rect(self.tela, carta.cor, (carta.posicao[0]+5, carta.posicao[1]+5, 130, 200), border_radius=50) #carta
                    self.lista_retangulos.append(rect)
                    self.tela.blit(carta.imagem, carta.posicao)

    def checar_colisao(self, posicao_mouse):
        
        for i, carta in enumerate(self.tabuleiro.lista_cartas):

            if self.lista_retangulos[i].collidepoint(posicao_mouse) and carta.virada == False and self.tabuleiro.cartas_viradas < 2:
                carta.virada = True
                self.tabuleiro.cartas_viradas += 1

    def checar_jogada_jogador(self):

        carta1, carta2 = None, None

        for carta in self.tabuleiro.lista_cartas:
            if carta.virada == True and carta not in self.tabuleiro.lista_viradas:
                if carta1 == None:
                    carta1 = carta
                else:
                    carta2 = carta

        # se o jogador achou um par
        if carta1.nome == carta2.nome and carta1.dono == None and carta2.dono == None:
            carta1.dono = "jogador"
            carta2.dono = "jogador"
            self.pontos_jogador += 1
            self.itens_jogador_texto = self.fonte.render(f"Jogador: {self.pontos_jogador}/{self.pontos_totais}", True, self.PRETO)
            self.tabuleiro.cartas_viradas = 0
            self.tabuleiro.lista_viradas.append(carta1)
            self.tabuleiro.lista_viradas.append(carta2)
            self.tempo_jogada = None

        else:
            #print(self.tempo_decorrido - self.tempo_jogada)
            if self.tempo_decorrido - self.tempo_jogada == 120:
                #print("não foi dessa vez.")
                carta1.virada = False
                carta2.virada = False
                self.tabuleiro.cartas_viradas = 0
                self.tempo_jogada = None
                self.vez_jogador = False
                self.vez_robo = True
                self.texto_jogador = self.fonte.render("Agora, é a vez do robô.", True, self.PRETO)
            else:
                self.texto_jogador = self.fonte.render("Não foi dessa vez!", True, self.PRETO)
                # print(self.tempo_decorrido - self.tempo_jogada)

    def jogada_robo(self):

        if self.vez_robo:
            carta1, carta2 = ia_jogo_memoria.escolher_cartas(self.tabuleiro.lista_cartas)
            print(f"Carta 1: {carta1.nome}, Carta 2: {carta2.nome}")
            self.qtd_jogadas_robo += 1
            self.tabuleiro.cartas_viradas = 2
            return carta1, carta2

    def checar_jogada_robo(self, carta1, carta2):

        if self.tempo_decorrido - self.tempo_jogada == 120:
            #Mostrar segunda carta
            carta1.virada = True
            carta2.virada = True

        if self.tempo_decorrido - self.tempo_jogada == 240:
            if carta1.nome == carta2.nome and carta1.dono == None and carta2.dono == None: # acertou
                carta1.dono = "robo"
                carta2.dono = "robo"
                self.pontos_robo += 1
                self.itens_robo_texto = self.fonte.render(f"Robô: {self.pontos_robo}/{self.pontos_totais}", True, self.PRETO)
                self.tabuleiro.cartas_viradas = 0
                self.tabuleiro.lista_viradas.append(carta1)
                self.tabuleiro.lista_viradas.append(carta2)
                self.tempo_jogada = None
            else:
                carta1.virada = False
                carta2.virada = False
                self.tabuleiro.cartas_viradas = 0
                self.vez_robo = False
                self.vez_jogador = True
                self.texto_jogador = self.fonte.render("É sua vez de jogar!", True, self.PRETO)
                self.tempo_jogada = None


    def desenhar_tela(self):

        self.relogio.tick(FPS)

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN and self.vez_jogador:
                posicao_mouse = pygame.mouse.get_pos()

                self.checar_colisao(posicao_mouse)        

        if self.vez_jogador and self.tabuleiro.cartas_viradas == 2:
            if self.tempo_jogada == None:
                self.tempo_jogada = self.tempo_decorrido
            self.checar_jogada_jogador()

        if self.vez_robo and self.tabuleiro.cartas_viradas < 2:
            global carta1, carta2
            carta1, carta2 = self.jogada_robo()

        if self.vez_robo and self.tabuleiro.cartas_viradas == 2:
            if self.tempo_jogada == None:
                self.tempo_jogada = self.tempo_decorrido
            self.checar_jogada_robo(carta1, carta2)

        self.tela.fill(self.PRETO)
        self.tela.blit(self.imagem_fundo, (0, 0))
        pygame.draw.rect(self.tela, self.AMARELO2, self.fundo_rect)
        pygame.draw.rect(self.tela, self.VERMELHO, self.retangulo_background, border_radius=20)

        self.desenhar_cartas()

        self.tempo_decorrido += 1
        segundos = self.tempo_decorrido // 60
        minutos = segundos // 60
        tempo_formatado = f"{minutos:02}:{segundos % 60:02}"

        self.tempo = self.fonte.render(tempo_formatado, True, self.PRETO)

        self.todas_sprites.draw(self.tela)

        self.tela.blit(self.titulo_fase_texto, (self.titulo_fase_x, self.titulo_fase_y))
        self.tela.blit(self.itens_jogador_texto, (self.itens_jogador_x, self.itens_jogador_y))
        self.tela.blit(self.tempo_texto, (self.tempo_texto_x, self.tempo_texto_y))
        self.tela.blit(self.tempo, (self.tempo_x, self.tempo_y))
        self.tela.blit(self.itens_robo_texto, (self.itens_robo_x, self.itens_robo_y))
        
        pygame.draw.rect(self.tela, self.AMARELO, (self.texto_jogador_x-10, self.texto_jogador_y-10, self.rect_texto_jogador.width+100, self.rect_texto_jogador.height+20), border_radius=20)
        self.tela.blit(self.texto_jogador, (self.texto_jogador_x, self.texto_jogador_y))

        pygame.display.flip()


    def executar(self):
        while True:
            self.desenhar_tela()


tela = TelaJogoMemoria(1280, 720)

tela.executar()
