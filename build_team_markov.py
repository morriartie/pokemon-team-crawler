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
    biggest_key = [v for v in biggest_key if v != '']
    return biggest_key

MARKOV_FILE = 'switches_markov.txt'

fstpkmn = sys.argv[1].title()
team = []
team.append(fstpkmn)
markov_pokes = json.loads(open(MARKOV_FILE).read().replace('\n','').replace('\t',''))
last_poke = fstpkmn
_continue = False

while(len(team)<6):
    print("----------------")
    print("current team: {}".format(','.join(team)))
    suggestions = show_indications(markov_pokes[last_poke])
    print("suggestions for {}: {}".format(last_poke,','.join(suggestions)))
    #
    not_added = True
    for pokm in suggestions:
        if(pokm not in team):
            print("adding {} to team".format(pokm))
            team.append(pokm)
            last_poke = pokm
            not_added = False
            break
        else:
            print("{} already in team, chosing next...".format(pokm))
    if(not_added):
        print("No options found, continuing from another node ... new node: ",end = '')
        last_poke = team[randint(0,len(team)-1)]
        print(last_poke)

print(('\n'*3)+','.join(team))
