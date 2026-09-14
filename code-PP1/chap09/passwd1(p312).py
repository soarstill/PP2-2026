while True:
	print('새로운 패스워드를 선택하시오 (문자와 숫자만 가능)')
	password = input()
	if password.isalnum():
		break
	print('문자와 숫자만을 이용하여 패스워드를 선택하시오.')
