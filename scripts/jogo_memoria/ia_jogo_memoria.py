import json

cartas_lembradas = []

def carregar_dados_tabuleiro(arquivo="./scripts/jogo_memoria/tabuleiro_treino.json"):
    with open(arquivo, 'r') as f:
        dados = json.load(f)
        possibilidades_jogadas = dados["possibilidades_jogadas"]
        entradas = []
        esperados = []
        for jogada in possibilidades_jogadas:
            entradas.append(jogada["entrada"])
            esperados.append(jogada["saida"])
        return entradas, esperados

def carregar_teste_tabuleiro(arquivo="./scripts/jogo_memoria/tabuleiro_treino.json"):
    with open(arquivo, 'r') as f:
        dados = json.load(f)
        possibilidades_teste = dados["possibilidades_teste"]
        entradas = []
        esperados = []
        for jogada in possibilidades_teste:
            entradas.append(jogada["entrada"])
            esperados.append(jogada["saida"])
        return entradas, esperados
    
def treinar_perceptron(entradas, esperados, pesos=[0, 0], taxa_aprendizado=0.1, epocas=1000, bias=1):
    
    for _ in range(epocas):
        for i, entrada in enumerate(entradas):
            soma = sum([entrada[j] * pesos[j] for j in range(len(entrada))]) + bias
            saida = 1 if soma >= 0 else 0
            erro = esperados[i] - saida
            for j in range(len(pesos)):
                pesos[j] = pesos[j] + (taxa_aprendizado * erro * entrada[j])
            bias = bias + (taxa_aprendizado * erro)

    return pesos, bias

def testar_perceptron(entradas, pesos, bias):
    resultados = []
    for entrada in entradas:
        soma = sum([entrada[i] * pesos[i] for i in range(len(entrada))]) + bias
        saida = 1 if soma >= 0 else 0
        resultados.append(saida)
    return resultados

entradas, esperados = carregar_dados_tabuleiro()
pesos, bias = treinar_perceptron(entradas, esperados)
print(pesos)
print(bias)
entradas_teste, esperados_teste = carregar_teste_tabuleiro()
resultados = testar_perceptron(entradas_teste, pesos, bias)
print(resultados)