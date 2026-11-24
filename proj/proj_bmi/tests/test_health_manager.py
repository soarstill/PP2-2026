"""HealthManager의 핵심 동작을 검증합니다.

AI 사용 정보
AI: Copilot (Copilot SDK in VS Code)
목적: 콘솔 테스트 메뉴의 정상 및 오류 처리 검증
프롬프트: "GUI 대신에 health_logic 에 TUI 로 테스트하는 함수를 추가할 수 있을까? __name__ == __main__ 에서 호출할 수 있도록"
작성자: [제출 전 본인 이름 기입]
날짜: 2026-11-24
"""

import csv
import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from modules.health_logic import DuplicateRecordError, HealthManager, run_tui


class HealthManagerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.manager = HealthManager(data_dir=self.root / "data", auto_load=False)
        self.record = self.manager.add_record(
            name="김민지",
            birth_year=1998,
            gender="여성",
            height=165,
            weight=61,
        )

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_create_update_and_duplicate_validation(self) -> None:
        self.assertRegex(self.record.id, r"^P\d{4}-\d{4}$")
        self.assertEqual(self.record.status, "정상")

        updated = self.manager.update_record(
            self.record.id,
            name="김민지",
            birth_year=1998,
            gender="여성",
            height=165,
            weight=70,
        )
        self.assertEqual(updated.id, self.record.id)
        self.assertEqual(updated.status, "과체중")
        self.assertAlmostEqual(updated.bmi, 25.71, places=2)

        with self.assertRaises(DuplicateRecordError):
            self.manager.add_record("김민지", 1998, "여성", 160, 50)

    def test_bmi_status_boundaries(self) -> None:
        self.assertEqual(self.manager.classify_bmi(18.49), "저체중")
        self.assertEqual(self.manager.classify_bmi(18.5), "정상")
        self.assertEqual(self.manager.classify_bmi(24.99), "정상")
        self.assertEqual(self.manager.classify_bmi(25.0), "과체중")
        self.assertEqual(self.manager.classify_bmi(30.0), "비만")

    def test_all_supported_formats_round_trip(self) -> None:
        formats = {
            "json": ".json",
            "csv": ".csv",
            "txt": ".txt",
            "pickle": ".pkl",
        }
        for file_format, extension in formats.items():
            with self.subTest(file_format=file_format):
                path = self.root / f"export{extension}"
                self.manager.export_to_file(path, file_format)
                loaded_manager = HealthManager(
                    data_dir=self.root / f"load-{file_format}",
                    auto_load=False,
                )
                self.assertEqual(loaded_manager.load_from_file(path), 1)
                self.assertEqual(loaded_manager.records[0], self.record)

    def test_csv_import_generates_id_and_skips_duplicate(self) -> None:
        path = self.root / "external.csv"
        with path.open("w", encoding="utf-8-sig", newline="") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=("이름", "생년", "성별", "신장 (cm)", "체중 (kg)"),
            )
            writer.writeheader()
            writer.writerow(
                {
                    "이름": "박서준",
                    "생년": 1995,
                    "성별": "남성",
                    "신장 (cm)": 180,
                    "체중 (kg)": 75,
                }
            )
            writer.writerow(
                {
                    "이름": "김민지",
                    "생년": 1998,
                    "성별": "여성",
                    "신장 (cm)": 165,
                    "체중 (kg)": 61,
                }
            )

        report = self.manager.import_csv(path)
        self.assertEqual(report.imported_count, 1)
        self.assertEqual(report.skipped_count, 1)
        imported_record = self.manager.search_records("박서준")[0]
        self.assertRegex(imported_record.id, r"^P\d{4}-\d{4}$")

    def test_tui_updates_and_deletes_selected_record(self) -> None:
        responses = [
            "3", self.record.id,
            "4", self.record.id, "김민지", "1998", "여성", "165", "70", "",
            "6",
            "5", self.record.id, "y",
            "0",
        ]
        output = io.StringIO()
        with patch("builtins.input", side_effect=responses), redirect_stdout(output):
            run_tui(self.manager)
        self.assertIn("수정 완료:", output.getvalue())
        self.assertIn("BMI: 25.71", output.getvalue())
        self.assertIn("전체 1명", output.getvalue())
        self.assertIn("삭제 완료.", output.getvalue())
        self.assertEqual(self.manager.records, ())

    def test_tui_rejects_invalid_input_and_can_continue(self) -> None:
        responses = [
            "1", "박서준", "1995", "남성", "0", "75", "",
            "1", "박서준", "1995", "남성", "180", "75", "",
            "0",
        ]
        output = io.StringIO()
        with patch("builtins.input", side_effect=responses), redirect_stdout(output):
            run_tui(self.manager)
        self.assertIn("처리 실패:", output.getvalue())
        self.assertIn("등록 완료:", output.getvalue())
        self.assertEqual(len(self.manager.records), 2)


if __name__ == "__main__":
    unittest.main()
