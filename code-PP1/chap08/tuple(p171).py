single_tuple = ("apple",) # 쉼표가 끝에 있어야 한다.
no_tuple = ("apple") # 쉼표가 없으면 튜플이 아니라 수식이 된다.
fruits = ("apple", "banana", "grape")
for f in fruits:
	print(f, end=" ") # apple banana grape 출력