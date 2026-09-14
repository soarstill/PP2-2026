gx = 100

def func1() :
    print("func1() :", gx)

def func2() :
    gx = 200			# 여기서 지역 변수 gx가 생성된다. 
    print("func2() :", gx)	# 지역 변수 gx를 사용한다. 

myfunc1()
myfunc2()
print("외부: ", gx)
