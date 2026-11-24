"""BMI 건강정보 관리 프로그램의 Tkinter 사용자 인터페이스입니다.

AI 사용 정보
AI: Copilot (Copilot SDK in VS Code)
목적: BMI 정보 관리 프로그램의 GUI 모듈 구현
프롬프트: "GUI는 사진처럼 BMI 게이지, 건강정보 입력, 기록 표를 제공해."
작성자: [제출 전 본인 이름 기입]
날짜: 2026-11-24
"""

from __future__ import annotations

import tkinter as tk
from datetime import date
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from modules.health_db import HealthRecord, StorageError
from modules.health_logic import BMI_STATUSES, GENDERS, HealthManager


class HealthGUI:
    """BMI 게이지, 건강정보 입력 폼, 기록 표와 파일 작업을 제공합니다."""

    def __init__(
        self,
        root: tk.Tk,
        manager: HealthManager,
        startup_error: str | None = None,
    ) -> None:
        """메인 창을 준비하고 이벤트와 관리 로직을 연결합니다."""
        self.root = root
        self.manager = manager
        self.selected_record_id: str | None = None
        self.current_bmi: float | None = None

        self.name_var = tk.StringVar()
        self.gender_var = tk.StringVar()
        self.birth_year_var = tk.StringVar()
        self.height_var = tk.StringVar()
        self.weight_var = tk.StringVar()
        self.bmi_var = tk.StringVar(value="BMI 정보를 보려면 기록을 선택하세요")
        self.status_var = tk.StringVar(value="")
        self.search_var = tk.StringVar()
        self.status_filter_var = tk.StringVar(value="전체")
        self.statistics_var = tk.StringVar()

        self.root.title("BMI 정보 관리 프로그램")
        self.root.geometry("1320x800")
        self.root.minsize(1000, 650)
        self._configure_style()
        self._build_layout()
        self._refresh_table()
        self._refresh_statistics()
        self._draw_bmi_gauge()

        if startup_error:
            self.root.after(
                100,
                lambda: messagebox.showerror(
                    "저장 파일 오류",
                    f"기본 저장 파일을 읽지 못했습니다.\n{startup_error}\n\n"
                    "빈 목록으로 시작합니다. 파일에서 다시 불러올 수 있습니다.",
                    parent=self.root,
                ),
            )

    def _configure_style(self) -> None:
        """화면 전체에 일관된 기본 글꼴과 행 높이를 적용합니다."""
        style = ttk.Style(self.root)
        if "vista" in style.theme_names():
            style.theme_use("vista")
        style.configure("Treeview", rowheight=30, font=("Malgun Gothic", 10))
        style.configure("Treeview.Heading", font=("Malgun Gothic", 10, "bold"))
        style.configure("Title.TLabel", font=("Malgun Gothic", 22, "bold"))
        style.configure("Primary.TButton", font=("Malgun Gothic", 11, "bold"))

    def _build_layout(self) -> None:
        """제목, 입력 패널, BMI 게이지, 검색과 기록 표를 배치합니다."""
        header = ttk.Frame(self.root, padding=(14, 12, 14, 4))
        header.pack(fill="x")
        ttk.Label(header, text="BMI 정보 관리 프로그램", style="Title.TLabel").pack(
            side="left", padx=(0, 20)
        )
        ttk.Button(header, text="파일에서 불러오기", command=self._load_file).pack(
            side="right", padx=(6, 0)
        )
        ttk.Button(header, text="파일로 내보내기", command=self._export_file).pack(
            side="right", padx=(6, 0)
        )
        ttk.Button(header, text="CSV 일괄 등록", command=self._import_csv).pack(
            side="right", padx=(6, 0)
        )

        content = ttk.Frame(self.root, padding=12)
        content.pack(fill="both", expand=True)
        content.columnconfigure(0, weight=0, minsize=330)
        content.columnconfigure(1, weight=1)
        content.rowconfigure(0, weight=1)

        self._build_input_panel(content)
        self._build_records_panel(content)

    def _build_input_panel(self, parent: ttk.Frame) -> None:
        """이름, 성별, 생년, 신장, 체중과 추가 정보를 입력받습니다."""
        panel = ttk.LabelFrame(parent, text="건강정보 입력", padding=14)
        panel.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        panel.columnconfigure(1, weight=1)

        fields = (
            ("이름", self.name_var),
            ("생년", self.birth_year_var),
            ("신장 (cm)", self.height_var),
            ("체중 (kg)", self.weight_var),
        )
        for row, (label, variable) in enumerate(fields):
            ttk.Label(panel, text=label).grid(
                row=row, column=0, sticky="w", pady=8, padx=(0, 10)
            )
            if label == "생년":
                entry = ttk.Spinbox(
                    panel,
                    from_=1900,
                    to=date.today().year,
                    textvariable=variable,
                    width=18,
                )
            else:
                entry = ttk.Entry(panel, textvariable=variable, width=22)
            entry.grid(row=row, column=1, sticky="ew", pady=8)

        gender_row = len(fields)
        ttk.Label(panel, text="성별").grid(
            row=gender_row, column=0, sticky="w", pady=8, padx=(0, 10)
        )
        gender_frame = ttk.Frame(panel)
        gender_frame.grid(row=gender_row, column=1, sticky="w", pady=8)
        for gender in GENDERS:
            ttk.Radiobutton(
                gender_frame,
                text=gender,
                value=gender,
                variable=self.gender_var,
            ).pack(side="left", padx=(0, 8))

        notes_row = gender_row + 1
        ttk.Label(panel, text="추가 정보").grid(
            row=notes_row, column=0, sticky="nw", pady=8, padx=(0, 10)
        )
        self.notes_text = tk.Text(panel, height=4, width=22, wrap="word")
        self.notes_text.grid(row=notes_row, column=1, sticky="ew", pady=8)

        action_row = notes_row + 1
        ttk.Button(
            panel,
            text="계산 및 추가",
            style="Primary.TButton",
            command=self._add_record,
        ).grid(row=action_row, column=0, columnspan=2, sticky="ew", pady=(16, 6))
        ttk.Button(panel, text="선택 항목 수정", command=self._update_record).grid(
            row=action_row + 1, column=0, columnspan=2, sticky="ew", pady=6
        )
        ttk.Button(panel, text="선택 항목 삭제", command=self._delete_record).grid(
            row=action_row + 2, column=0, columnspan=2, sticky="ew", pady=6
        )
        ttk.Button(panel, text="입력 초기화", command=self._clear_form).grid(
            row=action_row + 3, column=0, columnspan=2, sticky="ew", pady=6
        )
        ttk.Label(
            panel,
            text="식별번호는 등록 시 자동으로 발급됩니다.",
            wraplength=280,
        ).grid(row=action_row + 4, column=0, columnspan=2, sticky="w", pady=(10, 0))

    def _build_records_panel(self, parent: ttk.Frame) -> None:
        """BMI 시각화, 검색 도구, 표와 요약 통계를 배치합니다."""
        right_panel = ttk.Frame(parent)
        right_panel.grid(row=0, column=1, sticky="nsew")
        right_panel.columnconfigure(0, weight=1)
        right_panel.rowconfigure(1, weight=1)

        bmi_panel = ttk.LabelFrame(right_panel, text="BMI 상태", padding=10)
        bmi_panel.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        bmi_panel.columnconfigure(0, weight=1)
        ttk.Label(
            bmi_panel,
            textvariable=self.bmi_var,
            anchor="center",
            font=("Malgun Gothic", 18, "bold"),
            foreground="#173a70",
        ).grid(row=0, column=0, sticky="ew", pady=(0, 2))
        ttk.Label(
            bmi_panel,
            textvariable=self.status_var,
            anchor="center",
            font=("Malgun Gothic", 12, "bold"),
        ).grid(row=1, column=0, sticky="ew")
        self.gauge_canvas = tk.Canvas(
            bmi_panel, height=125, background="white", highlightthickness=0
        )
        self.gauge_canvas.grid(row=2, column=0, sticky="ew", pady=(0, 2))
        self.gauge_canvas.bind("<Configure>", lambda _event: self._draw_bmi_gauge())

        table_panel = ttk.LabelFrame(right_panel, text="건강정보 목록", padding=8)
        table_panel.grid(row=1, column=0, sticky="nsew")
        table_panel.columnconfigure(0, weight=1)
        table_panel.rowconfigure(1, weight=1)

        search_bar = ttk.Frame(table_panel)
        search_bar.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        search_bar.columnconfigure(0, weight=1)
        ttk.Entry(search_bar, textvariable=self.search_var).grid(
            row=0, column=0, sticky="ew", padx=(0, 6)
        )
        ttk.Button(search_bar, text="검색", command=self._refresh_table).grid(
            row=0, column=1, padx=(0, 6)
        )
        ttk.Button(
            search_bar,
            text="전체 보기",
            command=self._clear_search,
        ).grid(row=0, column=2, padx=(0, 10))
        ttk.Label(search_bar, text="BMI 상태").grid(row=0, column=3, padx=(0, 4))
        status_filter = ttk.Combobox(
            search_bar,
            textvariable=self.status_filter_var,
            values=("전체", *BMI_STATUSES),
            state="readonly",
            width=10,
        )
        status_filter.grid(row=0, column=4)
        status_filter.bind("<<ComboboxSelected>>", lambda _event: self._refresh_table())

        table_frame = ttk.Frame(table_panel)
        table_frame.grid(row=1, column=0, sticky="nsew")
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        columns = (
            "record_date",
            "id",
            "name",
            "gender",
            "birth_year",
            "height",
            "weight",
            "bmi",
            "status",
            "actions",
        )
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse",
            height=12,
        )
        headings = {
            "record_date": "날짜",
            "id": "식별번호",
            "name": "이름",
            "gender": "성별",
            "birth_year": "생년",
            "height": "신장 (cm)",
            "weight": "체중 (kg)",
            "bmi": "BMI",
            "status": "상태",
            "actions": "작업",
        }
        widths = {
            "record_date": 96,
            "id": 110,
            "name": 90,
            "gender": 65,
            "birth_year": 65,
            "height": 90,
            "weight": 90,
            "bmi": 70,
            "status": 80,
            "actions": 120,
        }
        for column in columns:
            self.tree.heading(column, text=headings[column])
            self.tree.column(column, width=widths[column], minwidth=55, anchor="center")
        self.tree.grid(row=0, column=0, sticky="nsew")

        vertical_scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.tree.yview
        )
        vertical_scrollbar.grid(row=0, column=1, sticky="ns")
        horizontal_scrollbar = ttk.Scrollbar(
            table_frame, orient="horizontal", command=self.tree.xview
        )
        horizontal_scrollbar.grid(row=1, column=0, sticky="ew")
        self.tree.configure(
            yscrollcommand=vertical_scrollbar.set,
            xscrollcommand=horizontal_scrollbar.set,
        )
        self.tree.bind("<<TreeviewSelect>>", self._on_record_selected)
        self.tree.bind("<Button-1>", self._on_tree_action)

        ttk.Label(
            table_panel,
            textvariable=self.statistics_var,
            anchor="w",
            padding=(2, 8, 2, 0),
        ).grid(row=2, column=0, sticky="ew")

    def _add_record(self) -> None:
        """입력 내용을 새 레코드로 등록하고 성공 여부를 알립니다."""
        try:
            record = self.manager.add_record(**self._form_values())
        except (ValueError, StorageError) as exc:
            messagebox.showerror("등록 실패", str(exc), parent=self.root)
            return
        self._refresh_table(select_id=record.id)
        self._refresh_statistics()
        messagebox.showinfo(
            "등록 완료",
            f"{record.name}님의 건강정보를 등록했습니다.\n식별번호: {record.id}",
            parent=self.root,
        )

    def _update_record(self) -> None:
        """선택한 레코드를 입력 내용으로 갱신합니다."""
        if not self.selected_record_id:
            messagebox.showwarning("수정할 항목 선택", "표에서 수정할 행을 선택하세요.", parent=self.root)
            return
        try:
            record = self.manager.update_record(
                self.selected_record_id, **self._form_values()
            )
        except (ValueError, KeyError, StorageError) as exc:
            messagebox.showerror("수정 실패", str(exc), parent=self.root)
            return
        self._refresh_table(select_id=record.id)
        self._refresh_statistics()
        messagebox.showinfo("수정 완료", "건강정보를 수정했습니다.", parent=self.root)

    def _delete_record(self) -> None:
        """확인 후 선택한 레코드를 삭제합니다."""
        if not self.selected_record_id:
            messagebox.showwarning("삭제할 항목 선택", "표에서 삭제할 행을 선택하세요.", parent=self.root)
            return
        record = self.manager.get_record(self.selected_record_id)
        if not messagebox.askyesno(
            "삭제 확인",
            f"{record.name}님의 건강정보를 삭제할까요?",
            parent=self.root,
        ):
            return
        try:
            self.manager.delete_record(record.id)
        except (KeyError, StorageError) as exc:
            messagebox.showerror("삭제 실패", str(exc), parent=self.root)
            return
        self._clear_form()
        self._refresh_table()
        self._refresh_statistics()
        messagebox.showinfo("삭제 완료", "건강정보를 삭제했습니다.", parent=self.root)

    def _load_file(self) -> None:
        """선택한 JSON, CSV, TXT 또는 Pickle 파일로 현재 목록을 교체합니다."""
        path = filedialog.askopenfilename(
            parent=self.root,
            title="건강정보 파일 불러오기",
            filetypes=self._filetypes(),
        )
        if not path:
            return
        if Path(path).suffix.lower() in (".pkl", ".pickle") and not messagebox.askyesno(
            "Pickle 파일 확인",
            "Pickle 파일은 신뢰할 수 있는 출처의 파일만 여세요. 계속할까요?",
            parent=self.root,
        ):
            return
        if self.manager.records and not messagebox.askyesno(
            "기록 교체 확인",
            "파일을 불러오면 현재 목록이 파일의 내용으로 교체됩니다. 계속할까요?",
            parent=self.root,
        ):
            return
        try:
            count = self.manager.load_from_file(path)
        except (StorageError, ValueError) as exc:
            messagebox.showerror("불러오기 실패", str(exc), parent=self.root)
            return
        self._clear_form()
        self._refresh_table()
        self._refresh_statistics()
        messagebox.showinfo(
            "불러오기 완료", f"{count}건의 기록을 불러왔습니다.", parent=self.root
        )

    def _export_file(self) -> None:
        """현재 목록을 사용자가 선택한 파일 형식으로 내보냅니다."""
        path = filedialog.asksaveasfilename(
            parent=self.root,
            title="건강정보 파일 내보내기",
            initialfile="health_data.json",
            defaultextension=".json",
            filetypes=self._filetypes(),
        )
        if not path:
            return
        try:
            self.manager.export_to_file(path)
        except (StorageError, ValueError) as exc:
            messagebox.showerror("내보내기 실패", str(exc), parent=self.root)
            return
        messagebox.showinfo(
            "내보내기 완료",
            f"{len(self.manager.records)}건을 파일로 저장했습니다.\n{path}",
            parent=self.root,
        )

    def _import_csv(self) -> None:
        """외부 CSV 파일을 중복 확인 후 일괄 등록합니다."""
        path = filedialog.askopenfilename(
            parent=self.root,
            title="CSV 일괄 등록",
            filetypes=(("CSV 파일", "*.csv"), ("모든 파일", "*.*")),
        )
        if not path:
            return
        try:
            report = self.manager.import_csv(path)
        except (StorageError, ValueError) as exc:
            messagebox.showerror("CSV 등록 실패", str(exc), parent=self.root)
            return

        self._refresh_table()
        self._refresh_statistics()
        message = (
            f"등록: {report.imported_count}건\n"
            f"중복 건너뜀: {report.skipped_count}건"
        )
        if report.errors:
            message += "\n\n오류:\n" + "\n".join(report.errors[:5])
            if len(report.errors) > 5:
                message += f"\n외 {len(report.errors) - 5}건"
            messagebox.showwarning("CSV 등록 결과", message, parent=self.root)
        else:
            messagebox.showinfo("CSV 등록 완료", message, parent=self.root)

    def _form_values(self) -> dict[str, str]:
        """입력 위젯의 값을 로직 모듈에 전달할 딕셔너리로 만듭니다."""
        return {
            "name": self.name_var.get(),
            "birth_year": self.birth_year_var.get(),
            "gender": self.gender_var.get(),
            "height": self.height_var.get(),
            "weight": self.weight_var.get(),
            "notes": self.notes_text.get("1.0", "end-1c"),
        }

    def _on_record_selected(self, _event: tk.Event) -> None:
        """표 선택 내용을 입력 폼과 BMI 게이지에 표시합니다."""
        selection = self.tree.selection()
        if not selection:
            return
        record_id = selection[0]
        try:
            record = self.manager.get_record(record_id)
        except KeyError:
            return
        self._display_record(record)

    def _display_record(self, record: HealthRecord) -> None:
        """선택된 레코드를 입력 폼과 BMI 게이지에 표시합니다."""
        self.selected_record_id = record.id
        self.name_var.set(record.name)
        self.gender_var.set(record.gender)
        self.birth_year_var.set(str(record.birth_year))
        self.height_var.set(f"{record.height:g}")
        self.weight_var.set(f"{record.weight:g}")
        self.notes_text.delete("1.0", "end")
        self.notes_text.insert("1.0", record.notes)
        self.current_bmi = record.bmi
        self.bmi_var.set(f"{record.name}님의 BMI 지수: {record.bmi:.1f}")
        self.status_var.set(record.status)
        self._draw_bmi_gauge()

    def _refresh_table(self, select_id: str | None = None) -> None:
        """검색 조건에 맞는 레코드를 Treeview에 표시합니다."""
        if not hasattr(self, "tree"):
            return
        for item in self.tree.get_children():
            self.tree.delete(item)
        records = self.manager.search_records(
            self.search_var.get(),
            self.status_filter_var.get(),
        )
        for record in records:
            self.tree.insert(
                "",
                "end",
                iid=record.id,
                values=(
                    record.record_date,
                    record.id,
                    record.name,
                    record.gender,
                    record.birth_year,
                    f"{record.height:g}",
                    f"{record.weight:g}",
                    f"{record.bmi:.2f}",
                    record.status,
                    "수정   |   삭제",
                ),
            )
        if select_id and self.tree.exists(select_id):
            self.tree.selection_set(select_id)
            self.tree.focus(select_id)
            self.tree.see(select_id)
            self._on_record_selected(None)

    def _on_tree_action(self, event: tk.Event) -> str | None:
        """표의 작업 열을 클릭하면 해당 행을 수정하거나 삭제합니다."""
        row_id = self.tree.identify_row(event.y)
        column_id = self.tree.identify_column(event.x)
        if not row_id or column_id != "#10":
            return None

        try:
            record = self.manager.get_record(row_id)
        except KeyError:
            return "break"
        if self.selected_record_id != row_id:
            self._display_record(record)

        bounds = self.tree.bbox(row_id, "actions")
        if not bounds:
            return "break"
        click_position = event.x - bounds[0]
        if click_position < bounds[2] * 0.5:
            self._update_record()
        else:
            self._delete_record()
        return "break"

    def _refresh_statistics(self) -> None:
        """요약 통계를 화면 아래쪽에 갱신합니다."""
        stats = self.manager.calculate_statistics()
        self.statistics_var.set(
            "전체 {count}명   평균 신장 {average_height:.1f} cm   "
            "평균 체중 {average_weight:.1f} kg   평균 BMI {average_bmi:.2f}".format(
                **stats
            )
        )

    def _draw_bmi_gauge(self) -> None:
        """사진과 같은 4색 BMI 구간 표시와 현재 BMI 마커를 그립니다."""
        canvas = getattr(self, "gauge_canvas", None)
        if canvas is None:
            return
        canvas.delete("all")
        width = max(canvas.winfo_width(), 420)
        left, right = 28, width - 28
        bar_top, bar_bottom = 34, 58
        maximum_bmi = 40.0
        boundaries = (0.0, 18.5, 25.0, 30.0, maximum_bmi)
        colors = ("#72c8ed", "#74dc85", "#f7df4b", "#f04444")
        labels = (
            ("저체중", "<18.5"),
            ("정상", "18.5–24.9"),
            ("과체중", "25.0–29.9"),
            ("비만", "≥30.0"),
        )
        span = right - left

        for index, (category, range_label) in enumerate(labels):
            segment_left = left + span * boundaries[index] / maximum_bmi
            segment_right = left + span * boundaries[index + 1] / maximum_bmi
            canvas.create_rectangle(
                segment_left,
                bar_top,
                segment_right,
                bar_bottom,
                fill=colors[index],
                outline=colors[index],
            )
            center = (segment_left + segment_right) / 2
            canvas.create_text(
                center,
                78,
                text=f"{category}\n{range_label}",
                font=("Malgun Gothic", 9),
                justify="center",
            )

        if self.current_bmi is not None:
            position = left + span * min(max(self.current_bmi, 0), maximum_bmi) / maximum_bmi
            canvas.create_polygon(
                position - 8,
                24,
                position + 8,
                24,
                position,
                34,
                fill="#111111",
                outline="#111111",
            )
            canvas.create_line(
                position,
                bar_top,
                position,
                bar_bottom,
                fill="#111111",
                width=2,
            )

    def _clear_form(self) -> None:
        """입력 내용을 비우고 선택 레코드와 BMI 게이지를 초기화합니다."""
        self.selected_record_id = None
        self.name_var.set("")
        self.gender_var.set("")
        self.birth_year_var.set("")
        self.height_var.set("")
        self.weight_var.set("")
        self.notes_text.delete("1.0", "end")
        self.current_bmi = None
        self.bmi_var.set("BMI 정보를 보려면 기록을 선택하세요")
        self.status_var.set("")
        if hasattr(self, "tree"):
            for selected in self.tree.selection():
                self.tree.selection_remove(selected)
        self._draw_bmi_gauge()

    def _clear_search(self) -> None:
        """검색어와 상태 필터를 초기화해 전체 목록을 표시합니다."""
        self.search_var.set("")
        self.status_filter_var.set("전체")
        self._refresh_table()

    @staticmethod
    def _filetypes() -> tuple[tuple[str, str], ...]:
        """파일 선택 대화상자에서 지원 형식을 표시합니다."""
        return (
            ("모든 지원 파일", "*.json *.csv *.txt *.pkl *.pickle"),
            ("JSON 파일", "*.json"),
            ("CSV 파일", "*.csv"),
            ("텍스트 파일", "*.txt"),
            ("Pickle 파일", "*.pkl *.pickle"),
            ("모든 파일", "*.*"),
        )
