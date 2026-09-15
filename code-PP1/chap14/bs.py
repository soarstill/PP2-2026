from bs4 import BeautifulSoup
import requests
response = requests.get("http://www.kma.go.kr/weather/forecast/mid-term-rss3.jsp?stnId=109")
print(response.text)