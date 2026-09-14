aList  =[1,2,3,4,5,1,2 ]
result ={ x for x in aList if x%2==0 }
print(result)

A ={"apple","banana","grape"}
B ={"apple","banana","grape","kiwi"}

if A < B : 			# 또는 A.issubset(B) :
	print("A는 B의 부분 집합입니다.")
