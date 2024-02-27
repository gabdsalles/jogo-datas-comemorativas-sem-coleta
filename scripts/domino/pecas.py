VERMELHO = (255, 0, 0)
AMARELO = (255, 255, 0)
AZUL = (0, 0, 255)
LARANJA = (255, 165, 0)
VERDE = (0, 128, 0)
MARROM = (139, 69, 19)

class Peca:

    def __init__(self, imagem1, imagem2, nome1, nome2, cor1, cor2):
        self.imagem1 = imagem1
        self.imagem2 = imagem2
        self.nome1 = nome1
        self.nome2 = nome2
        self.cor1 = cor1
        self.cor2 = cor2
        self.dono = None

        if cor1 == cor2:
            self.tipo = "dupla"
        else:
            self.tipo = "simples"



class Pecas:

    def __init__(self):
        self.lista_pecas = []
        self.cores = {'cruz': AZUL, 'ramos': VERMELHO, 'chocolate': MARROM, 'coelho': AMARELO, 'cesta': LARANJA, 'ovo': VERDE}
        self.inicializar_pecas()

    def inicializar_pecas(self):
        figuras = ['cruz', 'ramos', 'chocolate', 'coelho', 'cesta', 'ovo']

        pecas_criadas = set()

        # Adicione a peça com as duas mesmas figuras
        for figura in figuras:
            cor_figura = self.cores[figura]
            nome = figura
            if nome not in pecas_criadas:
                peca = Peca(f"assets/imagens/pascoa_horizontal/{figura}.png", f"assets/imagens/pascoa_horizontal/{figura}.png", nome, nome, cor_figura, cor_figura)
                self.lista_pecas.append(peca)
                pecas_criadas.add(nome)

            # Adicione a peça com duas figuras diferentes
            for outra_figura in figuras:
                if figura != outra_figura:
                    cor_outra_figura = self.cores[outra_figura]
                    nome = f'{figura} {outra_figura}'
                    nome_inverso = f'{outra_figura} {figura}'
                    if nome not in pecas_criadas and nome_inverso not in pecas_criadas:
                        peca = Peca(f"assets/imagens/pascoa_horizontal/{figura}.png", f"assets/imagens/pascoa_horizontal/{outra_figura}.png", figura, outra_figura, cor_figura, cor_outra_figura)
                        self.lista_pecas.append(peca)
                        pecas_criadas.add(nome)
                        pecas_criadas.add(nome_inverso)

# pecas = Pecas()
# for peca in pecas.lista_pecas:
#     print(peca.nome1, peca.nome2, peca.cor1, peca.cor2)

# print(f"comprimento: {len(pecas.lista_pecas)}")