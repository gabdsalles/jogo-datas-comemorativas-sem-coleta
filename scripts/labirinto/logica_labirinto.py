from pygame.locals import *

BRANCO = (255, 255, 255)
    
def pegar_coordenadas_robo(lista_rect): #coordenadas: x = 1140, y = 625
        
        for retangulo, cor in reversed(lista_rect):
            if cor == BRANCO:
                x, y, _, _ = retangulo
                return x, y
        
        return None

def pegar_coordenadas_personagem(lista_rect): #x = 480, y = 65

    for retangulo, cor in lista_rect:
        if cor == BRANCO:
            x, y, _, _ = retangulo
            return x, y
            
def determinar_posicao_robo(caminho):
    
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