import turtle

def main():
    print("hello")

#삼각형 그리기
t = turtle.Turtle()
t.shape("turtle")
t.speed(2)
t.color("red")
t.forward(100)
t.left(120)
t.forward(100)
t.left(120)
t.forward(100)
t.left(120)

## 다각형 그리기
def polygone(length, edges_number):
    for i in range(edges_number):
        t.forward(length)
        t.left(360 / edges_number)

t.penup()  # 펜을 들어서 이동할 때 선이 그려지지 않도록 함
t.goto(-200, 0)  # 거북이 위치 이동
t.pendown()  # 펜을 내려서 이동할 때 선이 그려지도록 함
polygone(100, 5)  # 오각형 그리기

turtle.done()

if __name__ == "__main__":
    main()