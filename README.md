
## Unit Converter (Python)
![unit-converter](./unit-converter.jpg)
### Overview
- 사용자가 입력한 길이(`단위:값`)를 기반으로, 해당 값을 다른 모든 단위로 변환해 출력하는 프로그램.
- 새로운 단위를 추가할 때 기존 코드의 변경이 최소화되도록 설계한다.
- 각 단위 변환 로직은 테스트 코드로 검증한다.

### 가상환경 설정 및 실행
```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 가상환경 활성화 (macOS/Linux)
source venv/bin/activate

# 실행
python src/UnitConverter.py

# 테스트
python -m pytest -q

# 가상환경 비활성화
deactivate
```

**CLI 입력 예시**

| 입력 | 동작 |
|------|------|
| `meter:2.5` | 전체 단위 변환 (text 포맷, 기본) |
| `json:meter:2.5` | JSON 출력 |
| `csv:feet:10` | CSV 출력 |
| `text:yard:1` | 표 형태 줄 출력 |
| `register:cubit:0.4572` | cubit 단위 등록 |
| `1 cubit = 0.4572 meter` | cubit 단위 등록 (자연어) |

### 기본 요구사항
1. 사용자 입력 예시:
   ```
   meter:2.5
   ```
   → 출력:
   ```
   2.5 meter = 8.2 feet
   2.5 meter = 2.7 yard
   ...
   ```

2. 현재 지원 단위:
   - meter
   - feet
   - yard

3. 새로운 단위가 추가될 때도 기존 코드의 변경이 최소화되도록 할 것.

4. 각 단위 간 변환이 정확히 계산되도록 테스트 코드를 작성할 것.

### 비즈니스 로직
- `1 meter = 3.28084 feet`
- `1 meter = 1.09361 yard`
- feet/yard 간의 비율은 meter 기반으로 계산.

### 품질 요구사항
- OCP를 만족하는 설계
- SRP를 만족하는 클래스 구성
- 입력 값 검증 (음수, 잘못된 형식, 없는 단위)

### 추가 요구사항
- **설정 외부화** ✅
   - 변환 비율을 외부 설정 파일(`config/units.json`)에서 로드
- **동적으로 단위와 비율을 등록** ✅
   - `register:cubit:0.4572` 또는 `1 cubit = 0.4572 meter`
- **출력 포맷 선택** ✅
   - `json:` / `csv:` / `text:` 접두사 또는 기본 text (표 형태)

> 상세 요구·테스트 명세: [`docs/PRD.md`](docs/PRD.md)

### 설계 구조 및 PRD 매핑

제안 아키텍처는 **Domain(Logic) · Application · Presentation(UI)** 3계층으로 구성한다.

| 계층 | 클래스 | 역할 |
|------|--------|------|
| Domain | `ConversionRegistry` | 단위와 meter 기준 변환 비율 저장·조회·등록 |
| Domain | `LengthConverter` | meter 기준 길이 변환 계산 |
| Domain | `InputValidator` | 형식·숫자·단위·음수 등 입력값 검증 |
| Application | `ConvertLengthUseCase` | 검증 → 변환 → 결과 DTO 반환 (UI 비의존) |
| Application | `RegisterUnitUseCase` | 동적 단위 등록 |
| Application | `app_factory.create_app()` | Registry·UseCase·Controller DI 조립 |
| Presentation (CLI) | `CliController` | CLI 실행 흐름 오케스트레이션 |
| Presentation (CLI) | `InputParser` / `InputCommandParser` | `단위:값`·등록·포맷 접두사 파싱 |
| Presentation (CLI) | `OutputFormatter` + `OutputFormatterFactory` | Text/JSON/CSV Strategy 및 런타임 선택 |
| Infrastructure | `ConfigLoader` | `config/units.json`에서 비율 로드 |
| Entry | `UnitConverter.py` | CLI `input()`/`print()` 진입점 |

#### Dual-Track

Logic(변환·검증)과 UI(입력·출력·포맷) 테스트를 **분리**한다. Track B를 먼저 GREEN한 뒤 Track A를 진행한다.

| Track | Layer | 대상 클래스 | Test ID | Mock | 테스트 경로 |
|-------|-------|-------------|---------|------|-------------|
| **B — Logic** | entity | `ConversionRegistry`, `LengthConverter`, `InputValidator`, `ConvertLengthUseCase`, `RegisterUnitUseCase` | `T-LOGIC-*` | Domain Mock **금지** | `tests/entity/` |
| **A — UI** | boundary | `CliController`, `InputParser`, `InputCommandParser`, `OutputFormatter*`, `OutputFormatterFactory` | `T-UI-*` | Domain Mock **허용** | `tests/boundary/` |

| Track | 검증 초점 | Mock 허용 이유 |
|-------|-----------|----------------|
| **B — Logic** | 변환 정확도·단위 등록·음수/미등록 단위 검증 | Domain은 순수 로직 — Mock 없이 실제 객체로 검증 |
| **A — UI** | 입력 파싱·출력 포맷·CLI/GUI 흐름 | Boundary는 Use Case·Converter를 Mock으로 대체 가능 |

**Track B — Logic 테스트**

| ID | 대상 | Given | Then | 상태 |
|----|------|-------|------|------|
| T-LOGIC-001 | `LengthConverter` | `meter:2.5` | 3단위 변환값 정확 (feet `8.2021…`, yard `2.734…`) | ✅ |
| T-LOGIC-002 | `LengthConverter` | `feet:10` | meter `3.048…` | ✅ |
| T-LOGIC-003 | `InputValidator` | value `< 0` | 검증 실패 | ✅ |
| T-LOGIC-004 | `InputValidator` | unit `inch` (미등록) | 검증 실패 | ✅ |
| T-LOGIC-005 | `ConversionRegistry` | `register("cubit", 0.4572)` | cubit 변환 가능 | ✅ |
| T-LOGIC-006 | `InputValidator` | `meter:abc` (숫자 아님) | 검증 실패 | ✅ |
| T-LOGIC-007 | `InputValidator` | value `0` | 검증 통과 | ✅ |
| T-LOGIC-008 | `InputValidator` | `meter`, `""` (빈 값) | 검증 실패 | ✅ |
| T-LOGIC-009 | `InputValidator` | `""`, `2.5` (빈 단위) | 검증 실패 | ✅ |
| T-LOGIC-010 | `InputValidator` | `meter`, `2.5` | 검증 통과 | ✅ |
| T-LOGIC-011 | `ConversionRegistry` | `meter` | `is_registered` True | ✅ |
| T-LOGIC-012 | `ConversionRegistry` | `register("cubit", …)` | `is_registered` True | ✅ |
| — | `RegisterUnitUseCase` | register cubit | Registry·변환 | ✅ |

**Track A — UI 테스트**

| ID | 대상 | Given | Then | 상태 |
|----|------|-------|------|------|
| T-UI-001 | `InputParser` | `"meter:2.5"` | `("meter", "2.5")` | ✅ |
| T-UI-002 | `InputParser` | `"invalid"` | 파싱 실패 | ✅ |
| T-UI-003 | `TextFormatter` | 변환 결과 dict | 줄 단위 텍스트 출력 | ✅ |
| T-UI-004 | `JsonFormatter` | 변환 결과 dict | 유효한 JSON | ✅ |
| T-UI-005 | `CliController` | Mock Use Case | 입력→출력 흐름 호출 | ✅ |
| T-UI-006 | `InputParser` | `"meter:"` | `("meter", "")` | ✅ |
| T-UI-007 | `InputParser` | `":2.5"` | `("", "2.5")` | ✅ |
| T-UI-008 | `InputParser` | `""` | 파싱 실패 | ✅ |
| T-UI-009 | `InputParser` | `"meter:2.5:extra"` | `("meter", "2.5:extra")` | ✅ |
| T-UI-010 | `CsvFormatter` | 변환 결과 dict | CSV 출력 | ✅ |
| T-UI-011 | `InputCommandParser` | `register:cubit:0.4572` | RegisterCommand | ✅ |
| T-UI-012 | `InputCommandParser` | `1 cubit = 0.4572 meter` | RegisterCommand | ✅ |
| T-UI-013 | `CliController` | register 명령 | Registry 반영 | ✅ |
| T-UI-014 | `OutputFormatterFactory` | `"json"` | JsonFormatter | ✅ |
| T-UI-015 | `OutputFormatterFactory` | `"csv"` | CsvFormatter | ✅ |
| T-UI-016 | `OutputFormatterFactory` | `"text"` | TextFormatter | ✅ |
| T-UI-017 | `OutputFormatterFactory` | `"xml"` | 지원하지 않는 포맷 오류 | ✅ |
| T-UI-018 | `InputCommandParser` | `json:meter:2.5` | format + unit + value | ✅ |
| T-UI-019 | `InputCommandParser` | `meter:2.5` | format=text (기본) | ✅ |
| T-UI-020 | `CliController` | `json:meter:2.5` | JSON E2E | ✅ |
| T-UI-021 | `CliController` | `csv:meter:2.5` | CSV E2E | ✅ |
| T-UI-022 | `CliController` | `text:meter:2.5` | 표 형태 E2E | ✅ |

**검증 현황:** `37 passed` · Golden **32/32 matched** (`tests/golden/`)

| 제외 (의도적) | 이유 |
|---------------|------|
| GUI 자동화 (PyQt 등) | GUI 프로토타입은 수동 검증 — 후속 세션 |
| `ConfigLoader` 파일 I/O | Infrastructure — 통합 테스트 또는 별도 Track |

#### Overview ↔ 설계 매핑

| PRD (Overview) | 담당 클래스 | 설명 |
|----------------|-------------|------|
| `단위:값` 입력 기반 전체 단위 변환·출력 | `CliController`, `InputParser`, `ConvertLengthUseCase`, `LengthConverter`, `OutputFormatter` | CLI에서 입력 수집 → Use Case 실행 → Formatter로 출력 |
| 새 단위 추가 시 기존 코드 변경 최소화 | `ConversionRegistry`, `LengthConverter` | Registry에 등록만으로 변환 로직 확장 (OCP) |
| 단위 변환 로직 테스트 코드 검증 | `LengthConverter`, `InputValidator`, `ConversionRegistry` | UI 없는 순수 Logic 클래스 대상 단위 테스트 |

#### 기본 요구사항 ↔ 설계 매핑

| PRD (기본 요구사항) | 담당 클래스 | 설명 |
|---------------------|-------------|------|
| `meter:2.5` 형식 입력 | `InputParser` | `:` 기준으로 unit·value 분리 |
| 모든 단위로 변환 결과 출력 | `LengthConverter`, `OutputFormatter` | `convert_all()` → Formatter가 줄 단위 텍스트 출력 |
| meter / feet / yard 지원 | `ConversionRegistry` | `config/units.json`에서 초기 비율 로드 |
| 단위 추가 시 변경 최소화 | `ConversionRegistry.register()` | `if/elif` 분기 없이 Registry 확장 |
| 변환 정확도 테스트 | `LengthConverter` (+ test) | meter 기준 변환식 단위 테스트 |

#### 비즈니스 로직 ↔ 설계 매핑

| PRD (비즈니스 로직) | 담당 클래스 | 설명 |
|---------------------|-------------|------|
| `1 meter = 3.28084 feet` | `ConversionRegistry` | `config/units.json` feet → meter 비율 |
| `1 meter = 1.09361 yard` | `ConversionRegistry` | `config/units.json` yard → meter 비율 |
| feet/yard 비율은 meter 기준 계산 | `LengthConverter` | 입력 → meter → 목표 단위 2단계 변환 |

#### 품질 요구사항 ↔ 설계 매핑

| PRD (품질 요구사항) | 담당 클래스 / 원칙 | 설명 |
|---------------------|-------------------|------|
| OCP (확장에 열림, 수정에 닫힘) | `ConversionRegistry`, `OutputFormatter` (Strategy) | 단위·출력 포맷 추가 시 기존 Converter/Formatter 미수정 |
| SRP (단일 책임) | 전 클래스 | 파싱·검증·변환·포맷·오케스트레이션 책임 분리 |
| 음수 입력 검증 | `InputValidator.validate()` | Use Case 진입 전 거부 |
| 잘못된 형식 검증 | `InputParser`, `InputValidator` | `:` 누락·숫자 변환 실패 처리 |
| 없는 단위 검증 | `InputValidator` | Registry 미등록 단위 거부 |

#### 추가 요구사항 ↔ 설계 매핑

| PRD (추가 요구사항) | 담당 클래스 | 설명 | 상태 |
|---------------------|-------------|------|------|
| 설정 외부화 (JSON) | `ConfigLoader` → `ConversionRegistry` | `config/units.json` 로드 | ✅ |
| YAML 설정 | `ConfigLoader` | — | ⏳ |
| 동적 단위·비율 등록 | `RegisterUnitUseCase`, `InputCommandParser`, `CliController` | register 명령 파싱 후 Registry 추가 | ✅ |
| JSON 출력 | `JsonFormatter` | Strategy | ✅ |
| CSV 출력 | `CsvFormatter` | Strategy | ✅ |
| 표 형태 출력 | `TextFormatter` | 기본 text 포맷 | ✅ |
| 런타임 포맷 선택 | `OutputFormatterFactory`, `InputCommandParser` | `{format}:{unit}:{value}` | ✅ |

#### UI 확장 시 Logic 분리 매핑

| 확장 시나리오 | Logic (재사용) | Presentation (UI별 추가) |
|---------------|----------------|--------------------------|
| CLI → GUI 추가 | `ConvertLengthUseCase`, `LengthConverter`, `InputValidator`, `ConversionRegistry` | `GuiController` (위젯 입력·테이블 표시) |
| CLI → Web API 추가 | 동일 Logic 계층 | `ApiController` (HTTP 요청/응답) |
| 출력 형식 추가 | Logic 변경 없음 | `OutputFormatter` 구현체 추가 |
| 단위 추가 | `ConversionRegistry` 등록만 | UI 변경 없음 (목록 자동 반영) |


## 생성형AI를 활용한 Activities (6 시간)

1. 문제 코드 및 기본 요구사항 분석 (0.5시간)
   - 기본 코드구조, 로직 이해
2. 기본 요구사항 및 품질 요구사항 구현 (2시간)
   - OCP를 만족하는 인터페이스 구현 
   - SRP를 만족하도록 클래스 구현 
   - 입력값 검증을 위한 구현
3. TC 구현 (0.5시간)
   - 단위변환 기능 검증 및 입력 값 검증 TC 작성 
4. 추가 요구사항 구현 (2시간)
   - 3개 요구사항 구현 및 TC 작성 
5. 회고 및 발표 (1시간)
   - 실습 목표와 달성도
   - AI를 어떻게 활용했나? 도움이 된 순간과 한계는?
   - TC를 추가해보면서 개선에 미친 영향, TC 작성 팁
   - 클린코드와 리팩토링에서 느낀 장점과 어려운점
