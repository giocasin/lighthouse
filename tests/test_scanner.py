import unittest
import tempfile
from pathlib import Path
from src.ingestion.scanner import scan_repo
from src.utils.types import FileType


class ScannerTestCase(unittest.TestCase):
    def write_file(self, path: Path, content: str = "x") -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def test_scan_repo_skips_ignored_dirs_and_extensions(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            self.write_file(tmp_path / "src" / "main.py")
            self.write_file(tmp_path / "node_modules" / "lib.js")   # ignored dir
            self.write_file(tmp_path / "logs" / "app.log")          # ignored dir
            self.write_file(tmp_path / "build" / "a.pyc")           # ignored extension

            result = scan_repo(tmp_path)
            rel_paths = {f.relative_path.as_posix() for f in result}

            self.assertIn("src/main.py", rel_paths)
            self.assertNotIn("node_modules/lib.js", rel_paths)
            self.assertNotIn("logs/app.log", rel_paths)
            self.assertNotIn("build/a.pyc", rel_paths)

    def test_scan_repo_sets_fields_correctly(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            self.write_file(tmp_path / "docs" / "guide.md", "hello")
            result = scan_repo(tmp_path)

            self.assertEqual(len(result), 1)
            f = result[0]
            self.assertEqual(f.relative_path, Path("docs/guide.md"))
            self.assertEqual(f.file_type, FileType.DOCS)
            self.assertEqual(f.size_bytes, 5)
            self.assertTrue(f.path.is_absolute())

    def test_scan_repo_returns_priority_sorted(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            self.write_file(tmp_path / "a.py")       # SOURCE_CODE -> 0.5
            self.write_file(tmp_path / "b.yaml")     # CONFIGURATION -> 0.8
            self.write_file(tmp_path / "c.md")       # DOCS -> 1.0
            self.write_file(tmp_path / "d.xyz")      # OTHER -> 0.1

            result = scan_repo(tmp_path)
            priorities = [f.priority for f in result]

            self.assertEqual(priorities, sorted(priorities, reverse=True))
            self.assertEqual(result[0].file_type, FileType.DOCS)

    def test_scan_repo_empty_repo(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            self.assertEqual(scan_repo(tmp_path), [])

    def test_scan_repo_nested_ignored_dirs(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            self.write_file(tmp_path / "valid" / "file.py")
            self.write_file(tmp_path / "valid" / "__pycache__" / "cached.pyc")
            self.write_file(tmp_path / "valid" / ".venv" / "lib.py")

            result = scan_repo(tmp_path)
            rel_paths = {f.relative_path.as_posix() for f in result}

            self.assertIn("valid/file.py", rel_paths)
            self.assertNotIn("valid/__pycache__/cached.pyc", rel_paths)
            self.assertNotIn("valid/.venv/lib.py", rel_paths)

    def test_scan_repo_classifies_languages(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            self.write_file(tmp_path / "script.py")
            self.write_file(tmp_path / "app.ts")
            self.write_file(tmp_path / "config.yaml")
            self.write_file(tmp_path / "README.md")

            result = scan_repo(tmp_path)
            type_map = {f.relative_path.name: f.file_type for f in result}

            self.assertEqual(type_map["script.py"], FileType.SOURCE_CODE)
            self.assertEqual(type_map["app.ts"], FileType.SOURCE_CODE)
            self.assertEqual(type_map["config.yaml"], FileType.CONFIGURATION)
            self.assertEqual(type_map["README.md"], FileType.DOCS)

