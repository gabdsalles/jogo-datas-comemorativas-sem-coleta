def calcular_custos(pecas_robo, esquerda_tabuleiro, direita_tabuleiro, peca):

    # Heurística: retorna quantas peças com a mesma figura já estão na mão do robô

    if peca.nome1 == peca.nome2:
        custo = 100
    else:
        custo = sum(1 for outra_peca in pecas_robo if outra_peca != peca and (outra_peca.nome1 == peca.nome1 or outra_peca.nome1 == peca.nome2 or outra_peca.nome2 == peca.nome1 or outra_peca.nome2 == peca.nome2))
    return custo

def heuristica_tabuleiro(tabuleiro, peca):

    # Retorna quantas peças com a mesma figura já estão no tabuleiro
    
    custo = sum(1 for peca_tabuleiro in tabuleiro if peca_tabuleiro.nome1 == peca.nome1 or peca_tabuleiro.nome1 == peca.nome2 or peca_tabuleiro.nome2 == peca.nome1 or peca_tabuleiro.nome2 == peca.nome2)
    return custo

def escolher_peca(pecas_robo, esquerda_tabuleiro, direita_tabuleiro, pecas_tabuleiro):
    pecas_possiveis = [peca for peca in pecas_robo if peca.nome1 == esquerda_tabuleiro or peca.nome2 == esquerda_tabuleiro or peca.nome1 == direita_tabuleiro or peca.nome2 == direita_tabuleiro]

    if len(pecas_possiveis) == 1:
        print("Só tinha uma peça possível", pecas_possiveis[0].nome1, pecas_possiveis[0].nome2)
        return pecas_possiveis[0]
    else:
        maior_custo = -1
        melhor_peca = []

        for peca in pecas_possiveis:
            custo = calcular_custos(pecas_robo, esquerda_tabuleiro, direita_tabuleiro, peca)
            print("Custo da peça", peca.nome1, peca.nome2, ":", custo)
            if custo > maior_custo:
                maior_custo = custo
                melhor_peca = [peca]
            elif custo == maior_custo:
                melhor_peca.append(peca)
        
        if len(melhor_peca) == 1:
            print("Só uma peça tem melhor custo", melhor_peca[0].nome1, melhor_peca[0].nome2)
            return melhor_peca[0]
        else: # se for maior que 1, quer dizer que tem 2 peças com o mesmo custo.
            menor_custo = float("inf")
            melhor_desempate = None
            
            for peca in melhor_peca:
                custo = heuristica_tabuleiro(pecas_tabuleiro, peca)
                print("Custo de desempate", peca.nome1, peca.nome2, ":", custo)
                if custo < menor_custo:
                    menor_custo = custo
                    melhor_desempate = peca

            print("Retornando a melhor no desempate", melhor_desempate.nome1, melhor_desempate.nome2, "com custo", menor_custo)
            return melhor_desempate
