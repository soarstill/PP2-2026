gx = 100

def func1() :
    print("func1() :", gx)

def func2() :
    global gx			# 전역 변수 gx를 사용하겠음
    gx = 200			# 전역 변수 gx가 200으로 변경
    print("func2() :", gx)

myfunc1()
myfunc2()
print("외부: ", gx)
