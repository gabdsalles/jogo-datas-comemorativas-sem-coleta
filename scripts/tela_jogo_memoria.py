import pygame
from pygame.locals import *
import sys
from robo import Robo
from crianca import Crianca
from carta import Tabuleiro, Carta

LARGURA = 1280
ALTURA = 720
FPS = 60

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

        self.titulo_fase_texto = self.fonte.render("Festa Junina", True, self.PRETO)
        self.titulo_fase_x = 30
        self.titulo_fase_y = 50

        self.itens_jogador_texto = self.fonte.render("Cartas do jogador", True, self.PRETO)
        self.itens_jogador_x = 30
        self.itens_jogador_y = 200

        self.pontuacao_jogador_texto = self.fonte.render(f"{self.pontos_jogador}/{self.pontos_totais}", True, self.PRETO)
        self.pontos_jogador_x = 30
        self.pontos_jogador_y = 250

        self.tempo_texto = self.fonte.render("Tempo", True, self.PRETO)
        self.tempo_texto_x = 30
        self.tempo_texto_y = 350

        self.tempo = self.fonte.render("00:00", True, self.PRETO)
        self.tempo_x = 30
        self.tempo_y = 400

        self.tempo_decorrido = 0

        self.itens_robo_texto = self.fonte.render("Cartas do robô", True, self.PRETO)
        self.itens_robo_x = 30
        self.itens_robo_y = 500

        self.pontuacao_robo_texto = self.fonte.render(f"{self.pontos_robo}/{self.pontos_totais}", True, self.PRETO)
        self.pontos_robo_x = 30
        self.pontos_robo_y = 550

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

    def desenhar_cartas(self):

            for carta in self.tabuleiro.lista_cartas:
                
                if carta.virada == False:
                    rect = pygame.draw.rect(self.tela, self.AZUL_FUNDO, (carta.posicao[0], carta.posicao[1], 140, 210), border_radius=50) #borda
                    self.lista_retangulos.append(rect)
                    self.tela.blit(self.fundo_carta, carta.posicao)
                else:
                    #pygame.draw.rect(self.tela, self.PRETO, (carta.posicao[0], carta.posicao[1], 140, 210), border_radius=50) #borda
                    rect = pygame.draw.rect(self.tela, carta.cor, (carta.posicao[0]+5, carta.posicao[1]+5, 130, 200), border_radius=50) #carta
                    self.lista_retangulos.append(rect)
                    self.tela.blit(carta.imagem, carta.posicao)

    def checar_colisao(self, posicao_mouse):
        
        for i, carta in enumerate(self.tabuleiro.lista_cartas):

            if self.lista_retangulos[i].collidepoint(posicao_mouse) and carta.virada == False and self.tabuleiro.cartas_viradas < 2:
                carta.virada = True
                self.tabuleiro.cartas_viradas += 1

    def checar_jogada(self):

        carta1, carta2 = None, None

        for carta in self.tabuleiro.lista_cartas:
            if carta.virada == True and carta not in self.tabuleiro.lista_viradas:
                if carta1 == None:
                    carta1 = carta
                else:
                    carta2 = carta

        if carta1.nome == carta2.nome and carta1.dono == None and carta2.dono == None:
            carta1.dono = "jogador"
            carta2.dono = "jogador"
            self.pontos_jogador += 1
            self.pontuacao_jogador_texto = self.fonte.render(f"{self.pontos_jogador}/{self.pontos_totais}", True, self.PRETO)
            #self.vez_jogador = False
            #self.vez_robo = True
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
                #self.vez_jogador = False
                #self.vez_robo = True
                self.texto_jogador = self.fonte.render("Agora, é a vez do robô.", True, self.PRETO)
            else:
                self.texto_jogador = self.fonte.render("Não foi dessa vez!", True, self.PRETO)


    def desenhar_tela(self):

        self.relogio.tick(FPS)

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN and self.vez_jogador:
                posicao_mouse = pygame.mouse.get_pos()

                self.checar_colisao(posicao_mouse)        

        if self.tabuleiro.cartas_viradas == 2:
            if self.tempo_jogada == None:
                self.tempo_jogada = self.tempo_decorrido
            self.checar_jogada()

        
        self.tela.fill(self.PRETO)
        self.tela.blit(self.imagem_fundo, (0, 0))
        pygame.draw.rect(self.tela, self.AMARELO, self.fundo_rect)
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
        self.tela.blit(self.pontuacao_jogador_texto, (self.pontos_jogador_x, self.pontos_jogador_y))
        self.tela.blit(self.tempo_texto, (self.tempo_texto_x, self.tempo_texto_y))
        self.tela.blit(self.tempo, (self.tempo_x, self.tempo_y))
        self.tela.blit(self.itens_robo_texto, (self.itens_robo_x, self.itens_robo_y))
        self.tela.blit(self.pontuacao_robo_texto, (self.pontos_robo_x, self.pontos_robo_y))
        
        if self.vez_jogador:
            pygame.draw.rect(self.tela, self.AMARELO, (self.texto_jogador_x-10, self.texto_jogador_y-10, self.rect_texto_jogador.width+100, self.rect_texto_jogador.height+20), border_radius=20)
            self.tela.blit(self.texto_jogador, (self.texto_jogador_x, self.texto_jogador_y))

        pygame.display.flip()


    def executar(self):
        while True:
            self.desenhar_tela()


tela = TelaJogoMemoria(1280, 720)

tela.executar()

#TO-DO:
# 4. Colocar algoritmo de IA para fazer as escolhas do robô
# 5. Melhorar alguns itens da interface para que o jogador saiba quando o robô está realizando uma jogada, quando o robô ou jogador acertou ou errou, etc
# 6. Colocar ações do jogador e do robô em forma de texto (e som, talvez)
# 7. Colocar efeitos sonoros para acerto/erro do jogador e do robô
