from itertools import islice
from random import randint
import sys


def random_chunk(li, min_chunk=1, max_chunk=3):
    li = [s.strip() for s in li]
        
    it = iter(li)
    while True:
        nxt = list(islice(it,randint(min_chunk, max_chunk)))
        if nxt:
            yield ','.join(nxt)
        else:
            break

for i in list(random_chunk(list(sys.stdin))):
    print(i)
