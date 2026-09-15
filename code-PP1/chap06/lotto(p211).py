import random

def getLotto() : 
	myList = []		# 공백 리스트 생성
	while len(myList) != 6:	# 6개의 숫자가 생성될 때까지 반복
		number = random.randint(1, 45)	# 1부터 45 사이의 난수 생성
		if number not in myList: 	# 리스트에 숫자가 없으면 
			myList.append(number)	# 리스트에 난수를 추가
	return myList 			# 리스트를 반환한다. 

lottoList = getLotto()
print(lottoList)
