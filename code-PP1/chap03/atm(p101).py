##
#	이 프로그램은 자판기에서 거스름돈을 계산한다.  
#
price = int(input("물건값을 입력하시오: "))
payment = int(input("받은 금액: "))

change = payment - price

print("\n거스름돈은 아래와 같습니다.")
# 거스름돈(500원 동전 개수)을 계산한다. 
nCoin500 = change//500
change = change%500

# 거스름돈(100원 동전 개수)을 계산한다. 
nCoin100 = change//100
change = change%100

# 거스름돈(10원 동전 개수)을 계산한다. 
nCoin10 = change//10
change = change%10

# 거스름돈(1원 동전 개수)을 계산한다. 
nCoin1 = change

print(f"500원={nCoin500}개 100원={nCoin100}개 10원={nCoin10}개 1원={nCoin1}개") 
