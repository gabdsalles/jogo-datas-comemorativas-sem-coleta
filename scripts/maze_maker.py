from random import shuffle, randrange, sample

def make_maze(w=10, h=10):
    vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
    ver = [["|  "] * w + ['|'] for _ in range(h)] + [[]]
    hor = [["+--"] * w + ['+'] for _ in range(h + 1)]

    def walk(x, y):
        vis[y][x] = 1

        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]:
                continue
            if xx == x:
                hor[max(y, yy)][x] = "+  "
            if yy == y:
                ver[y][max(x, xx)] = "   "
            walk(xx, yy)

    walk(randrange(w), randrange(h))

    # Divide o labirinto em quatro quadrantes
    quadrantes = [
        [(0, 0, w // 2, h // 2), "NW"],
        [(w // 2, 0, w, h // 2), "NE"],
        [(0, h // 2, w // 2, h), "SW"],
        [(w // 2, h // 2, w, h), "SE"],
    ]

    # Embaralha a ordem dos quadrantes
    shuffle(quadrantes)

    # Coloca um item em cada quadrante
    for (x1, y1, x2, y2), _ in quadrantes:
        x_item = randrange(x1 + 1, x2 - 1)
        y_item = randrange(y1 + 1, y2 - 1)
        ver[y_item][x_item] = " i "
    
    # Coloca um item no meio do labirinto
    x_meio = w // 2
    y_meio = h // 2
    ver[y_meio][x_meio] = " i "

    s = ""
    for (a, b) in zip(hor, ver):
        s += ''.join(a + ['\n'] + b + ['\n'])
    return s

if __name__ == '__main__':
    print(make_maze())
