s1=input("첫 번째 문자열:")
s2=input("두 번째 문자열:")

s1 = s1.lower()		# 문자열을 소문자로 만드는 메소드, 9장 참조
s2 = s2.lower()
list1 = s1.split(" ")		# 문자열을 단어로 분리하는 메소드, 9장 참조
list2 = s2.split(" ")

total = len(list1)		# 단어의 개수
n = len(list(set(list1)&set(list2)))	# 세트 교집합으로 공통 단어 개수 계산

print(f"\n표절률 = {100*n/total}")
