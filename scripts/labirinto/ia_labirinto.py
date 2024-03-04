from collections import deque

TABULEIRO = [
    "+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+",
    "|  i    |       |     |   |    i  |   | |   |",
    "+ + +-+ +-+-+-+ + + +-+ + + +-+-+ + + + + + +",
    "| | | |   |   | | |   | | | |   |   | |   | |",
    "+-+ + +-+ + + + + +-+ + + +-+ +-+-+-+ + +-+ +",
    "|   | |   | | | |   |   |      i  |   | |   |",
    "+ +-+ + +-+ + + + +-+-+-+-+-+ + + + +-+ + + +",
    "| |   |     | |   |   |     | | | |   | | | |",
    "+ + +-+-+-+-+ +-+-+ + + +-+ +-+ + +-+ + + + +",
    "| |    i    |       | | | |   | |   | | | | |",
    "+ +-+-+ +-+-+ +-+-+-+ + + +-+ + + +-+ + + + +",
    "| |   |       |   |   | |   |  i| |   | | | |",
    "+ + + +-+-+-+-+ + + +-+ + + +-+ +-+ +-+-+ + +",
    "| | |   |      i| | |   | |     |   |     | |",
    "+ + +-+ + +-+-+-+ + + +-+-+-+-+ + +-+ + +-+ +",
    "| |   |   |   |   | |  i   i  | |   | | | | |",
    "+ +-+ +-+-+ +-+ +-+ + +-+-+-+ + +-+ +-+ + + +",
    "|   |   |  i|   |   |  i  |   | | |     |  i|",
    "+-+ +-+ +-+ + +-+-+ +-+-+ + +-+ + +-+-+-+ +-+",
    "|     |     |     | | |   | |  i| |   |   | |",
    "+ +-+-+-+-+ +-+-+ + + + +-+ + +-+ + + + +-+ +",
    "|      i  | |   | | |     | |     | |   |   |",
    "+-+-+-+ +-+-+ +-+ + +-+-+-+ +-+-+ + +-+-+ +-+",
    "|  i| |   |     | |    i    |   | | |   |   |",
    "+ + + + + +-+-+ + +-+-+-+ +-+-+ + + + + +-+ +",
    "| |   | |      i|  i  | | |   |   |   | |   |",
    "+ +-+-+ +-+-+-+-+-+-+ + + + + + +-+-+-+ + + +",
    "|     |     |   |     |   | | |       | | | |",
    "+ +-+ +-+-+ +-+ + +-+-+-+-+ + +-+-+-+ + + +-+",
    "| | |     | |   | |         |   |  i| | |   |",
    "+ + +-+ +-+ + + + + +-+-+-+-+-+ + + +-+ +-+ +",
    "|     |       | |             |   |         |",
    "+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
]

posicoes_itens_matriz = [(i, j) for i, linha in enumerate(TABULEIRO) for j, celula in enumerate(linha) if celula == 'i']

def direcao_valida_robo(pos_robo, tabuleiro):
    
    possible_directions = ["left", "right", "up", "down"]
    valid_directions = []
    x = pos_robo[0]
    y = pos_robo[1]
    for direction in possible_directions:

        if direction == "up":
            x = pos_robo[0] - 1
            y = pos_robo[1]
            #print(f"up: x={x}, y={y}")
        elif direction == "left":
            x = pos_robo[0]
            y = pos_robo[1] - 1
            #print(f"left: x={x}, y={y}")
        elif direction == "right":
            x = pos_robo[0]
            y = pos_robo[1] + 1
            #print(f"right: x={x}, y={y}")
        elif direction == "down":
            x = pos_robo[0] + 1
            y = pos_robo[1]
            #print(f"down: x={x}, y={y}")
        
        if 0 <= x < len(tabuleiro) and 0 <= y < len(tabuleiro[0]) and tabuleiro[x][y] == " ":
            valid_directions.append(direction)

        
    print(f"Direções válidas: {valid_directions}")
    return valid_directions

def encontrar_caminho_para_item(tabuleiro, pos_inicial, pos_itens):
    visitados = set()
    fila = deque([(pos_inicial, [])]) 
    while fila:
        pos_atual, caminho_atual = fila.popleft()
        x, y = pos_atual

        if pos_atual in pos_itens:
            caminho = caminho_atual + [pos_atual]
            for ponto in caminho:
                x = ponto[0]
                y = ponto[1]
                if x % 2 == 0 or y % 2 == 0:
                    caminho.remove(ponto)
            
            # print(caminho)
            return caminho

        direcoes = [(0, 1), (1, 0), (0, -1), (-1, 0)]  
        for dx, dy in direcoes:
            nova_pos = (x + dx, y + dy)
            if 0 <= nova_pos[0] < len(tabuleiro) and 0 <= nova_pos[1] < len(tabuleiro[0]) and tabuleiro[nova_pos[0]][nova_pos[1]] not in  ["+", "|", "-"]:
                if nova_pos not in visitados:
                    visitados.add(nova_pos)
                    fila.append((nova_pos, caminho_atual + [pos_atual])) 

    return None  

caminho = encontrar_caminho_para_item(TABULEIRO, (31, 43), posicoes_itens_matriz)
print("Caminho encontrado:", caminho)
