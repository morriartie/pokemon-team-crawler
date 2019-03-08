COMMENT_CHAR = '#'
OPTION_CHAR = '='

def parse_conf(file):
	options = {}
	f = open(file)
	for line in f:
		if COMMENT_CHAR in line:
			line, comment = line.split(COMMENT_CHAR)
		if OPTION_CHAR in line:
			option, value = line.split(OPTION_CHAR)
			option = option.strip()
			value = value.strip()
			options[option] = value
	f.close()
	return options