import collections
import re
import networkx as nx
import matplotlib.pyplot as plt
import ftfy

f = open('arq-son.txt', 'r', encoding="utf-8")


def getProvince(line):
    # TODO
    return re.sub(r'\W', '', line[0], re.UNICODE)


def getLocal(line):
    # TODO
    return line[1]


def getCancao(line):
    # TODO
    return re.match(r'[^;(]*', line[2]).group(0)


def getCantores(line):
    # TODO
    res = [re.match(r'[^;(\s]*', i).group(0) for i in re.split(';', line[3])]
    return [i for i in res if i != '']


# Provincia::LocalOrig::Titulo::Musicos::SuporteDigital::

s = ftfy.fix_text(f.read())
v = re.split(r'::\n', s, flags=re.MULTILINE)
arr = [re.split('::', i) for i in v[1:]]
arr[-1].pop()

# ------------- a) -------------

prov = collections.defaultdict(int)
loc = collections.defaultdict(int)

for line in arr:
    prov[getProvince(line)] += 1
    loc[getLocal(line)] += 1

for i, j in prov.items():
    print(f"{i}: {j}")

for i, j in loc.items():
    print(f"{i}: {j}")

# ------------- b) -------------

comMP3 = []

for line in arr:
    if re.search(r'.mp3', line[-2]):
        comMP3.append(getCancao(line))

for i in comMP3:
    print(i)

# ------------- c) -------------


# ------------- d) -------------

cantores = collections.defaultdict(int)

for line in arr:
    for i in getCantores(line):
        cantores[i] += 1

for i, j in cantores.items():
    print(f"{i}: {j}")

# ------------- e) -------------

adjList = collections.defaultdict(list)

for line in arr:
    cancao = getCancao(line)
    for i in getCantores(line):
        adjList[cancao].append(i)

for i, j in adjList.items():
    print(f'{i}: {j}')


