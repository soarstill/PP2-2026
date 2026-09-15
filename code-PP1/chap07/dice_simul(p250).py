import matplotlib.pyplot as plt
import random

values = [random.randint(0, 5) for i in range(600)]

faces = [ 1, 2, 3, 4, 5, 6 ]
rolls = [ 0, 0, 0, 0, 0, 0 ]

for x in values :
	rolls[x] = rolls[x] + 1

plt.bar(faces, rolls)			# 리스트에 저장된 값으로 그래프를 그린다. 
plt.show()				# 그래프를 화면에 출력한다. 
