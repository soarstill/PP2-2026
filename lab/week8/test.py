
with open("sample.txt", "r",encoding="utf-8") as f:
    line = f.readline().strip()
    words = line.split()
    print(words ) # 첫줄을 단어단위로 분리한 후 리스트로 출력