from random import shuffle, randrange, sample

def make_maze(w=14, h=10, num_items=18):
    vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
    ver = [["| "] * w + ['|'] for _ in range(h)] + [[]]
    hor = [["+-"] * w + ['+'] for _ in range(h + 1)]

    def walk(x, y):
        vis[y][x] = 1

        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]:
                continue
            if xx == x:
                hor[max(y, yy)][x] = "+ "
            if yy == y:
                ver[y][max(x, xx)] = "  "
            walk(xx, yy)

    walk(randrange(w), randrange(h))

    # Encontrar células brancas (espaços vazios)
    white_cells = [(x, y) for y in range(h) for x in range(w) if ver[y][x] == "  "]

    # Embaralhar as células brancas e escolher num_items delas para colocar itens
    items_cells = sample(white_cells, min(num_items, len(white_cells)))

    for x, y in items_cells:
        ver[y][x] = "i "

    s = ""
    for (a, b) in zip(hor, ver):
        s += ''.join(a + ['\n'] + b + ['\n'])
    return s

if __name__ == '__main__':
    print(make_maze())
