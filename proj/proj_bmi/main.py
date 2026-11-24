"""BMI 정보 관리 프로그램의 실행 진입점입니다.

AI 사용 정보
AI: Copilot (Copilot SDK in VS Code)
목적: BMI 정보 관리 프로그램의 실행 진입점 구현
프롬프트: "객체지향. HealthRecord, HealthManager, HealthGUI 등의 역할 분담."
작성자: [제출 전 본인 이름 기입]
날짜: 2026-11-24
"""

import tkinter as tk

from modules.health_db import StorageError
from modules.health_gui import HealthGUI
from modules.health_logic import HealthManager


def main() -> None:
    """관리자와 Tkinter GUI를 준비하고 이벤트 루프를 실행합니다."""
    root = tk.Tk()
    startup_error = None
    try:
        manager = HealthManager()
    except StorageError as exc:
        manager = HealthManager(auto_load=False)
        startup_error = str(exc)

    HealthGUI(root, manager, startup_error=startup_error)
    root.mainloop()


if __name__ == "__main__":
    main()
