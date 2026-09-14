from tkinter import *
from tkinter import filedialog

def FileOpen():
    filename = filedialog.askopenfilename(parent=root,
                                          filetypes=(("JPG files", "*.jpg"),
                                          ("all files", "*.*")))
    print(filename)
   
root = Tk()

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New")
filemenu.add_command(label="Open", command=FileOpen)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

root.config(menu=menubar)
root.mainloop()
