##
#	이 프로그램은 중첩 반복문을 사용하여서 모든 조합을 출력한다. 
#
coffee = [ "Americano" , "Latte" , "Mocha" ] 
cake = [ "CheeseCake" , "StrawberryCake", "ChocolateCake" ]

for co in coffee:
    for ca in cake:
        print(co + " " + ca)
