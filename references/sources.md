# 근거 자료와 반영 범위

이 스킬은 공개 편집 지침과 작성자가 지정한 문체 선호를 연구·기술 문서에 맞게 정리했습니다. 아래의 반영은 전체 소스나 실행 기능의 통합을 뜻하지 않습니다.

## 2026-10-24 대조한 두 저장소

| 출처 | 반영한 원칙과 위치 | 포함하지 않은 기능·범위 |
|---|---|---|
| [im-not-ai의 실행 지침](https://github.com/epoko77-ai/im-not-ai/blob/main/skills/humanize-korean/SKILL.md) | 의미·서법 보존 → SKILL 2·3·5절, 번역투·추상명사·대조·쉼표 검토 → L1 | 전체 분류 목록, 경로 선택, 다중 에이전트 실행, 변경률·구조 게이트, 자동 서법 복원은 미구현 |
| [korean-humanizer의 지침](https://github.com/dotoricode/korean-humanizer/blob/main/SKILL.md) 및 [카탈로그](https://github.com/dotoricode/korean-humanizer/blob/main/references/ko-ai-signals.md) | 의미·추정 강도 보존, 개인 선호, 문서별 어조 → SKILL·register-guide. 있다·것·수·논리 연결어 보존 → L1-10 | 전체 12범주 카탈로그·브랜드 프로필 로더는 미구현. 발화체·SNS 규칙은 대상 밖. 해당 저장소의 기술 문서 제외 범위는 이 스킬의 연구·기술 문서 목적에 맞게 달리 정함 |

위 파일 본문을 GitHub를 통해 대조했습니다. im-not-ai에서 확인한 트리 리비전은 `b37e0206d31fffd9149bf57168d4d62eb2086bee`, korean-humanizer의 SKILL.md 파일 blob은 `b9c179a4d846b1311c380db660de64cb744b0a11`입니다. 위 링크는 main을 가리키므로 이후 내용이 바뀔 수 있습니다. 지속적인 자동 동기화는 하지 않습니다.

변경률 상한은 채택하지 않았습니다. 문장을 많이 바꿔도 의미를 보존할 수 있고 적게 바꿔도 의미를 훼손할 수 있으므로 원문과 결과의 주장·조건·수치·서법을 직접 대조합니다. 검사기 후보 수를 교정 품질 점수로 사용하지 않습니다.

## 기존 참고 자료

기존 버전은 K-Humanizer의 추상명사 구체화·일괄 치환 금지와 patina의 정의형 은유·의인화·속격 연쇄를 참고 자료로 명시했습니다. 각각 L1-1·L1-3, L1-4·L2-4·L2-5에 대응합니다. 이번 대조에서는 이 두 저장소의 최신 버전 전체를 재검증하지 않았습니다.

작성자가 지적한 사례는 [문체 안내](style-patterns.md)와 [로드맵 사례](case-study-roadmap.md)에 있습니다. 문법 오류 판정이나 AI 작성자 판별용 분류가 아닙니다.

## References

[1] epoko77-ai, "im-not-ai: Korean AI writing pattern taxonomy and humanizer," *GitHub Repository*, 2026. [Online]. Available: https://github.com/epoko77-ai/im-not-ai

[2] dotoricode, "korean-humanizer: Korean AI writing checklist and humanizer skill," *GitHub Repository*, 2026. [Online]. Available: https://github.com/dotoricode/korean-humanizer

[3] evergreentree97, "K-Humanizer: Korean LLM text naturalizer," *GitHub Repository*, v0.1 pre-release, 2026. [Online]. Available: https://github.com/evergreentree97/K-Humanizer

[4] devswha, "patina: Pattern-based humanizer for Korean, English, Chinese, and Japanese (189 named patterns, v9.1.0)," *GitHub Repository*, 2026. [Online]. Available: https://github.com/devswha/patina
