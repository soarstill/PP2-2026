import tkinter as tk
from tkinter import messagebox, ttk


def on_button_click(name):
    messagebox.showinfo("알림", f"'{name}' 버튼이 눌렸습니다.")


root = tk.Tk()
root.title("Widgets Test")
root.geometry("620x720")
root.configure(bg="#CECAD3")

menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)

pad_opts = {"padx": 10, "pady": 6}

# Row 1: Button and checkboxes
lbl_button = tk.Label(root, text="Button:", bg="#D4D0C8", anchor="w")
lbl_button.grid(row=0, column=0, sticky="w", **pad_opts)

btn_sample = tk.Button(
    root,
    text="Button",
    width=12,
    relief="raised",
    command=lambda: on_button_click("Button"),
)
btn_sample.grid(row=0, column=1, sticky="w", **pad_opts)

chk_frame = tk.Frame(root, bg="#D4D0C8")
chk_frame.grid(row=0, column=2, rowspan=3, sticky="nw", padx=30, pady=5)

chk_enabled = tk.Checkbutton(chk_frame, text="Enabled", bg="#D4D0C8")
chk_enabled.select()
chk_enabled.pack(anchor="w", pady=2)

chk_visible = tk.Checkbutton(chk_frame, text="Visible", bg="#D4D0C8")
chk_visible.select()
chk_visible.pack(anchor="w", pady=2)

chk_editable = tk.Checkbutton(chk_frame, text="Editable", bg="#D4D0C8")
chk_editable.select()
chk_editable.pack(anchor="w", pady=2)

# Row 2: TextField
lbl_textfield = tk.Label(root, text="TextField:", bg="#D4D0C8", anchor="w")
lbl_textfield.grid(row=1, column=0, sticky="w", **pad_opts)

entry_text = tk.Entry(root, width=30, relief="sunken")
entry_text.grid(row=1, column=1, sticky="w", **pad_opts)


def on_enter(event=None):
    messagebox.showinfo("입력값", f"입력된 값: {entry_text.get()}")


entry_text.bind("<Return>", on_enter)

'''
Entry 위젯 이벤트 예시:
entry_text.bind("<Button-1>", on_click)
entry_text.bind("<ButtonRelease-1>", on_release)
entry_text.bind("<Double-Button-1>", on_double)
entry_text.bind("<Button-3>", on_right)
entry_text.bind("<B1-Motion>", on_drag)
entry_text.bind("<MouseWheel>", on_wheel)
entry_text.bind("<Enter>", on_mouse_in)
entry_text.bind("<Leave>", on_mouse_out)
entry_text.bind("<FocusIn>", on_focus_in)
entry_text.bind("<FocusOut>", on_focus_out)
'''

# Row 3: PasswordField
lbl_password = tk.Label(root, text="PasswordField:", bg="#D4D0C8", anchor="w")
lbl_password.grid(row=2, column=0, sticky="w", **pad_opts)

entry_pass = tk.Entry(root, width=30, show="*", relief="sunken")
entry_pass.grid(row=2, column=1, sticky="w", **pad_opts)

# Row 4: TextArea and attribute buttons
lbl_textarea = tk.Label(root, text="TextArea:", bg="#D4D0C8", anchor="w")
lbl_textarea.grid(row=3, column=0, sticky="nw", **pad_opts)

txt_frame = tk.Frame(root)
txt_frame.grid(row=3, column=1, sticky="w", **pad_opts)

scrollbar = tk.Scrollbar(txt_frame)
scrollbar.pack(side="right", fill="y")

text_area = tk.Text(
    txt_frame,
    width=28,
    height=7,
    relief="sunken",
    yscrollcommand=scrollbar.set,
)
text_area.insert(
    "1.0",
    "Use the checkboxes and\n"
    "buttons on the right to set the\n"
    "attributes of the widgets on the\n"
    "left.\n\n"
    "The font support is not hooked\n"
    "up yet.",
)
text_area.pack(side="left", fill="both")
scrollbar.config(command=text_area.yview)

btn_frame = tk.Frame(root, bg="#D4D0C8")
btn_frame.grid(row=3, column=2, sticky="nw", padx=30, pady=5)

buttons = [
    "BackgroundColor",
    "ForegroundColor",
    "Font",
    "ToolTip",
    "Background BackgroundColor",
]
for btn_text in buttons:
    button = tk.Button(
        btn_frame,
        text=btn_text,
        width=22,
        relief="raised",
        command=lambda name=btn_text: on_button_click(name),
    )
    button.pack(pady=3, anchor="w")

# Row 5: StaticText
lbl_static_lbl = tk.Label(root, text="StaticText:", bg="#D4D0C8", anchor="w")
lbl_static_lbl.grid(row=4, column=0, sticky="w", **pad_opts)

lbl_static_val = tk.Label(root, text="StaticText", bg="#D4D0C8")
lbl_static_val.grid(row=4, column=1, sticky="w", **pad_opts)

# Row 6: CheckBox
lbl_checkbox_lbl = tk.Label(root, text="CheckBox:", bg="#D4D0C8", anchor="w")
lbl_checkbox_lbl.grid(row=5, column=0, sticky="w", **pad_opts)

chk_sample = tk.Checkbutton(root, text="CheckBox", bg="#D4D0C8")
chk_sample.grid(row=5, column=1, sticky="w", **pad_opts)

# Row 7: RadioGroup and image area
lbl_radiogroup = tk.Label(root, text="RadioGroup:", bg="#D4D0C8", anchor="w")
lbl_radiogroup.grid(row=6, column=0, sticky="nw", **pad_opts)

radio_frame = tk.LabelFrame(
    root,
    text="A RadioBox",
    bg="#D4D0C8",
    padx=10,
    pady=5,
)
radio_frame.grid(row=6, column=1, sticky="w", **pad_opts)

radio_var = tk.StringVar(value="one")
r1 = tk.Radiobutton(
    radio_frame, text="one", value="one", variable=radio_var, bg="#D4D0C8"
)
r2 = tk.Radiobutton(
    radio_frame, text="two", value="two", variable=radio_var, bg="#D4D0C8"
)
r3 = tk.Radiobutton(
    radio_frame, text="three", value="three", variable=radio_var, bg="#D4D0C8"
)
r1.pack(anchor="w")
r2.pack(anchor="w")
r3.pack(anchor="w")

lbl_image = tk.Label(root, text="Image:", bg="#D4D0C8")
lbl_image.grid(row=6, column=2, sticky="nw", padx=30, pady=5)

canvas_img = tk.Canvas(
    root,
    width=100,
    height=100,
    bg="#A0B0C0",
    highlightthickness=1,
    highlightbackground="gray",
)
canvas_img.grid(row=6, column=2, sticky="nw", padx=90, pady=5)

for i in range(0, 100, 10):
    canvas_img.create_line(i, 0, i, 100, fill="#B0C0D0")
    canvas_img.create_line(0, i, 100, i, fill="#B0C0D0")

# Row 8: Choice and ImageButton
lbl_choice = tk.Label(root, text="Choice:", bg="#D4D0C8", anchor="w")
lbl_choice.grid(row=7, column=0, sticky="w", **pad_opts)

combo_choice = ttk.Combobox(
    root,
    values=["one", "two", "three"],
    width=8,
    state="readonly",
)
combo_choice.set("two")
combo_choice.grid(row=7, column=1, sticky="w", **pad_opts)

lbl_imgbtn = tk.Label(root, text="ImageButton:", bg="#D4D0C8")
lbl_imgbtn.grid(row=7, column=2, sticky="w", padx=30, pady=5)

edit_icon = tk.PhotoImage(file="edit_icon.png")
btn_edit = tk.Button(
    root,
    text=" edit",
    image=edit_icon,
    compound="left",
    width=80,
    bg="#6A6A9B",
    fg="white",
    relief="raised",
    command=lambda: on_button_click("edit"),
)
btn_edit.image = edit_icon
btn_edit.grid(row=7, column=2, sticky="w", padx=120, pady=5)

# Row 9: List and borderless TextField label
lbl_list = tk.Label(root, text="List:", bg="#D4D0C8", anchor="w")
lbl_list.grid(row=8, column=0, sticky="nw", **pad_opts)

listbox = tk.Listbox(root, width=10, height=4, relief="sunken")
for item in ["one", "two", "three"]:
    listbox.insert("end", item)
listbox.select_set(2)
listbox.grid(row=8, column=1, sticky="w", **pad_opts)

lbl_noborder = tk.Label(root, text="TextField with no border", bg="#D4D0C8")
lbl_noborder.grid(row=8, column=2, sticky="nw", padx=30, pady=5)

# Row 10: Slider
lbl_slider = tk.Label(root, text="Slider:", bg="#D4D0C8", anchor="w")
lbl_slider.grid(row=9, column=0, sticky="w", **pad_opts)

slider = tk.Scale(
    root,
    from_=0,
    to=100,
    orient="horizontal",
    showvalue=False,
    width=10,
    length=200,
    bg="#D4D0C8",
    bd=1,
)
slider.set(20)
slider.grid(row=9, column=1, columnspan=2, sticky="w", **pad_opts)

lbl_percent = tk.Label(
    root,
    bg="#D4D0C8",
    fg="#333333",
    font=("맑은 고딕", 8, "bold"),
)


def on_slide(value=None):
    value = slider.get()
    from_value = float(slider.cget("from"))
    to_value = float(slider.cget("to"))
    percent = (
        (value - from_value)
        / (to_value - from_value)
        * 100
    )
    lbl_percent.config(text=f"{percent:.0f}%")
    x, _ = slider.coords(value)
    lbl_percent.place(
        x=slider.winfo_x() + x,
        y=slider.winfo_y() - 2,
        anchor="s",
    )


slider.config(command=on_slide)
root.update_idletasks()
on_slide()

# Row 11: StaticLine
lbl_line = tk.Label(root, text="StaticLine:", bg="#D4D0C8", anchor="w")
lbl_line.grid(row=10, column=0, sticky="w", **pad_opts)

sep_line = tk.Frame(root, height=2, bd=1, relief="sunken", bg="gray")
sep_line.grid(row=10, column=1, columnspan=2, sticky="we", padx=10, pady=10)

# Show a tooltip with the widget's variable name when clicked.
var_names = {
    str(widget): name
    for name, widget in list(globals().items())
    if isinstance(widget, tk.Widget)
}
tip = {"win": None, "job": None}


def hide_tip():
    if tip["job"]:
        root.after_cancel(tip["job"])
        tip["job"] = None
    if tip["win"]:
        tip["win"].destroy()
        tip["win"] = None


def show_tip(event):
    widget = event.widget
    name = var_names.get(str(widget), widget.winfo_class())
    if "text" in widget.keys() and widget.cget("text"):
        name += f" ({widget.cget('text')})"

    hide_tip()
    window = tk.Toplevel(root)
    window.wm_overrideredirect(True)
    window.wm_geometry(f"+{event.x_root + 12}+{event.y_root + 12}")
    tk.Label(
        window,
        text=name,
        bg="#FFFFE0",
        relief="solid",
        bd=1,
        padx=6,
        pady=2,
    ).pack()
    tip["win"] = window
    tip["job"] = root.after(1500, hide_tip)


def bind_tips(widget):
    widget.bind("<Button-1>", show_tip, add="+")
    for child in widget.winfo_children():
        bind_tips(child)


for child in root.winfo_children():
    bind_tips(child)

root.mainloop()
