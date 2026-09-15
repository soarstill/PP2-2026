##
#	이 프로그램은 명왕성까지 빛이 가는 시간을 계산한다. 
#
speed = 300000.0			# 빛의 속도
distance = 4800000000.0		# 거리
secs = distance / speed		# 걸리는 시간, 단위는 초	
secs = int(secs)			# 부동소수점수->정수 변환
time = secs // 3600			# 초를 시간으로 변환, //은 정수 나눗셈
minute = (secs % 3600) // 60		# 남은 초를 분으로 변환
print(time, "시간", minute, "분")
