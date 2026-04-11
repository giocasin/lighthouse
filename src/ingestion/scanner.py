import logging
from dataclasses import dataclass
from pathlib import Path
from src.utils.types import FileType

logger = logging.getLogger(__name__)

@dataclass
class FileInfo:
    path: Path
    relative_path: Path
    file_type: FileType
    size_bytes: int
    
    @property
    def priority(self) -> float:
        return self.file_type.priority
    
IGNORE_DIRS = {'.git', 'node_modules', '__pycache__', '.venv', 'bin', 'obj', '.idea', '.vscode', '.prettierrc', '.eslint', 'logs'}
IGNORE_EXTENSIONS = {'.pyc', '.pdb', '.exe', '.dll', '.lock'}

def scan_repo(repo_path: Path) -> list[FileInfo]:
    res = []
    content = list(repo_path.rglob('*'))
    for item in content:
        if item.is_file():
            if any(parent.name in IGNORE_DIRS for parent in item.parents):
                logger.debug(f"Skipping {item} because it is in an ignored directory.")
                continue
            if item.suffix in IGNORE_EXTENSIONS:
                logger.debug(f"Skipping {item} because it has an ignored extension.")
                continue
            file_info = FileInfo(item.resolve(), item.relative_to(repo_path), FileType.from_extension(item.suffix), item.stat().st_size)
            logger.debug(f"Adding {file_info}")
            res.append(file_info)
    return sorted(res, key=lambda x: x.priority, reverse=True)
