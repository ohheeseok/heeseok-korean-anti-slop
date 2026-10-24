"""Flag Korean anti-slop candidates (L1–L3) in text, Markdown, or HTML files.

Usage:
    python scan_slop.py FILE [FILE ...] [--hidden] [--examples N] [--rules L2,L3-1]

Prints, per rule, how many candidates were found and a few examples with line numbers,
followed by a sentence-ending (register) summary. The scanner only lists candidates;
whether each one is slop depends on context (technical terms, quotes, natural usage).
--skip-quoted drops `code` spans and quoted examples, useful for scanning style guides.
--hidden also scans HTML attribute text (aria-label, alt, title, placeholder),
<title>, <desc>, <meta name="description"> and Korean string literals inside <script>.
"""
import argparse
import html as htmllib
import re
import sys
from pathlib import Path

H = '가-힣'
NB = rf'(?<![{H}])'  # previous char is not Hangul (keeps 지도 from matching 속하지도)

RULES = [
    # Layer 1: structural translationese
    ('L1-1', '장황한 조사·후치사', r'[을를] 통해|에 있어서?|함에 있어|에 의해|[와과] 관련하여|에 기반하여|을 바탕으로'),
    ('L1-2', '이중 피동', r'되어지|되어진|어지게 된다|어지게 됩니다|여지게 된다|여지게 됩니다'),
    ('L1-3', '한자어 추상명사', r'고도화|제고|역량 강화|기반 마련|체계 구축|방향성|가능성을 제시|중요성|필요성'),
    ('L1-4', '속격 연쇄 A의 B의 C', rf'[{H}A-Za-z]+의 [{H}A-Za-z]+의 [{H}A-Za-z]+'),
    ('L1-5', '가짜 대조', r'단순히|단순한 [^ ]+ 넘어|[^ ]+을 넘어|가 아니라|이 아니라'),
    ('L1-6', '훈계형 결말·결산어', r'결론적으로|따라서|(^|[.!?] )요약하면,?|이를 통해|시사하는 바|주목할 만|매우 중요|할 때입니다|할 때이다|하는 이유다|핵심은|중요한 것은|관건은|과제도 남아|한계도 분명'),
    ('L1-7', '연결어미 뒤 쉼표', rf'[{H}](고|며|지만|면서|아서|어서|거나|으며|므로|는데),'),
    ('L1-8', 'AI 고빈도 어휘', r'해당 |이러한|다양한|포괄적|혁신적|획기적|활용|도모|모색|극대화|것이다|것입니다'),
    # Layer 2: metaphor, aphorism, personification
    ('L2-1', '물리·촉각 조작 은유 동사', r'채운다|채우는|채워|좁힌다|좁혀|좁히|묶는|묶나|묶어|묶지|관통|가로지르|가로질러|되먹|따라가|맞닿|손잡이|다이얼|스위치를 켜|기어를|영점|퍼즐|단추를|렌즈'),
    ('L2-2', '도구·장소·신체 명사 은유', NB + r'(지도|해부|좌표계|좌표|관문|골격|뼈대|프런티어|청사진|나침반|초석|DNA|아틀라스|여정)'
                                       r'|\b(ATLAS|BRIDGES?|FIELD MAP|WORKING PATH|JOURNEY|BLUEPRINT|COMPASS)\b'),
    ('L2-3', '숫자·크기 대비 경구', rf'{NB}(하나|둘|셋)(지만|,) |[{H}]+ 하나, [{H}]+ (둘|셋|넷|다섯|여섯|일곱|여덟)|아니라 방향|아니라 밀도'),
    ('L2-4', '정의형 은유 등식', rf'(이란|란) [^.]{{0,25}}(이다|입니다)|[{H}]+의 (예술|언어|시그니처|건축물|설계도|심장|엔진|문법|화폐|통화)(이다|입니다|다)'),
    ('L2-5', '무생물 행위주(의인화) 후보', r'놓친다|놓치게|갖춰진다|갖춰지|보여준다|말해준다|드러낸다|증명한다|요구한다|보장하지|보장한다|가린다|가리기'),
    ('L2-6', '해석을 뜻하는 읽는다', r'(로|으로) 읽(는다|지 않|습니다|어야)|읽는다\.|읽지 않는다'),
    # Personal review candidate; not a grammatical error or automatic rewrite.
    ('L3-1a', '작성자 지정 원칙문(문맥 검토)', r'성공을 전제하지 않(?:는다|습니다|음)'),
    # Layer 3: manifesto endings, collocations, compressed nouns, calqued questions
    ('L3-2', '영어 직역 연어', r'효과를 절제|절제한다|비용을 (?:세|센다|셉니다|셀)|셀지|질문으로 적|가정을 남|예산을 태|신호를 되먹'),
    ('L3-3', '과압축 명사구 후보', rf'([{H}A-Za-z0-9]+·){{2,}}[{H}A-Za-z0-9]+의 |조기 종료\s*·\s*재샘플링의 오판 비용'),
    ('L3-4', '번역투 간접의문문', r'무엇을 [^.]{0,30}(하고|이고) 어떤 [^.]{0,30}지|(무엇을|어떤|어디에|어디서) [^.]{0,30}(는지|을지|할지|ㄹ지) (정한|적는|기록|결정)'),
]

SENT_END = re.compile(r'(?<=[.?!])\s+|\n+')
ENDINGS = [
    ('합쇼체(~습니다/~니다)', re.compile(r'(습니다|니다)[.?!]?$')),
    ('해라체 선언형(~한다/~않는다/~이다)', re.compile(rf'[{H}](한다|않는다|이다|없다|있다|된다|했다|였다|진다)[.?!]?$')),
    ('지시형(~하십시오/~하세요)', re.compile(r'(십시오|세요)[.?!]?$')),
    ('명사형·개조식', re.compile(rf'(^|[\s{H}A-Za-z0-9)])(기록|측정|확보|기각|필요|가능|불가|아님|않음|포함|제외|확인|비교|작성|사용|금지|준비|확대|진행|선택|구분|결정|조건|경우)[.?!]?$')),
]


def visible_text(raw, hidden):
    """Return (text, hidden_text) from HTML; keeps line structure roughly."""
    hidden_parts = []
    if hidden:
        hidden_parts += re.findall(r'(?:aria-label|alt|title|placeholder)="([^"]*[가-힣][^"]*)"', raw)
        hidden_parts += re.findall(r'<(?:title|desc)[^>]*>([^<]*[가-힣][^<]*)</(?:title|desc)>', raw)
        hidden_parts += re.findall(r'<meta name="description" content="([^"]*)"', raw)
        for js in re.findall(r'<script(?![^>]*application/json)[^>]*>(.*?)</script>', raw, flags=re.S):
            hidden_parts += re.findall(r"'([^'\n]*[가-힣][^'\n]*)'", js)
    body = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', raw, flags=re.S)
    body = re.sub(r'<svg.*?</svg>', lambda m: '\n'.join(re.findall(r'>([^<]+)<', m.group(0))), body, flags=re.S)
    body = re.sub(r'</(p|li|td|th|h\d|dd|dt|summary|figcaption|caption|div|tr|small)>|<br\s*/?>', '\n', body)
    body = htmllib.unescape(re.sub(r'<[^>]+>', ' ', body))
    return body, '\n'.join(htmllib.unescape(h) for h in hidden_parts)


def load(path, hidden, skip_quoted=False):
    raw = Path(path).read_text(encoding='utf-8', errors='replace')
    if path.lower().endswith(('.html', '.htm')):
        text, hid = visible_text(raw, hidden)
        text = text + ('\n' + hid if hid else '')
    else:
        text = raw
    if skip_quoted:
        # style guides quote the bad examples; drop `code`, "…", “…”, ‘…’ spans
        text = re.sub(r'`[^`\n]*`|"[^"\n]*"|“[^”\n]*”|‘[^’\n]*’', ' ', text)
    return text


def scan(text, rules, n_examples):
    lines = text.split('\n')
    print(f'{"규칙":7} {"건수":>4}  설명')
    for rid, name, pat in rules:
        rx = re.compile(pat)
        hits = []
        for i, line in enumerate(lines, 1):
            if rid == 'L2-6' and line.strip().startswith('읽기'):
                continue
            for m in rx.finditer(line):
                a, b = max(0, m.start() - 28), min(len(line), m.end() + 28)
                hits.append((i, re.sub(r'\s+', ' ', line[a:b]).strip()))
        print(f'{rid:7} {len(hits):>4}  {name}')
        for i, ctx in hits[:n_examples]:
            print(f'          L{i}: …{ctx}…')
    # L3-1: runs of declarative endings
    sents = [re.sub(r'\s+', ' ', s).strip() for s in SENT_END.split(text)]
    sents = [s for s in sents if len(s) > 6 and re.search(f'[{H}]', s)]
    decl = ENDINGS[1][1]
    runs, cur = [], []
    for s in sents:
        if decl.search(s):
            cur.append(s)
        else:
            if len(cur) >= 3:
                runs.append(cur)
            cur = []
    if len(cur) >= 3:
        runs.append(cur)
    print(f'{"L3-1":7} {len(runs):>4}  선언형 종결 3문장 이상 연속(십계명식)')
    for r in runs[:n_examples]:
        print('          · ' + ' / '.join(x[:40] for x in r[:3]))
    print('\n종결어미 분포(문장 단위, 참고용)')
    for name, rx in ENDINGS:
        print(f'  {name:28} {sum(1 for s in sents if rx.search(s)):>4}')
    print(f'  {"전체 문장":28} {len(sents):>4}')


def main():
    # Korean Windows consoles default to cp949; set UTF-8 before argparse prints help.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8')
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('files', nargs='+')
    ap.add_argument('--hidden', action='store_true', help='HTML 숨은 텍스트와 스크립트 문자열도 검사')
    ap.add_argument('--skip-quoted', action='store_true', help='백틱·따옴표 안의 예시 문구는 검사에서 제외')
    ap.add_argument('--examples', type=int, default=3)
    ap.add_argument('--rules', default='', help='쉼표로 구분한 규칙 ID 접두어(예: L2,L3-2)')
    args = ap.parse_args()
    prefixes = [p.strip() for p in args.rules.split(',') if p.strip()]
    rules = [r for r in RULES if not prefixes or any(r[0].startswith(p) for p in prefixes)]
    for f in args.files:
        print(f'=== {f}')
        scan(load(f, args.hidden, args.skip_quoted), rules, args.examples)
        print()


if __name__ == '__main__':
    main()
