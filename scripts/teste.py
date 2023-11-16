import pygame

# Dimensões do tabuleiro
largura_tabuleiro = 600
altura_tabuleiro = 500

# Número de colunas e linhas para as cartas
num_colunas = 5
num_linhas = 2

# Calcula as dimensões de cada célula
largura_celula = largura_tabuleiro // num_colunas
altura_celula = altura_tabuleiro // num_linhas

# Lista para armazenar as posições das cartas
posicoes_cartas = []

# Loop para gerar as posições das cartas
for linha in range(num_linhas):
    for coluna in range(num_colunas):
        x = coluna * largura_celula
        y = linha * altura_celula
        posicoes_cartas.append((x+600, y+100))

# Exibe as posições das cartas
print("Posições das cartas:")
for posicao in posicoes_cartas:
    print(posicao)
