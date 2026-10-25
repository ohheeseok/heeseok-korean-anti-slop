"""CLI regression checks; candidate detection does not prove editing quality."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'scan_slop.py'

class ScanTests(unittest.TestCase):
    def run_scan(self, text, *args):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'input.txt'
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

    def test_single_sentence_is_not_repetition(self):
        self.assertEqual(self.run_scan('성공을 전제하지 않는다.')['L3-1'], 0)
        self.assertGreater(self.run_scan('자료를 기록한다. 수치를 확인한다. 결과를 검증한다.')['L3-1'], 0)

if __name__ == '__main__':
    unittest.main()
