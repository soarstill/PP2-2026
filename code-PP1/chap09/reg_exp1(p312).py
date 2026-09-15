def checkNumber(phoneNumber):
	if len(phoneNumber) != 13:
		return False
	if phoneNumber[0:3] != '010':
		return False
	if phoneNumber[3] != '-':
		return False
	for i in range(4, 8):
		if not phoneNumber[i].isdecimal():
			return False
	if phoneNumber[8] != '-':
			return False
	for i in range(9, 13):
		if not phoneNumber[i].isdecimal():
			return False
	return True
print('010-8888-6666->', checkNumber('010-8888-6666'))
print('000-1111-abcd->', checkNumber('000-1111-abcd'))
