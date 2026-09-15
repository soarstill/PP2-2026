from tkinter import *
from tkinter import filedialog

def FileOpen():
    global img
    filename = filedialog.askopenfilename(parent=root,
                                          filetypes=(("PNG files", "*.png"),
                                          ("all files", "*.*")))
    img = PhotoImage(file=filename)
    canvas.create_image(20, 20, anchor=NW, image=img)
   
root = Tk()
canvas = Canvas(root,  width=500, height=150)
canvas.pack()
img = None		# 이미지 객체를 가르키는 변수가 미리 생성되어 있어야 한다. 

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New")
filemenu.add_command(label="Open", command=FileOpen)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

root.config(menu=menubar)
root.mainloop()
