import tkinter as tk
import random

root = tk.Tk()
root.title("버튼으로 도형 그리기 예제")
root.geometry("700x500")

# --- 1. 왼쪽: 캔버스 도화지 배치 ---
canvas = tk.Canvas(root, bg="white", bd=1, relief="solid")
canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)

# --- 2. 오른쪽: 제어용 버튼 프레임 배치 ---
ctrl_frame = tk.LabelFrame(root, text="도형 생성기", padx=15, pady=15)
ctrl_frame.pack(side="right", fill="y", padx=10, pady=10)


# --- 🎨 무작위 속성 값을 반환하는 헬퍼 함수 ---
def get_random_props():
    # 캔버스 크기 범위 안에서 랜덤한 시작 좌표(x1, y1)와 크기(size) 결정
    x1 = random.randint(20, 350)
    y1 = random.randint(20, 350)
    size = random.randint(40, 100)
    
    # 랜덤 색상 추출
    colors = ["#FF5733", "#33FF57", "#3357FF", "#F3FF33", "#FF33F3", "#33FFF0", "#FFAF33"]
    color = random.choice(colors)
    
    return x1, y1, size, color


# --- 🛠️ 각 도형 생성용 이벤트 함수 ---

def draw_line():
    x1, y1, size, color = get_random_props()
    # 직선 생성 (x1, y1) -> (x1 + size, y1 + size)
    canvas.create_line(x1, y1, x1 + size, y1 + size, fill=color, width=3)

def draw_rectangle():
    x1, y1, size, color = get_random_props()
    # 사각형 생성
    canvas.create_rectangle(x1, y1, x1 + size, y1 + size, fill=color, outline="black")

def draw_oval():
    x1, y1, size, color = get_random_props()
    # 원 생성 (가로세로 크기를 같게 주어 정원 생성)
    canvas.create_oval(x1, y1, x1 + size, y1 + size, fill=color, outline="black")

def draw_polygon():
    x1, y1, size, color = get_random_props()
    # 삼각형 꼭짓점 3개 좌표 계산
    points = [x1, y1 + size, x1 + (size // 2), y1, x1 + size, y1 + size]
    canvas.create_polygon(points, fill=color, outline="black")

def draw_text():
    x1, y1, _, color = get_random_props()
    canvas.create_text(x1, y1, text="✨ 짜잔!", font=("Arial", 14, "bold"), fill=color)

def clear_canvas():
    # 도화지 전체 싹 비우기
    canvas.delete("all")


# --- 🎛️ 사이드바에 버튼 배치 ---
tk.Button(ctrl_frame, text="➖ 선 그리기", command=draw_line, width=15).pack(pady=8)
tk.Button(ctrl_frame, text="⬛ 사각형 그리기", command=draw_rectangle, width=15).pack(pady=8)
tk.Button(ctrl_frame, text="🔮 원 그리기", command=draw_oval, width=15).pack(pady=8)
tk.Button(ctrl_frame, text="🔺 삼각형 그리기", command=draw_polygon, width=15).pack(pady=8)
tk.Button(ctrl_frame, text="🔤 글자 쓰기", command=draw_text, width=15).pack(pady=8)

# 구분선 역할을 할 빈 라벨
tk.Label(ctrl_frame).pack(pady=10)

tk.Button(ctrl_frame, text="🧹 화면 비우기", command=clear_canvas, width=15, bg="lightcoral", fg="white").pack(pady=5)

root.mainloop()
