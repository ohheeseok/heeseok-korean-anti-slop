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

    def test_single_sentence_is_not_repetition(self):
        self.assertEqual(self.run_scan('성공을 전제하지 않는다.')['L3-1'], 0)
        self.assertGreater(self.run_scan('자료를 기록한다. 수치를 확인한다. 결과를 검증한다.')['L3-1'], 0)

if __name__ == '__main__':
    unittest.main()
