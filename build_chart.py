import json

d = json.loads(open('switches_markov.txt').read().replace('\n',''))
vals = []
pokes = {}
avr = 8.628571428571428
for pokemon in d:
    for pok in d:
        if pokemon in d[pok]:
            if(pokemon not in pokes):
                pokes[pokemon] = 1
            else:
                pokes[pokemon]+=1

for p in pokes:
    if(pokes[p]>4):
        print("{} : {} | std dev: {}".format(p,pokes[p],int(((pokes[p]-avr)**2)**(1/2))))
    vals.append(pokes[p])
