import json
import tempfile
import unittest
from pathlib import Path

from naver_draft import read_draft


class DraftTests(unittest.TestCase):
    def test_valid(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "draft.json"
            path.write_text(json.dumps({"title": " 제목 ", "body": "가" * 40}), encoding="utf-8")
            self.assertEqual(read_draft(path)[0], "제목")

    def test_empty_title(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "draft.json"
            path.write_text(json.dumps({"title": "", "body": "가" * 40}), encoding="utf-8")
            with self.assertRaises(ValueError):
                read_draft(path)


if __name__ == "__main__":
    unittest.main()
