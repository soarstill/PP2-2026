import re

def check():
    while True:
        password = input("패스워드를 입력하시오: ")
        if len(password) < 8:
            print("패스워드는 최소한 8글자이어야 합니다.")
        elif re.search('[0-9]', password) is None:
            print("패스워드는 적어도 하나의 숫자를 가져야 합니다.") 
        elif re.search('[A-Z]', password) is None: 
            print("패스워드는 적어도 대문자를 가져야 합니다.") 
        else:
            print("규정에 맞는 패스워드입니다.")
            break

check()
