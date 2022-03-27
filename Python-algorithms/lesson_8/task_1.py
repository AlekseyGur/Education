# 1. На улице встретились N друзей. Каждый пожал руку всем остальным друзьям (по одному разу). Сколько рукопожатий было?
# Примечание. Решите задачу при помощи построения графа.


N = int(input('Введите количество друзей: '))

graph = [[1 for _ in range(N)] for __ in range(N)]

for i, v in enumerate(graph):
    for j, _ in enumerate(v):
        if i == j:
            graph[i][j] = 0  # нельзя пожать руку самому себе

handshakes = []  # комбинации рукопожатий
for curent, friend in enumerate(graph):
    for i, vertex in enumerate(friend):
        if vertex != 0:
            index = f'{curent}-{i}'
            if curent < i:
                index = f'{i}-{curent}'
            if index not in handshakes:
                handshakes.append(index)

print(f'Всего рукопожатий: {len(handshakes)}')
