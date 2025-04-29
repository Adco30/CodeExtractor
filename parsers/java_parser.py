import javalang
from pathlib import Path

from constants import logger


class JavaParser:
    def parse(self, file_path: Path) -> list[str]:
        try:
            tree = javalang.parse.parse(file_path.read_text(encoding="utf-8"))
            details = []
            for _, node in tree.filter(javalang.tree.ClassDeclaration):
                details.append(f"class {node.name}")
                for method in node.methods:
                    params = ", ".join(f"{p.type.name} {p.name}" for p in method.parameters)
                    ret = method.return_type.name if method.return_type else "void"
                    details.append(f"    {ret} {method.name}({params})")
            return details
        except (javalang.parser.JavaSyntaxError, IOError) as e:
            logger.error(f"JavaParser failed on {file_path}: {e}")
            return []
