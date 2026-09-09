#
# 생일 축하 함수
#
def say_happy_birthday(name:str) -> None:
    print("안녕하세요")
    print(name + "님의 생일을 축하합니다")
    return None

def test_happy_birthday() :
    say_happy_birthday("해상")
    say_happy_birthday("주영")
    say_happy_birthday("성민")
    say_happy_birthday("현준")  
    
def test_happy_birthday2() :
    names = ["해상", "주영", "성민", "현준"]
    for name in names:
        say_happy_birthday(name)

def test_happy_birthday3() :
    say_happy_birthday(3.14159)
    say_happy_birthday(100)
    say_happy_birthday([1,2,3])

if __name__ == "__main__":
#    test_happy_birthday()
#    test_happy_birthday2()
    test_happy_birthday3()
