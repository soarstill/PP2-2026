import tkinter as tk

window = tk.Tk()
window.title("Hello 송해상")
window.geometry("400x200")

label = tk.Label(window, text="Hello, GUI!")
label.pack()

window.mainloop()