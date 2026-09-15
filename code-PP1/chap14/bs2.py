from bs4 import BeautifulSoup
import requests
response = requests.get("http://www.kma.go.kr/weather/forecast/mid-term-rss3.jsp?stnId=109")
soup = BeautifulSoup(response.content, 'html.parser')
for data in soup.select("location"):
	print(data.select_one("city").get_text())
	print(data.select_one("wf").get_text())
	print(data.select_one("tmn").get_text())
	print(data.select_one("tmx").get_text())