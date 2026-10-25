# heeseok-korean-anti-slop

연구·기술 문서와 강의·실습 자료에 반복되는 한국어 AI 문체를 찾아 고치는 Codex·Claude Code용 스킬입니다. 번역투, 과장된 은유, 선언문 나열을 검토하되 **사실·수치·인용·전문 용어와 주장의 강도는 보존**합니다.

문체 교정 지침과 Python 검사기를 제공합니다. 검사기는 의심 표현을 표시하며 문맥에 따른 교정은 스킬을 사용하는 에이전트와 작성자가 판단합니다. **AI 작성 여부를 판별하는 도구는 아닙니다.**

## 어떤 AI 문체를 고치나요?

이 스킬은 작성자가 피하고 싶은 다음 문체를 교정합니다. 네 명칭은 이 저장소에서 사용하는 편집 분류이며 서로 겹칠 수 있습니다.

| 문체 | 대표 패턴 | 교정 대상 |
| --- | --- | --- |
| **은유·경구형 슬롭(Metaphor & Aphoristic Slop)** | `6칸을 채운다`, `손잡이를 돌린다`, `사람은 하나지만 자리는 두 개입니다` | 실제 작업을 대신하는 은유와 경구형 대조 |
| **은유·수사학 슬롭(Rhetorical Slop)** | `진짜 무대가 시작됩니다`, `본질은 속도가 아니라 밀도입니다` | 설명보다 앞서는 비유·수사·정의형 단언 |
| **초압축 메니페스토 슬롭(Hyper-Compressed Manifesto Slop)** | `성공을 전제하지 않는다`, `조기 종료·재샘플링의 오판 비용을 기록한다` | 조건과 대상을 압축한 원칙문 나열 |
| **원칙주의적 의사 엄밀성(Performative Epistemic Rigor)** | `연구 부재를 단정하지 않고 비교 조건과 반증 가능한 질문으로 적는다`, `효과를 절제한다` | 엄밀한 원칙처럼 들리지만 조건·기준·호응이 불분명한 문체 |

앞의 두 문체는 주로 L2, 뒤의 두 문체는 주로 L3에서 다룹니다. 자세한 설명은 [문체 안내](references/style-patterns.md)에 있습니다.

### 왜 이런 문체가 나왔는가?

“군더더기 없이 핵심 원칙만 요약해”라는 요청에 영어 격언형 지침을 직역한 듯한 문체가 나올 수 있다는 **설명 가설**입니다.

> Never presuppose success. Count the cost of early stopping. Temper the effect of plan modifications.

위 문장은 번역투를 설명하기 위한 가상의 예시입니다. “LLM이 영어로 먼저 구상한 뒤 한국어로 직역한다”는 내부 과정을 확인한 자료는 아닙니다. 이 스킬은 원인을 단정하지 않고 작성자가 원치 않는 출력 패턴을 교정합니다. [가설의 범위와 교정 기준](references/style-patterns.md)

## 세 가지 교정 레이어

| 레이어 | 검토하는 표현 | 교정 방향 |
| --- | --- | --- |
| L1 구조적 번역투 | `~에 있어서`, 이중 피동, 추상명사·속격 연쇄, 가짜 대조, 정보 없는 맺음말 | 실제 행위와 대상을 밝히고 불필요한 조사·수식을 줄입니다. |
| L2 은유·경구 | `손잡이를 돌린다`, `혁신의 나침반`, 인위적인 대구, 정의형 은유, 의인화 | 비유가 가리키는 작업과 관계를 직접 설명합니다. 뜻이 불분명하면 작성자에게 확인합니다. |
| L3 선언문·연어 | `~하지 않는다`의 반복, `효과를 절제한다`, 과압축 명사구, 번역투 간접의문문 | 문서에 맞는 종결어미를 쓰고 생략된 조건과 자연스러운 서술어 호응을 복원합니다. |

같은 표현도 문맥에 따라 자연스러울 수 있습니다. 기술 용어로 굳은 `파이프라인`, `백본`, `증류` 등은 기계적으로 치환하지 않습니다. 자세한 판정 조건과 예외는 [SKILL.md](SKILL.md)와 [레이어별 참고 문서](references/)에 있습니다.

## 교정 예시

| 원문 | 교정 예시 | 규칙 |
| --- | --- | --- |
| `기업의 데이터의 안전한 관리의 효율성` | 기업 데이터를 안전하게 관리하는 효율 | L1-4 속격 연쇄 |
| `가정을 남긴다.` | 가정을 명시합니다. | L3-2 직역 연어 |
| `비용을 센다.` | 비용을 산정합니다. | L3-2 직역 연어 |
| `조기 종료·재샘플링의 오판 비용을 기록한다.` | 생성을 일찍 멈추거나 다시 샘플링할 때 판단이 잘못되어 발생한 비용을 기록합니다. | L3-3 과압축 명사구 |

원문에 없는 성과, 수치, 담당자나 원인을 추가하지 않습니다. `~일 수 있다`를 `~이다`로 바꾸거나 계획을 완료된 사실로 바꾸지 않습니다. 문서의 종류에 따라 적절한 종결어미도 달라집니다.

## 설치

저장소 루트에 `SKILL.md`가 있습니다. 저장소 전체를 스킬 폴더에 복제하면 참고 문서와 검사기도 함께 설치됩니다. **아래 명령은 대상 폴더가 없을 때** 사용합니다. 이미 설치했다면 업데이트 명령을 사용하십시오.

### Codex

사용자 스킬 경로인 `~/.agents/skills/`에 설치합니다.

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.agents\skills" | Out-Null
git clone https://github.com/ohheeseok/heeseok-korean-anti-slop.git "$env:USERPROFILE\.agents\skills\heeseok-korean-anti-slop"
```

macOS / Linux:

```bash
mkdir -p ~/.agents/skills
git clone https://github.com/ohheeseok/heeseok-korean-anti-slop.git ~/.agents/skills/heeseok-korean-anti-slop
```

프로젝트 전용 경로는 `.agents/skills/heeseok-korean-anti-slop/`입니다. 경로와 스킬 검색 방식은 [OpenAI 공식 문서](https://learn.chatgpt.com/docs/build-skills)를 참고하십시오.

### Claude Code

사용자 스킬 경로인 `~/.claude/skills/`에 설치합니다.

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills" | Out-Null
git clone https://github.com/ohheeseok/heeseok-korean-anti-slop.git "$env:USERPROFILE\.claude\skills\heeseok-korean-anti-slop"
```

macOS / Linux:

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/ohheeseok/heeseok-korean-anti-slop.git ~/.claude/skills/heeseok-korean-anti-slop
```

프로젝트 전용 경로는 `.claude/skills/heeseok-korean-anti-slop/`입니다. 자세한 설정은 [Claude Code 공식 문서](https://code.claude.com/docs/en/skills)를 참고하십시오.

양쪽에 별도로 복제했다면 업데이트도 각 폴더에서 진행해야 합니다. 기존에 한 폴더를 junction이나 symlink로 공유하고 있다면 실제 파일이 있는 폴더에서만 업데이트합니다.

### 업데이트

설치한 스킬 폴더에서 실행합니다.

```bash
git pull --ff-only
```

로컬 변경이나 서로 다른 커밋 때문에 업데이트가 중단되면 변경 사항을 먼저 확인하십시오. 위 명령은 로컬 변경 사항을 강제로 덮어쓰지 않습니다.

## 사용

에이전트에 스킬 이름과 교정할 문서를 지정합니다.

```text
heeseok-korean-anti-slop 스킬로 report.html을 검토해줘.
번역투·은유·선언문 반복을 고치되 수치, 인용, 전문 용어와 추측의 강도는 유지해줘.
```

```text
이 실험 지침을 자연스러운 한국어로 윤문해줘.
원문에 없는 사실은 추가하지 말고 의미가 불분명하면 확인할 항목을 알려줘.
```

교정 결과에는 다음 내용을 포함하도록 지침이 구성되어 있습니다.

1. 교정문
2. `위치 | 원문 | 교정 | 규칙 ID` 형식의 핵심 교정 요약
3. 수치·인용·용어·헤지 보존 확인
4. 검토 후 남긴 표현과 이유
5. 의미가 불분명해 확인이 필요한 항목(해당할 때만, 본문 밖에 작성)

## 반영 범위와 검증 한계

im-not-ai와 korean-humanizer에서 연구·기술 문서에 필요한 편집 원칙을 선별했습니다. 전체 카탈로그, 다중 에이전트 실행, 변경률 게이트나 자동 복원 기능을 통합한 것은 아닙니다. [출처별 반영 범위](references/sources.md)를 참고하십시오.

검사기는 작성자가 제시한 8개 문장을 모두 검토 후보로 표시합니다. 이는 탐지 회귀 검사 결과이며 실제 교정 품질이나 일반 문장의 탐지율을 입증하지 않습니다. `성공을 전제하지 않는다`는 개인 선호 후보(L3-1a)이고 선언문 연속 검사(L3-1)와 구분합니다.

회귀 검사는 저장소 루트에서 `python -m unittest discover -s tests -v`로 실행합니다.

Claude Opus 5.5(high)와 Gemini 4 Argon(medium)의 독립·교차 검토를 반영했습니다. [검토 결과와 반영 판단](docs/review-2026-10-24.md), [의미 보존 점검 사례](references/behavioral-checks.md)를 확인할 수 있습니다.

## 강의·실습 자료를 검토할 때

v1.0.4는 어려운 전문용어 없이도 나타나는 ‘손·자리·층’ 비유, 조작 대상이 불분명한 지시어, 교훈형 완료 판정을 다룹니다. 강의의 자연스러운 구어체·질문, 시연용 대화·같은 프롬프트의 반복, 복사본·중단·되돌리기 절차는 보존합니다. [강의 자료 지침](references/lecture-prose.md)과 [첫 사례 분석](docs/case-first-contact.md)을 참고하십시오.

자료 분석·스킬 개선만 요청하면 원문은 읽기 전용으로 다룹니다. 교정 예시는 스킬이나 분석 보고서에만 적습니다.

## 논문·기술 해설을 검토할 때

v1.0.5는 ‘호라이즌 3형제’ 같은 캐릭터화, 예측과 정제를 배타적으로 대비하는 구호, ‘동시에 해결·구조적으로 보장’ 같은 결론의 조건·근거를 검토합니다. 기술 용어와 로봇의 실제 손잡이 조작은 보존하며, 강한 주장을 근거 없이 낮추지 않습니다. v1.0.6은 `X가 병목입니다`라는 진단형 결말이 실제 제약 설명을 대신하며 반복되는지도 검토합니다. [기술 해설 지침](references/technical-explanation.md)과 [Diffusion Policy 사례 분석](docs/case-diffusion-policy.md)을 참고하십시오.

## 검사기

Python 표준 라이브러리만 사용합니다. 별도 패키지나 API 키가 필요하지 않습니다. 파일을 읽어 후보와 종결어미 분포를 출력하며 **파일을 수정하지 않습니다.**

저장소 루트에서 실행하는 예시입니다. `report.html`과 `draft.md` 등은 검사할 실제 파일 경로로 바꾸십시오.

```bash
# 텍스트, Markdown, HTML 검사
python scripts/scan_slop.py report.html

# HTML의 aria-label, title, alt 등 숨은 텍스트도 포함
python scripts/scan_slop.py report.html --hidden

# L2·L3 규칙별 후보를 최대 5개씩 표시
python scripts/scan_slop.py draft.md --rules L2,L3 --examples 5

# 백틱과 따옴표로 표시한 예시 구간 제외
python scripts/scan_slop.py style-guide.md --skip-quoted

# 여러 파일 검사
python scripts/scan_slop.py draft.md report.html --examples 2
```

`--rules`는 규칙 ID 접두어를 쉼표로 지정합니다. `L3-1` 선언형 연속 검사와 종결어미 분포는 별도 집계이므로 `--rules`와 관계없이 출력됩니다.

결과의 행 번호는 추출한 텍스트 기준이며 HTML 소스 행 번호와 다를 수 있습니다. 성공적으로 실행되면 후보가 발견되어도 종료 코드는 `0`입니다. 후보 개수를 통과·실패 기준이나 AI 작성 확률로 해석하지 마십시오. 실제 칸·손잡이·수학적 좌표계도 어휘상 후보로 표시될 수 있으므로 문맥을 보고 남깁니다. L3-3은 한글 명사와 비용·오차·이득·효과 등의 제한된 조합을 찾으며 모든 압축 명사구를 탐지하지 않습니다. L2-8은 일부 강의형 신체·앱·층 비유를 표시합니다. L2-9는 기술 용어를 꾸미는 일부 친족·생존·삽입 비유를, L1-12는 포괄적 해결·보장 표현을 표시합니다. 강한 표현도 실제 증명·정의가 있으면 적절할 수 있습니다. 지시 대상·인용 경계·여러 장에 걸친 대조·요약의 조건·근거는 사람이 문맥에서 판단합니다.

## 적용 범위와 한계

- 연구 노트, 논문 초안, 제안서, 실험 지침, 로드맵, README, 슬라이드·HTML의 한국어 문구를 대상으로 합니다.
- 채팅 말투, 문학적 글, 인용 원문, 코드와 로그는 교정 대상에서 제외합니다.
- 시각 디자인을 교정하거나 AI 작성 여부를 판별하지 않습니다.
- 정규식 검사에는 오탐과 누락이 있습니다. HTML 검사도 브라우저 렌더링이나 완전한 DOM 분석을 대신하지 않습니다.
- 후보가 `0`개라고 해서 문장이 정확하거나 자연스럽다는 뜻은 아닙니다. 사실 확인과 전문 분야 검토는 별도로 필요합니다.
- 학술지나 연구실의 문체 규정과 사용자의 명시적 지침을 우선합니다.

## 파일 구성

```text
heeseok-korean-anti-slop/
├── SKILL.md
├── README.md
├── CHANGELOG.md
├── references/
│   ├── style-patterns.md
│   ├── layer1-translationese.md
│   ├── layer2-metaphor-aphorism.md
│   ├── layer3-manifesto-collocation.md
│   ├── register-guide.md
│   ├── case-study-roadmap.md
│   └── sources.md
└── scripts/
    └── scan_slop.py
```

실제 교정 전후 기록은 [case-study-roadmap.md](references/case-study-roadmap.md)에, 버전별 변경 사항은 [CHANGELOG.md](CHANGELOG.md)에 있습니다.

## 근거 자료

원본 스킬은 im-not-ai, korean-humanizer, K-Humanizer, patina의 규칙과 실제 교정 사례를 참고해 정리했습니다. 각 자료의 반영 범위와 링크는 [sources.md](references/sources.md)에 기록되어 있습니다.

규칙이나 검사기 개선을 제안하려면 문서 종류, 문제가 되는 문장, 기대하는 교정 예시를 함께 제시해 주십시오.
