import matplotlib.pyplot as plt

Y = [38, 22, 15, 25]
labels = ["Apples", "Pear", "Strawberry", "Cherries"]
explode = [0.1, 0, 0, 0]					

plt.pie(Y, labels = labels, explode = explode)	# 파이 챠트
plt.show() 