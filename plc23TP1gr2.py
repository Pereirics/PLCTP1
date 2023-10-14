import collections
import re
import networkx as nx
import matplotlib.pyplot as plt
import webbrowser
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

comMP3 = list(set(comMP3))

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

instrumentos = dict(sorted(instrumentos.items(), key=lambda item: item[1], reverse=True))

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

pos = nx.random_layout(grafo)

plt.figure(figsize=(50, 50))  # Adjust the figure size as needed
nx.draw(grafo, pos, with_labels=True, node_size=100)

# Save the visualization as an HTML image map
plt.savefig("graph_visualization.png")


print("----------------------------------------------------------------------------------------------------------")
print("Construir um Grafo de Canções/Cantores que associa cada canção aos cantores/tocadores referidos no registo")
print("----------------------------------------------------------------------------------------------------------")

####################################     HTML EXTRA    ####################
with open('out.html', 'w') as file:

    file.write('<html>\n<head>\n<title>TP1</title>\n</head>\n<body>\n')

# A   
    file.write('<p style="font-size: 24px;">Calcular a frequência de registos por Província e por Local.</p>\n')
    #provincias
    file.write('<table border="1">\n')
    file.write('<table border="1" style="width: 300px;">\n')
    file.write('<tr><th>Provincia</th><th>Registos</th></tr>\n')
    for i, j in prov.items():
        file.write(f'<tr><td>{i}</td><td>{j}</td></tr>\n')
    file.write('</table>\n')
    #locais
    file.write('<table border="1">\n')
    file.write('<table border="1" style="width: 300px;">\n')
    file.write('<tr><th>Local</th><th>Registos</th></tr>\n')
    for i, j in loc.items():
        file.write(f'<tr><td>{i}</td><td>{j}</td></tr>\n')
    file.write('</table>\n')
    
    
# B
    file.write('<p style="font-size: 24px;">Calcular a percentagem de canções que têm pelo menos uma gravação "mp3."</p>\n')
    
    file.write(f'<p>Percentagem: {percent}%</p>')

    file.write('<ul>\n')
    if comMP3:
        file.write('<li>' + comMP3[0])

    for index, song in enumerate(comMP3[1:], start=1):
        if index % 5 == 0:
            file.write('</li>\n<li>')
        elif index != 0:
            file.write(' || ')
        file.write(song)
        
    file.write('</li>\n</ul>\n')
    
    
# C
    file.write('<p style="font-size: 24px;">Calcular a distribuição por instrumento musical.</p>\n')

    file.write('<table border="1">\n')
    file.write('<table border="1" style="width: 300px;">\n')
    file.write('<tr><th>Provincia</th><th>Registos</th></tr>\n')
    for i, j in instrumentos.items():
        file.write(f'<tr><td>{i}</td><td>{j}</td></tr>\n')
    file.write('</table>\n')
    
    
# D
    file.write('<p style="font-size: 24px;">Identificar todos os Musicos e calcular o número de vezes que são mencionados.</p>\n')
    file.write('<table border="1">\n')
    file.write('<table border="1" style="width: 300px;">\n')
    file.write('<tr><th>Músicos</th><th>Registos</th></tr>\n')
    for i, j in musicos.items():
        file.write(f'<tr><td>{i}</td><td>{j}</td></tr>\n')
    file.write('</table>\n')
    
    
    file.write('</body>\n</html>')

# E
    file.write('<p style="font-size: 24px;">Construir um Grafo de Canções/Cantores que associa cada canção aos cantores/tocadores referidos no registo.</p>\n')
    file.write('<img src="graph_visualization.png" alt="Grafo Canções/Cantores">')

webbrowser.open('out.html')