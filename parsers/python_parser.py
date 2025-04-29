import ast
from pathlib import Path

from constants import logger


class PythonParser:
    def parse(self, file_path: Path) -> list[str]:
        try:
            source = file_path.read_text(encoding="utf-8")
            tree = ast.parse(source)
            details = []
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    details.append(f"class {node.name}:")
                if isinstance(node, ast.FunctionDef):
                    args = ", ".join(arg.arg for arg in node.args.args)
                    details.append(f"def {node.name}({args})")
            return details
        except (SyntaxError, IOError) as e:
            logger.error(f"PythonParser failed on {file_path}: {e}")
            return []
