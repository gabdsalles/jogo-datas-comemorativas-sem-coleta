import random
import pygame
from pygame.locals import *
from collections import deque
import sys, json, copy
import scripts.domino.ia_domino as ia

from scripts.domino.pecas import Pecas
from scripts.domino.posicoes_pecas import posicoes_retangulos_jogador, Posicao, posicoes_borda_esquerda, posicoes_borda_direita, posicoes_imagem_esquerda, posicoes_imagem_direita, posicoes_retangulo_esquerda, posicoes_retangulo_direita

LARGURA = 1280
ALTURA = 720
FPS = 60
QTD_INICIAL_PECAS = 6
POSICAO_INICIAL = Posicao((760, 177, 70, 5), (760, 115, 70, 130), (760, 115), (760, 180), "dupla")

class TelaDomino:

    """A tela do dominó tem como data comemorativa a Páscoa. O jogador joga contra um robô e o objetivo é ficar com zero
    peças na mão o mais rápido possível, antes do robô. O sistema de compras é automático, tanto para o jogador quanto para
    o robô. O jogador pode clicar nas peças para jogar, e o robô joga automaticamente. O jogo termina quando um dos jogadores
    fica sem peças. O jogador pode voltar à tela inicial a qualquer momento. O tempo é contado e exibido na tela, assim como
    a quantidade de peças de cada jogador."""
    
    def __init__(self, largura, altura):

        """Inicializa a tela e seus componentes. Carrega as configurações do arquivo game_data.json.
        Carrega também as imagens, músicas e estruturas de dados pra armazenar as peças do tabuleiro."""
        
        pygame.init()
        pygame.mixer.init()

        with open("./data/game_data.json", "r", encoding="utf-8") as arquivo:
            self.configuracoes = json.load(arquivo)

        self.sons = self.configuracoes["sons"]
        self.texto_narracao = self.configuracoes["textos_fases"]["pascoa"]
        
        pygame.mixer.music.set_volume(self.sons["volume_jogador"])
        self.musica_de_fundo = pygame.mixer.music.load(self.configuracoes["narracoes"]["pascoa"])
        pygame.mixer.music.play()

        self.som_pontuacao_jogador = pygame.mixer.Sound('./assets/sons/ponto_jogador.wav')
        self.som_pontuacao_jogador.set_volume(self.sons["volume_jogador"])
        self.som_compras = pygame.mixer.Sound('./assets/sons/ponto_robo.wav')

        self.narracao = True
        self.jogando = False
        self.perdeu = False
        self.ganhou = False

        self.LARGURA = largura
        self.ALTURA = altura
        self.tela = pygame.display.set_mode((self.LARGURA, self.ALTURA))
        pygame.display.set_caption('Dominó')
        self.relogio = pygame.time.Clock()

        self.imagem_fundo = pygame.image.load("assets/imagens/pascoa_fundo.png").convert()
        self.lista_imagens_narracao = [pygame.image.load("assets/imagens/pascoa_narracao/pascoa1.png"), pygame.image.load("assets/imagens/pascoa_narracao/pascoa2.png"),
                                       pygame.image.load("assets/imagens/pascoa_narracao/pascoa3.png")]

        self.BRANCO = (255, 255, 255)
        self.PRETO = (0, 0, 0)
        self.AMARELO = (255, 255, 0)
        self.VERMELHO = (255, 0, 0)
        self.AZUL_FUNDO = (0, 61, 80)
        self.AMARELO2 = (233, 255, 101)
        self.AZUL_CLARO = (175, 217, 232)
        self.cor_botoes = (106, 224, 97)

        self.fonte = pygame.font.Font(None, 36)
        self.fonte_maior = pygame.font.Font('assets/fonts/archivo_black.ttf', 48)
        self.fonte_menor = pygame.font.Font('assets/fonts/archivo_black.ttf', 30)
        self.fonte_narracao = pygame.font.SysFont("calibri", 30, bold=True, italic=True)
        self.fundo_rect = pygame.rect.Rect(0, 0, 280, 720)
        self.tabuleiro_rect = pygame.rect.Rect(310, 100, 940, 440)

        self.lista_pecas = Pecas().lista_pecas
        self.pecas_jogador = []
        self.pecas_robo = []
        self.pecas_tabuleiro = deque()
        self.cores = Pecas().cores

        self.lista_retangulos_tabuleiro = deque()
        self.lista_retangulos_tabuleiro.append(POSICAO_INICIAL.posicao_retangulo)
        self.lista_imagens_tabuleiro = deque()
        self.lista_imagens_tabuleiro.append(POSICAO_INICIAL.posicao_imagem1)
        self.lista_imagens_tabuleiro.append(POSICAO_INICIAL.posicao_imagem2)
        self.lista_bordas_tabuleiro = deque()
        self.lista_bordas_tabuleiro.append(POSICAO_INICIAL.posicao_borda)
        self.nomes_pecas_tabuleiro = deque()

        self.posicoes_retangulos_jogador = copy.deepcopy(posicoes_retangulos_jogador)
        self.posicoes_borda_esquerda = copy.deepcopy(posicoes_borda_esquerda)
        self.posicoes_borda_direita = copy.deepcopy(posicoes_borda_direita)
        self.posicoes_imagem_esquerda = copy.deepcopy(posicoes_imagem_esquerda)
        self.posicoes_imagem_direita = copy.deepcopy(posicoes_imagem_direita)
        self.posicoes_retangulo_esquerda = copy.deepcopy(posicoes_retangulo_esquerda)
        self.posicoes_retangulo_direita = copy.deepcopy(posicoes_retangulo_direita)

        self.titulo_fase_texto = self.fonte_maior.render("Páscoa", True, self.PRETO)
        self.titulo_fase_x = 70
        self.titulo_fase_y = 20

        self.tempo_texto = self.fonte.render("Tempo: ", True, self.PRETO)
        self.tempo_texto_x = 10
        self.tempo_texto_y = 675

        self.tempo = self.fonte.render("00:00", True, self.PRETO)
        self.tempo_x = 100
        self.tempo_y = 675

        self.tempo_decorrido = 0

        self.imagem_voltar = pygame.image.load("assets/imagens/voltar.png")
        self.botao_voltar = pygame.rect.Rect(10, 10, 30, 30)

        self.texto_jogador = self.fonte.render("É sua vez de jogar!", True, self.PRETO)
        self.texto_jogador_x = 15
        self.texto_jogador_y = 600
        self.rect_texto_jogador = self.texto_jogador.get_rect()

        self.qtd_pecas_jogador = QTD_INICIAL_PECAS
        self.qtd_pecas_robo = QTD_INICIAL_PECAS

        self.itens_jogador_texto = self.fonte.render(f"Peças do jogador: {self.qtd_pecas_jogador}", True, self.PRETO)
        self.itens_jogador_x = 20
        self.itens_jogador_y = 100

        self.itens_robo_texto = self.fonte.render(f"Peças do robô: {self.qtd_pecas_robo}", True, self.PRETO)
        self.itens_robo_x = 45
        self.itens_robo_y = 550

        self.lista_rect_jogador = []

        for i in range(QTD_INICIAL_PECAS):
            peca = random.choice(self.lista_pecas)
            self.pecas_jogador.append(peca)
            self.lista_pecas.remove(peca)

            peca = random.choice(self.lista_pecas)
            self.pecas_robo.append(peca)
            self.lista_pecas.remove(peca)
        
        self.vez_jogador = False
        self.vez_robo = False

        self.compras_texto = self.fonte.render(f"Pilha de compras: {len(self.lista_pecas)} ", True, self.PRETO)
        self.compras_texto_x = 20
        self.compras_texto_y = 150

        self.fundo_carta = pygame.image.load("assets/imagens/pascoa/fundo_carta.png")
        self.fundo_carta = pygame.transform.scale(self.fundo_carta, (167, 250))

        self.tempo_jogada = None
        
        self.qtd_jogadas_jogador = 0
        self.qtd_jogadas_robo = 0

        self.esquerda_tabuleiro = None
        self.direita_tabuleiro = None
        self.pecas_pra_esquerda = 0
        self.pecas_pra_direita = 0

    def desenhar_grid(self, tela, largura_tela, altura_tela, grid_largura, grid_altura):

        """Função auxiliar, não é desenhada na versão final do jogo. Desenha um grid na tela para facilitar
         a disposição dos componentes da tela. O grid é desenhado com linhas horizontais e verticais."""
        
        # Desenhe as linhas horizontais do grid
        for y in range(0, altura_tela, grid_altura):
            pygame.draw.line(tela, (100, 100, 100), (0, y), (largura_tela, y))

        # Desenhe as linhas verticais do grid
        for x in range(0, largura_tela, grid_largura):
            pygame.draw.line(tela, (100, 100, 100), (x, 0), (x, altura_tela))
    
    def checar_colisao(self, posicao_mouse):
            
        """Checa se o mouse colidiu com alguma peça do jogador. Retorna o índice da peça clicada, ou None."""
        
        for i, rect in enumerate(self.lista_rect_jogador):
            if rect.collidepoint(posicao_mouse):
                return i
                        
        return None
    
    def checar_jogada_jogador(self, peca_clicada):

        """Checa se a peça clicada pode ser jogada no tabuleiro. Se sim, a peça é jogada e removida da mão do jogador.
        Se não, a função retorna None. A função também atualiza a vez do jogador e do robô, e atualiza a quantidade de peças.
        Primeiro checa se a peça clicada pode ser jogada à esquerda do tabuleiro. Se não, checa se pode ser jogada à direita."""
        peca = self.pecas_jogador[peca_clicada]
        # print(peca.nome1, peca.nome2)
        if peca.nome1 == self.esquerda_tabuleiro or peca.nome2 == self.esquerda_tabuleiro:
            
            if peca.nome1 == self.esquerda_tabuleiro:
                self.nomes_pecas_tabuleiro.appendleft(peca.nome1)
                self.esquerda_tabuleiro = peca.nome2
                self.nomes_pecas_tabuleiro.appendleft(peca.nome2)
                # print("nome1")
            elif peca.nome2 == self.esquerda_tabuleiro:
                self.nomes_pecas_tabuleiro.appendleft(peca.nome2)
                self.esquerda_tabuleiro = peca.nome1
                self.nomes_pecas_tabuleiro.appendleft(peca.nome1)
                # print("nome2")
            
            self.pecas_tabuleiro.appendleft(peca)
            self.pecas_jogador.remove(peca)
            self.som_pontuacao_jogador.play()
            self.qtd_pecas_jogador -= 1
            self.vez_jogador = False
            self.vez_robo = True
            self.texto_jogador = self.fonte.render("É a vez do robô jogar!", True, self.PRETO)
            self.rect_texto_jogador = self.texto_jogador.get_rect()
            self.itens_jogador_texto = self.fonte.render(f"Peças do jogador: {self.qtd_pecas_jogador}", True, self.PRETO)
            self.qtd_jogadas_jogador += 1
            self.pecas_pra_esquerda += 1
            self.incluir_peca_tabuleiro(peca, "esquerda")
        
        elif peca.nome1 == self.direita_tabuleiro or peca.nome2 == self.direita_tabuleiro:
            
            if peca.nome1 == self.direita_tabuleiro:
                self.nomes_pecas_tabuleiro.append(peca.nome1)
                self.direita_tabuleiro = peca.nome2
                self.nomes_pecas_tabuleiro.append(peca.nome2)
            else:
                self.nomes_pecas_tabuleiro.append(peca.nome2)
                self.direita_tabuleiro = peca.nome1
                self.nomes_pecas_tabuleiro.append(peca.nome1)
            
            self.pecas_tabuleiro.append(peca)
            self.pecas_jogador.remove(peca)
            self.qtd_pecas_jogador -= 1
            self.som_pontuacao_jogador.play()
            self.vez_jogador = False
            self.vez_robo = True
            self.texto_jogador = self.fonte.render("É a vez do robô jogar!", True, self.PRETO)
            self.rect_texto_jogador = self.texto_jogador.get_rect()
            self.itens_jogador_texto = self.fonte.render(f"Peças do jogador: {self.qtd_pecas_jogador}", True, self.PRETO)
            self.qtd_jogadas_jogador += 1
            self.pecas_pra_direita += 1
            self.incluir_peca_tabuleiro(peca, "direita")   
    
    def limpar_tabuleiro(self, peca):

        """Essa função é chamada quando os espaços para as peças do tabuleiro acabam.
        Ela limpa o tabuleiro, devolve as peças do tabuleiro para a pilha de compras e continua o jogo."""
        
        self.posicoes_retangulo_esquerda = copy.deepcopy(posicoes_retangulo_esquerda)
        self.posicoes_retangulo_direita = copy.deepcopy(posicoes_retangulo_direita)
        self.posicoes_imagem_esquerda = copy.deepcopy(posicoes_imagem_esquerda)
        self.posicoes_imagem_direita = copy.deepcopy(posicoes_imagem_direita)
        self.posicoes_borda_esquerda = copy.deepcopy(posicoes_borda_esquerda)
        self.posicoes_borda_direita = copy.deepcopy(posicoes_borda_direita)
        self.lista_retangulos_tabuleiro = deque()
        self.lista_retangulos_tabuleiro.append(POSICAO_INICIAL.posicao_retangulo)
        self.lista_imagens_tabuleiro = deque()
        self.lista_imagens_tabuleiro.append(POSICAO_INICIAL.posicao_imagem1)
        self.lista_imagens_tabuleiro.append(POSICAO_INICIAL.posicao_imagem2)
        self.lista_bordas_tabuleiro = deque()
        self.lista_bordas_tabuleiro.append(POSICAO_INICIAL.posicao_borda)
        self.nomes_pecas_tabuleiro = deque()
        self.esquerda_tabuleiro = peca.nome1
        self.direita_tabuleiro = peca.nome2
        self.nomes_pecas_tabuleiro.append(peca.nome1)
        self.nomes_pecas_tabuleiro.append(peca.nome2)
        self.lista_pecas.extend(self.pecas_tabuleiro)
        self.lista_pecas.remove(peca)
        self.pecas_tabuleiro = deque()
        self.compras_texto = self.fonte.render(f"Pilha de compras: {len(self.lista_pecas)} ", True, self.PRETO)

    def incluir_peca_tabuleiro(self, peca, posicao):

        """Se o espaço para as peças do tabuleiro acabou, essa função é chamada para limpar o tabuleiro, chamando
        a função self.limpar_tabuleiro acima."""
        if self.pecas_pra_esquerda == 9 or self.pecas_pra_direita == 9: #acabou as posições
            self.limpar_tabuleiro(peca)
            self.pecas_pra_esquerda = 0
            self.pecas_pra_direita = 0
            return None
        
        if posicao == "esquerda":

            self.lista_retangulos_tabuleiro.appendleft(self.posicoes_retangulo_esquerda[0])

            self.posicoes_retangulo_esquerda.pop(0)

            self.lista_imagens_tabuleiro.appendleft(self.posicoes_imagem_esquerda[0])
            self.lista_imagens_tabuleiro.appendleft(self.posicoes_imagem_esquerda[1])
            self.posicoes_imagem_esquerda.pop(0)
            self.posicoes_imagem_esquerda.pop(0)

            self.lista_bordas_tabuleiro.appendleft(self.posicoes_borda_esquerda[0])
            self.posicoes_borda_esquerda.pop(0)

        elif posicao == "direita":
            self.lista_retangulos_tabuleiro.append(self.posicoes_retangulo_direita[0])
            self.posicoes_retangulo_direita.pop(0)

            self.lista_imagens_tabuleiro.append(self.posicoes_imagem_direita[0])
            self.lista_imagens_tabuleiro.append(self.posicoes_imagem_direita[1])
            self.posicoes_imagem_direita.pop(0)
            self.posicoes_imagem_direita.pop(0)

            self.lista_bordas_tabuleiro.append(self.posicoes_borda_direita[0])
            self.posicoes_borda_direita.pop(0)
    
    def desenhar_pecas_jogador(self, tela, pecas_jogador):

        """A partir da lista de peças do jogador, desenha-se as bordas das peças e as duas imagens de cada peça.
        A posição das peças depende da quantidade de peças do jogador: essa posição é definida no dicionário disponível em posicoes_pecas.py."""
        
        self.lista_rect_jogador = []
        
        # desenhar retangulos
        for i in range(self.qtd_pecas_jogador):
            
            rect_peca = pygame.rect.Rect(posicoes_retangulos_jogador[self.qtd_pecas_jogador][i])
            pygame.draw.rect(tela, self.AZUL_CLARO, posicoes_retangulos_jogador[self.qtd_pecas_jogador][i])
        
        #desenhar bordas
            pygame.draw.rect(tela, self.AMARELO, posicoes_retangulos_jogador[self.qtd_pecas_jogador][i], 5)
            pygame.draw.rect(tela, self.BRANCO, (posicoes_retangulos_jogador[self.qtd_pecas_jogador][i][0], posicoes_retangulos_jogador[self.qtd_pecas_jogador][i][1] + 90, 90, 5), 5)

        # desenhar imagem 1 das peças
            imagem1 = pygame.image.load(pecas_jogador[i].imagem1)
            pygame.draw.rect(tela, pecas_jogador[i].cor1, (posicoes_retangulos_jogador[self.qtd_pecas_jogador][i][0] + 5, posicoes_retangulos_jogador[self.qtd_pecas_jogador][i][1] + 5, 80, 85))
            tela.blit(imagem1, (posicoes_retangulos_jogador[self.qtd_pecas_jogador][i][0] + 10, posicoes_retangulos_jogador[self.qtd_pecas_jogador][i][1] + 10))
        # desenhar imagem 2 das peças
            imagem2 = pygame.image.load(pecas_jogador[i].imagem2)
            pygame.draw.rect(tela, pecas_jogador[i].cor2, (posicoes_retangulos_jogador[self.qtd_pecas_jogador][i][0] + 5, posicoes_retangulos_jogador[self.qtd_pecas_jogador][i][1] + 95, 80, 85))
            tela.blit(imagem2, (posicoes_retangulos_jogador[self.qtd_pecas_jogador][i][0] + 10, posicoes_retangulos_jogador[self.qtd_pecas_jogador][i][1] + 100))

            self.lista_rect_jogador.append(rect_peca)
    
    def desenhar_pecas_robo(self, tela):

        """As peças do robô são desenhadas de forma similar às peças do jogador, mas em posições diferentes, na parte
        de cima da tela. A posição das peças depende da quantidade de peças do robô: essa posição é definida no dicionário
        disponível em posicoes_pecas.py. Aqui não desenhamos as imagens das peças, apenas as bordas."""
        
        for i in range(self.qtd_pecas_robo):
            pygame.draw.rect(tela, self.AZUL_CLARO, (posicoes_retangulos_jogador[self.qtd_pecas_robo][i][0], 0, posicoes_retangulos_jogador[self.qtd_pecas_robo][i][2], 90))
            pygame.draw.rect(tela, self.AMARELO, (posicoes_retangulos_jogador[self.qtd_pecas_robo][i][0], 0, posicoes_retangulos_jogador[self.qtd_pecas_robo][i][2], 90), 5)

    def desenhar_tabuleiro(self, tela):

        """Desenha as peças do tabuleiro, as bordas e os retângulos que representam as posições das peças do tabuleiro."""
        
        for i, nome in enumerate(self.nomes_pecas_tabuleiro):
            cor = self.cores[nome.split()[0]]
            pygame.draw.rect(tela, cor, (self.lista_imagens_tabuleiro[i][0], self.lista_imagens_tabuleiro[i][1], 65, 65))
            imagem = pygame.image.load(f"assets/imagens/pascoa_horizontal/{nome}.png")
            imagem = pygame.transform.scale(imagem, (60, 60))
            tela.blit(imagem, self.lista_imagens_tabuleiro[i])

        for rect in self.lista_bordas_tabuleiro:
            pygame.draw.rect(tela, self.BRANCO, rect, 5)

        for rect in self.lista_retangulos_tabuleiro:
            pygame.draw.rect(tela, self.AMARELO, rect, 5)

    def checar_compra(self, pecas):

        """Checa se o jogador ou o robô precisam comprar mais cartas. Se sim, a função retorna True."""

        esquerda = sum(1 for peca in pecas if peca.nome1 == self.esquerda_tabuleiro or peca.nome2 == self.esquerda_tabuleiro)
        direita = sum(1 for peca in pecas if peca.nome1 == self.direita_tabuleiro or peca.nome2 == self.direita_tabuleiro)
        # print("Possibilidades à esquerda: ", esquerda)
        # print("Possibilidades à direita: ", direita)
        if esquerda == 0 and direita == 0:
            return True
        else:
            return False
        
    def comprar_peca(self, pecas, quem_joga):
            
            """Compra uma peça para o jogador ou para o robô. A peça é retirada da pilha de compras e adicionada à mão.
            A variável quem_joga tem duas possibilidades: jogador ou robô."""
            
            if self.lista_pecas == []: # se não tiver mais peças pra comprar
                peca = random.choice(self.pecas_tabuleiro)
                self.limpar_tabuleiro(peca)
            
            peca = random.choice(self.lista_pecas)
            pecas.append(peca)
            self.lista_pecas.remove(peca)
            self.compras_texto = self.fonte.render(f"Pilha de compras: {len(self.lista_pecas)} ", True, self.PRETO)

            if quem_joga == "jogador":
                self.qtd_pecas_jogador += 1
                #self.som_compras.play()
                self.itens_jogador_texto = self.fonte.render(f"Peças do jogador: {self.qtd_pecas_jogador}", True, self.PRETO)
                self.vez_jogador = False
                self.vez_robo = True
                self.texto_jogador = self.fonte.render("É a vez do robô jogar!", True, self.PRETO)

            elif quem_joga == "robo":
                self.qtd_pecas_robo += 1
                self.itens_robo_texto = self.fonte.render(f"Peças do robô: {self.qtd_pecas_robo}", True, self.PRETO)
                self.vez_jogador = True
                self.vez_robo = False
                self.texto_jogador = self.fonte.render("É a sua vez de jogar!", True, self.PRETO)
            
            # print(f"{quem_joga} comprou uma peça!")

    def escolher_quem_joga_primeiro(self):

        """Esta função é chamada no início do jogo, após a distribuição das peças. O jogo vai dar a vez
        para quem tem mais peças duplas. O jogo vai tirar uma das duplas de quem tem a vez para ser a
        peça inicial do tabuleiro. Se ninguém tiver duplas, o jogo escolhe uma peça aleatória para ser a
        inicial e escolhe a vez também aleatoriamente."""
        
        duplas_jogador = sum(1 for peca in self.pecas_jogador if peca.tipo == "dupla")
        duplas_robo = sum(1 for peca in self.pecas_robo if peca.tipo == "dupla")

        if duplas_jogador == duplas_robo == 0:
            duplas_tabuleiro = [peca for peca in self.lista_pecas if peca.tipo == "dupla"]
            peca_inicial = random.choice(duplas_tabuleiro)
            peca_inicial.dono = None
            self.nomes_pecas_tabuleiro.append(peca_inicial.nome1)
            self.nomes_pecas_tabuleiro.append(peca_inicial.nome2)
            self.pecas_tabuleiro.append(peca_inicial)
            self.lista_pecas.remove(peca_inicial)
        
        if duplas_jogador >= duplas_robo and duplas_jogador > 0:
            self.texto_jogador = self.fonte.render("É a vez do robô jogar!", True, self.PRETO)
            self.rect_texto_jogador = self.texto_jogador.get_rect()
            peca_inicial = random.choice([peca for peca in self.pecas_jogador if peca.tipo == "dupla"])
            peca_inicial.dono = None
            self.pecas_tabuleiro.append(peca_inicial)
            self.pecas_jogador.remove(peca_inicial)
            self.esquerda_tabuleiro = peca_inicial.nome1
            self.direita_tabuleiro = peca_inicial.nome2
            self.nomes_pecas_tabuleiro.append(peca_inicial.nome1)
            self.nomes_pecas_tabuleiro.append(peca_inicial.nome2)
            self.qtd_pecas_jogador -= 1
            self.itens_jogador_texto = self.fonte.render(f"Peças do jogador: {self.qtd_pecas_jogador}", True, self.PRETO)
            self.vez_robo = True
            self.vez_jogador = False
        
        else:
            self.texto_jogador = self.fonte.render("É a sua vez de jogar!", True, self.PRETO)
            self.rect_texto_jogador = self.texto_jogador.get_rect()
            peca_inicial = random.choice([peca for peca in self.pecas_robo if peca.tipo == "dupla"])
            peca_inicial.dono = None
            peca_inicial.posicao = POSICAO_INICIAL
            self.pecas_tabuleiro.append(peca_inicial)
            self.pecas_robo.remove(peca_inicial)
            self.esquerda_tabuleiro = peca_inicial.nome1
            self.direita_tabuleiro = peca_inicial.nome2
            self.nomes_pecas_tabuleiro.append(peca_inicial.nome1)
            self.nomes_pecas_tabuleiro.append(peca_inicial.nome2)
            self.qtd_pecas_robo -= 1
            self.itens_robo_texto = self.fonte.render(f"Peças do robô: {self.qtd_pecas_robo}", True, self.PRETO)
            self.vez_jogador = True
            self.vez_robo = False
        
        # print(duplas_jogador, duplas_robo)
    
    def escolher_peca_robo(self):
        
        """Função que escolhe a peça que o robô vai jogar. A escolha é feita baseada nas peças disponíveis,
        na função ia.escolher_peca. A peça escolhida é jogada no tabuleiro e removida da mão do robô"""

        peca = ia.escolher_peca(self.pecas_robo, self.esquerda_tabuleiro, self.direita_tabuleiro, self.pecas_tabuleiro)
        # print(peca.nome1, peca.nome2)
        if peca.nome1 == self.esquerda_tabuleiro or peca.nome2 == self.esquerda_tabuleiro:
                
                if peca.nome1 == self.esquerda_tabuleiro:
                    self.nomes_pecas_tabuleiro.appendleft(peca.nome1)
                    self.esquerda_tabuleiro = peca.nome2
                    self.nomes_pecas_tabuleiro.appendleft(peca.nome2)
                elif peca.nome2 == self.esquerda_tabuleiro:
                    self.nomes_pecas_tabuleiro.appendleft(peca.nome2)
                    self.esquerda_tabuleiro = peca.nome1
                    self.nomes_pecas_tabuleiro.appendleft(peca.nome1)
                
                self.pecas_tabuleiro.appendleft(peca)
                self.pecas_robo.remove(peca)
                self.qtd_pecas_robo -= 1
                print("jogada do robô...", peca.nome1, peca.nome2)
                self.vez_jogador = True
                self.vez_robo = False
                self.texto_jogador = self.fonte.render("É a sua vez de jogar!", True, self.PRETO)
                self.rect_texto_jogador = self.texto_jogador.get_rect()
                self.itens_robo_texto = self.fonte.render(f"Peças do robô: {self.qtd_pecas_robo}", True, self.PRETO)
                self.qtd_jogadas_robo += 1
                self.pecas_pra_esquerda += 1
                self.incluir_peca_tabuleiro(peca, "esquerda")
        
        elif peca.nome1 == self.direita_tabuleiro or peca.nome2 == self.direita_tabuleiro:

            if peca.nome1 == self.direita_tabuleiro:
                self.nomes_pecas_tabuleiro.append(peca.nome1)
                self.direita_tabuleiro = peca.nome2
                self.nomes_pecas_tabuleiro.append(peca.nome2)
            
            elif peca.nome2 == self.direita_tabuleiro:
                self.nomes_pecas_tabuleiro.append(peca.nome2)
                self.direita_tabuleiro = peca.nome1
                self.nomes_pecas_tabuleiro.append(peca.nome1)
            
            self.pecas_tabuleiro.append(peca)
            self.pecas_robo.remove(peca)
            self.qtd_pecas_robo -= 1
            self.vez_jogador = True
            self.vez_robo = False
            self.texto_jogador = self.fonte.render("É a sua vez de jogar!", True, self.PRETO)
            self.rect_texto_jogador = self.texto_jogador.get_rect()
            self.itens_robo_texto = self.fonte.render(f"Peças do robô: {self.qtd_pecas_robo}", True, self.PRETO)
            self.qtd_jogadas_robo += 1
            self.pecas_pra_direita += 1
            self.incluir_peca_tabuleiro(peca, "direita")
    
    def desenhar_perdeu(self):
        
        """Se o jogador perdeu o jogo, essa função é chamada. Ela desenha uma tela de game over e dá a opção
        de voltar para a tela de seleção de fases ou jogar a fase novamente."""
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                pos_mouse = pygame.mouse.get_pos()
                if self.botao_voltar.collidepoint(pos_mouse):
                    #limpar variáveis de tempo, pontuação, etc e recomeçar o jogo
                    # print("Clicou no Sim!")
                    return "pascoa"
                if self.botao_nao.collidepoint(pos_mouse):
                    # voltar para a seleção de fases
                    # print("Clicou no Não!")
                    return "selecao_fases"

        self.tela.fill(self.PRETO)
        self.tela.blit(self.imagem_fundo, (0, 0))
        pygame.draw.rect(self.tela, self.AMARELO2, self.fundo_rect)

        self.tela.blit(self.titulo_fase_texto, (self.titulo_fase_x, self.titulo_fase_y))
        self.tela.blit(self.itens_jogador_texto, (self.itens_jogador_x, self.itens_jogador_y))
        self.tela.blit(self.compras_texto, (self.compras_texto_x, self.compras_texto_y))
        self.tela.blit(self.tempo_texto, (self.tempo_texto_x, self.tempo_texto_y))
        self.tela.blit(self.tempo, (self.tempo_x, self.tempo_y))
        self.tela.blit(self.itens_robo_texto, (self.itens_robo_x, self.itens_robo_y))
        pygame.draw.rect(self.tela, self.AZUL_FUNDO, (40, 220, 187, 270))
        self.tela.blit(self.fundo_carta, (50, 230), (0, 0, 200, 300))

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

        """Se o jogador ganhou o jogo, essa função é chamada. Ela desenha uma tela de "você ganhou!" 
        e dá a opção de voltar para a tela de seleção de fases."""
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                pos_mouse = pygame.mouse.get_pos()
                if self.botao_voltar.collidepoint(pos_mouse):
                    # print("Clicou no voltar!")
                    # alterar o locked do json pra segunda fase == False

                    with open("./data/game_data.json", "r") as arquivo:
                        dados = json.load(arquivo)
                        dados["locked"]["festa_junina"] = False

                    with open("./data/game_data.json", "w") as arquivo:
                        json.dump(dados, arquivo, indent=4, ensure_ascii=False)
                    # voltar para a seleção de fases
                    return "selecao_fases"

        self.tela.fill(self.PRETO)
        self.tela.blit(self.imagem_fundo, (0, 0))
        pygame.draw.rect(self.tela, self.AMARELO2, self.fundo_rect)

        self.tela.blit(self.titulo_fase_texto, (self.titulo_fase_x, self.titulo_fase_y))
        self.tela.blit(self.itens_jogador_texto, (self.itens_jogador_x, self.itens_jogador_y))
        self.tela.blit(self.compras_texto, (self.compras_texto_x, self.compras_texto_y))
        self.tela.blit(self.tempo_texto, (self.tempo_texto_x, self.tempo_texto_y))
        self.tela.blit(self.tempo, (self.tempo_x, self.tempo_y))
        self.tela.blit(self.itens_robo_texto, (self.itens_robo_x, self.itens_robo_y))
        pygame.draw.rect(self.tela, self.AZUL_FUNDO, (40, 220, 187, 270))
        self.tela.blit(self.fundo_carta, (50, 230), (0, 0, 200, 300))

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
    
    def desenhar_tela(self):

        """Desenha a tela da fase do dominó."""
        self.relogio.tick(FPS)

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                posicao_mouse = pygame.mouse.get_pos()

                if self.botao_voltar.collidepoint(posicao_mouse):
                    return "selecao_fases"

                peca_clicada = self.checar_colisao(posicao_mouse)
                if peca_clicada is not None and self.vez_jogador:
                    self.checar_jogada_jogador(peca_clicada)

            if self.vez_jogador and self.qtd_pecas_jogador > 0:
                precisa_comprar = self.checar_compra(self.pecas_jogador)
                if precisa_comprar:
                    self.comprar_peca(self.pecas_jogador, "jogador")

            if self.vez_robo and self.qtd_pecas_robo > 0:
                precisa_comprar = self.checar_compra(self.pecas_robo)
                if precisa_comprar:
                    self.comprar_peca(self.pecas_robo, "robo")
                else:
                    self.escolher_peca_robo()

        self.tela.fill(self.PRETO)
        self.tela.blit(self.imagem_fundo, (0, 0))
        pygame.draw.rect(self.tela, self.AMARELO2, self.fundo_rect)
        pygame.draw.rect(self.tela, self.AZUL_FUNDO, self.tabuleiro_rect)

        self.tempo_decorrido += 1
        segundos = self.tempo_decorrido // 60
        minutos = segundos // 60
        tempo_formatado = f"{minutos:02}:{segundos % 60:02}"

        self.tempo = self.fonte.render(tempo_formatado, True, self.PRETO)

        pygame.draw.rect(self.tela, self.PRETO, self.botao_voltar)
        self.tela.blit(self.imagem_voltar, (10, 10))
        self.tela.blit(self.titulo_fase_texto, (self.titulo_fase_x, self.titulo_fase_y))
        self.tela.blit(self.itens_jogador_texto, (self.itens_jogador_x, self.itens_jogador_y))
        self.tela.blit(self.compras_texto, (self.compras_texto_x, self.compras_texto_y))
        self.tela.blit(self.tempo_texto, (self.tempo_texto_x, self.tempo_texto_y))
        self.tela.blit(self.tempo, (self.tempo_x, self.tempo_y))
        self.tela.blit(self.itens_robo_texto, (self.itens_robo_x, self.itens_robo_y))
        pygame.draw.rect(self.tela, self.AZUL_FUNDO, (40, 220, 187, 270))
        self.tela.blit(self.fundo_carta, (50, 230), (0, 0, 200, 300))
        
        pygame.draw.rect(self.tela, self.AMARELO, (self.texto_jogador_x-10, self.texto_jogador_y-10, self.rect_texto_jogador.width+20, self.rect_texto_jogador.height+20), border_radius=20)
        self.tela.blit(self.texto_jogador, (self.texto_jogador_x, self.texto_jogador_y))

        self.desenhar_pecas_jogador(self.tela, self.pecas_jogador)
        self.desenhar_pecas_robo(self.tela)

        if self.vez_jogador == False and self.vez_robo == False:
            self.escolher_quem_joga_primeiro()

        self.desenhar_tabuleiro(self.tela)

        # self.desenhar_grid(self.tela, self.LARGURA, self.ALTURA, 50, 100)

        pygame.display.flip()

        if self.qtd_pecas_jogador == 0 and self.jogando == True:
            self.ganhou = True
            self.jogando = False
        
        if self.qtd_pecas_robo == 0 and self.jogando == True:
            self.perdeu = True
            self.jogando = False

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
            self.musica_de_fundo = pygame.mixer.music.load(self.configuracoes["musicas"]["pascoa"])
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
                    self.narracao = False
                    self.jogando = True
                    self.musica_de_fundo = pygame.mixer.music.load(self.configuracoes["musicas"]["pascoa"])
                    pygame.mixer.music.set_volume(self.sons["volume_musica"])
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
            self.tela.blit(imagem, (15, y_imagem))
            y_imagem += 200
        
        pygame.draw.rect(self.tela, self.AMARELO2, (350, 50, 880, 620), border_radius=40)
        self.box_text(self.tela, self.fonte_narracao, 700, 1200, 150, self.texto_narracao)

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

# tela = TelaDomino(1280, 720)
# tela.executar()