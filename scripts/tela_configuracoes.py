import pygame
from pygame.locals import *
import sys

class TelaConfiguracoes:
    def __init__(self, largura, altura):
        pygame.init()

        self.LARGURA = largura
        self.ALTURA = altura
        self.tela = pygame.display.set_mode((self.LARGURA, self.ALTURA))
        pygame.display.set_caption('Tela Inicial')

        self.BRANCO = (255, 255, 255)
        self.PRETO = (0, 0, 0)
        self.AMARELO = (255, 255, 0)

        self.fonte = pygame.font.Font(None, 36)

        self.imagem_fundo = pygame.image.load("assets/imagens/tela_inicial_fundo.png").convert()

        self.texto_titulo = self.fonte.render("Configurações", True, self.PRETO)
        self.texto_titulo_x = 570
        self.texto_titulo_y = 150

        self.ret_fundo = pygame.Rect(570, 300, 300, 500)
        self.ret_fundo.center = (self.LARGURA // 2, self.ALTURA // 2)
        self.ret_titulo = pygame.Rect(self.texto_titulo_x - 80, self.texto_titulo_y - 40, 300, 100)

    def desenhar_tela(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN: 
                pos_mouse = pygame.mouse.get_pos()
                if self.ret_jogar.collidepoint(pos_mouse):
                    print("Clicou em Jogar")
                    return "selecao_fases"
                    
                elif self.ret_config.collidepoint(pos_mouse):
                    print("Clicou em Configurações")
                elif self.ret_sair.collidepoint(pos_mouse):
                    pygame.quit()
                    sys.exit()

        self.tela.fill(self.PRETO)
        self.tela.blit(self.imagem_fundo, (0, 0))

        pygame.draw.rect(self.tela, self.PRETO, self.ret_fundo)
        pygame.draw.rect(self.tela, self.AMARELO, self.ret_titulo)

        self.tela.blit(self.texto_titulo, (self.ret_titulo.centerx - self.texto_titulo.get_width() // 2, self.ret_titulo.centery - 30))


        pygame.display.flip()

    def executar(self):
        while True:
            retorno = self.desenhar_tela()
            if retorno != None:
                return retorno
