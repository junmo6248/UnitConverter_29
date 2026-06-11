# UnitConverter_29 — Product Requirements Document (PRD)

| 항목 | 내용 |
|------|------|
| 프로젝트 | Unit Converter — 길이 단위 변환 (Python) |
| 워크북 ID | UnitConverter_29 |
| 버전 | 2.0 |
| 최종 갱신 | 2026-06-11 |
| SSOT | 본 문서 (`docs/PRD.md`) |

---

## 1. 개요 (Overview)

### 1.1 목적

사용자가 입력한 길이(`단위:값`)를 기반으로, 해당 값을 **등록된 모든 단위**로 변환해 출력하는 CLI 프로그램.

### 1.2 핵심 목표

- 새 단위 추가 시 **기존 코드 변경 최소화** (OCP)
- **SRP**를 만족하는 클래스·계층 구조
- **Dual-Track TDD** + **Golden Master**로 변환·검증 품질 보장
- UI(CLI/GUI/API)와 Logic **분리** — Use Case 중심

### 1.3 참고 문서

| 유형 | 경로 |
|------|------|
| 워크북·실습 가이드 | [`README.md`](../README.md) |
| Activity 1 — 설계 분석 | [`Report/01.UnitConverter_29-Activity1-요구사항-설계-분석-보고서.md`](../Report/01.UnitConverter_29-Activity1-요구사항-설계-분석-보고서.md) |
| Activity 3 — RED 스켈레톤 | [`Report/02.UnitConverter_29-Activity3-입력검증-RED-스켈레톤-보고서.md`](../Report/02.UnitConverter_29-Activity3-입력검증-RED-스켈레톤-보고서.md) |
| Activity 2·3 — TDD GREEN | [`Report/03.UnitConverter_29-Activity2-3-TDD-GREEN-보고서.md`](../Report/03.UnitConverter_29-Activity2-3-TDD-GREEN-보고서.md) |
| Golden Master | [`Report/04.UnitConverter_29-Golden-Master-전체-보고서.md`](../Report/04.UnitConverter_29-Golden-Master-전체-보고서.md) |
| Activity 4 — 포맷 선택 RED | [`Report/05.UnitConverter_29-출력-포맷-선택-RED-스켈레톤-보고서.md`](../Report/05.UnitConverter_29-출력-포맷-선택-RED-스켈레톤-보고서.md) |
| 세션 Transcript | [`Prompting/`](../Prompting/) |

---

## 2. 기능 요구사항 (FR)

### FR-1 — 입력·변환·출력 (기본)

| ID | 요구사항 | 우선순위 | 상태 |
|----|----------|----------|------|
| FR-1.1 | 사용자 입력 형식: `{단위}:{숫자}` (예: `meter:2.5`) | P0 | ✅ |
| FR-1.2 | 입력값을 meter·feet·yard 등 **등록된 전체 단위**로 변환 | P0 | ✅ |
| FR-1.3 | 변환 결과를 줄 단위 텍스트로 출력 (예: `2.5 meter = 8.2 feet`) | P0 | ✅ (`TextFormatter`, 기본 `text` 포맷) |
| FR-1.4 | CLI 진입점에서 Parser → UseCase → Formatter 흐름 | P1 | ✅ (`CliController`, `UnitConverter.py` → `create_app()`) |
| FR-1.5 | 런타임 출력 포맷 선택: `{format}:{단위}:{숫자}` | P1 | ✅ (`OutputFormatterFactory`, T-UI-014~022) |

**입력·출력 예시**

```
입력: meter:2.5          → text (기본, 표 형태)
입력: json:meter:2.5     → JSON
입력: csv:meter:2.5      → CSV
입력: text:meter:2.5     → 표 형태 줄 출력

출력 (text / meter:2.5):
2.5 meter = 2.5 meter
2.5 meter = 8.2021 feet
2.5 meter = 2.7340 yard
```

### FR-2 — 지원 단위·변환 규칙

| ID | 요구사항 | 우선순위 | 상태 |
|----|----------|----------|------|
| FR-2.1 | 기본 단위: meter, feet, yard | P0 | ✅ |
| FR-2.2 | `1 meter = 3.28084 feet` | P0 | ✅ (`config/units.json` → `ConversionRegistry`) |
| FR-2.3 | `1 meter = 1.09361 yard` | P0 | ✅ |
| FR-2.4 | feet/yard 간 비율은 **meter 기준** 2단계 변환 | P0 | ✅ (`LengthConverter`) |
| FR-2.5 | 소수 변환 정확도 — golden 기준 4자리 | P1 | ✅ |

### FR-3 — 입력값 검증 (품질)

| ID | 요구사항 | Test ID | 상태 |
|----|----------|---------|------|
| FR-3.1 | 음수 입력 거부 | T-LOGIC-003 | ✅ |
| FR-3.2 | `:` 없는 형식 거부 | T-UI-002 | ✅ |
| FR-3.3 | 숫자 변환 불가 (`meter:abc`) 거부 | T-LOGIC-006 | ✅ |
| FR-3.4 | 미등록 단위 (`inch`) 거부 | T-LOGIC-004 | ✅ |
| FR-3.5 | 빈 값·빈 단위 거부 | T-LOGIC-008, 009 | ✅ |
| FR-3.6 | 0 및 정상 값 통과 | T-LOGIC-007, 010 | ✅ |

### FR-4 — 확장성 (OCP)

| ID | 요구사항 | Test ID | 상태 |
|----|----------|---------|------|
| FR-4.1 | 단위 추가 시 `if/elif` 수정 없이 Registry 확장 | T-LOGIC-011 | ✅ |
| FR-4.2 | `register(unit, to_meter_factor)` 동적 등록 | T-LOGIC-012, 005 | ✅ |
| FR-4.3 | cubit 등록 예: `1 cubit = 0.4572 meter` | T-LOGIC-005 | ✅ |
| FR-4.4 | 출력 포맷 Strategy (Text/JSON/CSV) | T-UI-003, 004, 010 | ✅ |
| FR-4.5 | 런타임 포맷 선택 (`json`/`csv`/`text`) | T-UI-014~022 | ✅ |

### FR-5 — 추가 요구사항

| ID | 요구사항 | 우선순위 | 상태 |
|----|----------|----------|------|
| FR-5.1 | 변환 비율 **설정 외부화** (JSON) | P1 | ✅ (`ConfigLoader`, `config/units.json`) |
| FR-5.1b | YAML 설정 지원 | P2 | ⏳ |
| FR-5.2 | CLI 동적 단위 등록 (`register:cubit:0.4572`, `1 cubit = 0.4572 meter`) | P2 | ✅ (T-UI-011~013) |
| FR-5.3 | CSV 출력 포맷 | P2 | ✅ (T-UI-010, 021) |
| FR-5.4 | GUI/Web API 확장 | P3 | ⏳ (설계만, README UI 확장 매핑) |

---

## 3. 비기능 요구사항 (NFR)

| ID | 요구사항 | 구현·검증 |
|----|----------|-----------|
| NFR-1 | **OCP** — 단위·포맷 확장 시 기존 Converter/Formatter 미수정 | `ConversionRegistry`, Formatter Strategy |
| NFR-2 | **SRP** — 파싱·검증·변환·포맷·오케스트레이션 분리 | Domain / Application / Boundary |
| NFR-3 | **UI/Logic 분리** — Use Case는 `input()`/`print()` 비의존 | `ConvertLengthUseCase` (DTO) |
| NFR-4 | **Dual-Track TDD** — Logic/UI 테스트 분리 | `tests/entity/`, `tests/boundary/` |
| NFR-5 | **Golden Master** — 출력 스냅샷 회귀 방지 | `tests/golden/*.approved.txt` |
| NFR-6 | **1 RED 묶음 = 1 commit** | GREEN 커밋 이력 (Report/03, 포맷 선택 3 commits) |
| NFR-7 | 변환 비율 SSOT | `config/units.json` → `ConfigLoader` → `ConversionRegistry` |

---

## 4. 아키텍처

### 4.1 계층 구조

```
Presentation (CLI)     Boundary: InputParser, InputCommandParser, CliController
                       OutputFormatter (Text/Json/Csv), OutputFormatterFactory
Application              ConvertLengthUseCase, RegisterUnitUseCase, app_factory
Domain (Logic)           ConversionRegistry, LengthConverter, InputValidator
Infrastructure           ConfigLoader → config/units.json
Entry                    UnitConverter.py → create_app().controller
```

### 4.2 클래스 책임

| 계층 | 클래스 | 역할 |
|------|--------|------|
| Domain | `ConversionRegistry` | 단위·meter 기준 비율 저장·조회·등록 |
| Domain | `LengthConverter` | meter 기준 `convert_all()` |
| Domain | `InputValidator` | 단위·숫자·음수 검증 |
| Application | `ConvertLengthUseCase` | 검증 → 변환 → DTO |
| Application | `RegisterUnitUseCase` | 동적 단위 등록 |
| Application | `app_factory.create_app()` | DI 조립 (Registry, UseCase, Controller) |
| Boundary | `InputParser` | `단위:값` 파싱 |
| Boundary | `InputCommandParser` | 변환·등록·포맷 접두사 파싱 |
| Boundary | `TextFormatter` / `JsonFormatter` / `CsvFormatter` | 출력 Strategy |
| Boundary | `OutputFormatterFactory` | `json`/`csv`/`text` → Formatter |
| Boundary | `CliController` | Parser → UseCase → Formatter |
| Infrastructure | `ConfigLoader` | JSON 설정 로드 |
| Entry | `UnitConverter.py` | CLI `input()`/`print()` 진입점 |

### 4.3 디렉터리 구조

```
src/
  domain/              # Logic
  application/         # Use Case, app_factory
  boundary/
    input/             # InputParser, InputCommandParser, commands
    output/            # Formatter Strategy, OutputFormatterFactory
  infrastructure/      # ConfigLoader
  UnitConverter.py     # CLI 진입점
config/
  units.json           # 변환 비율 SSOT
tests/
  entity/              # Track B
  boundary/            # Track A
  golden/              # Golden Master (32 files)
  _approval.py
Report/
Prompting/
docs/
  PRD.md               # 본 문서
```

---

## 5. Dual-Track 테스트 명세

### 5.1 Track 정의

| Track | Layer | 경로 | Mock |
|-------|-------|------|------|
| **B — Logic** | entity | `tests/entity/` | Domain Mock **금지** |
| **A — UI** | boundary | `tests/boundary/` | Domain Mock **허용** |

### 5.2 Track B — Logic (15건)

| Test ID | 대상 | Given | Then | FR | Golden |
|---------|------|-------|------|-----|--------|
| T-LOGIC-001 | `LengthConverter` | `meter:2.5` | 3단위 정확 | FR-2 | ✅ |
| T-LOGIC-002 | `LengthConverter` | `feet:10` | meter ≈ 3.048 | FR-2 | ✅ |
| T-LOGIC-003 | `InputValidator` | value `< 0` | 검증 실패 | FR-3.1 | ✅ |
| T-LOGIC-004 | `InputValidator` | unit `inch` | 검증 실패 | FR-3.4 | ✅ |
| T-LOGIC-005 | `ConversionRegistry` | `register("cubit", 0.4572)` | cubit 변환 | FR-4.3 | ✅ |
| T-LOGIC-006 | `InputValidator` | `meter:abc` | 검증 실패 | FR-3.3 | ✅ |
| T-LOGIC-007 | `InputValidator` | value `0` | 통과 | FR-3.6 | ✅ |
| T-LOGIC-008 | `InputValidator` | 빈 value | 검증 실패 | FR-3.5 | ✅ |
| T-LOGIC-009 | `InputValidator` | 빈 unit | 검증 실패 | FR-3.5 | ✅ |
| T-LOGIC-010 | `InputValidator` | `meter`, `2.5` | 통과 | FR-3.6 | ✅ |
| T-LOGIC-011 | `ConversionRegistry` | `meter` | registered | FR-4.1 | ✅ |
| T-LOGIC-012 | `ConversionRegistry` | register cubit | registered | FR-4.2 | ✅ |
| — | `RegisterUnitUseCase` | register cubit | Registry 반영 | FR-5.2 | — |
| — | `RegisterUnitUseCase` | register 후 convert | cubit 변환 | FR-5.2 | — |

### 5.3 Track A — UI (22건)

| Test ID | 대상 | Given | Then | FR | Golden |
|---------|------|-------|------|-----|--------|
| T-UI-001 | `InputParser` | `"meter:2.5"` | parse OK | FR-1.1 | ✅ |
| T-UI-002 | `InputParser` | `"invalid"` | parse_error | FR-3.2 | ✅ |
| T-UI-003 | `TextFormatter` | results dict | 줄 텍스트 | FR-1.3 | ✅ |
| T-UI-004 | `JsonFormatter` | results dict | 유효 JSON | FR-4.4 | ✅ |
| T-UI-005 | `CliController` | Mock UseCase | 흐름 호출 | FR-1.4 | ✅ |
| T-UI-006 | `InputParser` | `"meter:"` | empty value | FR-1.1 | ✅ |
| T-UI-007 | `InputParser` | `":2.5"` | empty unit | FR-1.1 | ✅ |
| T-UI-008 | `InputParser` | `""` | parse_error | FR-3.2 | ✅ |
| T-UI-009 | `InputParser` | `"meter:2.5:extra"` | split `:`, 1 | FR-1.1 | ✅ |
| T-UI-010 | `CsvFormatter` | results dict | CSV | FR-5.3 | ✅ |
| T-UI-011 | `InputCommandParser` | `register:cubit:0.4572` | RegisterCommand | FR-5.2 | — |
| T-UI-012 | `InputCommandParser` | `1 cubit = 0.4572 meter` | RegisterCommand | FR-5.2 | — |
| T-UI-013 | `CliController` | register 명령 | Registry 반영 | FR-5.2 | ✅ |
| T-UI-014 | `OutputFormatterFactory` | `"json"` | JsonFormatter | FR-4.5 | ✅ |
| T-UI-015 | `OutputFormatterFactory` | `"csv"` | CsvFormatter | FR-4.5 | ✅ |
| T-UI-016 | `OutputFormatterFactory` | `"text"` | TextFormatter | FR-4.5 | ✅ |
| T-UI-017 | `OutputFormatterFactory` | `"xml"` | 오류 | FR-4.5 | ✅ |
| T-UI-018 | `InputCommandParser` | `json:meter:2.5` | format+json | FR-1.5 | ✅ |
| T-UI-019 | `InputCommandParser` | `meter:2.5` | format=text | FR-1.5 | ✅ |
| T-UI-020 | `CliController` | `json:meter:2.5` | JSON E2E | FR-1.5 | ✅ |
| T-UI-021 | `CliController` | `csv:meter:2.5` | CSV E2E | FR-5.3 | ✅ |
| T-UI-022 | `CliController` | `text:meter:2.5` | 표 E2E | FR-1.3 | ✅ |

### 5.4 의도적 제외

| 항목 | 이유 |
|------|------|
| GUI 자동화 | 후속 세션 — 수동 검증 |
| `ConfigLoader` I/O | Infrastructure 통합 테스트 별도 |

---

## 6. Golden Master 명세

### 6.1 절차

1. `tests/_approval.py` — `assert_matches_golden`
2. `tests/golden/{test-id}.approved.txt` 연결
3. `UPDATE_GOLDEN=1 pytest …` — 기준 생성
4. `UPDATE_GOLDEN` 없이 **matched** 확인

### 6.2 포맷

| 1행 | Track B | Track A |
|-----|---------|---------|
| 상태 | `ok` \| `validation_error` | `ok` \| `parse_error` \| `validation_error` |
| 2행+ | `key=value` (알파벳 순) | 동일 (CLI 출력은 `format_text_output_golden` / `format_json_output_golden` 사용) |

- 갱신: **`UPDATE_GOLDEN=1`만** — 수동 편집 우회 **금지**
- Command: `.cursor/commands/golden-master.md`
- 현재: **32/32 golden matched** (37 tests total)

---

## 7. 구현 현황

| Activity | 내용 | Report | 상태 |
|----------|------|--------|------|
| 1 | 요구사항·OCP/SRP 설계·PRD 매핑 | Report/01 | ✅ |
| 2·3 | TC — RED→GREEN (기본·검증) | Report/02, 03 | ✅ |
| 3+ | Golden Master (초기 21건) | Report/04 | ✅ |
| 4 | ConfigLoader, CSV, CLI 등록, 포맷 선택 | Report/05 | ✅ |

### 7.1 pytest 현황

```bash
python -m pytest -q
# 37 passed
```

### 7.2 미완 항목

| 항목 | FR | 비고 |
|------|-----|------|
| YAML 설정 로드 | FR-5.1b | JSON만 지원 |
| GUI `GuiController` | FR-5.4 | 설계만 (README UI 확장 매핑) |
| Web API | FR-5.4 | 미착수 |
| `ConfigLoader` 전용 TC | — | Infrastructure — 의도적 제외 |
| T-UI-011, 012 golden | — | 선택적 후속 |

---

## 8. 성공 기준 (Success Criteria)

| # | 기준 | 결과 |
|---|------|------|
| SC-1 | meter/feet/yard 변환 정확 | ✅ |
| SC-2 | 입력 검증 4종 (음수·형식·단위·숫자) | ✅ |
| SC-3 | OCP/SRP 3계층 구조 | ✅ |
| SC-4 | Dual-Track 37 TC GREEN | ✅ |
| SC-5 | Golden Master 32 matched | ✅ |
| SC-6 | 설정 외부화 (JSON) | ✅ |
| SC-7 | CSV 출력 | ✅ |
| SC-8 | E2E CLI (`UnitConverter.py`) | ✅ |
| SC-9 | 런타임 포맷 선택 (json/csv/text) | ✅ |
| SC-10 | CLI 동적 단위 등록 | ✅ |

---

## 9. 로드맵

| 단계 | 작업 | 비고 |
|------|------|------|
| 후속 | YAML 설정 지원 | FR-5.1b |
| 후속 | GUI `GuiController` | FR-5.4, 수동 검증 |
| 후속 | Web API `ApiController` | FR-5.4 |
| Activity 5 | 회고·발표 | Report/06 예정 |

---

## 10. Cursor Commands

| Command | 역할 |
|---------|------|
| `/export` | Report + Prompting Transcript Export |
| `/golden-master` | Golden Master 구축·검증 |

---

*본 PRD는 [`Report/`](../Report/)·[`Prompting/`](../Prompting/) 세션 산출물과 [`README.md`](../README.md) 워크북을 종합한 SSOT입니다.*
