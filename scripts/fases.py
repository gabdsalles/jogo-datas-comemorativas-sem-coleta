from pygame.locals import *
import pygame

class Fase:

    """A classe Fase define um objeto que representa uma fase do jogo. Cada fase tem um retângulo que a representa
    na tela de seleção de fases, um nome e uma imagem."""
    
    def __init__(self, retangulo, nome, imagem):
        
        self.retangulo = retangulo
        self.nome = nome
        self.imagem = imagem


class ListaFases:

    """Essa classe controla a lista de fases do jogo. Ela é responsável por criar as fases e armazená-las em uma lista.
    Ela também é responsável por desenhar as fases na tela de seleção de fases."""
    
    def __init__(self):

        self.lista_retangulos = [pygame.rect.Rect(150, 150, 300, 200), pygame.rect.Rect(500, 150, 300, 200), pygame.rect.Rect(850, 150, 300, 200), pygame.rect.Rect(150, 400, 300, 200), pygame.rect.Rect(500, 400, 300, 200), pygame.rect.Rect(850, 400, 300, 200)]
        self.lista_nomes_fase = ["Páscoa", "Festa Junina", "Natal"]
        self.lista_imagens_fase = ["assets/imagens/fase1.png", "assets/imagens/fase2.png", "assets/imagens/fase3.png"]
        
        fase1 = Fase(pygame.rect.Rect(150, 150, 300, 200), "Páscoa", "assets/imagens/fase1.png")
        fase2 = Fase(pygame.rect.Rect(500, 150, 300, 200), "Festa Junina", "assets/imagens/fase2.png")
        fase3 = Fase(pygame.rect.Rect(850, 150, 300, 200), "Natal", "assets/imagens/fase3.png")
        fase4 = Fase(pygame.rect.Rect(150, 400, 300, 200), "Em desenvolvimento", "assets/imagens/dia_folclore.png")
        fase5 = Fase(pygame.rect.Rect(500, 400, 300, 200), "Em desenvolvimento", "assets/imagens/dia_criancas.png")
        fase6 = Fase(pygame.rect.Rect(850, 400, 300, 200), "Em desenvolvimento", "assets/imagens/carnaval.png")


        # quando tiver mais fases, fazer de forma mais automatica, pegando das listas acima

        self.lista_fases = [fase1, fase2, fase3, fase4, fase5, fase6]