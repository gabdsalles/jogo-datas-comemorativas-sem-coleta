import pygame
from pygame.locals import *
import sys, json

FPS = 60

class TelaConfiguracoes:
    """Na tela de configurações do jogo, é possível ajustar o volume. Esta tela é acessada apenas a
    partir da tela inicial e, ao clicar no botão voltar, retorna à tela inicial. O ajuste do volume ocorre
    usando botões de + e - e a barra de volume. O volume é salvo no arquivo game_data, que é um JSON."""
    def __init__(self, largura, altura):
        """Inicializa a tela e seus componentes. Carrega as configurações do arquivo game_data.json."""
        pygame.init()

        with open("./data/game_data.json", "r") as arquivo:
            self.configuracoes = json.load(arquivo)
        
        self.LARGURA = largura
        self.ALTURA = altura
        self.tela = pygame.display.set_mode((self.LARGURA, self.ALTURA))
        pygame.display.set_caption('Configurações')
        self.relogio = pygame.time.Clock()

        # Cores
        self.BRANCO = (255, 255, 255)
        self.PRETO = (0, 0, 0)
        self.AMARELO = (255, 255, 0)

        # Fonte
        self.fonte = pygame.font.Font(None, 36)

        # Imagem
        self.imagem_fundo = pygame.image.load("assets/imagens/tela_inicial_fundo.png").convert()

        # Textos e botões
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

        # Retângulos
        self.ret_fundo = pygame.Rect(0, 0, self.ret_fundo_width, self.ret_fundo_height)
        self.ret_fundo.center = (self.ret_fundo_x, self.ret_fundo_y)
        self.ret_titulo = self.texto_titulo.get_rect(center=(self.LARGURA // 2, self.texto_titulo_y))
        self.ret_volume = self.texto_volume.get_rect(center=(self.LARGURA // 2, self.texto_volume_y))

        # Volume
        self.volume = self.configuracoes["sons"]["volume_musica"] * 100
        self.volume_maximo = 100
        self.volume_minimo = 0

        self.clicks = 0
        self.tempo = 0
        self.tempo_formatado = "00:00"

    def desenhar_tela(self):
        """Desenha a tela de configurações. O volume é ajustado a partir de botões e uma barra de volume.
        Também é responsável por capturar os eventos de clique do mouse."""

        self.relogio.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                return "quit"
            if event.type == MOUSEBUTTONDOWN: 
                self.clicks += 1
                pos_mouse = pygame.mouse.get_pos()
                if self.botao_menos_rect.collidepoint(pos_mouse):
                    self.diminuir_volume()
                elif self.botao_mais_rect.collidepoint(pos_mouse):
                    self.aumentar_volume()
                elif self.botao_voltar.collidepoint(pos_mouse):
                    return "tela_inicial"

        self.tela.fill(self.PRETO)
        self.tela.blit(self.imagem_fundo, (0, 0))

        self.tempo += 1
        segundos = self.tempo // 60
        minutos = segundos // 60
        self.tempo_formatado = f"{minutos:02}:{segundos % 60:02}"

        pygame.draw.rect(self.tela, self.AMARELO, self.ret_fundo)

        self.tela.blit(self.texto_titulo, self.ret_titulo)
        self.tela.blit(self.texto_volume, self.ret_volume)

        # Barra de volume
        volume_bar_x = self.ret_fundo.centerx - self.volume_bar_width // 2
        volume_bar_y = self.ret_fundo.centery - self.volume_bar_height // 2
        pygame.draw.rect(self.tela, self.PRETO, (volume_bar_x, volume_bar_y, self.volume_bar_width, self.volume_bar_height))
        # Bolinha de volume
        volume_proporcao = self.volume / self.volume_maximo
        volume_bola_x = volume_bar_x + (self.volume_bar_width * volume_proporcao)
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
        """Aumenta o volume da música se o volume for menor que o máximo permitido (1.0). Salva o volume no JSON"""
        if self.volume < self.volume_maximo:
            self.volume += 10
            pygame.mixer.music.set_volume(self.volume / 100)
            self.alterar_volume_json()

    def diminuir_volume(self):
        """Diminui o volume da música se o volume for maior que o mínimo permitido (0.0). Salva o volume no JSON"""
        if self.volume > self.volume_minimo:
            self.volume -= 10
            pygame.mixer.music.set_volume(self.volume / 100)
            self.alterar_volume_json()

    def alterar_volume_json(self):

        """Altera o volume da música no arquivo JSON."""
        self.configuracoes["sons"]["volume_musica"] = self.volume / 100
        with open("./data/game_data.json", "w") as arquivo:
            json.dump(self.configuracoes, arquivo, ensure_ascii=False, indent=4)

    def executar(self):
        """Enquanto a tela de configurações estiver ativa, desenha a tela e captura os eventos de clique do mouse."""
        while True:
            retorno = self.desenhar_tela()
            if retorno != None:
                if retorno == "quit":
                    pygame.quit()
                    sys.exit()
                return retorno

