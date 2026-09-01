import matplotlib.pylab as plt
from sklearn import linear_model

reg = linear_model.LinearRegression()

X = [ [10.0], [12.0], [14.0], [16.0], [18.0],
[20.0], [22.0], [24.0], [26.0], [28.0] ] # 기온(℃)
y = [15, 18, 22, 25, 30, 32, 35, 40, 43, 47] # 아이스크림 판매량(임의 수치)

reg.fit(X, y) # 학습 수행
plt.scatter(X, y, color='black') # 학습 데이터 산포도 출력

y_pred = reg.predict(X) # 예측값 계산
plt.plot(X, y_pred, color='blue', linewidth=3) # 예측 직선 출력

plt.title("Temperature vs Ice Cream Sales") # 그래프 제목/라벨
plt.xlabel("Temperature (°C)")
plt.ylabel("Sales")
plt.show() # 그래프 보여주기

temp = float(input("기온을 입력하세요: "))
print("예상 판매량:", reg.predict([[temp]])[0])
