#
# 연락처 관리프로그램
# 기능:
# 1. 연락처 추가
# 2. 연락처 삭제
# 3. 연락처 검색
# 4. 연락처 목록 보기
# 5. 연락처 수정
# 6. 프로그램 종료

# 데이터구조: 
# 연락처는 딕셔너리로 관리하며, 키는 전화번호, 값은 이름, 키, 몸무게으로 구성
# 예: contacts = {"010-1234-5678": {"이름": "홍길동", "키": 175, "몸무게": 70}}

contacts = {}

# 연락처 추가 함수
def add_contact(phone, name, height, weight):
    contacts[phone] = {"이름": name, "키": height, "몸무게": weight}
    return contacts[phone]

# 연락처 삭제 함수
def delete_contact(phone):
    if phone in contacts:
        del contacts[phone]

# 연락처 검색 함수
def search_contact(phone):
    return contacts.get(phone, None)

# 연락처 검색 by 이름 함수 : typehint 포함
def search_contact_by_name(name: str) -> dict:
    result = {}
    for phone, info in contacts.items():
        if info["이름"] == name:
            result[phone] = info
    return result

# 연락처 목록 보기 함수
def list_contacts():
    return contacts

# 연락처 수정 함수
def update_contact(phone, name=None, height=None, weight=None):
    if phone in contacts:
        if name is not None:
            contacts[phone]["이름"] = name
        if height is not None:
            contacts[phone]["키"] = height
        if weight is not None:
            contacts[phone]["몸무게"] = weight
    return contacts.get(phone, None)

# 프로그램 종료 함수
def exit_program():
    print("프로그램을 종료합니다.")
    exit()