shipping_cost = ( 0 if price >= 20000 else 3000 )

absolute_value = (x if x > 0 else -x)	// 절대값 계산
max_value = (x if x > y else y)		// 최대값 계산
min_value = (x if x < y else y)		// 최소값 계산


x = int(input("첫 번째 수 ="))
y = int(input("두 번째 수 ="))
max_value = (x if x > y else y)
min_value = (y if x > y else x)
print("큰 수=", max_value, "작은 수=", min_value)
