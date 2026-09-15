from tkinter import *

root = Tk()
root.geometry("600x200") 

def callback(event):
    print(event.x, event.y, "에서 마우스 이벤트 발생")

root.bind("<Button-1>", callback)
root.mainloop()
