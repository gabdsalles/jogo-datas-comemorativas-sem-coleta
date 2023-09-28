import pygame
from pygame.locals import *
import sys
import maze_maker

class TelaLabirinto:
    def __init__(self, largura, altura):
        pygame.init()

        self.LARGURA = largura
        self.ALTURA = altura
        self.tela = pygame.display.set_mode((self.LARGURA, self.ALTURA))
        pygame.display.set_caption('Fase 1 - Labirinto')

        self.BRANCO = (255, 255, 255)
        self.PRETO = (0, 0, 0)
        self.AMARELO = (255, 255, 0)
        self.VERMELHO = (255, 0, 0)

        self.pontos_jogador = 0
        self.pontos_robo = 0
        self.pontos_totais = 5

        self.fonte = pygame.font.Font('fonts/archivo_black.ttf', 36)
        self.fundo_rect = pygame.rect.Rect(0, 0, 300, 720)
        self.tabuleiro = maze_maker.make_maze(8, 8)
        print(self.tabuleiro)

        self.titulo_fase_texto = self.fonte.render("Natal", True, self.BRANCO)
        self.titulo_fase_x = 120
        self.titulo_fase_y = 50

        self.itens_jogador_texto = self.fonte.render("Itens do jogador", True, self.BRANCO)
        self.itens_jogador_x = 50
        self.itens_jogador_y = 150

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
        self.itens_robo_y = 450

        self.pontuacao_robo_texto = self.fonte.render(f"{self.pontos_robo}/{self.pontos_totais}", True, self.BRANCO)
        self.pontos_robo_x = 50
        self.pontos_robo_y = 550

    def desenhar_tela(self):

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                pass

            if event.type == MOUSEBUTTONDOWN:
                pass          

        self.tela.fill(self.VERMELHO)

        distancia = 30

        x, y = 450, 50  # Posição inicial para desenhar o labirinto
        for linha in self.tabuleiro.splitlines():
            for caractere in linha:
                if caractere == ' ':
                    pygame.draw.rect(self.tela, self.BRANCO, (x, y, distancia, distancia))
                x += distancia  # Avança horizontalmente
            x = 450  # Volta para a posição inicial na próxima linha
            y += distancia
        
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

#TO-DO:
# 1. Ajustar as posições dos textos
# 2. Fazer com que os textos de tempo e pontuação mudem
# 3. Melhorar o desenho do labirinto
# 4. Colocar uma imagem pra servir como "jogador"
# 5. Controlar movimentos do jogador (pygame.event)
# 6. Checar colisões com o labirinto (direções possíveis)
# 7. Colocar itens no labirinto
# 8. Checar colisões com os itens
# 9. Colocar o robô no labirinto
# 10. Implementar algoritmo de IA no robô

