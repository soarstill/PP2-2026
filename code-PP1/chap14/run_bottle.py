import sqlite3
from bottle import route, run
 
@route('/')
def itemlist():			# 웹 메인 페이지를 반환한다. 
    con = sqlite3.connect('inventory.db')
    cur = con.cursor()
    
    html = "<h1> 재고 리스트</h1>"
    cur.execute("SELECT * FROM stock")
    result = cur.fetchall()

    for row in result:
        html += "<li>"+ row[0] + ": " + str(row[1]) + "개 </li>\n"

    con.close()
    return html

run()				# 웹서버 실행