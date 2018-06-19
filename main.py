from parse import lex

if __name__ == "__main__":
	s = ""
	print("Type 'exit' to stop")
	while (s.lower() != "exit"):
		s = input("> ")
		lex(s)