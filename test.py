import collections
import re

import ftfy

f = open('test', 'r', encoding="utf-8")


def getProvince(s: str):
    return re.sub(r'\W', '', s, re.UNICODE)


def getLocal(s: str):
    return s

def getCancao(s: str):
    return re.match(r'[^;(]*', s).group(0)

def getCantor(s: str):
    return re.match(r'[^;(]*', s).group(0)


s = ftfy.fix_text(f.read())
v = re.split(r'::\n', s, flags=re.MULTILINE)
arr = [re.split('::', i) for i in v[1:]]
arr[-1].pop()

# ------------- a) -------------

semConcelho = []
comConcelho = []

for i in arr:
    if len(i) < 5 or ';' in i[1]:
        semConcelho.append(i)
    else:
        comConcelho.append(i)

prov = collections.defaultdict(int)
loc = collections.defaultdict(int)

for x, y, *tail in comConcelho:
    prov[getProvince(x)] += 1
    loc[getLocal(y)] += 1

for x, *tail in semConcelho:
    prov[getProvince(x)] += 1


# ------------- b) -------------

comMP3 = []
semMP3 = []
for i in comConcelho:
    if re.search(r'.mp3', i[-2]):
        comMP3.append(i[2])
    else:
        semMP3.append(i[2])
for i in semConcelho:
    if re.search(r'.mp3', i[-2]):
        comMP3.append(i[1])
    else:
        semMP3.append(i[1])
comMP3 = [getCancao(i) for i in comMP3]
semMP3 = [getCancao(i) for i in semMP3]

# ------------- c) -------------




# ------------- d) -------------

cantores = collections.defaultdict(int)
for i in comConcelho:
    cantores[getCantor(i[3])] += 1
for i in semConcelho:
    cantores[getCantor(i[2])] += 1

for i, j in cantores.items():
    print(f"{i}: {j}")

# ------------- e) -------------

