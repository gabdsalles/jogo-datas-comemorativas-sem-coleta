import pygame
from pygame.locals import *
import sys

class TelaFases:
    def __init__(self, largura, altura):
        pygame.init()

        self.LARGURA = largura
        self.ALTURA = altura
        self.tela = pygame.display.set_mode((self.LARGURA, self.ALTURA))
        pygame.display.set_caption('Tela de Fases')

        self.BRANCO = (255, 255, 255)
        self.PRETO = (0, 0, 0)
        self.AMARELO = (233, 255, 101)

        self.porta_rect = pygame.rect.Rect(790, 300, 160, 320)
        self.fonte = pygame.font.Font(None, 36)

        self.fonte_titulo = pygame.font.Font("assets/fonts/archivo_black.ttf", 48)
        self.texto_titulo = self.fonte_titulo.render("Fases", True, self.PRETO)

        self.texto_voltar = self.fonte.render("Voltar", True, self.BRANCO)
        self.ret_voltar = pygame.rect.Rect(10, 10, 200, 50)

        self.texto_jogar = self.fonte.render("Jogar", True, self.PRETO)
        self.ret_jogar = pygame.rect.Rect(300, 10, 200, 50)
        self.mostrar_botao_jogar = False

        self.lista_retangulos = [pygame.rect.Rect(150, 150, 300, 200), pygame.rect.Rect(500, 150, 300, 200), pygame.rect.Rect(850, 150, 300, 200), pygame.rect.Rect(150, 400, 300, 200), pygame.rect.Rect(500, 400, 300, 200), pygame.rect.Rect(850, 400, 300, 200)]

    def desenhar_grid(self):
        for x in range(0, self.LARGURA, 50):
            pygame.draw.line(self.tela, self.PRETO, (x, 0), (x, self.ALTURA))

        for y in range(0, self.ALTURA, 50):
            pygame.draw.line(self.tela, self.PRETO, (0, y), (self.LARGURA, y))
    
    def desenhar_tela(self):

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                if self.ret_voltar.collidepoint(pygame.mouse.get_pos()):
                    print("Clicou em Voltar")

                if self.ret_jogar.collidepoint(pygame.mouse.get_pos()) and self.mostrar_botao_jogar:
                    print("Clicou em Jogar")

        self.tela.fill(self.AMARELO)

        pygame.draw.rect(self.tela, self.PRETO, self.ret_voltar)
        self.tela.blit(self.texto_voltar, (self.ret_voltar.centerx - self.texto_voltar.get_width() // 2, self.ret_voltar.centery - self.texto_voltar.get_height() // 2))

        self.tela.blit(self.texto_titulo, (self.LARGURA // 2 - self.texto_titulo.get_width() // 2, 50))

        for ret in self.lista_retangulos:
            pygame.draw.rect(self.tela, self.PRETO, ret)

        #self.desenhar_grid()

        pygame.display.flip()

    def executar(self):
        while True:
            self.desenhar_tela()

telaFases = TelaFases(1280, 720)
telaFases.executar()
