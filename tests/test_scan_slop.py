"""CLI regression checks; candidate detection does not prove editing quality."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'scan_slop.py'

class ScanTests(unittest.TestCase):
    def run_scan(self, text, *args, suffix='.txt'):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / ('input' + suffix)
            p.write_text(text, encoding='utf-8')
            result = subprocess.run([sys.executable, str(SCRIPT), str(p), *args], capture_output=True, encoding='utf-8', check=True)
            counts = {}
            for line in result.stdout.splitlines():
                fields = line.split()
                if len(fields) > 1 and fields[0].startswith(('L1-', 'L2-', 'L3-')) and fields[1].isdigit():
                    counts[fields[0]] = int(fields[1])
            self.assertEqual(p.read_text(encoding='utf-8'), text)
            return counts

    def test_user_examples(self):
        examples = [
            ('6칸을 채운다.', 'L2-1'),
            ('손잡이를 돌린다.', 'L2-1'),
            ('사람은 하나지만 자리는 두 개입니다.', 'L2-3'),
            ('성공을 전제하지 않는다.', 'L3-1a'),
            ('연구 부재를 단정하지 않고 비교 조건과 반증 가능한 질문으로 적는다.', 'L3-2'),
            ('조기 종료·재샘플링의 오판 비용을 기록한다.', 'L3-3'),
            ('계획 수정과 단순 검증 선택의 효과를 절제한다.', 'L3-2'),
            ('모델을 실행하기 전에 무엇을 고정하고 어떤 비용을 셀지 정한다.', 'L3-4'),
        ]
        for text, rule in examples:
            with self.subTest(text=text):
                self.assertGreater(self.run_scan(text).get(rule, 0), 0)

    def test_cost_inflection(self):
        self.assertGreater(self.run_scan('비용을 센다. 비용을 셉니다. 비용을 셀지 결정합니다.')['L3-2'], 0)

    def test_preserved_text_and_quotes(self):
        text = '실패할 수 있습니다. 자료가 있습니다. 측정한 것만 포함합니다. VAE·VQ의 성능을 비교합니다.'
        self.assertEqual(sum(self.run_scan(text).values()), 0)
        self.assertEqual(sum(self.run_scan('`성공을 전제하지 않는다.` "조기 종료·재샘플링의 오판 비용"', '--skip-quoted').values()), 0)

    def test_generalized_noun_candidates(self):
        for text in ['학습 중단·재시작의 판정 비용', '학습·추론의 연산 비용', '병렬 확정의 의존성 오차', '이해 감독의 생성 이득']:
            with self.subTest(text=text):
                self.assertGreater(self.run_scan(text)['L3-3'], 0)
        self.assertEqual(self.run_scan('VAE·VQ·FSQ의 성능을 비교한다.')['L3-3'], 0)
        self.assertGreater(self.run_scan('기업의 안전한 데이터의 관리 효율')['L1-4'], 0)

    def test_past_tense_is_not_present_dictum(self):
        self.assertEqual(self.run_scan('자료를 수집했다. 결과는 유의하였다. 부록에 원자료가 있다.')['L3-1'], 0)

    def test_literal_phrases_require_context_review(self):
        # Lexical matches remain visible, so humans must apply the literal-use exception.
        self.assertGreater(self.run_scan('실제 양식의 6칸을 채운다. 장치의 손잡이를 돌린다.')['L2-1'], 0)
        self.assertGreater(self.run_scan('모델을 3차원 좌표계로 시각화한다.')['L2-2'], 0)

    def test_lecture_metaphor_candidates(self):
        for text in ['손이 없어서 못 한 겁니다.', 'AI에 눈을 달아 줍니다.', '같은 앱 안에 다른 자리가 있습니다.', '도구 화면에서 자리를 옮깁니다.', '1층에서 부탁하기', '3층으로 옮기고 폴더 지정하기']:
            with self.subTest(text=text):
                self.assertGreater(self.run_scan(text)['L2-8'], 0)

    def test_lecture_concrete_instructions_and_literal_terms(self):
        for text in ['강의실은 3층에 있습니다.', '네트워크의 3계층을 설명합니다.', '장치의 손잡이를 돌립니다.', '화면에서 작업 폴더를 선택합니다.', '복사본으로 작업합니다. 바꾸기 전 목록을 저장합니다. 되돌리기 확인 전에는 실습이 완료되지 않습니다.', '사진 파일 이름을 날짜별로 정리해줘']:
            with self.subTest(text=text):
                self.assertEqual(self.run_scan(text)['L2-8'], 0)

    def test_technical_rhetoric_candidates(self):
        for text in ['세 난점을 동시에 해결합니다.', '두 항목이 정확히 일대일로 대응합니다.', '이 성질을 구조적으로 보장합니다.', '별도의 장치 없이 성능이 개선됩니다.', '논문이 보장하는 범위입니다.']:
            with self.subTest(text=text):
                self.assertGreater(self.run_scan(text)['L1-12'], 0)
        for text in ['호라이즌 3형제', '파라미터 세 형제', '다봉 액션 분포는 어떻게 살아남는가', '정책 안에 예측 모델을 심는 행위입니다.']:
            with self.subTest(text=text):
                self.assertGreater(self.run_scan(text)['L2-9'], 0)

    def test_technical_terms_and_literal_robot_motion(self):
        # Existing lexical rules may still flag handles/coordinates; the new rules
        # must not conflate them with characters or blanket guarantees.
        text = '에너지 지형과 기울기장을 설명합니다. 관측 호라이즌은 2입니다. 로봇은 크랭크 손잡이를 3회 이상 돌립니다. 본문은 10회, 부록은 16회로 표기합니다.'
        counts = self.run_scan(text)
        self.assertEqual(counts['L1-12'], 0)
        self.assertEqual(counts['L2-9'], 0)

    def test_technical_collocation_candidates_and_git(self):
        self.assertGreater(self.run_scan('한 모드에만 커밋합니다. 외부 교란에 우아하게 반응했습니다.')['L3-2'], 0)
        self.assertEqual(self.run_scan('Git에 변경 사항을 커밋합니다.')['L3-2'], 0)

    def test_sensory_abstract_expression_candidates(self):
        for text in ['정서의 결을 살립니다.', '여운의 농도를 높입니다.', '맥락의 밀도를 더합니다.', '메시지의 농도를 짙게 합니다.']:
            with self.subTest(text=text):
                self.assertGreater(self.run_scan(text)['L2-10'], 0)

    def test_literal_density_and_word_boundary(self):
        for text in ['용액의 농도를 측정합니다.', '재료의 밀도를 기록합니다.', '나무의 결을 살립니다.', '정서의 결정 요인을 분석합니다.']:
            with self.subTest(text=text):
                self.assertEqual(self.run_scan(text)['L2-10'], 0)

    def test_metacopy_candidates(self):
        for text, count in [
            ('본 절에서는 제안 방법의 핵심 아이디어를 살펴보고자 한다.', 1),
            ('이 장에서는 변경 이력을 정리한다.', 1),
            ('지금부터 이 장표를 통해 수집 지연의 변화를 살펴보겠습니다.', 1),
            ('결론부터 말씀드리면, 측정값은 동일합니다.', 1),
            ('한마디로 요약하면, 두 조건의 편차가 큽니다.', 1),
            ('두 조건의 차이를 한눈에 보여 드립니다.', 1),
            ('설정 절차를 알기 쉽게 설명했습니다.', 1),
            ('여러분의 이해를 돕기 위해 핵심만 간결하게 정리했습니다.', 1),
            ('도움이 되셨기를 바랍니다.', 1),
            ('도움이 되길 바랍니다.', 1),
            ('본 글에서는 핵심 개념을 살펴봤습니다.', 1),
            ('이 글에서는 변경점을 정리했습니다.', 1),
            ('본 글에서 원리를 알아 보겠습니다.', 1),
            ('본 절에서는 v2.1 변경점을 살펴본다.', 1),
        ]:
            with self.subTest(text=text):
                self.assertEqual(self.run_scan(text)['L1-16'], count)

    def test_regulatory_and_disclaimer_register_candidates(self):
        for text, count in [
            ('사내 규정 제4조에 따른 발급 권한 준수 차원에서, 배포 키의 발급은 운영팀에 한하여 허용됩니다.', 2),
            ('초기화 명령 실행 전 관련 백업 절차를 사전에 이행하실 것을 권장드립니다.', 2),
            ('후속 조치가 수반됩니다.', 1),
            ('동일한 요청의 반복은 지양되어야 합니다.', 1),
            ('제출 기한에 유의하시기 바랍니다.', 1),
            ('운영팀에 한해 허용됩니다.', 1),
            ('사전 이행을 권장 드립니다.', 2),
            ('후속조치가 수반됩니다.', 1),
            ('사본 보존이 강력히 권장됩니다.', 1),
        ]:
            with self.subTest(text=text):
                self.assertEqual(self.run_scan(text)['L3-8'], count)

    def test_unsupported_disclaimer_and_hedge_candidates(self):
        for text, count in [
            ('본 결과는 다양한 요인에 따라 달라질 수 있으므로 해석에 신중을 기할 필요가 있다.', 2),
            ('모든 환경에 적용되는 만능 해법은 아니므로 다각적인 검토가 필요합니다.', 2),
            ('결과는 상황에 따라 다를 수 있습니다.', 1),
            ('수치의 해석에는 신중한 접근이 필요하다.', 1),
            ('이 방법이 보편적인 해결책은 아닙니다.', 1),
            ('전문가에게 문의하세요.', 1),
            ('이 자료는 참고용으로만 사용하세요.', 1),
            ('추가 논의의 여지가 있는 것으로 보입니다.', 1),
            ('보편적인 해결책은 아닐 수 있다.', 1),
            ('만능 해법이 아닌 이상 검토해야 한다.', 1),
            ('보안전문가에게 문의하세요.', 1),
            ('상황에 따라 달라질 수 있습니다.', 1),
            ('도입 전에 신중한 검토가 필요합니다.', 1),
        ]:
            with self.subTest(text=text):
                self.assertEqual(self.run_scan(text)['L3-9'], count)

    def test_overjustification_candidates(self):
        for text, count in [
            ('설정 옵션을 세 개만 둔 것은 기능 부족이 아니라 전략적 설계입니다.', 2),
            ('이 부분은 확장성을 고려해 의도적으로 분리한 설계입니다.', 1),
            ('일각에서는 속도가 느리다는 우려를 제기할 수 있으나, 이는 정확도의 가치를 간과한 단편적 시각입니다.', 2),
            ('파서 테스트를 꼼꼼히 검토했습니다.', 1),
            ('버그가 아니라 의도된 설계입니다.', 2),
            ('기능부족이 아니라 전략적 선택입니다.', 2),
            ('파서를 꼼꼼하게 검토한 결과입니다.', 1),
            ('안정성을 우선한 합리적인 트레이드오프입니다.', 1),
        ]:
            with self.subTest(text=text):
                self.assertEqual(self.run_scan(text)['L3-10'], count)

    def test_new_rules_preserve_concrete_research_and_technical_prose(self):
        cases = {
            'L1-16': [
                '2장에서는 데이터셋을, 3장에서는 실험을 설명한다.',
                '이 문서는 v2 마이그레이션 절차만 다룬다.',
                '제외 기준은 부록 A에 있다.',
                '10분 실습 후 질문을 받겠습니다.',
                '이 보고서는 조망권 변화의 영향을 조사했다.',
                '이 문서는 REST API v2 에러 코드를 정리한 명세서입니다.',
                '본 절에서는 앞 절에서 소개한 손실 함수를 적용한다.',
                '이해를 돕기 위해 입출력 예제를 추가했습니다.',
                '실험 조건은 3장에 설명한다.',
            ],
            'L3-8': [
                '외부 반출은 기관생명윤리위원회 승인 후에만 허용된다.',
                '사내 규정 제4조에 따라 운영팀만 배포 키를 발급할 수 있습니다.',
                '개인식별정보는 로그에 저장하지 않아야 한다.',
                '이 계정에는 배포 권한이 없습니다.',
                '2차 측정에 한하여 허용 오차를 0.2 mm로 설정했다.',
                '안전 조치 요구사항을 표에 기록했다.',
                '고온 조건에 한하여 허용 범위를 5%로 완화했다.',
                '모든 표본은 IRB 관련 절차에 따라 익명화되었다.',
            ],
            'L3-9': [
                '표본이 12명이고 한 기관에서만 모았으므로 다른 기관에 그대로 적용하기 어려울 수 있다.',
                '실패할 수 있습니다.',
                '이 메시지 큐는 최소 1회 전송만 보장한다.',
                '저조도 조건은 아직 검증하지 않았다.',
                '인증 모듈 변경이므로 신중한 검토 부탁드립니다.',
                '캐시 적중률은 워크로드 상황에 따라 달라질 수 있다.',
                '임상 판단은 반드시 의료 전문가와 상의해야 한다.',
                '운영상황에 따라 다를 수 있다.',
            ],
            'L3-10': [
                '배치를 키우니 오히려 응답 시간이 길어졌다.',
                '노이즈를 의도적으로 주입했다.',
                '메모리 부족으로 불가피하게 학습을 중단했다.',
                '4GB 메모리 한도 때문에 4비트 양자화를 선택했다.',
                '기존 클라이언트가 이 필드를 읽으므로 이번 릴리스에서는 유지했습니다.',
                '실험용 신호를 의도적으로 주입한 뒤 설계 변경 이력을 기록했다.',
                '의도적으로 높인 설계값을 입력했다.',
                '실험용 신호를 의도적으로 주입한 뒤에 설계 변경 이력을 기록했다.',
                '이 오차는 모델의 결함이 아니라 라벨링 오류에서 비롯되었다.',
                '합리적 선택 이론에 따라 기대 효용을 정식화했다.',
                '비합리적 선택이 관찰되었다.',
                '입력값을 철저히 검증합니다.',
                '의도된 대로 동작합니다.',
            ],
        }
        for rule, texts in cases.items():
            for text in texts:
                with self.subTest(rule=rule, text=text):
                    self.assertEqual(self.run_scan(text)[rule], 0)

    def test_new_bounded_patterns_stay_in_the_same_sentence(self):
        for rule, text in [
            ('L1-16', '본 문서는 운영 절차를 다룬다. 배포 로그를 살펴본다.'),
            ('L1-16', '지금부터 수집을 시작합니다. 결과는 나중에 살펴보겠습니다.'),
            ('L3-9', '만능 도구를 사용했다. 아니, 사용 기록을 다시 확인했다.'),
            ('L3-10', '의도적으로 노이즈를 주입했다. 설계는 그대로 두었다.'),
            ('L3-10', '일부에서는 배포를 연기했다. 작업은 계속할 수 있지만 로그를 먼저 확인한다.'),
        ]:
            with self.subTest(rule=rule, text=text):
                self.assertEqual(self.run_scan(text)[rule], 0)

    def test_new_rules_skip_quoted_examples_and_preserve_unquoted_prose(self):
        examples = {
            'L1-16': '결론부터 말씀드리면, 결과는 같습니다.',
            'L3-8': '제출 기한에 유의하시기 바랍니다.',
            'L3-9': '이 자료는 참고용으로만 사용하세요.',
            'L3-10': '파서 테스트를 꼼꼼히 검토했습니다.',
        }
        text = '\n'.join(f'“{phrase}” `{phrase}`\n```text\n{phrase}\n```\n{phrase}' for phrase in examples.values())
        counts = self.run_scan(text)
        unquoted = self.run_scan(text, '--skip-quoted')
        for rule in examples:
            with self.subTest(rule=rule):
                self.assertEqual(counts[rule], 4)
                self.assertEqual(unquoted[rule], 1)

    def test_single_sentence_is_not_repetition(self):
        self.assertEqual(self.run_scan('성공을 전제하지 않는다.')['L3-1'], 0)
        self.assertGreater(self.run_scan('자료를 기록한다. 수치를 확인한다. 결과를 검증한다.')['L3-1'], 0)

    def test_rule_filter_applies_to_declarative_runs(self):
        text = '자료를 기록한다. 수치를 확인한다. 결과를 검증한다. 손잡이를 돌린다.'
        counts = self.run_scan(text, '--rules', 'L2')
        self.assertTrue(counts)
        self.assertTrue(all(key.startswith('L2') for key in counts))
        counts = self.run_scan(text, '--rules', 'L3-1')
        self.assertEqual(set(counts), {'L3-1', 'L3-1a'})
        self.assertGreater(counts['L3-1'], 0)

    def test_rule_ids_do_not_select_other_digit_suffixes(self):
        counts = self.run_scan('동시에 해결합니다. 정서의 결을 살립니다.', '--rules', 'L1-1,L2-1')
        self.assertEqual(set(counts), {'L1-1', 'L2-1'})

    def test_new_rule_selectors_distinguish_layers_and_digit_suffixes(self):
        text = '본 절에서는 결과를 살펴본다. 파서 테스트를 꼼꼼히 검토했습니다.'
        counts = self.run_scan(text, '--rules', 'L1')
        self.assertEqual(counts['L1-16'], 1)
        self.assertTrue(all(key.startswith('L1-') for key in counts))
        self.assertEqual(set(self.run_scan(text, '--rules', 'L1-1')), {'L1-1'})
        self.assertEqual(set(self.run_scan(text, '--rules', 'L3-1')), {'L3-1', 'L3-1a'})
        self.assertEqual(self.run_scan(text, '--rules', 'L3-10'), {'L3-10': 1})

    def test_short_sentences_and_interruptions_in_declarative_runs(self):
        self.assertEqual(self.run_scan('기록한다. 확인한다. 검증한다.')['L3-1'], 1)
        for text in [
            '자료를 기록한다. 결과입니다. 수치를 확인한다. 맞습니다. 결과를 검증한다.',
            '자료를 기록한다. OK. 수치를 확인한다. 결과를 검증한다.',
        ]:
            with self.subTest(text=text):
                self.assertEqual(self.run_scan(text)['L3-1'], 0)

    def test_html_hidden_text_and_body_are_separate(self):
        text = '''<HEAD><TITLE>정서의 결</TITLE><STYLE>맥락의 밀도</STYLE></HEAD>
        <p aria-label='여운의 농도'>구체적인 본문입니다.</p>
        <meta content='혁신적' name='description'>
        <SCRIPT>const message="효과를 절제한다"; const caption=`맥락의 밀도`;
        // "정서의 결" is a comment, not a message.
        </SCRIPT><script type='application/json'>["정서의 결"]</script>'''
        body = self.run_scan(text, suffix='.html')
        self.assertEqual(sum(body.values()), 0)
        hidden = self.run_scan(text, '--hidden', suffix='.html')
        self.assertEqual(hidden['L2-10'], 3)
        self.assertEqual(hidden['L3-2'], 1)
        self.assertEqual(hidden['L1-8'], 1)

    def test_html_inline_markup_and_entities(self):
        text = '<p>정서의 <em>결</em>을 살립니다.</p><p>여운의&#32;농도를 높입니다.</p>'
        self.assertEqual(self.run_scan(text, suffix='.html')['L2-10'], 2)

    def test_skip_quoted_excludes_fences_and_preserves_unquoted_prose(self):
        text = '''```text
정서의 결을 살립니다.
```
~~~text
여운의 농도를 높입니다.
~~~
'정서의 결' “여운의 농도” `맥락의 밀도`
맥락의 밀도를 더합니다.
'''
        self.assertGreater(self.run_scan(text)['L2-10'], 1)
        self.assertEqual(self.run_scan(text, '--skip-quoted')['L2-10'], 1)

    def test_inline_multiple_backticks_do_not_start_a_fence(self):
        text = '```정서의 결```\n``여운의 농도``\n맥락의 밀도를 더합니다.'
        self.assertEqual(self.run_scan(text, '--skip-quoted')['L2-10'], 1)

    def test_empty_rule_selectors_are_rejected(self):
        for selector in ['', ' ', ',', 'L2,,L3', 'L2,']:
            with self.subTest(selector=selector):
                with self.assertRaises(subprocess.CalledProcessError) as context:
                    self.run_scan('정서의 결을 살립니다.', '--rules', selector)
                self.assertEqual(context.exception.returncode, 2)

    def test_invalid_options_are_reported(self):
        for args in [('--rules', 'L9'), ('--rules', 'L1-15'), ('--examples', '-1')]:
            with self.subTest(args=args):
                with self.assertRaises(subprocess.CalledProcessError) as context:
                    self.run_scan('정서의 결을 살립니다.', *args)
                self.assertEqual(context.exception.returncode, 2)

    def test_multiple_files_preserve_bytes_and_order(self):
        with tempfile.TemporaryDirectory() as directory:
            paths = [Path(directory) / 'first.txt', Path(directory) / 'second.html']
            texts = ['정서의 결을 살립니다.', '<svg><text>여운의 농도</text><desc>맥락의 밀도</desc></svg>']
            for path, text in zip(paths, texts):
                path.write_text(text, encoding='utf-8')
            before = [(path.read_bytes(), path.stat().st_mtime_ns) for path in paths]
            result = subprocess.run([sys.executable, str(SCRIPT), *map(str, paths), '--hidden',
                                     '--rules', 'L2-10', '--examples', '0'],
                                    capture_output=True, encoding='utf-8', check=True)
            headers = [line for line in result.stdout.splitlines() if line.startswith('=== ')]
            self.assertEqual(headers, ['=== ' + str(path) for path in paths])
            self.assertEqual(before, [(path.read_bytes(), path.stat().st_mtime_ns) for path in paths])
            self.assertEqual(result.returncode, 0)

    def test_examples_limit_controls_output(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'input.txt'
            path.write_text('정서의 결을 살립니다.\n' * 5, encoding='utf-8')
            for count in [0, 2]:
                result = subprocess.run([sys.executable, str(SCRIPT), str(path), '--rules', 'L2-10',
                                         '--examples', str(count)],
                                        capture_output=True, encoding='utf-8', check=True)
                example_lines = [line for line in result.stdout.splitlines()
                                 if line.lstrip().startswith('L') and ': …' in line]
                self.assertEqual(len(example_lines), count)

    def test_symbols_used_as_verbs_between_korean_phrases(self):
        for text in ['범위: 복원 ≠ 생성(MAE)', '② 폭 ≥ 토큰 차원', '요약: 공유 표현 → 생성 이득', '(MAE) → 차원']:
            with self.subTest(text=text):
                self.assertEqual(self.run_scan(text, '--rules', 'L3-12')['L3-12'], 1)

    def test_symbols_in_values_math_and_code_are_not_candidates(self):
        text = ('8층→16층에서 Acc.는 오른다. 0.31 대 0.41. 수식 $d \\ge 토큰$과 \\(폭 ≥ 차원\\)\n'
                '`입력 → 출력` 단계, ``토큰 ≠ 패치``, 값 3 → 5')
        self.assertEqual(self.run_scan(text, '--rules', 'L3-12')['L3-12'], 0)

    def test_exclude_removes_rules_after_selection(self):
        text = '자료를 모으고, 정서의 결을 살립니다.'
        counts = self.run_scan(text, '--exclude', 'L1-7')
        self.assertNotIn('L1-7', counts)
        self.assertEqual(counts['L2-10'], 1)
        self.assertEqual(set(self.run_scan(text, '--rules', 'L1', '--exclude', 'L1-7')), {r for r in self.run_scan(text, '--rules', 'L1') if r != 'L1-7'})
        self.assertNotIn('L3-1', self.run_scan('기록한다. 측정한다. 비교한다.', '--exclude', 'L3'))
        for args in [('--exclude', 'L9'), ('--exclude', ',')]:
            with self.subTest(args=args):
                with self.assertRaises(subprocess.CalledProcessError) as context:
                    self.run_scan(text, *args)
                self.assertEqual(context.exception.returncode, 2)

    def run_with_baseline(self, original, edited, *args):
        with tempfile.TemporaryDirectory() as d:
            base, target = Path(d) / 'original.txt', Path(d) / 'edited.txt'
            base.write_text(original, encoding='utf-8')
            target.write_text(edited, encoding='utf-8')
            result = subprocess.run([sys.executable, str(SCRIPT), str(target), '--baseline', str(base), *args],
                                    capture_output=True, encoding='utf-8', check=True)
            self.assertEqual(base.read_text(encoding='utf-8'), original)
            return result.stdout.split('기준 원문보다 늘어난 후보', 1)[1]

    def test_baseline_reports_candidates_added_by_the_edit(self):
        added = self.run_with_baseline('지운 설명과 남은 설명. 겨눈 비교.',
                                       '통제 비교에서 배제된 설명과 남은 설명. 해당 비교. 따라서 해당 행을 본다.')
        self.assertIn('해당 0→2', added)
        self.assertIn('따라서 0→1', added)
        self.assertNotIn('L2-1', added)

    def test_baseline_ignores_candidates_already_in_the_original(self):
        added = self.run_with_baseline('해당 값을 쓴다. 다양한 조건.', '해당 값을 쓴다. 여러 조건.')
        self.assertIn('없음', added)

if __name__ == '__main__':
    unittest.main()
