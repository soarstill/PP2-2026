import turtle 
t = turtle.Turtle()		# t는 전역 변수가 된다. 
t.shape("turtle")
t.speed(0)

def f(x):
    return x**2+1

def changeColor():
    t.color("blue")		# 전역 변수 t를 사용한다. 

t.goto(200, 0)
t.goto(0, 0)
t.goto(0, 200)
t.goto(0, 0)

changeColor()
for x in range(150):
	t.goto(x, int(0.01*f(x)))

turtle.done()
