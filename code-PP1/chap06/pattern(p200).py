import random

def printPattern(rows=5, char="#"):
	for _ in range(rows):
		for _ in range(5):
			print(char, end="")
		print()

printPattern(5, "A")
printPattern(3)
