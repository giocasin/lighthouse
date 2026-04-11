import logging
from dataclasses import dataclass

from pathlib import Path
from langchain_text_splitters import MarkdownTextSplitter, RecursiveCharacterTextSplitter
from src.ingestion.scanner import FileInfo
from src.utils.types import FileType

@dataclass
class Chunk:
    content: str
    source_file: FileInfo
    chunk_index: int
    metadata: dict


SplitterConfig = tuple[type, int, int] # (file type, chunk size, overlap)

SPLITTER_CONFIG: dict[FileType, SplitterConfig] = {
    FileType.SOURCE_CODE: (RecursiveCharacterTextSplitter, 1000, 200),
    FileType.DOCS: (MarkdownTextSplitter, 2000, 400),
    FileType.CONFIGURATION: (RecursiveCharacterTextSplitter, 1500, 300),
    FileType.OTHER: (MarkdownTextSplitter, 500, 100)
}

def chunk_file(file_info: FileInfo) -> list[Chunk]:
    splitter = _get_splitter(file_info.file_type)

    try:
        chunks = splitter.split_text(read_file(file_info.path))
        return [
            Chunk(
                content=chunk,
                source_file=file_info,
                chunk_index=i,
                metadata={
                    "file_path": str(file_info.path),
                    "file_type": file_info.file_type.value,
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                    "size_bytes": file_info.size_bytes
                }
            )
            for i, chunk in enumerate(chunks)
        ]
    except Exception as e:
        logging.error(f"Error chunking file {file_info.path}: {e}")
        return []

def read_file(path: Path) -> str:
    try:
        with path.open('r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logging.error(f"Error reading file {path}: {e}")
        return ""
    

def _get_splitter(file_type: FileType):
    splitter_class, chunk_size, overlap = SPLITTER_CONFIG[file_type]
    return splitter_class(chunk_size=chunk_size, chunk_overlap=overlap)