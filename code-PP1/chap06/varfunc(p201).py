def varfunc(*args ):   
	print (args)

print("하나의 값으로 호출")
varfunc(10)
print("여러 개의 값으로 호출")
varfunc(10, 20, 30)

def add(*numbers) :
	sum = 0
	for n in numbers:
		sum = sum + n
	return sum

print(add(10, 20))
print(add(10, 20, 30))
