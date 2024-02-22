VERMELHO = (255, 0, 0)
AMARELO = (255, 255, 0)
AZUL = (0, 0, 255)
LARANJA = (255, 165, 0)
VERDE = (0, 128, 0)
MARROM = (139, 69, 19)

class Peca:

    def __init__(self, imagem1, imagem2, nome, cor1, cor2):
        self.imagem1 = imagem1
        self.imagem2 = imagem2
        self.nome = nome
        self.cor1 = cor1
        self.cor2 = cor2
        self.dono = None

        if cor1 == cor2:
            self.tipo = "simples"
        else:
            self.tipo = "dupla"



class Pecas:

    def __init__(self):
        self.lista_pecas = []
        self.inicializar_pecas()

    def inicializar_pecas(self):
        figuras = ['cruz', 'ramos', 'chocolate', 'coelho', 'cesta', 'ovo']
        cores = {'cruz': 'azul', 'ramos': 'vermelho', 'chocolate': 'marrom', 'coelho': 'cinza', 'cesta': 'amarelo', 'ovo': 'branco'}

        pecas_criadas = set()

         # Adicione a peça com as duas mesmas figuras
        for figura in figuras:
            cor_figura = cores[figura]
            nome = figura
            if nome not in pecas_criadas:
                peca = Peca(f"assets/imagens/pascoa/{figura}.png", f"assets/imagens/pascoa/{figura}.png", f"{nome} {nome}", cor_figura, cor_figura)
                self.lista_pecas.append(peca)
                pecas_criadas.add(nome)

            # Adicione a peça com duas figuras diferentes
            for outra_figura in figuras:
                if figura != outra_figura:
                    cor_outra_figura = cores[outra_figura]
                    nome = f'{figura} {outra_figura}'
                    nome_inverso = f'{outra_figura} {figura}'
                    if nome not in pecas_criadas and nome_inverso not in pecas_criadas:
                        peca = Peca(f"assets/imagens/pascoa/{figura}.png", f"assets/imagens/pascoa/{outra_figura}.png", nome, cor_figura, cor_outra_figura)
                        self.lista_pecas.append(peca)
                        pecas_criadas.add(nome)
                        pecas_criadas.add(nome_inverso)



# pecas = Pecas()
# for peca in pecas.lista_pecas:
#     print(peca.nome, peca.cor1, peca.cor2)

# print(f"comprimento: {len(pecas.lista_pecas)}")