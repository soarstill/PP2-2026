from tkinter import *				
root = Tk()					

label1 = Label(root,    text="안녕하세요?",	bg="yellow",    fg="blue",
		  	width=80,    height=2    )
label2 = Label(root,    text="파이썬을 공부합니다.",	font=("궁서체", 32))

label1.pack()					
label2.pack()					
root.mainloop()
