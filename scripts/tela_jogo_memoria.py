import json
import random
import pygame
from pygame.locals import *
import sys
from scripts.jogo_memoria.carta import Tabuleiro
import scripts.jogo_memoria.ia_jogo_memoria as ia

LARGURA = 1280
ALTURA = 720
FPS = 60

carta1, carta2 = None, None

class TelaJogoMemoria:

    """A tela do jogo da memória tem como data comemorativa a Festa Junina. O jogador joga contra um robô e o objetivo é achar mais
    pares de cartas do que o robô. A tela possui uma narração inicial, que pode ser pulada. Na parte inferior da tela,
    o jogo informa de quem é a vez. Se está na vez do jogador, o jogo aguarda o clique do jogador para virar duas cartas.
    Depois, passa para a vez do robô. O jogo termina quando todas as cartas forem viradas e o jogador ou o robô tiverem
    encontrado todos os pares. Ao final do jogo, o jogador é informado se ganhou ou perdeu e pode voltar para a seleção de fases."""
    
    def __init__(self, largura, altura):

        """Inicializa a tela e seus componentes. Carrega a música de fundo e as imagens da tela do jogo da memória"""
        
        pygame.init()

        with open("./data/game_data.json", "r", encoding='utf-8') as arquivo:
            self.configuracoes = json.load(arquivo)

        self.sons = self.configuracoes["sons"]
        self.texto_narracao = self.configuracoes["textos_fases"]["festa_junina"]
        
        pygame.mixer.music.set_volume(self.sons["volume_jogador"])
        self.musica_de_fundo = pygame.mixer.music.load(self.configuracoes["narracoes"]["festa_junina"])
        pygame.mixer.music.play()

        self.som_pontuacao_jogador = pygame.mixer.Sound('./assets/sons/ponto_jogador.wav')
        self.som_pontuacao_robo = pygame.mixer.Sound('./assets/sons/ponto_robo.wav')

        self.narracao = True
        self.jogando = False
        self.perdeu = False
        self.ganhou = False

        self.LARGURA = largura
        self.ALTURA = altura
        self.tela = pygame.display.set_mode((self.LARGURA, self.ALTURA))
        pygame.display.set_caption('Jogo da Memória')
        self.relogio = pygame.time.Clock()

        self.imagem_fundo = pygame.image.load("assets/imagens/festa_junina/festajunina_fundo.jpg").convert()
        self.lista_imagens_narracao = [pygame.image.load("assets/imagens/festa_junina_narracao/festajunina1.png"), pygame.image.load("assets/imagens/festa_junina_narracao/festajunina2.png"), 
                                       pygame.image.load("assets/imagens/festa_junina_narracao/festajunina3.png")]

        self.BRANCO = (255, 255, 255)
        self.PRETO = (0, 0, 0)
        self.AMARELO = (255, 255, 0)
        self.VERMELHO = (255, 0, 0)
        self.AZUL_FUNDO = (0, 61, 80)
        self.AMARELO2 = (233, 255, 101)
        self.cor_botoes = (106, 224, 97)

        self.pontos_jogador = 0
        self.pontos_robo = 0
        self.pontos_totais = 5

        self.lista_cartas_jogador = []
        self.lista_cartas_robo = []

        self.fonte = pygame.font.Font(None, 36)
        self.fonte_maior = pygame.font.Font('assets/fonts/archivo_black.ttf', 48)
        self.fonte_menor = pygame.font.Font('assets/fonts/archivo_black.ttf', 30)
        self.fonte_narracao = pygame.font.SysFont("calibri", 30, bold=True, italic=True)
        self.fundo_rect = pygame.rect.Rect(0, 0, 300, 720)

        self.titulo_fase_texto = self.fonte_menor.render("Festa Junina", True, self.PRETO)
        self.titulo_fase_x = 60
        self.titulo_fase_y = 20

        self.itens_jogador_texto = self.fonte.render(f"Jogador: {self.pontos_jogador}/{self.pontos_totais}", True, self.PRETO)
        self.itens_jogador_x = 75
        self.itens_jogador_y = 100

        self.tempo_texto = self.fonte.render("Tempo: ", True, self.PRETO)
        self.tempo_texto_x = 10
        self.tempo_texto_y = 675

        self.tempo = self.fonte.render("00:00", True, self.PRETO)
        self.tempo_x = 100
        self.tempo_y = 675

        self.tempo_decorrido = 0

        self.imagem_voltar = pygame.image.load("assets/imagens/voltar.png")
        self.botao_voltar = pygame.rect.Rect(10, 10, 30, 30)

        self.itens_robo_texto = self.fonte.render(f"Robô: {self.pontos_robo}/{self.pontos_totais}", True, self.PRETO)
        self.itens_robo_x = 90
        self.itens_robo_y = 380

        self.texto_jogador = self.fonte.render("É sua vez de jogar!", True, self.PRETO)
        self.texto_jogador_x = 500
        self.texto_jogador_y = 630
        self.rect_texto_jogador = self.texto_jogador.get_rect()

        self.vez_jogador = True
        self.vez_robo = False

        self.retangulo_background = pygame.rect.Rect(450, 100, 775, 500)
        self.lista_retangulos = []

        self.fundo_carta = pygame.image.load("assets/imagens/cartas/fundo_carta.png")

        self.tabuleiro = Tabuleiro()
        

        self.tempo_jogada = None
        
        self.qtd_jogadas_jogador = 0
        self.qtd_jogadas_robo = 0

        self.posicoes_cartas_jogador = [(30, 150), (120, 150), (210, 150), (60, 250), (150, 250)]
        self.posicoes_cartas_robo = [(30, 430), (120, 430), (210, 430), (60, 580), (150, 580)]

    def desenhar_cartas(self):

        """Desenha as cartas do jogo da memória na tela. Se a carta estiver virada, desenha a imagem da carta. Se não, desenha
        o fundo da carta."""
        
        for carta in self.tabuleiro.lista_cartas:
            
            if carta.virada == False:
                rect = pygame.draw.rect(self.tela, self.AZUL_FUNDO, (carta.posicao[0], carta.posicao[1], 140, 210), border_radius=50) #borda
                self.lista_retangulos.append(rect)
                self.tela.blit(self.fundo_carta, carta.posicao)
            else:
                # pygame.draw.rect(self.tela, self.PRETO, (carta.posicao[0], carta.posicao[1], 140, 210), border_radius=50) #borda
                rect = pygame.draw.rect(self.tela, carta.cor, (carta.posicao[0]+5, carta.posicao[1]+5, 130, 200), border_radius=50) #carta
                self.lista_retangulos.append(rect)
                self.tela.blit(carta.imagem, carta.posicao)

    def checar_colisao(self, posicao_mouse):
        
        """Checa se o clique do jogador foi em cima de uma carta. Se sim, vira a carta."""
        
        for i, carta in enumerate(self.tabuleiro.lista_cartas):

            if self.lista_retangulos[i].collidepoint(posicao_mouse) and carta.virada == False and self.tabuleiro.cartas_viradas < 2:
                carta.virada = True
                self.tabuleiro.cartas_viradas += 1
                print(f"Carta {i} virada.")

    def checar_jogada_jogador(self):

        """Checa se o jogador acertou um par de cartas. Se sim, adiciona um ponto ao jogador e vira as cartas. Se não, desvira as cartas.
        A função segura a virada das cartas por 2 segundos, para que o jogador possa ver as cartas viradas."""
        
        carta1, carta2 = None, None

        for carta in self.tabuleiro.lista_cartas:
            if carta.virada == True and carta not in self.tabuleiro.lista_viradas:
                if carta1 == None:
                    carta1 = carta
                else:
                    carta2 = carta

        # se o jogador achou um par
        if carta1.nome == carta2.nome and carta1.dono == None and carta2.dono == None:
            carta1.dono = "jogador"
            carta2.dono = "jogador"
            self.pontos_jogador += 1
            self.som_pontuacao_jogador.play()
            self.itens_jogador_texto = self.fonte.render(f"Jogador: {self.pontos_jogador}/{self.pontos_totais}", True, self.PRETO)
            self.tabuleiro.cartas_viradas = 0
            self.tabuleiro.lista_viradas.append(carta1)
            self.tabuleiro.lista_viradas.append(carta2)
            self.lista_cartas_jogador.append(carta1)
            self.tempo_jogada = None
            self.qtd_jogadas_jogador += 1
            ia.limpar_cartas_lembradas()

        else:
            #print(self.tempo_decorrido - self.tempo_jogada)
            if self.tempo_decorrido - self.tempo_jogada == 120:
                #print("não foi dessa vez.")
                carta1.virada = False
                carta2.virada = False
                self.tabuleiro.cartas_viradas = 0
                self.tempo_jogada = None
                self.vez_jogador = False
                self.vez_robo = True
                self.texto_jogador = self.fonte.render("Agora, é a vez do robô.", True, self.PRETO)
                self.qtd_jogadas_jogador += 1
            else:
                self.texto_jogador = self.fonte.render("Não foi dessa vez!", True, self.PRETO)
                # print(self.tempo_decorrido - self.tempo_jogada)

    def jogada_robo(self):

        """Aqui, o robô escolhe as cartas da sua jogada, na função ia.escolher_Cartas. A função retorna as cartas escolhidas."""
        
        if self.vez_robo:
            carta1, carta2 = ia.escolher_cartas(self.tabuleiro.lista_cartas)
            # print(f"Carta 1: {carta1.nome}, Carta 2: {carta2.nome}")
            self.qtd_jogadas_robo += 1
            self.tabuleiro.cartas_viradas = 2
            return carta1, carta2

    def checar_jogada_robo(self, carta1, carta2):

        """Similar à função checar_jogada_jogador, essa função checa se o robô acertou um par de cartas. Se sim, adiciona um ponto ao robô e vira as cartas.
        Se não, desvira as cartas. A função segura a virada das cartas por 2 segundos, para que o jogador possa ver as cartas viradas."""
        
        if self.tempo_decorrido - self.tempo_jogada == 120:
            #Mostrar segunda carta
            carta1.virada = True
            carta2.virada = True

        if self.tempo_decorrido - self.tempo_jogada == 240:
            if carta1.nome == carta2.nome and carta1.dono == None and carta2.dono == None: # acertou
                carta1.dono = "robo"
                carta2.dono = "robo"
                self.pontos_robo += 1
                self.som_pontuacao_robo.play()
                self.itens_robo_texto = self.fonte.render(f"Robô: {self.pontos_robo}/{self.pontos_totais}", True, self.PRETO)
                self.tabuleiro.cartas_viradas = 0
                self.tabuleiro.lista_viradas.append(carta1)
                self.tabuleiro.lista_viradas.append(carta2)
                self.lista_cartas_robo.append(carta1)
                self.tempo_jogada = None
                ia.limpar_cartas_lembradas()
            else:
                carta1.virada = False
                carta2.virada = False
                self.tabuleiro.cartas_viradas = 0
                self.vez_robo = False
                self.vez_jogador = True
                self.texto_jogador = self.fonte.render("É sua vez de jogar!", True, self.PRETO)
                self.tempo_jogada = None
                ia.atualizar_cartas_lembradas(random.choice([carta1, carta2]))


    def desenhar_cartas_jogador(self):

        """Desenha as cartas do jogador na tela, na esquerda da tela. As cartas são desenhadas em posições pré-definidas."""
        
        largura_carta = 60
        altura_carta = 100
        tamanho_retangulo = (largura_carta, altura_carta)

        for i, carta in enumerate(self.lista_cartas_jogador):
            x = self.posicoes_cartas_jogador[i][0]
            y = self.posicoes_cartas_jogador[i][1]

            rect = pygame.Rect(x, y, largura_carta, altura_carta)
            pygame.draw.rect(self.tela, self.AZUL_FUNDO, rect, border_radius=30)

            imagem_carta = carta.imagem
            imagem_carta = pygame.transform.scale(imagem_carta, tamanho_retangulo)

            self.tela.blit(imagem_carta, (x, y))

    def desenhar_cartas_robo(self):

        """Desenha as cartas do robô na tela, na esquerda da tela. As cartas são desenhadas em posições pré-definidas."""
        
        largura_carta = 60
        altura_carta = 100
        tamanho_retangulo = (largura_carta, altura_carta)

        for i, carta in enumerate(self.lista_cartas_robo):
            x = self.posicoes_cartas_robo[i][0]
            y = self.posicoes_cartas_robo[i][1]

            rect = pygame.Rect(x, y, largura_carta, altura_carta)
            pygame.draw.rect(self.tela, self.AZUL_FUNDO, rect, border_radius=30)

            imagem_carta = carta.imagem
            imagem_carta = pygame.transform.scale(imagem_carta, tamanho_retangulo)

            self.tela.blit(imagem_carta, (x, y))

    def desenhar_tela(self):

        """Desenha a tela do jogo da memória. A tela é composta por um fundo, cartas, botões e textos. A função checa se o jogador ou o robô
        estão jogando e chama as funções de jogada do jogador e do robô. A função também checa se o jogo terminou e se o jogador ganhou ou perdeu."""
        
        self.relogio.tick(FPS)

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN and self.vez_jogador:
                posicao_mouse = pygame.mouse.get_pos()
                
                if self.botao_voltar.collidepoint(posicao_mouse):
                    return "selecao_fases"

                self.checar_colisao(posicao_mouse)        

        if self.vez_jogador and self.tabuleiro.cartas_viradas == 2:
            if self.tempo_jogada == None:
                self.tempo_jogada = self.tempo_decorrido
            self.checar_jogada_jogador()

        if self.vez_robo and self.tabuleiro.cartas_viradas < 2:
            global carta1, carta2
            carta1, carta2 = self.jogada_robo()

        if self.vez_robo and self.tabuleiro.cartas_viradas == 2:
            if self.tempo_jogada == None:
                self.tempo_jogada = self.tempo_decorrido
            self.checar_jogada_robo(carta1, carta2)

        self.tela.fill(self.PRETO)
        self.tela.blit(self.imagem_fundo, (0, 0))
        pygame.draw.rect(self.tela, self.AMARELO2, self.fundo_rect)
        pygame.draw.rect(self.tela, self.VERMELHO, self.retangulo_background, border_radius=20)

        self.desenhar_cartas()

        self.tempo_decorrido += 1
        segundos = self.tempo_decorrido // 60
        minutos = segundos // 60
        tempo_formatado = f"{minutos:02}:{segundos % 60:02}"

        self.tempo = self.fonte.render(tempo_formatado, True, self.PRETO)

        pygame.draw.rect(self.tela, self.PRETO, self.botao_voltar)
        self.tela.blit(self.imagem_voltar, (10, 10))
        self.tela.blit(self.titulo_fase_texto, (self.titulo_fase_x, self.titulo_fase_y))
        self.tela.blit(self.itens_jogador_texto, (self.itens_jogador_x, self.itens_jogador_y))
        self.tela.blit(self.tempo_texto, (self.tempo_texto_x, self.tempo_texto_y))
        self.tela.blit(self.tempo, (self.tempo_x, self.tempo_y))
        self.tela.blit(self.itens_robo_texto, (self.itens_robo_x, self.itens_robo_y))
        
        pygame.draw.rect(self.tela, self.AMARELO, (self.texto_jogador_x-10, self.texto_jogador_y-10, self.rect_texto_jogador.width+100, self.rect_texto_jogador.height+20), border_radius=20)
        self.tela.blit(self.texto_jogador, (self.texto_jogador_x, self.texto_jogador_y))

        self.desenhar_cartas_jogador()
        self.desenhar_cartas_robo()

        pygame.display.flip()

        if self.pontos_jogador + self.pontos_robo == 5:
            if self.pontos_jogador > self.pontos_robo:
                self.ganhou = True
            else:
                self.perdeu = True
            self.jogando = False


    def desenhar_perdeu(self):

        """Desenha a tela de derrota do jogador. O jogador é informado que perdeu e pode jogar novamente ou voltar para a seleção de fases."""
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                pos_mouse = pygame.mouse.get_pos()
                if self.botao_voltar.collidepoint(pos_mouse):
                    #print("Clicou no Sim!")
                    return "festa junina"
                if self.botao_nao.collidepoint(pos_mouse):
                    # voltar para a seleção de fases
                    #print("Clicou no Não!")
                    return "selecao_fases"
        
        self.tela.blit(self.imagem_fundo, (0, 0))
        pygame.draw.rect(self.tela, self.AMARELO2, self.fundo_rect)

        self.tela.blit(self.titulo_fase_texto, (self.titulo_fase_x, self.titulo_fase_y))
        self.tela.blit(self.itens_jogador_texto, (self.itens_jogador_x, self.itens_jogador_y))
        self.tela.blit(self.tempo_texto, (self.tempo_texto_x, self.tempo_texto_y))
        self.tela.blit(self.tempo, (self.tempo_x, self.tempo_y))
        self.tela.blit(self.itens_robo_texto, (self.itens_robo_x, self.itens_robo_y))

        self.desenhar_cartas_jogador()
        self.desenhar_cartas_robo()

        pygame.draw.rect(self.tela, self.AMARELO2, (400, 100, 780, 520), border_radius=40)
        self.imagem_robo = pygame.image.load("assets/imagens/robo_maior.png")
        self.tela.blit(self.imagem_robo, (450, 200))

        texto_perdeu = self.fonte_maior.render("Você perdeu! :(", True, self.PRETO)
        self.tela.blit(texto_perdeu, (740, 170))
        texto_jogar_novamente = self.fonte_menor.render("Quer jogar novamente?", True, self.PRETO)
        self.tela.blit(texto_jogar_novamente, (760, 300))

        cor_botoes = (242, 104, 104)
        self.botao_voltar = pygame.draw.rect(self.tela, cor_botoes, (810, 400, 100, 50), border_radius=20)
        texto_sim = self.fonte.render("Sim", True, self.PRETO)
        self.tela.blit(texto_sim, (830, 410))

        self.botao_nao = pygame.draw.rect(self.tela, cor_botoes, (1010, 400, 100, 50), border_radius=20)
        texto_nao = self.fonte.render("Não", True, self.PRETO)
        self.tela.blit(texto_nao, (1030, 410))

        pygame.display.flip()
    
    def desenhar_ganhou(self):
        
        """Desenha a tela de vitória do jogador. O jogador é informado que ganhou e pode voltar para a seleção de fases."""
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                pos_mouse = pygame.mouse.get_pos()
                if self.botao_voltar.collidepoint(pos_mouse):
                    # voltar para a seleção de fases
                    #print("Clicou no voltar!")

                    with open("./data/game_data.json", "r") as arquivo:
                        dados = json.load(arquivo)
                        dados["locked"]["natal"] = False

                    with open("./data/game_data.json", "w") as arquivo:
                        json.dump(dados, arquivo, indent=4, ensure_ascii=False)
                    # voltar para a seleção de fases
                    return "selecao_fases"
        
        self.tela.blit(self.imagem_fundo, (0, 0))
        pygame.draw.rect(self.tela, self.AMARELO2, self.fundo_rect)

        self.tela.blit(self.titulo_fase_texto, (self.titulo_fase_x, self.titulo_fase_y))
        self.tela.blit(self.itens_jogador_texto, (self.itens_jogador_x, self.itens_jogador_y))
        self.tela.blit(self.tempo_texto, (self.tempo_texto_x, self.tempo_texto_y))
        self.tela.blit(self.tempo, (self.tempo_x, self.tempo_y))
        self.tela.blit(self.itens_robo_texto, (self.itens_robo_x, self.itens_robo_y))

        self.desenhar_cartas_jogador()
        self.desenhar_cartas_robo()

        pygame.draw.rect(self.tela, self.AMARELO2, (400, 100, 780, 520), border_radius=40)
        self.imagem_robo = pygame.image.load("assets/imagens/robo_maior.png")
        self.tela.blit(self.imagem_robo, (450, 200))

        texto_ganhou = self.fonte_maior.render("Você ganhou! :)", True, self.PRETO)
        self.tela.blit(texto_ganhou, (740, 200))
        texto_voltar = self.fonte_menor.render("Volte para a seleção", True, self.PRETO)
        texto_voltar2 = self.fonte_menor.render("de fases", True, self.PRETO)
        self.tela.blit(texto_voltar, (800, 330))
        self.tela.blit(texto_voltar2, (900, 360))

        cor_botoes = (106, 224, 97)
        self.botao_voltar = pygame.draw.rect(self.tela, cor_botoes, (910, 430, 100, 50), border_radius=20)
        texto_voltar = self.fonte.render("Voltar", True, self.PRETO)
        self.tela.blit(texto_voltar, (920, 440))

        pygame.display.flip()

    def box_text(self, surface, font, x_start, x_end, y_start, text):
        
        """Função auxiliar chamada na função desenhar_narracao, que desenha a tela e o texto de narração.
        Essa função quebra o texto em linhas para que ele caiba na tela. Também desenha o texto na tela"""
        
        x = x_start
        y = y_start
        words = text.split(' ')
        
        line_width = 0
        space_width = font.render(' ', True, self.PRETO).get_width() * 1.1

        for word in words:
            word_t = font.render(word, True, self.PRETO)
            word_width = word_t.get_width()
            
            if line_width + word_width <= x_end - x_start:
                surface.blit(word_t, (x, y))
                x += word_width + space_width
                line_width += word_width + space_width
            else:
                y += word_t.get_height() * 1.25
                x = x_start
                line_width = 0
                surface.blit(word_t, (x, y))
                x += word_width + space_width
                line_width += word_width + space_width
    
    def desenhar_narracao(self):
        
        """Desenha a tela, os textos e as imagens de narração daquela fase. O jogador pode pular a narração
        no botão "Pular", no canto inferior direito da tela."""
        
        if pygame.mixer.get_busy():
            self.musica_de_fundo = pygame.mixer.music.load(self.configuracoes["musicas"]["festa_junina"])
            pygame.mixer.music.set_volume(self.sons["volume_musica"])
            self.narracao = False
            self.jogando = True
            pygame.mixer.music.play(-1)
            return None
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                pos_mouse = pygame.mouse.get_pos()
                if self.botao_pular.collidepoint(pos_mouse):
                    self.musica_de_fundo = pygame.mixer.music.load(self.configuracoes["musicas"]["festa_junina"])
                    pygame.mixer.music.set_volume(self.sons["volume_musica"])
                    self.narracao = False
                    self.jogando = True
                    pygame.mixer.music.play(-1)
                    return None
                elif self.botao_voltar.collidepoint(pos_mouse):
                    return "selecao_fases"

        self.tela.fill(self.PRETO)
        self.tela.blit(self.imagem_fundo, (0, 0))
        pygame.draw.rect(self.tela, self.AMARELO2, self.fundo_rect)

        pygame.draw.rect(self.tela, self.PRETO, self.botao_voltar)
        self.tela.blit(self.imagem_voltar, (10, 10))
        
        self.tela.blit(self.titulo_fase_texto, (self.titulo_fase_x, self.titulo_fase_y))

        y_imagem = 100
        for imagem in self.lista_imagens_narracao:
            self.tela.blit(imagem, (25, y_imagem))
            y_imagem += 200
        
        pygame.draw.rect(self.tela, self.AMARELO2, (350, 50, 880, 620), border_radius=40)
        self.box_text(self.tela, self.fonte_narracao, 700, 1200, 130, self.texto_narracao)

        self.imagem_robo = pygame.image.load("assets/imagens/robo_maior.png")
        self.tela.blit(self.imagem_robo, (350, 200))

        self.botao_pular = pygame.rect.Rect(1100, 600, 100, 50)
        pygame.draw.rect(self.tela, self.cor_botoes, self.botao_pular, border_radius=20)
        texto_pular = self.fonte.render("Pular", True, self.PRETO)
        self.tela.blit(texto_pular, (1120, 615))
        
        pygame.display.flip()

    def executar(self):
        
        """Função principal que chama as outras funções de desenho e controle do jogo. As variáveis booleanas
        self.narracao, self.jogando, self.ganhou e self.perdeu controlam o que é desenhado na tela."""
        
        while True:
            
            if self.narracao:
                retorno = self.desenhar_narracao()
            
            if self.jogando:
                retorno = self.desenhar_tela()

            if self.ganhou:
                retorno = self.desenhar_ganhou()
            
            if self.perdeu:
                retorno = self.desenhar_perdeu()
            
            if retorno != None:
                pygame.mixer.music.stop()
                if retorno == "selecao_fases":
                    self.musica_de_fundo = pygame.mixer.music.load("./assets/sons/musica_fundo.wav")
                    pygame.mixer.music.play(-1)
                return retorno
