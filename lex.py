import sys
from re import compile

RESERVED = "RESERVED"
NUM = "NUM"
ID = "ID"

token_exprs = [
	(r'\s+',                   None),
	(r'=',                     RESERVED),
	(r'\(',                    RESERVED),
	(r'\)',                    RESERVED),
	(r'\+',                    RESERVED),
	(r'-',                     RESERVED),
	(r'\*',                    RESERVED),
	(r'/',                     RESERVED),
	(r'\^',                    RESERVED),
	(r'\.',                    RESERVED),
	(r'\d+(\.\d+)?',           NUM),
	(r'\w',                    ID),
]

def lex(expr):
	return lex_e(expr, token_exprs)

def lex_e(expr, token_exprs):
	pos = 0
	tokens = []
	while pos < len(expr):
		match = None
		for token_expr in token_exprs:
			pattern, tag = token_expr
			regex = compile(pattern)
			match = regex.match(expr, pos)
			if match:
				text = match.group(0)
				if tag:
					token = (text, tag)
					tokens.append(token)
				break
		if not match:
			sys.stderr.write("Illegal character: " + expr[pos] + "\n")
			sys.exit(1)
		else:
			pos = match.end(0)
	#print(tokens)
	return tokens