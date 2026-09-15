import random
import os

os.mkdir("math_ex")

for i in range(100):
	f = open(f"math_ex/ex{i}.txt", "w")
	f.write("다음의 문제를 풀어서 제출하세요\n")
	f.write("이름:       점수:        \n\n")

	for k in range(10):
		x = random.randint(0, 100)
		y = random.randint(0, 100)
		op = random.choice("+-*/")
		f.write(f"{x} {op} {y} = \n")
	f.close()
