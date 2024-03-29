import pygame
from pygame.locals import *
import sys, json
from scripts.dados import atualizar_contagem_telas, salvar_dados_gerais, salvar_dados_outras_telas

FPS = 60

class TelaInicial:
    
    """A tela inicial do jogo é a primeira a ser exibida. Nela, o jogador pode escolher entre jogar, acessar
    as configurações ou sair do jogo. A tela inicial é acessada ao iniciar o jogo e, ao clicar em jogar, o jogo
    avança para a seleção de fases. Ao clicar em configurações, o jogo avança para a tela de configurações. Ao
    clicar em sair, o jogo é encerrado. A tela inicial possui uma música de fundo que é executada ao ser inicializada."""

    def __init__(self, largura, altura):
        
        """Inicializa a tela e seus componentes. Carrega a música de fundo e as imagens da tela inicial."""

        pygame.init()

        with open("./data/game_data.json", "r", encoding="utf-8") as arquivo:
            self.configuracoes = json.load(arquivo)

        self.volume = self.configuracoes["sons"]["volume_musica"]
        self.relogio = pygame.time.Clock()
        self.clicks = 0

        self.LARGURA = largura
        self.ALTURA = altura
        self.tela = pygame.display.set_mode((self.LARGURA, self.ALTURA))
        pygame.display.set_caption('Tela Inicial')

        self.musica_de_fundo = pygame.mixer.music.load("./assets/sons/musica_fundo.wav")
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play()

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

        self.tempo = 0
        self.tempo_formatado = "00:00"

    def desenhar_tela(self):
        
        """Desenha os componentes da tela inicial e verifica os cliques do jogador. Retorna a próxima tela a
        ser exibida."""
        self.relogio.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                return "quit"
            if event.type == MOUSEBUTTONDOWN:
                self.clicks += 1
                pos_mouse = pygame.mouse.get_pos()
                if self.ret_jogar.collidepoint(pos_mouse):
                    #print("Clicou em Jogar")
                    return "selecao_fases"
                    
                elif self.ret_config.collidepoint(pos_mouse):
                    #print("Clicou em Configurações")
                    return "configuracoes"
                elif self.ret_sair.collidepoint(pos_mouse):
                    salvar_dados_gerais(self.configuracoes["quantas_vezes_jogou_cada_tela"])
                    salvar_dados_outras_telas(self.clicks, self.tempo_formatado, "tela_inicial")
                    pygame.quit()
                    sys.exit()

        self.tela.fill(self.PRETO)
        self.tela.blit(self.imagem_fundo, (0, 0))

        self.tempo += 1
        segundos = self.tempo // 60
        minutos = segundos // 60
        self.tempo_formatado = f"{minutos:02}:{segundos % 60:02}"

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
        
        """Executa a tela inicial até que o jogador clique em jogar, configurações ou sair."""
        
        while True:
            retorno = self.desenhar_tela()
            if retorno != None:
                salvar_dados_outras_telas(self.clicks, self.tempo_formatado, "tela_inicial")
                if retorno == "quit":
                    salvar_dados_gerais(self.configuracoes["quantas_vezes_jogou_cada_tela"])
                    pygame.quit()
                    sys.exit()
                else:
                    atualizar_contagem_telas(retorno)
                return retorno
