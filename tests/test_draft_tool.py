import json
import tempfile
import unittest
from pathlib import Path
from draft_tool import load_draft

class DraftValidationTests(unittest.TestCase):
    def write(self, data):
        directory = tempfile.TemporaryDirectory()
        path = Path(directory.name) / "draft.json"
        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        self.addCleanup(directory.cleanup)
        return path

    def test_valid(self):
        draft = load_draft(self.write({"title": "제목", "body": "본문"}))
        self.assertEqual(draft["title"], "제목")

    def test_empty_body(self):
        with self.assertRaises(ValueError):
            load_draft(self.write({"title": "제목", "body": "  "}))

    def test_long_title(self):
        with self.assertRaises(ValueError):
            load_draft(self.write({"title": "가" * 101, "body": "본문"}))

if __name__ == "__main__":
    unittest.main()
