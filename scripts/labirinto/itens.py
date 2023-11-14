class Item:

    def __init__(self, nome, imagem):
        self.nome = nome
        self.imagem = imagem
        self.passou = False #variável que vê se o jogador passou pelo item
        self.dono = None #quem passou pelo item, o jogador ou o robô
        self.posicao = None

class ListaItens:
    
    def __init__(self):
        
        santa = Item("santa", "assets/imagens/natal/santa.png")
        tree = Item("tree", "assets/imagens/natal/tree.png")
        giftbox = Item("giftbox", "assets/imagens/natal/giftbox.png")
        bell = Item("bell", "assets/imagens/natal/bell.png")
        bengala = Item("bengala", "assets/imagens/natal/bengala.png")

        self.lista_itens = [santa, tree, giftbox, bell, bengala]