class Item:

    def __init__(self, nome, imagem):
        self.nome = nome
        self.imagem = imagem
        self.passou = False #variável que vê se o jogador passou pelo item
        self.dono = None #quem passou pelo item, o jogador ou o robô
        self.posicao = None

class ListaItens:
    
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


        