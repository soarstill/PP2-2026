import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv("sales_data.csv") # CSV 파일을 읽는다.
monthList = df ['month'].tolist() # "month" 열을 추출하여서 리스트로 만든다.
tvData = df ['tv'].tolist() # "tv" 열을 추출하여서 리스트로 만든다.
laptopData = df ['laptop'].tolist()
phoneData = df ['phone'].tolist()
# 각 리스트를 하나의 그래프에 중첩해서 그린다. 마커도 사용한다.
plt.plot(monthList, tvData, label = 'tv sales', marker='o', linewidth=3)
plt.plot(monthList, laptopData, label = 'laptop sales', marker='o', linewidth=3)
plt.plot(monthList, phoneData, label = 'phone sales', marker='o', linewidth=3)
# 그래프의 레이블, 레전드, 눈금을 설정한다.
plt.xlabel('month')
plt.ylabel('unit')
plt.legend(loc='upper left')
plt.xticks(monthList)
plt.yticks([1000, 2000])
plt.title('Sales Data')
plt.show()