# 생일 축하 프로그램
# 작성자: H.S.Song
# 작성일: 2024-06-05


#-----------------------
# 생일 축하 함수 정의
#-----------------------
def say_happy_birthday(name:str) -> None:
    '''
    주어진 이름에 대해 생일 축하 메시지를 출력함
    
    매개변수:
    name (str): 생일 축하 메시지를 출력할 사람의 이름
    반환값:
    None
    '''
    print("안녕하세요")
    print(name + "님의 생일을 축하합니다")
    return None




#--------------------------
# 테스트 함수 정의
#--------------------------

def test_happy_birthday() :
    '''
    여러 이름에 대해 생일 축하 메시지를 출력하는 테스트 함수 : 단순히 여러 이름을 개별적으로 호출하여 테스트함
    '''
    say_happy_birthday("해상")
    say_happy_birthday("주영")
    say_happy_birthday("성민")
    say_happy_birthday("현준")  
    
def test_happy_birthday2() :
    '''  
    여러 이름에 대해 생일 축하 메시지를 출력하는 테스트 함수
    리팩토링 : 여러 이름에 대해 반복적으로 생일 축하 메시지를 출력하도록 개선
    '''
    names = ["해상", "주영", "성민", "현준"]
    for name in names:
        say_happy_birthday(name)

def test_happy_birthday3() :
    '''
    여러 이름에 대해 생일 축하 메시지를 출력하는 테스트 함수 : 잘못된 타입의 입력에 대해 테스트함
    '''
    say_happy_birthday(3.14159)
    say_happy_birthday(100)
    say_happy_birthday([1,2,3])

if __name__ == "__main__":
    '''
    메인 함수 : 테스트 함수를 호출
    if 문은 이 파일이 직접 실행될 때만 메인 함수를 호출하도록 하는 역할을 함
    모듈을 import 할 때의 __name__ 값은 "__main__"이 아니고 
    모듈의 이름이 됨. 이 모듈의 이름은 "happy"임.
    작업폴더부터의 경로를 기준으로 하면 이 모듈의 이름은 "lab.week2.happy"임.
    '''
#    test_happy_birthday()
#    test_happy_birthday2()
    test_happy_birthday3()
