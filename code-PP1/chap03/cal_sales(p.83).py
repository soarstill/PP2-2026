total_sales = 0
milk_count = int(input("판매된 우유의 개수: "))
cola_count = int(input("판매된 콜라의 개수: "))
krice_count = int(input("판매된 김밥의 개수: "))

total_sales += milk_count*2000
total_sales += cola_count*3000
total_sales += krice_count*3500

print(f"\n오늘 총 매출은 {total_sales}원입니다.") 
