# 근거 자료와 반영 범위

이 스킬은 공개 편집 지침과 작성자가 지정한 문체 선호를 연구·기술 문서에 맞게 정리했습니다. 아래의 반영은 전체 소스나 실행 기능의 통합을 뜻하지 않습니다.

## 2026-10-24 대조한 두 저장소

| 출처 | 반영한 원칙과 위치 | 포함하지 않은 기능·범위 |
|---|---|---|
| [im-not-ai의 실행 지침](https://github.com/epoko77-ai/im-not-ai/blob/main/skills/humanize-korean/SKILL.md) | 의미·서법 보존 → SKILL 2절·register-guide, 번역투·추상명사·대조·쉼표 검토 → L1 | 전체 분류 목록, 경로 선택, 다중 에이전트 실행, 변경률·구조 게이트, 자동 서법 복원은 미구현 |
| [korean-humanizer의 지침](https://github.com/dotoricode/korean-humanizer/blob/main/SKILL.md) 및 [카탈로그](https://github.com/dotoricode/korean-humanizer/blob/main/references/ko-ai-signals.md) | 의미·추정 강도 보존, 개인 선호, 문서별 어조 → SKILL·register-guide. 있다·것·수·논리 연결어 보존 → L1-10 | 전체 12범주 카탈로그·브랜드 프로필 로더는 미구현. 발화체·SNS 규칙은 대상 밖. 해당 저장소의 기술 문서 제외 범위는 이 스킬의 연구·기술 문서 목적에 맞게 달리 정함 |

위 파일 본문을 GitHub를 통해 대조했습니다. im-not-ai에서 확인한 트리 리비전은 `b37e0206d31fffd9149bf57168d4d62eb2086bee`, korean-humanizer의 SKILL.md 파일 blob은 `b9c179a4d846b1311c380db660de64cb744b0a11`입니다. 위 링크는 main을 가리키므로 이후 내용이 바뀔 수 있습니다. 지속적인 자동 동기화는 하지 않습니다.

변경률 상한은 채택하지 않았습니다. 문장을 많이 바꿔도 의미를 보존할 수 있고 적게 바꿔도 의미를 훼손할 수 있으므로 원문과 결과의 주장·조건·수치·서법을 직접 대조합니다. 검사기 후보 수를 교정 품질 점수로 사용하지 않습니다.

## 기존 참고 자료

기존 버전은 K-Humanizer의 추상명사 구체화·일괄 치환 금지와 patina의 정의형 은유·의인화·속격 연쇄를 참고 자료로 명시했습니다. 각각 L1-1·L1-3, L1-4·L2-4·L2-5에 대응합니다. 이번 대조에서는 이 두 저장소의 최신 버전 전체를 재검증하지 않았습니다.

작성자가 지적한 사례는 [문체 안내](style-patterns.md)와 [로드맵 사례](case-study-roadmap.md)에 있습니다. 문법 오류 판정이나 AI 작성자 판별용 분류가 아닙니다.

## 2026-10-25 비교에서 참고한 구성 방식

| 자료 | 참고한 점 | 이 스킬에 반영한 범위 |
|---|---|---|
| [yoonmoon](https://github.com/amondnet/yoonmoon/blob/main/skills/humanize/SKILL.md) | 과장 제거와 성분 생략 방지를 함께 점검 | 기존 의미 보존 기준에 필수 조사·어미·조건절의 과삭제 점검을 연결 |
| [blader/humanizer](https://github.com/blader/humanizer/blob/main/SKILL.md) | 문장뿐 아니라 문단의 대조·경구·반복 결말을 검토 | 긴 문서의 실제 설명과 수사용 반복을 구분하는 기준 보완 |
| [humanizer-kr](https://github.com/liam-nextdomain/humanizer-kr/blob/main/humanizer-kr/SKILL.md) | 교정 예시와 보존 반례, 절별 검토와 전체 문맥 대조 | 이 스킬용 합성 대조 사례를 새로 작성. 고정 분할 길이·빈도 임계값이나 외부 교정 예시를 정답으로 가져오지 않음 |
| [K-Humanizer](https://github.com/evergreentree97/K-Humanizer), [ashgreat/humanizer](https://github.com/ashgreat/humanizer/blob/main/SKILL.md) | 사례·교정 쌍·보존 기준·실패 결과를 함께 검토 | 평가 입력의 출처와 실제 출력을 남기고 의미 보존과 문체 개선을 분리 |

외부 예문·데이터셋·실행 스크립트를 복제하지 않았습니다. 새 [대조 사례](contrast-examples.md)와 [평가 자료](../evals/README.md)는 합성 입력과 기존에 공개한 자체 사례에서 만들었습니다. 사용자가 수락한 실제 문단 쌍이 확보되기 전에는 그 종류의 평가 자료가 있다고 보고하지 않습니다. 공개 지침의 설계 방식이 유용하다는 판단과 실제 교정 성능의 우열은 구분합니다.

## 2026-11-22 메타카피·규정·면책투·과잉 정당화 추가

세 유형은 사용자의 질문에서 시작해 세 모델(Claude, Codex, Gemini)이 독립 답변과 상호 검토를 거쳐 정리했습니다. 논의와 채택하지 않은 제안은 [검토 기록](../docs/review-2026-11-22.md)에 있습니다.

| 자료 | 확인한 내용 | 이 스킬에 반영한 범위 |
|---|---|---|
| Hyland & Tse [5] | 학술 글의 메타담화를 글의 구성을 안내하는 표현과 독자와의 관계를 조정하는 표현(헤지·강조어·태도 표지·참여 표지·자기 언급)으로 나누는 대표 문헌 | 이 분류를 빌려 메타담화를 정상 기능으로 보고, 내용·조건·근거를 대신할 때만 교정한다는 이 스킬의 경계를 정함(L1-16·L3-9). 교정 기준 자체는 이 스킬의 편집 판단 |
| Chang [6] | 에이전트가 원자료를 확장한 보고서에서 원자료보다 강한 주장을 한 뒤 다시 면책하는 현상(over-defensive writing)을 다루고, 반론을 분리하는 실행 구조를 제안. 원인(가상의 AI 심사자를 의식한 글쓰기)은 초록에서 저자의 가정으로 제시 | 일반 문서에서 과잉 주장과 면책의 짝을 근거 수준의 주장으로 합치는 판단(L3-9)은 이 연구를 참고한 이 스킬의 편집 가설. 원인은 가설로만 기록 |
| Cox 외 [7] | 지시 학습 모델이 일부 과제에서 연쇄 추론(CoT)을 쓰기 전에 답을 정한다고 보고. 사후 추론이 유용할 수 있다는 점도 언급 | 과잉 정당화의 원인 가설 참고. 한국어 문서 문체의 원인을 입증하는 자료로 쓰지 않음 |
| Turpin 외 [8] | 연쇄 추론 프롬프팅에서 의도적으로 넣은 편향 단서가 답을 바꿔도 모델의 설명이 그 단서를 언급하지 않는 실험 | 위와 같음 |

사용자가 제공한 비교 글의 교정 예시는 원문에 없는 수치·환경·계획을 넣었습니다. 그 문형은 [행동 점검 사례](behavioral-checks.md)의 실패 점검 입력으로만 반영했습니다. 같은 글이 인용한 Inc. 칼럼은 접근이 막혀 확인하지 못했으므로 반영하지 않았습니다. [6]·[7]은 arXiv 초록 페이지에서 서지 정보와 주장 범위를 확인했으며 본문 전체를 검토하지는 않았습니다. [5]·[8]은 이번 작업에서 원문을 다시 열어 보지 않은 기존 문헌입니다.

## 2026-11-26 발표 덱 교정 피드백 반영

사용자가 논문 리뷰 발표 덱 네 편을 1.3.0으로 교정한 뒤 정리한 피드백을 반영했습니다. 덱과 교정 기록은 비공개 자료이므로 저장소에 넣지 않았고 예시는 같은 문형으로 다시 쓰거나 짧게 줄였습니다.

| 피드백에서 확인한 내용 | 반영한 범위 |
|---|---|
| 이해를 막은 것은 작성자가 만들어 정의 없이 반복한 라벨이었고 검사기 후보에는 거의 나타나지 않음 | L3-11 추가. 검사기로 탐지하지 않는 문맥 규칙으로 명시 |
| 원 내용을 모르는 편집자는 라벨을 풀지 못하고 은유·연어만 고쳤으며 은유를 `배제`·`해당` 같은 추상어로 옮김 | SKILL 2절의 대상 확인 경로와 라벨 단위 확인 사항, 4절의 교정 회귀 점검, L2-1의 교정이 아닌 예, 검사기 `--baseline` |
| `VLM 조건`처럼 두 단어로 행위자를 지운 압축, 동사 없는 질문 조각, 명사로 끝나는 캡션·안내 | L3-3·L3-4·L3-5 보완 |
| 화살표·부등호가 동사 역할을 하는 정리 줄 | L3-12와 검사기 후보 규칙 |
| 본문 수치에 잘못 붙은 `약`, 슬라이드 삽입 뒤 어긋난 상호참조 번호 | L3-9 보완, 긴 문서 검토 항목 |
| L1-7 쉼표 후보가 다른 후보를 가림 | 검사기 `--exclude` |

피드백이 제안한 라벨 탐지 검사기와 평가 사례 추가는 반영하지 않았습니다. 형태소 분석 없이 정의되지 않은 라벨을 찾으면 오탐이 많고 원 자료가 비공개라 평가 자료의 출처 기준(evals/README.md)을 충족하지 못하기 때문입니다.

## References

[1] epoko77-ai, "im-not-ai: Korean AI writing pattern taxonomy and humanizer," *GitHub Repository*, 2026. [Online]. Available: https://github.com/epoko77-ai/im-not-ai

[2] dotoricode, "korean-humanizer: Korean AI writing checklist and humanizer skill," *GitHub Repository*, 2026. [Online]. Available: https://github.com/dotoricode/korean-humanizer

[3] evergreentree97, "K-Humanizer: Korean LLM text naturalizer," *GitHub Repository*, v0.1 pre-release, 2026. [Online]. Available: https://github.com/evergreentree97/K-Humanizer

[4] devswha, "patina: Pattern-based humanizer for Korean, English, Chinese, and Japanese (189 named patterns, v9.1.0)," *GitHub Repository*, 2026. [Online]. Available: https://github.com/devswha/patina

[5] K. Hyland and P. Tse, "Metadiscourse in academic writing: A reappraisal," *Applied Linguistics*, vol. 25, no. 2, pp. 156–177, 2004.

[6] X. Chang, "A harness reducing over-defensive writing in agents by isolating objections," arXiv:2610.36717, Oct. 2026. [Online]. Available: https://arxiv.org/abs/2610.36717

[7] K. Cox, D. Kianersi, and A. Garriga-Alonso, "Post-hoc reasoning in chain of thought: Decoding and steering pre-committed answers," arXiv:2603.01437, Mar. 2026 (v2 Jul. 2026). [Online]. Available: https://arxiv.org/abs/2603.01437

[8] M. Turpin, J. Michael, E. Perez, and S. R. Bowman, "Language models don't always say what they think: Unfaithful explanations in chain-of-thought prompting," in *Advances in Neural Information Processing Systems*, 2023. [Online]. Available: https://arxiv.org/abs/2305.04388

## 사용자 제공 강의 사례

v1.0.4는 사용자가 읽기 전용 분석을 요청한 초보자용 강의 11장을 사례로 사용했습니다. 사례에서 도출한 판단 기준은 [강의 자료 지침](lecture-prose.md)과 [행동 점검 사례](behavioral-checks.md)에 있습니다. 원본 강의와 사례 분석 기록은 이 저장소에 포함하지 않습니다.

## 사용자 제공 기술 해설 사례

v1.0.5는 사용자가 읽기 전용으로 제공한 Diffusion Policy 해설 HTML의 본문·그림 설명·동적 안내 문자열을 분석했습니다. 원 논문의 수학적·실험적 주장 전체를 재검증한 작업은 아닙니다. 편집 기준은 [기술 해설 지침](technical-explanation.md)에 정리했습니다. 원본 HTML과 사례 분석 기록은 이 저장소에 포함하지 않습니다.
