import pygame
from pygame.locals import *
import sys, json

class TelaConfiguracoes:
    def __init__(self, largura, altura):
        pygame.init()

        with open("./data/game_data.json", "r") as arquivo:
            self.configuracoes = json.load(arquivo)
        
        self.LARGURA = largura
        self.ALTURA = altura
        self.tela = pygame.display.set_mode((self.LARGURA, self.ALTURA))
        pygame.display.set_caption('Configurações')

        self.BRANCO = (255, 255, 255)
        self.PRETO = (0, 0, 0)
        self.AMARELO = (255, 255, 0)

        self.fonte = pygame.font.Font(None, 36)

        self.imagem_fundo = pygame.image.load("assets/imagens/tela_inicial_fundo.png").convert()

        self.texto_titulo = self.fonte.render("Configurações", True, self.PRETO)
        self.texto_volume = self.fonte.render("Volume:", True, self.PRETO)

        self.imagem_voltar = pygame.image.load("assets/imagens/voltar.png")
        self.botao_voltar = pygame.rect.Rect(10, 10, 30, 30)

        # Posição dos elementos
        self.texto_titulo_x = self.LARGURA // 2
        self.texto_titulo_y = 150
        self.texto_volume_x = self.LARGURA // 2
        self.texto_volume_y = 220
        self.ret_fundo_x = self.LARGURA // 2
        self.ret_fundo_y = self.ALTURA // 2
        self.ret_fundo_width = 300
        self.ret_fundo_height = 500
        self.volume_bar_width = 200
        self.volume_bar_height = 10
        self.botao_menos_x = self.LARGURA // 2 - 130
        self.botao_menos_y = self.ALTURA // 2 + 70
        self.botao_mais_x = self.LARGURA // 2 + 80
        self.botao_mais_y = self.ALTURA // 2 + 70

        self.ret_fundo = pygame.Rect(0, 0, self.ret_fundo_width, self.ret_fundo_height)
        self.ret_fundo.center = (self.ret_fundo_x, self.ret_fundo_y)
        self.ret_titulo = self.texto_titulo.get_rect(center=(self.LARGURA // 2, self.texto_titulo_y))
        self.ret_volume = self.texto_volume.get_rect(center=(self.LARGURA // 2, self.texto_volume_y))

        # Volume
        self.volume = 50
        self.volume_maximo = 100
        self.volume_minimo = 0

    def desenhar_tela(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN: 
                pos_mouse = pygame.mouse.get_pos()
                if self.botao_menos_rect.collidepoint(pos_mouse):
                    self.diminuir_volume()
                elif self.botao_mais_rect.collidepoint(pos_mouse):
                    self.aumentar_volume()
                elif self.botao_voltar.collidepoint(pos_mouse):
                    return "tela_inicial"

        self.tela.fill(self.PRETO)
        self.tela.blit(self.imagem_fundo, (0, 0))

        pygame.draw.rect(self.tela, self.AMARELO, self.ret_fundo)

        self.tela.blit(self.texto_titulo, self.ret_titulo)
        self.tela.blit(self.texto_volume, self.ret_volume)

        # Barra de volume
        volume_bar_x = self.ret_fundo.centerx - self.volume_bar_width // 2
        volume_bar_y = self.ret_fundo.centery - self.volume_bar_height // 2
        pygame.draw.rect(self.tela, self.PRETO, (volume_bar_x, volume_bar_y, self.volume_bar_width, self.volume_bar_height))
        # Bolinha de volume
        volume_bola_x = volume_bar_x + (self.volume / self.volume_maximo) * self.volume_bar_width
        volume_bola_y = volume_bar_y + self.volume_bar_height // 2
        pygame.draw.circle(self.tela, self.PRETO, (int(volume_bola_x), volume_bola_y), 8)

        pygame.draw.rect(self.tela, self.PRETO, self.botao_voltar)
        self.tela.blit(self.imagem_voltar, (10, 10))

        self.botao_menos_rect = pygame.draw.rect(self.tela, self.PRETO, (self.botao_menos_x, self.botao_menos_y, 50, 50))
        self.botao_mais_rect = pygame.draw.rect(self.tela, self.PRETO, (self.botao_mais_x, self.botao_mais_y, 50, 50))
        menos_text = self.fonte.render("-", True, self.BRANCO)
        mais_text = self.fonte.render("+", True, self.BRANCO)
        self.tela.blit(menos_text, (self.botao_menos_x + 15, self.botao_menos_y + 15))
        self.tela.blit(mais_text, (self.botao_mais_x + 15, self.botao_mais_y + 15))

        pygame.display.flip()

    def aumentar_volume(self):
        if self.volume < self.volume_maximo:
            self.volume += 10
            self.alterar_volume_json()

    def diminuir_volume(self):
        if self.volume > self.volume_minimo:
            self.volume -= 10
            self.alterar_volume_json()

    def alterar_volume_json(self):

        self.configuracoes["sons"]["volume_musica"] = self.volume / 100
        with open("./data/game_data.json", "w") as arquivo:
            json.dump(self.configuracoes, arquivo, ensure_ascii=False, indent=4)

    def executar(self):
        while True:
            retorno = self.desenhar_tela()
            if retorno != None:
                return retorno

