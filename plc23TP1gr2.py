import collections
import re
import networkx as nx
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

print("-----------------------------------------------------------")
print("Calcular a frequência de registos por Província e por Local")
print("-----------------------------------------------------------")

print("\nPROVINCIAS")
for i, j in prov.items():
    print(f"{i}: {j}")

print("\nLOCAIS")
for i, j in loc.items():
    print(f"{i}: {j}")

print("\n\n")
# ------------- b) -------------

comMP3 = []

for line in arr:
    if re.search(r"\.mp3", line[-2]):
        comMP3.append(getCancao(line))

percent = len(comMP3) / len(arr) * 100

print("------------------------------------------------------------------------------------------------------------")
print("Calcular a percentagem de canções que têm pelo menos uma gravação \"mp3\", indicando o título dessas canções")
print("------------------------------------------------------------------------------------------------------------")

print(f"PERCENTAGEM\n{percent}")

print("\nTITULOS")
for mus in comMP3:
    print(mus)

print("\n\n")

# ------------- c) -------------

instrumentos = collections.defaultdict(int)

vazia = []

for line in arr:
    inst = getInstrumentos(line)
    if len(inst) == 0:
        vazia.append(line)
    else:
        for i in inst:
            instrumentos[i] += 1

for line in vazia:
    for i in getInstrumentos(line):
        instrumentos[i] += 1

print("-----------------------------------------------")
print("Calcular a distribuição por instrumento musical")
print("-----------------------------------------------")

for i, j in instrumentos.items():
    print(f"{i}: {j}")

print("\n\n")

# ------------- d) -------------

musicos = collections.defaultdict(int)

vazia = []

for line in arr:
    musc = getMusicos(line)
    if len(musc) == 0:
        vazia.append(line)
    for i in musc:
        musicos[i] += 1

for line in vazia:
    for i in getMusicos(line):
        instrumentos[i] += 1

print("-------------------------------------------------------------------------------------------------")
print("Identificar todos os Musicos/cantores registados e calcular o número de vezes que são mencionados")
print("-------------------------------------------------------------------------------------------------")

for i, j in musicos.items():
    print(f"{i}: {j}")

print("\n\n")

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

print("----------------------------------------------------------------------------------------------------------")
print("Construir um Grafo de Canções/Cantores que associa cada canção aos cantores/tocadores referidos no registo")
print("----------------------------------------------------------------------------------------------------------")

# os.execv("/usr/bin/xdot", ["xdot", "musicas_cantores_grafo.dot"])
