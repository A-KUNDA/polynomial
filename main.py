import sys
from lex import lex
from ast import parse

if __name__ == "__main__":
	text = ""
	print("Type 'exit' or 'quit' to stop")
	while (True):
		text = input("> ")
		if text.lower() in ("exit", "quit"):
			break
		tokens = lex(text)
		#print(tokens)
		parse_result = parse(tokens)
		#print(parse_result)
		if not parse_result:
			sys.stderr.write("Parse Error!\\n")
			sys.exit(1)
		ast = parse_result.value
		env = {}
		#print(parse_result)
		#print(ast)
		print(ast.eval(env))