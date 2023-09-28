import pygame
from pygame.locals import *
import sys
from personagem import Personagem
from tela_labirinto import TelaLabirinto

class TelaFases:
    def __init__(self, largura, altura):
        pygame.init()

        self.LARGURA = largura
        self.ALTURA = altura
        self.tela = pygame.display.set_mode((self.LARGURA, self.ALTURA))
        pygame.display.set_caption('Tela de Fases')
        self.telaLabirinto = TelaLabirinto(self.LARGURA, self.ALTURA)

        self.BRANCO = (255, 255, 255)
        self.PRETO = (0, 0, 0)
        self.AMARELO = (255, 255, 0)

        self.porta_rect = pygame.rect.Rect(790, 300, 160, 320)
        self.fonte = pygame.font.Font(None, 36)

        self.personagem = Personagem()
        self.todas_sprites = pygame.sprite.Group()
        self.todas_sprites.add(self.personagem)
        self.posicao_relativa = self.personagem.rect.x

        self.texto_voltar = self.fonte.render("Voltar", True, self.PRETO)
        self.ret_voltar = pygame.rect.Rect(10, 10, 200, 50)

        self.texto_jogar = self.fonte.render("Jogar", True, self.PRETO)
        self.ret_jogar = pygame.rect.Rect(300, 10, 200, 50)
        self.mostrar_botao_jogar = False

        self.imagem_fundo = pygame.image.load("assets/fases_imagem.png").convert()
        self.imagem_fundo_rect = self.imagem_fundo.get_rect()
        self.imagem_fundo_posx = 0

    def verificar_colisao_porta(self):
        # Verifica se o personagem colidiu com a porta
        if self.personagem.rect.colliderect(self.porta_rect):
            self.mostrar_botao_jogar = True
        else:
            self.mostrar_botao_jogar = False

    def desenhar_tela(self):
        self.verificar_colisao_porta()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                #print(self.posicao_relativa)
                if event.key == K_d and self.personagem.rect.x < self.LARGURA // 2:
                    self.personagem.rect.x += 50
                    self.posicao_relativa += 50

                if event.key == K_d and self.personagem.rect.x == 650:
                    self.imagem_fundo_posx -= 50
                    self.porta_rect.x -= 50
                    self.posicao_relativa += 50
                
                if event.key == K_a and self.personagem.rect.x > 100:
                    self.personagem.rect.x -= 50
                    self.posicao_relativa -= 50
                
                if event.key == K_a and self.personagem.rect.x == 100 and self.posicao_relativa != 100:
                    self.imagem_fundo_posx += 50
                    self.porta_rect.x += 50
                    self.posicao_relativa -= 50

            if event.type == MOUSEBUTTONDOWN:
                if self.ret_voltar.collidepoint(pygame.mouse.get_pos()):
                    print("Clicou em Voltar")

                if self.ret_jogar.collidepoint(pygame.mouse.get_pos()) and self.mostrar_botao_jogar:
                    print("Clicou em Jogar")
                    self.telaLabirinto.executar()


        if self.posicao_relativa % 1600 == 0 and self.posicao_relativa != 0:
            self.porta_rect.x = self.LARGURA            

        self.tela.fill(self.PRETO)
        self.tela.blit(self.imagem_fundo, (self.imagem_fundo_posx, 0))
        
        if self.mostrar_botao_jogar:
            pygame.draw.rect(self.tela, self.AMARELO, self.ret_jogar)
            self.tela.blit(self.texto_jogar, (self.ret_jogar.centerx - self.texto_jogar.get_width() // 2, self.ret_jogar.centery - self.texto_jogar.get_height() // 2))

        pygame.draw.rect(self.tela, self.AMARELO, self.ret_voltar)
        #pygame.draw.rect(self.tela, self.AMARELO, self.porta_rect)
        self.tela.blit(self.texto_voltar, (self.ret_voltar.centerx - self.texto_voltar.get_width() // 2, self.ret_voltar.centery - self.texto_voltar.get_height() // 2))
        self.todas_sprites.draw(self.tela)
        self.todas_sprites.update()

        pygame.display.flip()

    def executar(self):
        while True:
            self.desenhar_tela()
