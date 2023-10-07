import collections
import re
import networkx as nx
import matplotlib.pyplot as plt
import ftfy

f = open('arq-son.txt', 'r', encoding="utf-8")


def getProvince(line):
    return re.sub(r'\W', '', line[0], re.UNICODE)


def getLocal(line):
    pattern = r',\s*(.*)$'
    match = re.search(pattern, line[1])
    if match:
        return match.group(1)
    else:
        return line[1]


def getCancao(line):
    return re.match(r'[^;(]*', line[2]).group(0)

def getInstrumentos(line):
    res = []
    line = re.split(';', line[3])
    
    pattern1 = r'(\((\D*)\))$'
    pattern2 = r'\((\D*) e (\D*)\)'
    pattern3 = r'\(.*\) (\D*)'

    for pedaco in line:
        pedaco = pedaco.strip()
        match1 = re.search(pattern1, pedaco)
        match2 = re.search(pattern2, pedaco)
        match3 = re.search(pattern3, pedaco)
        if match3:
            res.append(match3.group(1).lower())
        elif match2:
            res.append(match2.group(1).lower())
            res.append(match2.group(2).lower())
        elif match1:
            res.append(match1.group(2).lower())
        elif pedaco in instrumentos:
            res.append(pedaco.lower())

    return res

def getMusicos(line):
    res = []
    line = re.split(';', line[3])
    
    pattern1 = r'(.+?) +\(\D*\)'

    for pedaco in line:
        pedaco = pedaco.strip()
        match1 = re.search(pattern1, pedaco)
        if match1:
            res.append(match1.group(1).lower())
        elif pedaco in musicos:
            res.append(pedaco.lower())
    return res
    

# Provincia::LocalOrig::Titulo::Musicos::SuporteDigital::...

s = ftfy.fix_text(f.read())
v = re.split(r'\n', s, flags=re.MULTILINE)
arr = [re.split('::', i) for i in v[1:]]
arr = [line[:-1] for line in arr]

for i in range(len(arr)-1, -1, -1):
    if len(arr[i]) < 6:
        del arr[i]

# ------------- a) -------------

prov = collections.defaultdict(int)
loc = collections.defaultdict(int)

for line in arr:
    prov[getProvince(line)] += 1
    loc[getLocal(line)] += 1

'''
print("\nPROVINCIAS")
for i, j in prov.items():
    print(f"{i}: {j}")

print("\nLOCAIS")
for i, j in loc.items():
    print(f"{i}: {j}")
'''
# ------------- b) -------------

comMP3 = []

for line in arr:
    if re.search(r'\.mp3', line[-2]):
        comMP3.append(getCancao(line))

percent = len(comMP3) / len(arr) * 100
'''
print(percent)

for mus in comMP3:
    print(mus)

'''
# ------------- c) -------------

instrumentos = collections.defaultdict(int)

for line in arr:
    for i in getInstrumentos(line):
        instrumentos[i] += 1
'''
for i, j in instrumentos.items():
    print(f"{i}: {j}")
'''
# ------------- d) -------------

musicos = collections.defaultdict(int)

for line in arr:
    for i in getMusicos(line):
        musicos[i] += 1
'''
for i, j in musicos.items():
    print(f"{i}: {j}")
'''

# ------------- e) -------------

adjList = collections.defaultdict(list)

for line in arr:
    cancao = getCancao(line)
    for i in getMusicos(line):
        if i not in adjList[cancao]:
            adjList[cancao].append(i)

grafo = nx.DiGraph()

for cancao, cantores in adjList.items():
    grafo.add_node(cancao)
    for cantor in cantores:
        grafo.add_node(cantor)
        grafo.add_edge(cantor, cancao)

nx.nx_pydot.write_dot(grafo, "musicas_cantores_grafo.dot")
