import sqlite3

con = sqlite3.connect('test.db')
cur = con.cursor()
for row in cur.execute('SELECT * FROM product ORDER BY price'):
	print(row)
