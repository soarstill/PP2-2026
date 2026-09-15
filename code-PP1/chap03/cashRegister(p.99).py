price = int(input("상품의 가격: "))
amount = int(input("상품의 개수: "))
disRate = int(input("할인율(%): "))/100.0

print()
payment = int(input("받은 금액: "))
total = price*amount
change = payment - (total - total*disRate)

# 결과를 출력한다. 
print(f"거스름돈: {int(change)}")		# change를 정수형으로 변환
