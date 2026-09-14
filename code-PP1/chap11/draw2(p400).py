from tkinter import *
import random

def drawRect(e):
	canvas.create_rectangle(e.x, e.y, e.x+random.randint(10, 100),  
				e.y+random.randint(5, 100), width=3, outline="blue")

def drawCircle(e):
	canvas.create_oval(e.x, e.y, e.x+random.randint(10, 100),  
				e.y+random.randint(5, 100), width=3, outline="red")

root = Tk()
canvas=Canvas(root, width=800, height=300, bg='white')
canvas.pack()

root.bind("<Button-1>", drawRect)
root.bind("<Button-3>", drawCircle)
root.mainloop()
