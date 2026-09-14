# 정상적인 파이썬 함수
def func1(x):
	return x + 10

# 람다 함수
func2 = lambda x : x + 10

result = func1(2)
print(result)
result = func2(2)
print(result)

func = lambda x, y : x + y
result = func(2, 3)
print(result)

myList = [1, 2, 3, 4, 5, 6, 7, 8, 9]
result = map(lambda x: x**2, myList) # [1, 4, 9, 16, 25, 36, 49, 64, 81]