from bs4 import BeautifulSoup
import requests
import openpyxl, smtplib, sys
from email.mime.text import MIMEText

response = requests.get("http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=1159068000")
soup = BeautifulSoup(response.content, 'html.parser')

weather = (soup.select('wfEn')[0]).text
temperature = (soup.select('temp')[0]).text
print(weather)
print(temperature)

if weather == "Rain" or weather == "Snow":
    session = smtplib.SMTP_SSL('smtp.naver.com', 465)
    session.ehlo()
    session.login('abc@naver.com', 'password') # 자신의 아이디와 패스워드로 변경

    msg = MIMEText('비가 온다고 합니다.\n 우산을 준비하세요!\n 감사합니다.')
    msg['Subject']='우산 준비!'
    msg['From']='abc@naver.com' # 변경하여야 함!
    msg['To']='abc@naver.com'
    print('abc@naver.com에게 이메일을 보내는 중입니다.')
    status = session.sendmail('abc@naver.com', 'abc@naver.com', msg.as_string())
    if status != {}:
        print(f'abc@naver.com 이메일 전송에서 문제 {status}가 발생하였습니다.' )
    session.quit()
