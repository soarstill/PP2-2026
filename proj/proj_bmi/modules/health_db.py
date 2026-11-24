"""건강 기록 데이터 모델과 네 가지 파일 형식의 입출력을 담당합니다.

AI 사용 정보
AI: Copilot (Copilot SDK in VS Code)
목적: BMI 정보 관리 프로그램의 데이터 모듈 구현
프롬프트: "4가지 파일 형식 모두 지원. ID는 자동생성. 파일내보내기, 불러오기 기능 포함. 객체지향."
작성자: [제출 전 본인 이름 기입]
날짜: 2026-11-24
"""

from __future__ import annotations

import csv
import json
import math
import os
import pickle
import tempfile
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Iterable, Mapping


FORMAT_EXTENSIONS = {
    "json": ".json",
    "csv": ".csv",
    "txt": ".txt",
    "pickle": ".pkl",
}

RECORD_FIELDS = (
    "id",
    "name",
    "birth_year",
    "gender",
    "height",
    "weight",
    "bmi",
    "status",
    "record_date",
    "notes",
)


class StorageError(Exception):
    """건강 기록 파일을 읽거나 쓸 때 발생한 오류입니다."""


@dataclass(frozen=True)
class HealthRecord:
    """한 사람의 건강정보와 현재 BMI 측정값을 표현합니다."""

    id: str
    name: str
    birth_year: int
    gender: str
    height: float
    weight: float
    bmi: float
    status: str
    record_date: str
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        """파일 저장과 모듈 간 전달에 사용할 딕셔너리를 반환합니다."""
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "height": self.height,
            "weight": self.weight,
            "bmi": self.bmi,
            "status": self.status,
            "record_date": self.record_date,
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, values: Mapping[str, Any]) -> HealthRecord:
        """저장된 딕셔너리를 검증해 건강정보 객체로 복원합니다."""
        try:
            record = cls(
                id=str(values["id"]).strip(),
                name=str(values["name"]).strip(),
                birth_year=int(values["birth_year"]),
                gender=str(values["gender"]).strip(),
                height=float(values["height"]),
                weight=float(values["weight"]),
                bmi=float(values["bmi"]),
                status=str(values["status"]).strip(),
                record_date=str(
                    values.get("record_date") or values.get("date") or date.today().isoformat()
                ),
                notes=str(values.get("notes", "")),
            )
        except (KeyError, TypeError, ValueError, OverflowError) as exc:
            raise ValueError(f"필수 필드가 없거나 형식이 올바르지 않습니다: {exc}") from exc

        if not record.id or not record.name:
            raise ValueError("식별번호와 이름은 비어 있을 수 없습니다.")
        if record.birth_year < 1:
            raise ValueError("생년은 양수여야 합니다.")
        if (
            not math.isfinite(record.height)
            or not math.isfinite(record.weight)
            or record.height <= 0
            or record.weight <= 0
        ):
            raise ValueError("키와 몸무게는 유효한 양수여야 합니다.")
        if not math.isfinite(record.bmi) or record.bmi <= 0:
            raise ValueError("BMI 값이 유효하지 않습니다.")
        return record


class HealthFileStore:
    """JSON, CSV, TXT, Pickle 파일의 저장과 읽기를 담당합니다."""

    @staticmethod
    def normalize_format(file_format: str | None, path: str | Path) -> str:
        """형식 이름 또는 파일 확장자를 표준 형식명으로 변환합니다."""
        if file_format:
            normalized = file_format.strip().lower().lstrip(".")
            if normalized == "pkl":
                normalized = "pickle"
        else:
            extension = Path(path).suffix.lower()
            normalized = {
                ".json": "json",
                ".csv": "csv",
                ".txt": "txt",
                ".pkl": "pickle",
                ".pickle": "pickle",
            }.get(extension, "")

        if normalized not in FORMAT_EXTENSIONS:
            raise ValueError(
                "지원하지 않는 파일 형식입니다. JSON, CSV, TXT, Pickle 중 선택하세요."
            )
        return normalized

    def save(
        self,
        records: Iterable[HealthRecord],
        path: str | Path,
        file_format: str | None = None,
    ) -> None:
        """레코드 목록을 지정한 파일 형식으로 안전하게 저장합니다."""
        destination = Path(path)
        normalized = self.normalize_format(file_format, destination)
        rows = [record.to_dict() for record in records]
        temporary_path: Path | None = None

        try:
            destination.parent.mkdir(parents=True, exist_ok=True)
            if normalized == "pickle":
                with tempfile.NamedTemporaryFile(
                    mode="wb", dir=destination.parent, delete=False
                ) as temporary_file:
                    temporary_path = Path(temporary_file.name)
                    pickle.dump(rows, temporary_file, protocol=pickle.HIGHEST_PROTOCOL)
                    temporary_file.flush()
                    os.fsync(temporary_file.fileno())
            else:
                with tempfile.NamedTemporaryFile(
                    mode="w",
                    encoding="utf-8",
                    newline="",
                    dir=destination.parent,
                    delete=False,
                ) as temporary_file:
                    temporary_path = Path(temporary_file.name)
                    if normalized == "json":
                        json.dump(rows, temporary_file, ensure_ascii=False, indent=2)
                    else:
                        delimiter = "," if normalized == "csv" else "|"
                        writer = csv.DictWriter(
                            temporary_file,
                            fieldnames=RECORD_FIELDS,
                            delimiter=delimiter,
                            lineterminator="\n",
                        )
                        writer.writeheader()
                        writer.writerows(rows)
                    temporary_file.flush()
                    os.fsync(temporary_file.fileno())

            os.replace(temporary_path, destination)
        except (OSError, TypeError, ValueError, csv.Error, pickle.PickleError) as exc:
            if temporary_path is not None:
                try:
                    temporary_path.unlink()
                except OSError:
                    pass
            raise StorageError(f"파일을 저장하지 못했습니다: {destination}\n{exc}") from exc

    def load(
        self,
        path: str | Path,
        file_format: str | None = None,
    ) -> list[HealthRecord]:
        """파일에서 레코드를 불러옵니다. 파일이 없으면 빈 목록을 반환합니다."""
        source = Path(path)
        normalized = self.normalize_format(file_format, source)
        if not source.exists():
            return []

        try:
            rows = self.read_rows(source, normalized)
            records = []
            for row_number, row in enumerate(rows, start=1):
                try:
                    records.append(HealthRecord.from_dict(row))
                except ValueError as exc:
                    raise StorageError(
                        f"{source}의 {row_number}번째 레코드가 올바르지 않습니다: {exc}"
                    ) from exc
            return records
        except StorageError:
            raise
        except (
            OSError,
            UnicodeError,
            json.JSONDecodeError,
            csv.Error,
            pickle.PickleError,
            EOFError,
            TypeError,
            ValueError,
        ) as exc:
            raise StorageError(f"파일을 읽지 못했습니다: {source}\n{exc}") from exc

    def read_rows(
        self,
        path: str | Path,
        file_format: str | None = None,
    ) -> list[dict[str, Any]]:
        """파일의 행을 딕셔너리 목록으로 읽습니다(CSV 일괄 등록에도 사용)."""
        source = Path(path)
        normalized = self.normalize_format(file_format, source)

        if normalized == "json":
            with source.open("r", encoding="utf-8") as file:
                payload = json.load(file)
            if isinstance(payload, dict) and isinstance(payload.get("records"), list):
                payload = payload["records"]
            if not isinstance(payload, list):
                raise ValueError("JSON 최상위 값은 레코드 목록이어야 합니다.")
            return [self._as_mapping(row) for row in payload]

        if normalized in ("csv", "txt"):
            delimiter = "," if normalized == "csv" else "|"
            with source.open("r", encoding="utf-8-sig", newline="") as file:
                return [
                    dict(row)
                    for row in csv.DictReader(file, delimiter=delimiter)
                    if row
                ]

        with source.open("rb") as file:
            payload = pickle.load(file)
        if not isinstance(payload, list):
            raise ValueError("Pickle 파일에는 레코드 목록이 있어야 합니다.")
        return [self._as_mapping(row) for row in payload]

    @staticmethod
    def _as_mapping(row: Any) -> dict[str, Any]:
        """저장 행을 딕셔너리로 정규화합니다."""
        if isinstance(row, HealthRecord):
            return row.to_dict()
        if isinstance(row, Mapping):
            return dict(row)
        raise ValueError("레코드는 딕셔너리 형식이어야 합니다.")
