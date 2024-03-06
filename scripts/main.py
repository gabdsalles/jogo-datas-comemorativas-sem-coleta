import pygame
from pygame.locals import *
from tela_domino import TelaDomino
from tela_selecao_fases import TelaFases
from tela_inicial import TelaInicial
from tela_jogo_memoria import TelaJogoMemoria
from tela_labirinto import TelaLabirinto
from tela_configuracoes import TelaConfiguracoes

LARGURA = 1280
ALTURA = 720

class ControladorTelas:
    def __init__(self):
        pygame.init()
        self.tela_atual = None
    
    def iniciar(self):
        while True:
            if self.tela_atual is None or self.tela_atual == "tela_inicial":
                tela_inicial = TelaInicial(LARGURA, ALTURA)
                self.tela_atual = tela_inicial.executar()
            elif self.tela_atual == "selecao_fases":
                tela_selecao_fases = TelaFases(LARGURA, ALTURA)
                self.tela_atual = tela_selecao_fases.executar()
            elif self.tela_atual == "pascoa":
                tela_domino = TelaDomino(LARGURA, ALTURA)
                self.tela_atual = tela_domino.executar()
            elif self.tela_atual == "festa junina":
                tela_jogo_memoria = TelaJogoMemoria(LARGURA, ALTURA)
                self.tela_atual = tela_jogo_memoria.executar()
            elif self.tela_atual == "natal":
                tela_labirinto = TelaLabirinto(LARGURA, ALTURA)
                self.tela_atual = tela_labirinto.executar()
            elif self.tela_atual == "configuracoes":
                tela_configuracoes = TelaConfiguracoes(LARGURA, ALTURA)
                self.tela_atual = tela_configuracoes.executar()

if __name__ == "__main__":
    controlador = ControladorTelas()
    controlador.iniciar()
