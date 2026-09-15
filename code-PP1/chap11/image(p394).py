from tkinter import *
root = Tk()

canvas = Canvas(root,  width=500, height=300)
canvas.pack()

img = PhotoImage(file="starship.png")
canvas.create_image(20, 20, anchor=NW, image=img)

root.mainloop()
