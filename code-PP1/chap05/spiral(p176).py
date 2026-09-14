import turtle 
import random

t = turtle.Turtle()
t.shape('turtle')
t.width(3)
t.speed(7)
colors = ['orange', 'red', 'violet', 'green', 'blue']

for i in range(100):
    t.color(random.choice(colors))	# 리스트 중에서 랜덤하게 하나를 선택한다.
    t.right(20 + i)
    t.forward(1 + (i * 6))
    t.right(30 + i)

turtle.done()
