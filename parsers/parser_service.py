from pathlib import Path

from parsers.java_parser import JavaParser
from parsers.python_parser import PythonParser
from parsers.swift_parser import SwiftParser


class ParserService:
    def __init__(self):
        self._by_ext = {
            ".py": PythonParser(),
            ".java": JavaParser(),
            ".swift": SwiftParser()
        }

    def detailed_view(self, file_path: Path) -> list[str]:
        parser = self._by_ext.get(file_path.suffix.lower())
        return parser.parse(file_path) if parser else []
