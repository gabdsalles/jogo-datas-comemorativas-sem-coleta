import numpy as np

class QLearning:
    def __init__(self, n_actions, alpha=0.1, gamma=0.9):
        self.alpha = alpha  
        self.gamma = gamma  
        self.q_values = np.zeros(n_actions)

    def update_q_value(self, action, reward, next_max_q_value):
        self.q_values[action] += self.alpha * (reward + self.gamma * next_max_q_value - self.q_values[action])

    def choose_action(self, epsilon):
        if np.random.uniform() < epsilon:
            return np.random.randint(len(self.q_values)) 
        else:
            return np.argmax(self.q_values)

def escolher_peca(pecas_robo, esquerda_tabuleiro, direita_tabuleiro):
    pecas_possiveis = [peca for peca in pecas_robo if peca.nome1 == esquerda_tabuleiro or peca.nome2 == esquerda_tabuleiro or peca.nome1 == direita_tabuleiro or peca.nome2 == direita_tabuleiro]

    if len(pecas_possiveis) == 1:
        return pecas_possiveis[0]
    else:
        n_actions = len(pecas_possiveis)
        epsilon = 0.1  # Taxa de exploração
        q_learning = QLearning(n_actions=n_actions)

        for _ in range(100):  # Número de iterações de treinamento
            action = q_learning.choose_action(epsilon)
            cont = sum(1 for p in pecas_possiveis if p.nome1 == pecas_possiveis[action].nome1 and p.nome2 == pecas_possiveis[action].nome2)
            if pecas_possiveis[action].nome1 == pecas_possiveis[action].nome2:
                reward = 1 # reward é maior para peças duplas
            elif cont > 1:
                reward = 0.5
            else:
                reward = 0 # reward é menor para peças simples
            next_max_q_value = 0.5
            q_learning.update_q_value(action, reward, next_max_q_value)

        best_action_index = q_learning.choose_action(epsilon=0)
        return pecas_possiveis[best_action_index]

