from io import BytesIO
from tokenize import tokenize
# change this to smaller custom files later

def lex(expr):
	t = tokenize(BytesIO(expr.encode('utf-8')).readline)
	tokens = [token[1] for token in t if token[1]]
	print(tokens)