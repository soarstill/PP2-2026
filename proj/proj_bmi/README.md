# Health Management Project

BMI 건강정보 관리 프로그램입니다. 한 사람당 하나의 건강정보를 관리하며,
BMI를 자동 계산하고 건강정보를 파일로 저장하거나 불러올 수 있습니다.

## 실행

프로젝트 폴더에서 다음 명령을 실행합니다.

```powershell
python main.py
```

GUI는 Tkinter를 사용합니다. 기본 데이터는 `data/health_data.json`에 저장하고,
JSON, CSV, TXT, Pickle 형식으로 불러오기와 내보내기를 지원합니다.
CSV 파일은 여러 사람을 한 번에 등록할 수 있습니다.

## 콘솔 테스트

GUI 없이 로직을 직접 시험하려면 프로젝트 폴더에서 다음 명령을 실행합니다.

```powershell
python -m modules.health_logic
```

`python modules\health_logic.py`로도 실행할 수 있습니다. 콘솔 테스트는 임시
데이터를 사용하므로 종료하면 기록이 삭제되며, 기존 GUI 데이터는 변경되지 않습니다.

BMI 구간은 화면 예시 기준입니다.

- 저체중: 18.5 미만
- 정상: 18.5 이상 25 미만
- 과체중: 25 이상 30 미만
- 비만: 30 이상

AI가 작성한 코드의 사용 정보는 각 Python 파일의 머리말에 기록되어 있습니다.
제출 전에 머리말의 작성자 이름을 본인 이름으로 바꾸세요.
