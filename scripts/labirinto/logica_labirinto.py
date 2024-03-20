from pygame.locals import *

BRANCO = (255, 255, 255)
    
def pegar_coordenadas_robo(lista_rect): #coordenadas: x = 1140, y = 625

    """Essa função recebe uma lista de retângulos e cores e retorna as coordenadas do robô em termos de matriz. A função percorre a lista
    de retângulos e cores e retorna as coordenadas do robô, que é o primeiro retângulo branco que a função encontra. Se a função não
    encontrar nenhum retângulo branco, ela retorna None."""

    for retangulo, cor in reversed(lista_rect):
        if cor == BRANCO:
            x, y, _, _ = retangulo
            return x, y
    
    return None

def pegar_coordenadas_personagem(lista_rect): #x = 480, y = 65

    """Funciona da mesma forma que a função pegar_coordenadas_robo, mas retorna as coordenadas do personagem em termos de matriz."""

    for retangulo, cor in lista_rect:
        if cor == BRANCO:
            x, y, _, _ = retangulo
            return x, y
            
def determinar_posicao_robo(caminho):
    
    """Essa função recebe uma lista de coordenadas que representam um caminho e retorna a direção que o robô deve seguir para chegar
    à próxima posição do caminho. A função retorna 'up' se a próxima posição do caminho estiver acima da posição atual, 'down' se a próxima
    posição do caminho estiver abaixo da posição atual, 'left' se a próxima posição do caminho estiver à esquerda da posição atual, 'right'
    se a próxima posição do caminho estiver à direita da posição atual, e 'none' se as posições forem iguais."""
    
    try:
        x_atual, y_atual = caminho[0]
        x_novo, y_novo = caminho[1]
    except IndexError:
        return 'none'
    else:
        if x_novo < x_atual:
            return 'up'
        elif x_novo > x_atual:
            return 'down'
        elif y_novo < y_atual:
            return 'left'
        elif y_novo > y_atual:
            return 'right'
        else:
            return 'none'  # Se as posições forem iguais