"""건강 기록의 검증, CRUD, 검색, 통계, 가져오기와 내보내기를 담당합니다.

AI 사용 정보
AI: Copilot (Copilot SDK in VS Code)
목적: BMI 정보 관리 프로그램의 비즈니스 로직 모듈 구현
프롬프트: "4가지 파일 형식 모두 지원. ID는 자동생성. 파일내보내기, 불러오기 기능 포함. 객체지향."
추가 프롬프트: "GUI 대신에 health_logic 에 TUI 로 테스트하는 함수를 추가할 수 있을까? __name__ == __main__ 에서 호출할 수 있도록"
작성자: [제출 전 본인 이름 기입]
날짜: 2026-11-24
"""

from __future__ import annotations

import math
import re
import tempfile
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Iterable, Mapping

if __package__:
    from .health_db import HealthFileStore, HealthRecord, StorageError
else:
    from health_db import HealthFileStore, HealthRecord, StorageError


BMI_STATUSES = ("저체중", "정상", "과체중", "비만")
GENDERS = ("남성", "여성", "기타")


class DuplicateRecordError(ValueError):
    """이미 등록된 사람을 다시 등록하려 할 때 발생합니다."""


@dataclass(frozen=True)
class ImportReport:
    """CSV 일괄 등록 결과의 요약입니다."""

    imported_count: int
    skipped_count: int
    errors: tuple[str, ...]


class HealthManager:
    """건강정보 레코드의 생성, 검색, 변경과 저장을 관리합니다."""

    def __init__(
        self,
        data_dir: str | Path | None = None,
        auto_load: bool = True,
    ) -> None:
        """관리자를 준비하고 기본 JSON 파일이 있으면 기록을 불러옵니다."""
        project_root = Path(__file__).resolve().parents[1]
        self.data_dir = Path(data_dir) if data_dir else project_root / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.default_path = self.data_dir / "health_data.json"
        self._active_path = self.default_path
        self._active_format = "json"
        self._store = HealthFileStore()
        self._records: list[HealthRecord] = []

        if auto_load and self.default_path.exists():
            self.load_from_file(self.default_path)

    @property
    def records(self) -> tuple[HealthRecord, ...]:
        """현재 등록된 레코드를 읽기 전용 튜플로 반환합니다."""
        return tuple(self._records)

    def add_record(
        self,
        name: str,
        birth_year: int | str,
        gender: str,
        height: float | str,
        weight: float | str,
        notes: str = "",
    ) -> HealthRecord:
        """새 사람의 건강정보를 검증해 ID를 발급하고 저장합니다."""
        record = self._build_record(
            name=name,
            birth_year=birth_year,
            gender=gender,
            height=height,
            weight=weight,
            notes=notes,
        )
        self._ensure_unique_person(record)
        self._records.append(record)
        try:
            self._save_active()
        except StorageError:
            self._records.pop()
            raise
        return record

    def update_record(
        self,
        record_id: str,
        name: str,
        birth_year: int | str,
        gender: str,
        height: float | str,
        weight: float | str,
        notes: str = "",
    ) -> HealthRecord:
        """선택한 사람의 정보를 갱신하고 BMI와 상태를 다시 계산합니다."""
        index = self._index_for_id(record_id)
        previous = self._records[index]
        updated = self._build_record(
            name=name,
            birth_year=birth_year,
            gender=gender,
            height=height,
            weight=weight,
            notes=notes,
            record_id=previous.id,
        )
        self._ensure_unique_person(updated, excluding_id=previous.id)
        self._records[index] = updated
        try:
            self._save_active()
        except StorageError:
            self._records[index] = previous
            raise
        return updated

    def delete_record(self, record_id: str) -> HealthRecord:
        """선택한 사람의 정보를 메모리와 영구 저장소에서 삭제합니다."""
        index = self._index_for_id(record_id)
        deleted = self._records.pop(index)
        try:
            self._save_active()
        except StorageError:
            self._records.insert(index, deleted)
            raise
        return deleted

    def get_record(self, record_id: str) -> HealthRecord:
        """식별번호에 해당하는 레코드를 반환합니다."""
        return self._records[self._index_for_id(record_id)]

    def search_records(
        self,
        query: str = "",
        status: str | None = None,
    ) -> list[HealthRecord]:
        """이름·식별번호와 선택적 BMI 상태로 레코드를 검색합니다."""
        normalized_query = query.strip().casefold()
        matches = [
            record
            for record in self._records
            if (
                not normalized_query
                or normalized_query in record.name.casefold()
                or normalized_query in record.id.casefold()
            )
            and (not status or status == "전체" or record.status == status)
        ]
        return sorted(matches, key=lambda record: (record.record_date, record.id), reverse=True)

    def calculate_statistics(self) -> dict[str, int | float]:
        """인원수와 평균 키, 몸무게, BMI를 계산합니다."""
        count = len(self._records)
        if count == 0:
            return {
                "count": 0,
                "average_height": 0.0,
                "average_weight": 0.0,
                "average_bmi": 0.0,
            }
        return {
            "count": count,
            "average_height": round(sum(item.height for item in self._records) / count, 2),
            "average_weight": round(sum(item.weight for item in self._records) / count, 2),
            "average_bmi": round(sum(item.bmi for item in self._records) / count, 2),
        }

    def load_from_file(self, path: str | Path, file_format: str | None = None) -> int:
        """지정 파일의 레코드로 현재 목록을 교체하고 이후 저장 대상으로 설정합니다."""
        source = Path(path)
        normalized_format = self._store.normalize_format(file_format, source)
        loaded_records = self._store.load(source, normalized_format)
        self._ensure_loaded_records_are_unique(loaded_records)
        self._records = loaded_records
        self._active_path = source
        self._active_format = normalized_format
        return len(self._records)

    def export_to_file(
        self,
        path: str | Path,
        file_format: str | None = None,
    ) -> None:
        """현재 레코드 전체를 선택한 파일 형식으로 내보냅니다."""
        self._store.save(self._records, path, file_format)

    def import_csv(self, path: str | Path) -> ImportReport:
        """CSV 레코드를 중복 확인 후 추가합니다. 외부 CSV의 ID는 자동 발급합니다."""
        rows = self._store.read_rows(path, "csv")
        original_records = list(self._records)
        imported_count = 0
        skipped_count = 0
        errors: list[str] = []

        for row_number, row in enumerate(rows, start=2):
            try:
                values = self._csv_values(row)
                record = self._build_record(**values)
                if self._is_duplicate(record):
                    skipped_count += 1
                    continue
                self._records.append(record)
                imported_count += 1
            except (KeyError, TypeError, ValueError) as exc:
                errors.append(f"{row_number}행: {exc}")

        if imported_count:
            try:
                self._save_active()
            except StorageError:
                self._records = original_records
                raise

        return ImportReport(imported_count, skipped_count, tuple(errors))

    def _build_record(
        self,
        name: str,
        birth_year: int | str,
        gender: str,
        height: float | str,
        weight: float | str,
        notes: str = "",
        record_id: str | None = None,
        record_date: str | None = None,
    ) -> HealthRecord:
        """입력 필드를 검증하고 BMI가 계산된 불변 레코드를 만듭니다."""
        clean_name = str(name).strip()
        if not clean_name:
            raise ValueError("이름을 입력하세요.")

        try:
            year = int(birth_year)
        except (TypeError, ValueError, OverflowError) as exc:
            raise ValueError("생년은 숫자로 입력하세요.") from exc
        current_year = date.today().year
        if year < 1900 or year > current_year:
            raise ValueError(f"생년은 1900년부터 {current_year}년 사이여야 합니다.")

        clean_gender = str(gender).strip()
        if clean_gender not in GENDERS:
            raise ValueError("성별을 선택하세요.")

        clean_height = self._positive_number(height, "신장")
        clean_weight = self._positive_number(weight, "체중")
        bmi = round(clean_weight / ((clean_height / 100) ** 2), 2)

        return HealthRecord(
            id=record_id or self._generate_id(),
            name=clean_name,
            birth_year=year,
            gender=clean_gender,
            height=clean_height,
            weight=clean_weight,
            bmi=bmi,
            status=self.classify_bmi(bmi),
            record_date=record_date or date.today().isoformat(),
            notes=str(notes).strip(),
        )

    @staticmethod
    def _positive_number(value: float | str, label: str) -> float:
        """숫자 입력이 유한한 양수인지 확인합니다."""
        try:
            number = float(value)
        except (TypeError, ValueError, OverflowError) as exc:
            raise ValueError(f"{label}는 숫자로 입력하세요.") from exc
        if not math.isfinite(number) or number <= 0:
            raise ValueError(f"{label}는 0보다 큰 숫자여야 합니다.")
        return number

    @staticmethod
    def classify_bmi(bmi: float) -> str:
        """사진의 구간에 따라 BMI 상태를 반환합니다."""
        if bmi < 18.5:
            return "저체중"
        if bmi < 25:
            return "정상"
        if bmi < 30:
            return "과체중"
        return "비만"

    def _generate_id(self) -> str:
        """현재 연도에 사용되지 않은 PYYYY-NNNN 식별번호를 발급합니다."""
        prefix = f"P{date.today().year}-"
        used_numbers = []
        for record in self._records:
            if record.id.startswith(prefix):
                suffix = record.id[len(prefix) :]
                if suffix.isdigit():
                    used_numbers.append(int(suffix))
        return f"{prefix}{max(used_numbers, default=0) + 1:04d}"

    def _ensure_unique_person(
        self,
        candidate: HealthRecord,
        excluding_id: str | None = None,
    ) -> None:
        """동일한 이름·생년·성별의 중복 등록을 막습니다."""
        if self._is_duplicate(candidate, excluding_id):
            raise DuplicateRecordError(
                "같은 이름, 생년, 성별의 사람이 이미 등록되어 있습니다."
            )

    def _is_duplicate(
        self,
        candidate: HealthRecord,
        excluding_id: str | None = None,
    ) -> bool:
        identity = (candidate.name.casefold(), candidate.birth_year, candidate.gender)
        return any(
            record.id != excluding_id
            and (
                record.name.casefold(),
                record.birth_year,
                record.gender,
            )
            == identity
            for record in self._records
        )

    @staticmethod
    def _ensure_loaded_records_are_unique(records: Iterable[HealthRecord]) -> None:
        """불러온 파일의 ID와 개인 식별 정보가 중복되지 않는지 확인합니다."""
        ids: set[str] = set()
        people: set[tuple[str, int, str]] = set()
        for record in records:
            identity = (record.name.casefold(), record.birth_year, record.gender)
            if record.id in ids or identity in people:
                raise StorageError("불러올 파일에 중복된 ID 또는 사람 정보가 있습니다.")
            ids.add(record.id)
            people.add(identity)

    def _index_for_id(self, record_id: str) -> int:
        """ID로 레코드 위치를 찾거나 명확한 오류를 발생시킵니다."""
        for index, record in enumerate(self._records):
            if record.id == record_id:
                return index
        raise KeyError(f"식별번호 {record_id}에 해당하는 기록이 없습니다.")

    def _save_active(self) -> None:
        """현재 선택된 영구 저장 파일에 모든 레코드를 저장합니다."""
        self._store.save(self._records, self._active_path, self._active_format)

    def _csv_values(self, row: Mapping[str, Any]) -> dict[str, Any]:
        """영문 또는 한국어 헤더를 사용하는 CSV 행을 입력 필드로 변환합니다."""
        normalized = {
            self._normalize_header(key): value
            for key, value in row.items()
            if key is not None
        }

        name = self._first_value(normalized, "name", "이름")
        birth_year = self._first_value(
            normalized, "birthyear", "생년", "출생연도", "출생년도"
        )
        if birth_year in (None, ""):
            age = self._first_value(normalized, "age", "나이")
            if age in (None, ""):
                raise ValueError("생년 또는 나이 열이 필요합니다.")
            birth_year = date.today().year - int(age)

        return {
            "name": name,
            "birth_year": birth_year,
            "gender": self._first_value(normalized, "gender", "성별"),
            "height": self._first_value(
                normalized, "height", "신장", "신장cm", "키", "키cm"
            ),
            "weight": self._first_value(
                normalized, "weight", "체중", "체중kg", "몸무게", "몸무게kg"
            ),
            "notes": self._first_value(normalized, "notes", "추가정보", "비고") or "",
            "record_date": self._first_value(normalized, "recorddate", "날짜") or None,
        }

    @staticmethod
    def _normalize_header(value: Any) -> str:
        """CSV 열 이름에서 공백과 구분 문자를 제거합니다."""
        return re.sub(r"[\s_()（）.\-]", "", str(value)).casefold()

    @staticmethod
    def _first_value(row: Mapping[str, Any], *names: str) -> Any:
        """별칭 목록에서 처음 발견한 CSV 값을 반환합니다."""
        for name in names:
            value = row.get(HealthManager._normalize_header(name))
            if value is not None:
                return value
        return None


def _read_record_fields() -> dict[str, str]:
    """콘솔에서 건강정보 입력값을 읽습니다."""
    return {
        "name": input("이름: "),
        "birth_year": input("생년: "),
        "gender": input("성별 (남성/여성/기타): "),
        "height": input("신장 (cm): "),
        "weight": input("체중 (kg): "),
        "notes": input("추가 정보 (없으면 Enter): "),
    }


def _print_record(record: HealthRecord) -> None:
    """레코드 한 건의 상세 정보를 출력합니다."""
    print(
        f"ID: {record.id} | 이름: {record.name} | 생년: {record.birth_year} | "
        f"성별: {record.gender} | 신장: {record.height:g} cm | "
        f"체중: {record.weight:g} kg | BMI: {record.bmi:.2f} | "
        f"상태: {record.status} | 날짜: {record.record_date} | "
        f"추가 정보: {record.notes or '-'}"
    )


def run_tui(manager: HealthManager) -> None:
    """콘솔 메뉴로 전달받은 관리자의 CRUD, 검색 및 통계를 시험합니다."""
    print("건강정보 콘솔 테스트")
    while True:
        print(
            "\n1. 등록  2. 전체 조회  3. 검색  4. 수정  "
            "5. 삭제  6. 통계  0. 종료"
        )
        try:
            choice = input("메뉴 선택: ").strip()
            if choice == "0":
                print("콘솔 테스트를 종료합니다.")
                return
            if choice == "1":
                record = manager.add_record(**_read_record_fields())
                print("등록 완료:")
                _print_record(record)
            elif choice in ("2", "3"):
                query = input("이름 또는 ID (전체 검색은 Enter): ") if choice == "3" else ""
                records = manager.search_records(query)
                if not records:
                    print("검색된 기록이 없습니다.")
                for record in records:
                    _print_record(record)
            elif choice == "4":
                record_id = input("수정할 ID: ").strip()
                manager.get_record(record_id)
                print("변경할 모든 정보를 입력하세요.")
                record = manager.update_record(record_id, **_read_record_fields())
                print("수정 완료:")
                _print_record(record)
            elif choice == "5":
                record_id = input("삭제할 ID: ").strip()
                record = manager.get_record(record_id)
                if input(f"{record.name}님을 삭제할까요? (y/N): ").strip().lower() == "y":
                    manager.delete_record(record_id)
                    print("삭제 완료.")
                else:
                    print("삭제를 취소했습니다.")
            elif choice == "6":
                stats = manager.calculate_statistics()
                print(
                    "전체 {count}명 | 평균 신장 {average_height:.2f} cm | "
                    "평균 체중 {average_weight:.2f} kg | 평균 BMI {average_bmi:.2f}".format(
                        **stats
                    )
                )
            else:
                print("올바른 메뉴 번호를 입력하세요.")
        except (ValueError, KeyError, StorageError) as exc:
            print(f"처리 실패: {exc}")
        except (EOFError, KeyboardInterrupt):
            print("\n콘솔 테스트를 종료합니다.")
            return


if __name__ == "__main__":
    print("임시 데이터로 테스트합니다. 종료하면 테스트 데이터가 삭제됩니다.")
    with tempfile.TemporaryDirectory(prefix="bmi_tui_") as temporary_directory:
        run_tui(HealthManager(data_dir=temporary_directory, auto_load=False))
