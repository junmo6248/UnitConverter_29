# Export — Report + Transcript

이번 Cursor 세션을 **Report 보고서**와 **Prompting Transcript** 두 파일로 내보낸다.

---

## 호출 방법

```
/export
/export 02 설계-PRD-매핑
/export 03 OCP-SRP-분석
```

- `/export` 뒤 텍스트가 있으면 **세션 번호·슬러그·제목 힌트**로 사용한다.
- 없으면 `Report/`·`Prompting/` 기존 파일에서 **다음 번호**를 자동 결정하고, 세션 내용으로 슬러그를 제안한다.
- **추가 질문 없이** `/export` 만으로도 동작한다 (슬러그는 채팅·README·산출물에서 자동 추출).

---

## 파일 번호·이름 규칙

| 항목 | 규칙 |
|------|------|
| 번호 | 2자리 접두사 `01.` `02.` … (기존 최대값 + 1) |
| 프로젝트 ID | `UnitConverter_29` 고정 |
| Report | `Report/NN.UnitConverter_29-<슬러그>.md` |
| Transcript | `Prompting/NN.UnitConverter_29-<슬러그>-Export-Transcript.md` |

**슬러그 예시 (NN은 Report·Transcript 공통)**

| 세션 유형 | Report | Transcript |
|-----------|--------|------------|
| 요구사항·코드 분석 | `NN.UnitConverter_29-요구사항-분석-보고서.md` | `NN.UnitConverter_29-요구사항-분석-Export-Transcript.md` |
| 설계·클래스 다이어그램 | `NN.UnitConverter_29-설계-다이어그램-보고서.md` | `NN.UnitConverter_29-설계-다이어그램-Export-Transcript.md` |
| OCP·SRP 분석 | `NN.UnitConverter_29-OCP-SRP-분석-보고서.md` | `NN.UnitConverter_29-OCP-SRP-분석-Export-Transcript.md` |
| PRD 매핑 | `NN.UnitConverter_29-PRD-매핑-보고서.md` | `NN.UnitConverter_29-PRD-매핑-Export-Transcript.md` |
| TDD (RED/GREEN) | `NN.UnitConverter_29-세션N-TDD-보고서.md` | `NN.UnitConverter_29-세션N-TDD-Export-Transcript.md` |
| 리팩토링 | `NN.UnitConverter_29-리팩토링-보고서.md` | `NN.UnitConverter_29-리팩토링-Export-Transcript.md` |

> Transcript는 `NN.UnitConverter_29-<중간슬러그>-Export-Transcript.md` 형식을 따른다.

**기존 파일 참고 (번호 중복 금지)**

```
Report/01.UnitConverter_29-<슬러그>.md
Prompting/01.UnitConverter_29-<슬러그>-Export-Transcript.md
```

---

## 작업 순서

1. **폴더 확인** — `Report/`, `Prompting/` 없으면 프로젝트 root에 생성.
2. **번호 결정** — `Report/`·`Prompting/`에서 `NN.` 최대값 확인 → 다음 번호.
3. **슬러그·제목 확정** — 세션 주제·산출물·명령 인자로 파일명 확정.
4. **Report 작성** — `Report/NN.UnitConverter_29-<슬러그>.md` 저장.
5. **Transcript 작성** — `Prompting/NN.UnitConverter_29-<슬러그>-Export-Transcript.md` 저장.
6. **보고** — 아래 Export 보고 template으로 결과 알림.

`git commit` / `git push`는 사용자 요청 시에만.

---

## Report 템플릿

세션 유형에 맞게 섹션을 고르되, **상단 메타 표**는 공통으로 넣는다.

```markdown
# UnitConverter_29 — <세션 제목>

| 항목 | 내용 |
|------|------|
| 프로젝트 | Unit Converter — 길이 단위 변환 (Python) |
| 워크북 ID | UnitConverter_29 |
| 단계 | Activity N — <단계명> |
| 작성일 | YYYY-MM-DD |
| 출처 | <이전 Report/Transcript 링크 또는 채팅 세션> |

---

## 1. 세션 요약

<이번 세션에서 한 일·결정·산출물 3~5문장>

## 2. 핵심 산출물

| 산출물 | 경로·상태 |
|--------|-----------|
| ... | ... |

## 3. PRD / 설계 매핑 (해당 시)

| PRD 항목 | 담당 클래스·결과 |
|----------|------------------|
| ... | ... |

## 4. 성공 기준 / 검증 (해당 시)

| # | 기준 | 결과 |
|---|------|------|
| SC-1 | ... | ✅ / ❌ / 진행 중 |

## 5. 다음 단계

- ...

---

*Transcript: [`Prompting/NN.UnitConverter_29-<슬러그>-Export-Transcript.md`](../Prompting/...)*
```

**설계·분석 세션**이면 클래스 다이어그램·OCP/SRP·UI/Logic 분리·PRD 매핑 표를 포함한다.  
**구현·TDD 세션**이면 Phase·변경 파일·pytest 결과·다음 Phase를 포함한다.

---

## Transcript 템플릿

```markdown
# UnitConverter_29 — <세션 제목>
_Exported on M/D/YYYY from Cursor — UnitConverter_29 session_

---

**User**

<사용자 메시지 요약 또는 원문>

---

**Cursor**

<에이전트 응답 요약 또는 핵심>

---

(... 세션의 User/Cursor 턴을 시간순으로 반복 ...)

---

## 세션 요약 (Export 부록)

| 항목 | 내용 |
|------|------|
| 세션 유형 | ... |
| 주제 (한 문장) | ... |
| 산출물 | `Report/NN....md`, 기타 파일 |
| 다음 단계 | ... |

*상세 보고서: [`Report/NN.UnitConverter_29-<슬러그>.md`](../Report/...)*

---

## 재사용 프롬프트 (원본)

\`\`\`
<이번 세션을 재현하는 대표 프롬프트 1개>
\`\`\`
```

- Transcript는 **대화 전체를 요약·축약**해도 되나, **핵심 User 프롬프트 원문**은 보존한다.
- 시뮬레이션 데이터면 **⚠️ 시뮬레이션** 라벨을 명시한다.
- 실제 경험 Transcript와 **혼합하지 않는다**.

---

## Export 보고 (완료 후)

답변 마지막에 아래를 채운다.

```
## Export 완료

- **번호:** NN
- **Report:** `Report/NN.UnitConverter_29-<슬러그>.md`
- **Transcript:** `Prompting/NN.UnitConverter_29-<슬러그>-Export-Transcript.md`
- **세션 한 줄:** <요약>
- **다음 권장:** <다음 Activity·Phase>
```

---

## 금지

- `01.` 형식 없이 저장
- Report·Transcript **서로 다른 NN** 사용
- 기존 Export 파일 **덮어쓰기** (새 번호로만 추가)
- Transcript 없이 Report만 저장 (항상 **쌍**으로 Export)
- 사용자 요청 없이 `git commit`

---

## 참조

- PRD·설계 매핑: `README.md`
- 소스: `src/UnitConverter.py`
- 기존 Export: `Report/`, `Prompting/`
- 테스트: `tests/`
