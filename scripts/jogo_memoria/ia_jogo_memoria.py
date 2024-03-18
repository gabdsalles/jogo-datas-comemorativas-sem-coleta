import random

from scripts.carta import Carta

cartas_lembradas = []

def escolher_cartas(lista_cartas):

    global cartas_lembradas

    lista_cartas = [carta for carta in lista_cartas if carta.dono == None and carta not in cartas_lembradas]

    for carta in cartas_lembradas:
        if carta in lista_cartas:
            cartas_lembradas.remove(carta)

    if len(cartas_lembradas) == 0:

        carta1 = random.choice(lista_cartas)
        carta2 = random.choice(lista_cartas)

        while carta2 == carta1:
            carta2 = random.choice(lista_cartas)

        return carta1, carta2
    
    else:
        
        tem_duas_iguais = False
        for carta in lista_cartas:
            if lista_cartas.count(carta.nome) == 2:
                tem_duas_iguais = True
                nome_cartas_iguais = carta.nome
                break

        if tem_duas_iguais:
            cartas_iguais = [carta for carta in lista_cartas if carta.nome == nome_cartas_iguais]
            carta1 = cartas_iguais[0]
            carta2 = cartas_iguais[1]

            return carta1, carta2

        
        carta1 = cartas_lembradas[0]
        carta2 = random.choice(lista_cartas)

        while carta2 == carta1:
            carta2 = random.choice(lista_cartas)

        return carta1, carta2

def atualizar_cartas_lembradas(carta):
    cartas_lembradas.append(carta)

def limpar_cartas_lembradas():
    global cartas_lembradas

    cartas_lembradas = []