from tkinter import *

# 이벤트 처리 함수를 정의한다. 
def process():
    tf = float(e1.get())		# e1에서 문자열을 읽어서 부동소수점형으로 변경
    tc = (tf-32.0)*5.0/9.0		# 화씨 온도를 섭씨 온도로 변환한다. 
    e2.delete(0, END)			# 처음부터 끝까지 지운다.
    e2.insert(0, str(tc))		# tc 변수의 값을 문자열로 변환하여 추가한다.
    
root  = Tk()

Label(root , text="화씨").grid(row=0, column=0)
Label(root, text="섭씨").grid(row=1, column=0)

e1 = Entry(root)
e2 = Entry(root)
e1.grid(row=0, column=1)
e2.grid(row=1, column=1)

Button(root, text="화씨->섭씨", command=process).grid(row=2, column=1)
root.mainloop()
