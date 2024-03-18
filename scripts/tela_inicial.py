import pygame
from pygame.locals import *
import sys

class TelaInicial:
    def __init__(self, largura, altura):
        pygame.init()

        self.LARGURA = largura
        self.ALTURA = altura
        self.tela = pygame.display.set_mode((self.LARGURA, self.ALTURA))
        pygame.display.set_caption('Tela Inicial')

        self.BRANCO = (255, 255, 255)
        self.PRETO = (0, 0, 0)
        self.AMARELO = (255, 255, 0)

        self.fonte = pygame.font.SysFont(None, 36)

        self.imagem_fundo = pygame.image.load("assets/imagens/tela_inicial_fundo.png").convert()

        self.texto_titulo_1 = self.fonte.render("Jogo das Datas", True, self.BRANCO)
        self.texto_titulo_2 = self.fonte.render("Comemorativas", True, self.BRANCO)
        self.texto_jogar = self.fonte.render("Jogar", True, self.PRETO)
        self.texto_config = self.fonte.render("Configurações", True, self.PRETO)
        self.texto_sair = self.fonte.render("Sair", True, self.PRETO)

        self.ret_jogar = pygame.Rect(self.LARGURA / 2 - 100, 280, 200, 50)
        self.ret_config = pygame.Rect(self.LARGURA / 2 - 100, 380, 200, 50)
        self.ret_sair = pygame.Rect(self.LARGURA / 2 - 100, 480, 200, 50)
        self.ret_fundo = pygame.Rect(570, 300, 300, 500)
        self.ret_fundo.center = (self.LARGURA // 2, self.ALTURA // 2)
        self.ret_titulo = pygame.Rect(570 - 80, 150, 300, 100)

    def desenhar_tela(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                pos_mouse = pygame.mouse.get_pos()
                if self.ret_jogar.collidepoint(pos_mouse):
                    #print("Clicou em Jogar")
                    return "selecao_fases"
                    
                elif self.ret_config.collidepoint(pos_mouse):
                    #print("Clicou em Configurações")
                    return "configuracoes"
                elif self.ret_sair.collidepoint(pos_mouse):
                    pygame.quit()
                    sys.exit()

        self.tela.fill(self.PRETO)
        self.tela.blit(self.imagem_fundo, (0, 0))

        pygame.draw.rect(self.tela, self.PRETO, self.ret_fundo)
        pygame.draw.rect(self.tela, self.PRETO, self.ret_titulo)
        pygame.draw.rect(self.tela, self.AMARELO, self.ret_jogar)
        pygame.draw.rect(self.tela, self.AMARELO, self.ret_config)
        pygame.draw.rect(self.tela, self.AMARELO, self.ret_sair)

        self.tela.blit(self.texto_titulo_1, (self.ret_titulo.centerx - self.texto_titulo_1.get_width() // 2, self.ret_titulo.centery - 30))
        self.tela.blit(self.texto_titulo_2, (self.ret_titulo.centerx - self.texto_titulo_2.get_width() // 2, self.ret_titulo.centery + 20))
        self.tela.blit(self.texto_jogar, (self.ret_jogar.centerx - self.texto_jogar.get_width() // 2, self.ret_jogar.centery - self.texto_jogar.get_height() // 2))
        self.tela.blit(self.texto_config, (self.ret_config.centerx - self.texto_config.get_width() // 2, self.ret_config.centery - self.texto_config.get_height() // 2))
        self.tela.blit(self.texto_sair, (self.ret_sair.centerx - self.texto_sair.get_width() // 2, self.ret_sair.centery - self.texto_sair.get_height() // 2))

        pygame.display.flip()

    def executar(self):
        while True:
            retorno = self.desenhar_tela()
            if retorno != None:
                return retorno
