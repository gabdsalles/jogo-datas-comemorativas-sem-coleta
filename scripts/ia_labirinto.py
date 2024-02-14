from queue import PriorityQueue

def heuristica(pos_atual, pos_alvo):
    """Calcula a distância de Manhattan entre dois pontos."""
    x1, y1 = pos_atual
    x2, y2 = pos_alvo
    return abs(x1 - x2) + abs(y1 - y2)

def encontrar_item_proximo(tabuleiro, posicao_robo, posicoes_itens):
    fila_prioridade = PriorityQueue()
    fila_prioridade.put((0, posicao_robo))
    visitados = set()
    custo = {posicao_robo: 0}
    item_proximo = None

    while not fila_prioridade.empty():
        _, pos_atual = fila_prioridade.get()

        if pos_atual in posicoes_itens:
            item_proximo = pos_atual
            break

        for direcao in [(0, 2), (0, -2), (2, 0), (-2, 0)]:
            x, y = pos_atual[0] + direcao[0], pos_atual[1] + direcao[1]
            nova_pos = (x, y)

            if 0 <= x < len(tabuleiro) and 0 <= y < len(tabuleiro[0]) and tabuleiro[x][y] not in ['+', '-', '|']:
                novo_custo = custo[pos_atual] + 1

                if novo_custo < custo.get(nova_pos, float('inf')):
                    custo[nova_pos] = novo_custo
                    prioridade = novo_custo + heuristica(nova_pos, posicoes_itens[0])
                    fila_prioridade.put((prioridade, nova_pos))
                    visitados.add(pos_atual)

    return item_proximo

def checar_paredes(tabuleiro, x, y):

    if tabuleiro[x][y] in ["+", "-", "|"]:
        return True
    else:
        return False

def encontrar_caminho_eficiente(tabuleiro, posicao_robo, posicao_alvo):
    fila_prioridade = PriorityQueue()
    fila_prioridade.put((0, posicao_robo))
    visitados = set()
    custo = {posicao_robo: 0}
    antecessor = {posicao_robo: None}

    while not fila_prioridade.empty():
        _, pos_atual = fila_prioridade.get()

        if pos_atual == posicao_alvo:
            caminho = []
            while pos_atual:
                caminho.append(pos_atual)
                pos_atual = antecessor[pos_atual]
            caminho.reverse()
            return caminho

        for direcao in [(0, 2), (0, -2), (2, 0), (-2, 0)]:

            x, y = pos_atual[0] + direcao[0], pos_atual[1] + direcao[1]
            nova_pos = (x, y)

            if 0 <= x < len(tabuleiro) and 0 <= y < len(tabuleiro[0]) and tabuleiro[x][y] not in ['+', '-', '|']:
                novo_custo = custo[pos_atual] + 1

                if novo_custo < custo.get(nova_pos, float('inf')):
                    custo[nova_pos] = novo_custo
                    prioridade = novo_custo + heuristica(nova_pos, posicao_alvo)
                    fila_prioridade.put((prioridade, nova_pos))
                    antecessor[nova_pos] = pos_atual
                    visitados.add(pos_atual)

    return None

# não deu certo. a ideia é fazer com que o objetivo do robô seja não encontrar o item mais próximo,
# mas sim percorrer o tabuleiro todo. aí, controla pelas paredes.