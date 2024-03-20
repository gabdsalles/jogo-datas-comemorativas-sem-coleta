class Item:

    """A classe Item representa um item que o jogador pode pegar. Cada item tem um nome, uma imagem, uma variável que vê se alguém já
    passou pelo item, se passou, quem é o dono, a posição do item na tela e a posição do item na matriz que representa o labirinto."""
    
    def __init__(self, nome, imagem):
        self.nome = nome
        self.imagem = imagem
        self.passou = False #variável que vê se o jogador passou pelo item
        self.dono = None #quem passou pelo item, o jogador ou o robô
        self.posicao = None
        self.posicao_matriz = None

class ListaItens:
    
    """Essa classe representa uma lista de itens. Ela é usada para criar uma lista de itens que o jogador pode pegar. A lista de itens
    é usada pra criar o labirinto. Depois, essa lista servirá para colocar os itens de forma aleatória no labirinto."""
    
    def __init__(self):
        
        self.lista_itens = [
            Item("santa", "assets/imagens/natal/santa.png"),
            Item("tree", "assets/imagens/natal/tree.png"),
            Item("giftbox", "assets/imagens/natal/giftbox.png"),
            Item("bell", "assets/imagens/natal/bell.png"),
            Item("bengala", "assets/imagens/natal/bengala.png"),
            Item("ball", "assets/imagens/natal/ball.png"),
            Item("santa", "assets/imagens/natal/santa.png"),
            Item("tree", "assets/imagens/natal/tree.png"),
            Item("giftbox", "assets/imagens/natal/giftbox.png"),
            Item("bell", "assets/imagens/natal/bell.png"),
            Item("bengala", "assets/imagens/natal/bengala.png"),
            Item("ball", "assets/imagens/natal/ball.png"),
            Item("santa", "assets/imagens/natal/santa.png"),
            Item("tree", "assets/imagens/natal/tree.png"),
            Item("giftbox", "assets/imagens/natal/giftbox.png"),
            Item("bell", "assets/imagens/natal/bell.png"),
            Item("bengala", "assets/imagens/natal/bengala.png"),
            Item("ball", "assets/imagens/natal/ball.png")
        ]

        self.lista_possibilidades_itens = [("santa", "assets/imagens/natal/santa.png"), ("tree", "assets/imagens/natal/tree.png"), ("giftbox", "assets/imagens/natal/giftbox.png"), ("bell", "assets/imagens/natal/bell.png"), ("bengala", "assets/imagens/natal/bengala.png"), ("ball", "assets/imagens/natal/ball.png")]


        