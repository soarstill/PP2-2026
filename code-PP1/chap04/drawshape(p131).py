import turtle
t = turtle.Turtle()
t.shape("turtle")

s = input("도형을 입력하시오: ")

if s == "사각형" :
    w = int(input("가로 길이"))
    h = int(input("세로 길이"))
    color = input("색상")
    t.pencolor(color)
    t.forward(w)
    t.left(90)
    t.forward(h)
    t.left(90)
    t.forward(w)
    t.left(90)
    t.forward(h)

turtle.done()
