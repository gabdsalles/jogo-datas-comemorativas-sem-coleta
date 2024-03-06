import json
import pygame
from pygame.locals import *
from fases import ListaFases
import sys, os

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

        self.fonte = pygame.font.Font(None, 36)

        self.fonte_titulo = pygame.font.Font("assets/fonts/archivo_black.ttf", 48)
        self.texto_titulo = self.fonte_titulo.render("Fases", True, self.PRETO)

        self.texto_voltar = self.fonte.render("Voltar", True, self.BRANCO)
        self.ret_voltar = pygame.rect.Rect(10, 10, 200, 50)

        self.lista_fases = ListaFases().lista_fases

        diretorio_atual = os.path.dirname(__file__)
        caminho_json = os.path.join(diretorio_atual, "data", "game_data.json")

        with open(caminho_json, "r") as arquivo:
            self.configuracoes = json.load(arquivo)

        locked = self.configuracoes["locked"]
        self.locked = [locked[fase] for fase in locked]

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
                    return "tela_inicial"

                for fase in self.lista_fases:
                    if not self.locked[self.lista_fases.index(fase)] and fase.retangulo.collidepoint(pygame.mouse.get_pos()):
                        print(f"Clicou na fase {fase.nome}")
                        if (fase.nome == "Páscoa"):
                            return "pascoa"
                        elif (fase.nome == "Festa Junina"):
                            return "festa junina"
                        elif (fase.nome == "Natal"):
                            return "natal"

        self.tela.fill(self.AMARELO)

        pygame.draw.rect(self.tela, self.PRETO, self.ret_voltar)
        self.tela.blit(self.texto_voltar, (self.ret_voltar.centerx - self.texto_voltar.get_width() // 2, self.ret_voltar.centery - self.texto_voltar.get_height() // 2))

        self.tela.blit(self.texto_titulo, (self.LARGURA // 2 - self.texto_titulo.get_width() // 2, 50))

        for fase in self.lista_fases:
            pygame.draw.rect(self.tela, self.PRETO, fase.retangulo)
            posicao_imagem = fase.retangulo.topleft
            if fase.nome == "Em desenvolvimento":
                imagem_preto_e_branco = pygame.image.load(fase.imagem).convert()
                imagem_preto_e_branco.set_alpha(128)
                self.tela.blit(imagem_preto_e_branco, (posicao_imagem[0], posicao_imagem[1]))
            else:
                self.tela.blit(pygame.image.load(fase.imagem), (posicao_imagem[0], posicao_imagem[1]))
            pygame.draw.rect(self.tela, self.BRANCO, fase.retangulo, 5)
            texto_fase = self.fonte.render(fase.nome, True, self.PRETO)
            self.tela.blit(texto_fase, (fase.retangulo.centerx - texto_fase.get_width() // 2, fase.retangulo.bottom + 10))
            if self.locked[self.lista_fases.index(fase)]:

                imagem_locked = pygame.image.load("assets/imagens/locked.png")
                self.tela.blit(imagem_locked, (fase.retangulo.centerx - imagem_locked.get_width() // 2, fase.retangulo.centery - imagem_locked.get_height() // 2))

        pygame.display.flip()

    def executar(self):
        while True:
            retorno = self.desenhar_tela()
            if retorno != None:
                return retorno
