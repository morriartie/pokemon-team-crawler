from bs4 import BeautifulSoup as bfs
from random import randint
import requests
import configparser
import time
import teamanalyzer as ta

def load_configs():
	CONFIG_FILE = "config"
	global URL
	global HISTORYFILE
	global DELAY
	options = configparser.parse_conf(CONFIG_FILE)
	# ~
	URL = options['URL']
	HISTORYFILE = options['HISTORYFILE']
	DELAY = options['DELAY']

def walkto(URL,find):
	r = requests.get(URL)
	data = r.text
	soup = bfs(data,"lxml")
	texts = []
	# texts
	for txts in soup.find_all(find):
		texts.append(txts.getText())
	return texts

def walkto2(URL):
	r = requests.get(URL)
	data = r.text
	soup = bfs(data,"lxml")
	doors = []
	texts = []
	# links
	for link in soup.find_all('a'):
		doors.append(link.get('href'))
	# texts
	for txts in soup.find_all('p'):
		texts.append(txts.getText())
	return doors, texts

def make_replays_list(URL,_filter,_except):
	replays = walkto2(URL)[0]
	replays = [URL+r for r in replays if _filter in r and _except not in r]
	return replays

def crawl():
	msg("Retrieving replay list")
	history = open(HISTORYFILE).read().split('\n')
	rlist = make_replays_list(URL,'gen7ou','double')
	some = False
	for replay in rlist:
		if(replay not in history):
			some = True
			msg("Proceeding to extract log from: "+replay)
			####
			ta.exec_proc(replay)
			####
			msg("Adding replay to history file: "+HISTORYFILE)
			with open(HISTORYFILE,'a') as file2:
				file2.write(replay+'\n')
			history = open(HISTORYFILE).read().split('\n')
	if(some==False):
		msg("No new replay available")

def msg(message):
	print(message)

def main():
	msg('\n')
	msg("Loading configurations...")
	load_configs()
	msg("Starting process...")
	counter = 0
	while(True):
		counter += 1
		msg('\n')
		msg("Starting cycle "+str(counter))
		crawl()
		msg("Waiting "+str(DELAY)+" second(s)")
		time.sleep(int(DELAY))

main()
