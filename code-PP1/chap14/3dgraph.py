from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt

# 3차원 축(axis)을 얻는다. 
axis = plt.axes(projection='3d')

# 3차원 데이터를 넘파이 배열로 생성한다. 
Z = np.linspace(0, 1, 100)		# 0에서 1까지 100개의 순차 데이터 생성
X = Z * np.sin(30 * Z)			# sin() 함수 적용
Y = Z * np.cos(30 * Z)			# cos() 함수 적용	

# 3차원 그래프를 그린다. 
axis.plot3D(X, Y, Z)	
plt.show()

