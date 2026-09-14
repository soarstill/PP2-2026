import re

pattern = r'010-\d\d\d\d-\d\d\d\d'
found = re.search(pattern, '제 휴대폰 번호는 010-1234-5678입니다.')
print('발견된 휴대폰 번호: ' + found.group())
