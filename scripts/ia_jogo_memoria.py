# A IA do robô, no jogo da memória, é um agente que escolhe cartas aleatoriamente.
# Ele tem a capacidade de se lembrar de duas cartas que virou, e, se elas forem iguais, ele as pega.

import random

from carta import Carta

cartas_lembradas = []

def escolher_cartas(lista_cartas):

    global cartas_lembradas
    lista_cartas = [carta for carta in lista_cartas if carta.dono == None and carta not in cartas_lembradas]

    if len(cartas_lembradas) == 0:

        carta1 = random.choice(lista_cartas)
        carta2 = random.choice(lista_cartas)

        while carta2 == carta1:
            carta2 = random.choice(lista_cartas)

        return carta1, carta2

def atualizar_cartas_lembradas(carta1, carta2):
    cartas_lembradas.append(carta1)
    cartas_lembradas.append(carta2)