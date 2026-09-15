f = open("test.txt", "w")
f.write("파이썬은 강력합니다.\n")
f.close()



f = open("test.txt", "r")
s = f.read()
f.close()
