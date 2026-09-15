from tkinter import *
root = Tk()

def process():
	if var1.get() == 1:
		label["text"] = "체크 박스 #1 선택"		
	else:
		label["text"] = "체크 박스 #1 선택 해제"		
		
var1 = IntVar()
Checkbutton(root, text="햄버거", variable=var1, command=process).pack()

label = Label(root, text="선택 안됨")
label.pack()
root.mainloop()
