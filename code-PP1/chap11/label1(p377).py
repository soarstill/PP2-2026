from tkinter import *				# tkinter 모듈을 포함

root = Tk()					# 루트 윈도우를 생성
root.geometry("500x200") 			# Width x Height
label = Label(root, text="Hello tkinter")	# 레이블 위젯을 생성
label.pack()					# 레이블 위젯을 윈도우에 배치

root.mainloop()				# 윈도우가 사용자 동작을 대기
