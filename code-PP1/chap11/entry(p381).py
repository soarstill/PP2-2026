from tkinter import *				
root = Tk()					

def process():
		label["text"] = entry.get()+"가 입력됨"		

entry = Entry(root, fg="black", bg="yellow", width=20)
entry.pack()					

button = Button(root, text="입력 후 클릭하세요!", command=process)
button.pack()
label = Label(root, text="아무 것도 입력 안됨!")
label.pack()
window.mainloop()	
