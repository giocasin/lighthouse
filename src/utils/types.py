from enum import Enum

class FileType(Enum):
    SOURCE_CODE = 'source_code'
    DOCS = 'docs'
    CONFIGURATION = 'configuration'
    OTHER = 'other'

    @property
    def priority(self) -> float:
        priorities = {
            FileType.SOURCE_CODE: 0.5,
            FileType.DOCS: 1.0,
            FileType.CONFIGURATION: 0.8,
            FileType.OTHER: 0.1
        }
        return priorities.get(self, 0.1)
    
    @classmethod
    def from_extension(cls, extension: str) -> 'FileType':
        name = extension.lower().strip()

        exact_match = {
        'dockerfile': cls.CONFIGURATION,
        'makefile': cls.CONFIGURATION,
        'procfile': cls.CONFIGURATION,
        'jenkinsfile': cls.CONFIGURATION,
        '.env': cls.CONFIGURATION,
        'readme': cls.DOCS,
        'license': cls.OTHER,
        }
    
        if name in exact_match:
            return exact_match[name]
        
        ext = name.split('.')[-1] if '.' in name else ''

        extension_match = {
            'md': cls.DOCS,
            'txt': cls.CONFIGURATION,
            'pdf': cls.DOCS,
            'yaml': cls.CONFIGURATION,
            'yml': cls.CONFIGURATION,
            'json': cls.CONFIGURATION,
            'xml': cls.CONFIGURATION,
            'py': cls.SOURCE_CODE,
            'js': cls.SOURCE_CODE,
            'java': cls.SOURCE_CODE,
            'cpp': cls.SOURCE_CODE,
            'c': cls.SOURCE_CODE,
            'go': cls.SOURCE_CODE,
            'rb': cls.SOURCE_CODE,
            'php': cls.SOURCE_CODE,
            'tsx': cls.SOURCE_CODE,
            'ts': cls.SOURCE_CODE,
            'html': cls.SOURCE_CODE,
            'css': cls.SOURCE_CODE,
            'sh': cls.SOURCE_CODE,
            'bat': cls.SOURCE_CODE,
            'csproj': cls.CONFIGURATION,
            'sln': cls.CONFIGURATION,
            'cs': cls.SOURCE_CODE,
            'cjs': cls.CONFIGURATION,
            'ini': cls.CONFIGURATION,
            'cfg': cls.CONFIGURATION,
            'conf': cls.CONFIGURATION,
        }
        return extension_match.get(ext, cls.OTHER)