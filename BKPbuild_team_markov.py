from random import randint
import json
import sys

# se o melhor pokemon sugerido ja estiver no time, sugerir o segundo melhor em vez disso

def show_indications(_dict):
    biggest_key = ['','','','','','']
    biggest_val = [0,0,0,0,0,0]
    for key in _dict.keys():
        if(_dict[key]>biggest_val[0]):
            biggest_val[5] = biggest_val[4]
            biggest_val[4] = biggest_val[3]
            biggest_val[3] = biggest_val[2]
            biggest_val[2] = biggest_val[1]
            biggest_val[1] = biggest_val[0]
            biggest_val[0] = _dict[key]
            #
            biggest_key[5] = biggest_key[4]
            biggest_key[4] = biggest_key[3]
            biggest_key[3] = biggest_key[2]
            biggest_key[2] = biggest_key[1]
            biggest_key[1] = biggest_key[0]
            biggest_key[0] = key
    biggest_key = [v for v in biggest_key if key != '']
    return biggest_key

MARKOV_FILE = 'switches_markov.txt'

toremove = ['-Mega','-Ash','-Mega-X','-Mega-Y']

fstpkmn = sys.argv[1].title()
team = []
team.append(fstpkmn)
markov_text = open(MARKOV_FILE).read().replace('\n','')
for te in toremove:
    markov_text = markov_text.replace(te,'')

with open('switches_markov','w') as file:
    file.write(markov_text)

markov_pokes = json.loads(markov_text)
last_poke = fstpkmn
_continue = False

while(len(team)<=6):
    print("team size: {}".format(len(team)))
    print("current team: {}".format(','.join(team)))
    suggestions = show_indications(markov_pokes[last_poke])
    #
    not_added = True
    for pokm in suggestions:
        if(pokm not in team):
            team.append(pokm)
            last_poke = pokm
            not_added = False
            break
    if(not_added):
        last_poke = team[randint(0,len(team)-1)]

print(','.join(team))
