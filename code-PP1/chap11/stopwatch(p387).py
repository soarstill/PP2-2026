from tkinter import *

root = Tk()

counter = 0

def clicked():
    global counter
    counter += 1
    label['text'] = '버튼 클릭 횟수: ' + str(counter)
        
label = Label(root, text="아직 눌려지지 않음")
label.pack()
button = Button(root, text="증가", command=clicked)
button.pack()

root.mainloop()
