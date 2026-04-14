import unittest
import tempfile
from pathlib import Path
from src.ingestion.chunker import chunk_file
from src.ingestion.scanner import FileInfo
from src.utils.types import FileType

class ChunkerTestCase(unittest.TestCase):
    def make_file_info(self, path: Path, file_type: FileType = FileType.SOURCE_CODE) -> FileInfo:
        return FileInfo(
            path=path,
            relative_path=path.absolute(),
            file_type=file_type,
            size_bytes=path.stat().st_size
        )

    def test_empty_file_returns_no_chunks(self):
        with tempfile.NamedTemporaryFile(suffix=".py") as temp_file:
            file_info = self.make_file_info(Path(temp_file.name))
            chunks = chunk_file(file_info)
            self.assertEqual(chunks, [])

    def test_binary_file_returns_no_chunks(self):
        with tempfile.NamedTemporaryFile(suffix=".exe") as temp_file:
            file_info = self.make_file_info(Path(temp_file.name), file_type=FileType.OTHER)
            chunks = chunk_file(file_info)
            self.assertEqual(chunks, [])

    def test_small_content_returns_single_chunk(self):
        with tempfile.NamedTemporaryFile(suffix=".py", mode='w+', encoding='utf-8') as temp_file:
            temp_file.write("print('Hello, world!')")
            temp_file.flush()
            file_info = self.make_file_info(Path(temp_file.name))
            chunks = chunk_file(file_info)
            self.assertEqual(len(chunks), 1)
            self.assertEqual(chunks[0].content, "print('Hello, world!')")
            self.assertEqual(chunks[0].source_file, file_info)
            self.assertEqual(chunks[0].chunk_index, 0)
            self.assertIsInstance(chunks[0].metadata, dict)

    def test_chunk_index_is_sequential(self):
        content = "Line 1\nLine 2\nLine 3\nLine 4\nLine 5" * 500
        with tempfile.NamedTemporaryFile(suffix=".py", mode='w+', encoding='utf-8') as temp_file:
            temp_file.write(content)
            temp_file.flush()
            file_info = self.make_file_info(Path(temp_file.name))
            chunks = chunk_file(file_info)
            self.assertTrue(all(chunk.chunk_index == i for i, chunk in enumerate(chunks)))

    def test_chunk_reference_source_file(self):
        with tempfile.NamedTemporaryFile(suffix=".py", mode='w+', encoding='utf-8') as temp_file:
            temp_file.write("print('Hello, world!')")
            temp_file.flush()
            file_info = self.make_file_info(Path(temp_file.name))
            chunks = chunk_file(file_info)
            self.assertTrue(all(chunk.source_file == file_info for chunk in chunks))

    def test_chunk_have_non_empty_content(self):
        with tempfile.NamedTemporaryFile(suffix=".py", mode='w+', encoding='utf-8') as temp_file:
            temp_file.write("print('Hello, world!')")
            temp_file.flush()
            file_info = self.make_file_info(Path(temp_file.name))
            chunks = chunk_file(file_info)
            self.assertTrue(all(chunk.content for chunk in chunks))

    def test_markdown_file_uses_appropriate_chunking(self):
        with tempfile.NamedTemporaryFile(suffix=".md", mode='w+', encoding='utf-8') as temp_file:
            temp_file.write("# Heading\n\nThis is a markdown file.")
            temp_file.flush()
            file_info = self.make_file_info(Path(temp_file.name), file_type=FileType.DOCS)
            chunks = chunk_file(file_info)
            self.assertEqual(len(chunks), 1)
            self.assertEqual(chunks[0].chunk_index, 0)

    def test_chunk_metadata_has_required_keys(self):
        with tempfile.NamedTemporaryFile(suffix=".md", mode='w+', encoding='utf-8') as temp_file:
            temp_file.write("# Heading\n\nThis is a markdown file.")
            temp_file.flush()
            file_info = self.make_file_info(Path(temp_file.name), file_type=FileType.DOCS)
            chunks = chunk_file(file_info)
            self.assertTrue(all(key in chunks[0].metadata for key in ["file_path", "file_type", "chunk_index", "total_chunks", "size_bytes"]))