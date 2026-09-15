from tkinter import *

mode = "pen"
old_x = None
old_y = None
mycolor = "black"

def paint(event):	# 이전 점과 현재 점 사이를 직선으로 연결한다. 
    global mode, old_x, old_y
    fill_color = mycolor
    if   old_x and old_y:
        canvas.create_line(old_x, old_y, event.x, event.y,
                           capstyle=ROUND, width=10, fill=fill_color)
    old_x = event.x
    old_y = event.y

def reset(event):	# 사용자가 마우스 버튼에서 손을 떼면 이전 점을 삭제한다. 
    global old_x, old_y
    old_x, old_y = None, None
    
root = Tk()	

canvas = Canvas(root, bg='white', width=600, height=400)
canvas.pack()
canvas.bind('<B1-Motion>', paint)
canvas.bind('<ButtonRelease-1>', reset)

root.mainloop()
