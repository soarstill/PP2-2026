import turtle			# (1)

t = turtle.Turtle()		# (2)
t.shape("turtle")		# (3)

t.color("blue")		# (4)
t.forward(100)			# (4)
t.left(90)			# (5)
t.forward(50)
t.backward(100)


screen = turtle.Screen()
screen.onclick(lambda x, y: screen.bye())
	
turtle.mainloop()		# (6)