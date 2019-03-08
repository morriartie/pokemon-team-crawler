import requests
import sys
import json

# TODO: limpar linhas que contenham falas de jogadores

DEBUG = 1
MARKOV_FILE = 'switches_markov.txt'
MARKOV_USES = 'switches_markov_uses.txt'
HISTORY_FILE = 'replays_watched.txt'

raw = None

log = []
p1pokes = {}
p2pokes = {}
switched_t1 = []
switched_t2 = []
switches_markov = {}
switches_markov_uses = {}
toremove = ['-Resolute','-Mega','-Ash','-Mega-X','-Mega-Y','']

def clean():
    print("CLEANING")
    global raw
    global p1pokes
    global p2pokes
    global log
    global switched_t1
    global switched_t2
    p1pokes = {}
    log = []
    p2pokes = {}
    switched_t1 = []
    switched_t2 = []

def connect(url):
    global raw
    raw = requests.get(url)
    raw = raw.text
    raw = raw.replace('\t','\n').split('\n')
    raw = [line for line in raw if line!='']

def read_log():
    global raw
    global p1pokes
    global p2pokes
    global log
    global cleaned
    # cutting battle log only
    capt = False
    #
    on_faint1 = False
    on_faint2 = False
    #
    for line in raw:
        #if('|join|' in line or '|J|' in line):
        if(1):
            capt = True
        #if('<script' in line):
        #    capt = False
        if(capt):
            log.append(line)

    p1active = ''
    p2active = ''
    for line in log:
        # getting teams
        if('|poke|p1|' in line):
            pkname = line.split('|')[3].split(',')[0]
            if('-' in pkname):
                if('-*' in pkname):
                    pkname = pkname.replace('-*','')
                print("'-' in {}, changing to {}".format(pkname,pkname.replace('-','_')))
                pkname = pkname.replace('-','_')
            p1pokes[pkname] = {}
            p1pokes[pkname]['moves'] = {}
            p1pokes[pkname]['item'] = ''
            p1pokes[pkname]['power'] = ''
            p1pokes[pkname]['switches'] = {}
        if('|poke|p2|' in line):
            pkname = line.split('|')[3].split(',')[0]
            if('-' in pkname):
                if('-*' in pkname):
                    pkname = pkname.replace('-*','')
                print("'-' in {}, changing to {}".format(pkname,pkname.replace('-','_')))
                pkname = pkname.replace('-','_')
            p2pokes[pkname] = {}
            p2pokes[pkname]['moves'] = {}
            p2pokes[pkname]['item'] = ''
            p2pokes[pkname]['power'] = ''
            p2pokes[pkname]['switches'] = {}
        # filtering name changes in megas or specials
        if('-' in p1active):
            if(p1active.replace('-','_') in p1pokes):
                print('not changing name: {}'.format(p1active))
                p1active = p1active.replace('-','_')
            else:
                print('changing name: {} -> '.format(p1active),end='')
                p1active = p1active.split('-')[0]
                print('{}'.format(p1active))
        ####
        # filtering name changes in megas or specials
        if('-' in p2active):
            if(p2active.replace('-','_') in p2pokes):
                print('not changing name: {}'.format(p2active))
                p2active = p2active.replace('-','_')
            else:
                print('changing name: {} -> '.format(p2active),end='')
                p2active = p2active.split('-')[0]
                print('{}'.format(p2active))
        ####
        # checking end of battle
        if('|win|' in line):
            pass
        # checking faint
        if('|faint|p1' in line):
            on_faint1 = True
        if('|faint|p2' in line):
            on_faint2 = True
        # getting switches
        if('|switch|p1' in line):
            switching_to = line.split('|')[-2].split(',')[0]
            if(p1active!='' and not on_faint1):
                add_to_markov(p1active, switching_to,1)
                #
                if(switching_to in p1pokes[p1active.replace('-','_')]['switches']):
                    p1pokes[p1active.replace('-','_')]['switches'][switching_to] += 1
                else:
                    p1pokes[p1active.replace('-','_')]['switches'][switching_to] = 1
            p1active = switching_to
            on_faint1 = False
        if('|switch|p2' in line):
            switching_to = line.split('|')[-2].split(',')[0]
            if(p2active!='' and not on_faint2):
                add_to_markov(p2active, switching_to,2)
                #
                if(switching_to in p2pokes[p2active]['switches']):
                    p2pokes[p2active]['switches'][switching_to] += 1
                else:
                    p2pokes[p2active]['switches'][switching_to] = 1
            p2active = switching_to
            on_faint2 = False
        # getting moves
        if('|move|p1' in line):
            mvname = line.split('|')[3]
            if(mvname in p1pokes[p1active]['moves']):
                p1pokes[p1active]['moves'][mvname] += 1
            else:
                p1pokes[p1active]['moves'][mvname] = 1
        if('|move|p2' in line):
            mvname = line.split('|')[3]
            if(mvname in p2pokes[p2active]['moves']):
                p2pokes[p2active]['moves'][mvname] += 1
            else:
                p2pokes[p2active]['moves'][mvname] = 1

        # getting item
        if('item:' in line):
            if not(line.split('item:')[-1]==''):
                if('p1' in line):
                    if(len(line.split(':'))>1):
                        p1pokes[p1active]['item'] = line.split(':')[-1]
                elif('p2' in line):
                    if(len(line.split(':'))>1):
                        p2pokes[p2active]['item'] = line.split(':')[-1]

def print_data(team_dict):
    print("Pokes: {}".format(','.join(team_dict.keys())))
    print("\n")
    print("________")
    for poke in team_dict:
        print(poke.upper())
        print('    ├ item: {}'.format(team_dict[poke]['item']))
        print('    ├ power: {}'.format(team_dict[poke]['power']))
        print('    ├ moves:')
        for i,move in enumerate(team_dict[poke]['moves']):
            conn1 = ('├','└')[i==len(team_dict[poke]['moves'])-1]
            conn2 = ('│',' ')[i==len(team_dict[poke]['moves'])-1]
            print('    │    '+conn1+'─ {}'.format(move))
            print('    │    '+conn2+'    └─ uses: {}'.format(team_dict[poke]['moves'][move]))
        print('    └ switches:')
        for i,swit in enumerate(team_dict[poke]['switches']):
            print('        └─ {}: {}'.format(swit,team_dict[poke]['switches'][swit]))
        print("______\n")

def add_to_markov(switching_from, switching_to,team):
    # TODO: Fazer uma cadeia considerando o pokemon oponente
    global switches_markov
    #
    if(switching_from not in switches_markov):
        switches_markov[switching_from] = {}
    if(switching_to not in switches_markov[switching_from]):
        switches_markov[switching_from][switching_to] = 1
    else:
        switches_markov[switching_from][switching_to] += 1
    #
    if(team==1):
        if(switching_from not in switched_t1):
            switched_t1.append(switching_from)
    if(team==2):
        if(switching_from not in switched_t2):
            switched_t2.append(switching_from)
    if(team==1):
        if(switching_to not in switched_t1):
            switched_t1.append(switching_to)
    if(team==2):
        if(switching_to not in switched_t2):
            switched_t2.append(switching_to)

def add_markov_uses():
    global switches_markov_uses
    #
    for pok in switched_t1:
        if(pok not in switches_markov_uses):
            switches_markov_uses[pok] = 1
        else:
            switches_markov_uses[pok] += 1
    for pok in switched_t2:
        if(pok not in switches_markov_uses):
            switches_markov_uses[pok] = 1
        else:
            switches_markov_uses[pok] += 1

def save_markov():
    global switches_markov
    global switched_t1
    global switched_t2
    global toremove
    # saving markov uses
    add_markov_uses()
    a = json.dumps(switches_markov_uses)
    #
    with open(MARKOV_USES,'w') as file:
        file.write(a)
    # saving markov dict
    d = json.dumps(switches_markov)
    for te in toremove:
        d = d.replace(te,'')
    with open(MARKOV_FILE,'w') as file:
        file.write(d.replace('_','-'))

def load_markov():
    global switches_markov
    global switches_markov_uses
    # loading uses
    raw_text = open(MARKOV_USES).read().replace('\n','').replace('\t','')
    if(raw_text!=''):
        switches_markov_uses = json.loads(raw_text)
    # loading dict
    raw_text = open(MARKOV_FILE).read().replace('\n','').replace('\t','')
    if(raw_text!=''):
        switches_markov = json.loads(raw_text)

def add_to_history(url):
    with open(HISTORY_FILE,'a') as file:
        file.write(url+'\n')

def exec_proc(url,print_out=False):
    if not(DEBUG):
        try:
            connect()
            load_markov()
            read_log()
            if(url not in open(HISTORY_FILE).read().split('\n')):
                save_markov()
                add_to_history()
            if(print_out):
                print("###################")
                print("Team 1:")
                print_data(p1pokes)
                print("###################")
                print("Team 2:")
                print_data(p2pokes)
        except:
            print("connection error") # heh, so as vezes
    else:
        connect(url)
        load_markov()
        read_log()
        if(url not in open(HISTORY_FILE).read().split('\n')):
            save_markov()
            add_to_history(url)
        print("###################")
        print("Team 1:")
        print_data(p1pokes)
        print("###################")
        print("Team 2:")
        print_data(p2pokes)
    clean()

if __name__=='__main__':
    exec_proc(sys.argv[1],print_out=True)
