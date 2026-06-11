# Golden Master — Approval Test 구축·검증

**GREEN PASS 직후** 대상 Test ID에 Golden Master(Approval Test)를 연결·검증한다.  
`src/` 동작 변경 없이 **출력 스냅샷**이 기준 파일과 일치하는지 확인한다.

---

## 호출 방법

```
/golden-master
/golden-master T-LOGIC-001
```

- 인자 없으면 채팅·최근 GREEN 보고·`pytest` 결과에서 **방금 PASS한 Test ID 1개**를 자동 선택한다.
- **한 번에 Test ID 1개**만 Golden Master를 구축·검증한다.

---

## Phase 선언 (필수)

답변 **첫 줄**은 반드시:

```
Phase: green | Layer: entity | Track: Logic
```

| 필드 | 값 | 기본 (이 프로젝트) |
|------|-----|-------------------|
| `Phase` | `green` | 고정 (GREEN 후속 · golden 연결) |
| `Layer` | `entity` \| `boundary` | `entity` |
| `Track` | `Logic` \| `UI` | `Logic` |

> **Track A (Boundary):** `T-UI-*` golden일 때 `Layer: boundary` 로만 바꾸면 본 Command를 **재사용**한다.

---

## 전제 조건

| # | 조건 |
|---|------|
| 1 | 대상 Test ID **`pytest` PASS** |
| 2 | `/green-minimal` 완료 또는 동등 GREEN 커밋·보고 존재 |
| 3 | `src/` **동작 변경 금지** (golden·테스트 assert 추가만) |
| 4 | `tests/golden/{id}.approved.txt` **미존재** 또는 `UPDATE_GOLDEN=1`로 갱신 |

미충족 시 중단하고 PASS 확보를 안내한다.

---

## 절차 (순서 고정)

| # | 단계 | 작업 |
|---|------|------|
| 1 | **`tests/_approval.py`** | `assert_matches_golden` 없으면 **생성** |
| 2 | **golden 연결** | `tests/golden/{id}.approved.txt` (`T-LOGIC-001` → `t-logic-001.approved.txt`) |
| 3 | **기준 생성** | `UPDATE_GOLDEN=1 pytest …` → `.approved.txt` 자동 생성 |
| 4 | **matched 확인** | `UPDATE_GOLDEN` 없이 동일 pytest → **matched** |

---

## Golden 파일 포맷 (고정)

### 공통 — 1행: 결과 상태 (에러 코드 문자열)

| 값 | 의미 |
|----|------|
| `ok` | 정상 변환·검증 통과 |
| `validation_error` | `InputValidator` 거부 (음수·미등록 단위·숫자 오류) |
| `parse_error` | `InputParser` 거부 (`:` 누락 등) |

> **워크북 공통 계약 참고:** MagicSquare 계열은 1행 `pass` \| `fail` \| `incomplete` + 2행 `int[6]` 1-index 를 쓴다.  
> **UnitConverter_29**는 길이 변환 도메인이므로 아래 **2행 이후 스냅샷** 규칙을 따른다.

### Track B — Logic (`T-LOGIC-*`)

| 줄 | 필드 | 형식 |
|----|------|------|
| 1 | 결과 상태 | `ok` \| `validation_error` |
| 2+ | 스냅샷 | `key=value` 한 줄씩, **키 알파벳 순** 고정 |

**변환 예 — T-LOGIC-001**

```
ok
feet=8.2021
meter=2.5
yard=2.734025
```

**검증 실패 예 — T-LOGIC-003**

```
validation_error
code=negative_value
unit=meter
value=-1
```

- 소수는 golden 생성 시 `pytest` 직렬화 함수가 반올림·자릿수를 **고정**한다 (기본 소수 4자리).
- **golden 수동 편집으로 통과 우회 금지.** 갱신은 `UPDATE_GOLDEN=1` 만.

### Track A — UI (`T-UI-*`)

| 줄 | 필드 | 형식 |
|----|------|------|
| 1 | 결과 상태 | `ok` \| `parse_error` |
| 2+ | 스롅샷 | `key=value` 알파벳 순 |

**파싱 예 — T-UI-001**

```
ok
unit=meter
value_str=2.5
```

**파싱 실패 예 — T-UI-002**

```
parse_error
input=invalid
```

---

## `assert_matches_golden` 계약

`tests/_approval.py`에 아래 계약을 둔다.

```python
from pathlib import Path

GOLDEN_DIR = Path(__file__).parent / "golden"


def assert_matches_golden(test_id: str, actual: str) -> None:
    slug = test_id.lower().replace("_", "-")
    path = GOLDEN_DIR / f"{slug}.approved.txt"
    if __import__("os").environ.get("UPDATE_GOLDEN") == "1":
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(actual, encoding="utf-8")
        return
    expected = path.read_text(encoding="utf-8")
    assert actual == expected, (
        f"golden mismatch: {path}\n--- expected ---\n{expected}\n--- actual ---\n{actual}"
    )
```

테스트별 `format_*_golden(actual_dict) -> str` 는 `tests/` 에 두고, **1행 상태 + 알파벳순 key=value** 로 직렬화한다.

---

## Test ID → golden · 직렬화 매핑 (SSOT)

| Test ID | Track | golden 파일 | 직렬화 대상 |
|---------|-------|---------------|-------------|
| T-LOGIC-001 | B | `t-logic-001.approved.txt` | `LengthConverter.convert_all(2.5, "meter")` |
| T-LOGIC-002 | B | `t-logic-002.approved.txt` | `convert_all(10, "feet")["meter"]` |
| T-LOGIC-003 | B | `t-logic-003.approved.txt` | `ValidationError` 스냅샷 |
| T-LOGIC-004 | B | `t-logic-004.approved.txt` | 미등록 단위 거부 |
| T-LOGIC-005 | B | `t-logic-005.approved.txt` | cubit 등록 후 `convert_all` |
| T-UI-001 | A | `t-ui-001.approved.txt` | `InputParser.parse` 결과 |
| T-UI-002 | A | `t-ui-002.approved.txt` | `ParseError` 스냅샷 |
| T-UI-003 | A | `t-ui-003.approved.txt` | `TextFormatter.format` 출력 |

채팅·인자에 Test ID가 없으면 **T-LOGIC-001** (최근 GREEN 변환 테스트) 우선.

---

## pytest 명령

**기준 생성 (Windows PowerShell)**

```powershell
$env:UPDATE_GOLDEN=1; python -m pytest tests/entity/test_length_converter.py::test_meter_2_5_converts_to_all_units_accurately -v
```

**matched 확인**

```powershell
Remove-Item Env:UPDATE_GOLDEN -ErrorAction SilentlyContinue
python -m pytest tests/entity/test_length_converter.py::test_meter_2_5_converts_to_all_units_accurately -v
```

**Track A 예 (T-UI-001)**

```powershell
$env:UPDATE_GOLDEN=1; python -m pytest tests/boundary/test_input_parser.py::test_valid_meter_colon_value_parses_unit_and_value -v
```

---

## 수정 범위

| 허용 | 금지 |
|------|------|
| `tests/_approval.py` 생성·추가 | golden **수동 편집** (우회) |
| `tests/golden/*.approved.txt` (`UPDATE_GOLDEN=1` 시만) | `src/` 동작 변경 |
| 대상 테스트에 golden assert **추가** (기존 AAA 유지) | skip·xfail·assert 완화 |
| `format_*_golden` 직렬화 (`tests/`) | Test ID **2개 이상** 동시 golden |
| | `git commit` (사용자 요청 시만) |

---

## 보고 형식 (완료 후)

답변 마지막에 아래를 채운다.

```
## Golden Master 보고

- **Test ID:** T-LOGIC-00N
- **Phase:** green | Layer: entity | Track: Logic
- **golden 경로:** `tests/golden/t-logic-00n.approved.txt`
- **matched:** ✅ / ❌
- **diff 요약:** <없음 | 1행 상태 코드 | 2행+ key=value — expected … / actual …>
- **pytest (UPDATE_GOLDEN=1):** PASSED / FAILED
- **pytest (matched):** PASSED / FAILED
- **다음:** 다음 Test ID golden 또는 `/export`
```

---

## 금지

- golden `.approved.txt` **수동 편집**으로 matched 우회
- `UPDATE_GOLDEN=1` 없이 기존 golden **덮어쓰기**
- PASS하지 않은 Test ID에 golden 연결
- golden 연결 중 `src/` 리팩토링·동작 변경

---

## 참조

- PRD·Dual-Track: `README.md`
- GREEN 절차: (프로젝트 green-minimal Command 추가 시 연결)
- Export: `.cursor/commands/export.md`
- 테스트: `tests/entity/`, `tests/boundary/`
