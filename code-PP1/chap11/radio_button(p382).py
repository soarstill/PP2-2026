from tkinter import *
root = Tk()

def process():
	if var1.get() == 1:
		label["text"] = "햄버거 선택"		
	elif var1.get() == 2:
		label["text"] = "피자 선택"		
	else:
		label["text"] = "김밥 선택"		
		
var1 = IntVar()
Radiobutton(root, text="햄버거", variable=var1, value=1, command=process).pack()
Radiobutton(root, text="피자", variable=var1, value=2, command=process).pack()
Radiobutton(root, text="김밥", variable=var1, value=3, command=process).pack()

label = Label(root, text="선택 안됨")
label.pack()
root.mainloop()
