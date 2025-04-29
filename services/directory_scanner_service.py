from pathlib import Path
import fnmatch

from parsers.parser_service import ParserService


class DirectoryScannerService:
    # Scans a directory tree, applies exclusions, and optionally expands details via ParserService.
    
    def __init__(self, parser_service=None):
        self.parser = parser_service or ParserService()

    def list_outline(
        self,
        root: Path,
        exclude_patterns: list[str],
        show_dotfiles: bool,
        detailed: bool
    ) -> str:
        excluded_dirs  = [p for p in exclude_patterns if "*" not in p and "." not in p]
        excluded_files = [p for p in exclude_patterns if "*" in p or "." in p]
        lines = []

        def should_exclude(p: Path) -> bool:
            if not show_dotfiles and p.name.startswith("."):
                return True
            if any(p.match(pat) for pat in excluded_files):
                return True
            if any(part in excluded_dirs for part in p.relative_to(root).parts):
                return True
            return False

        def traverse(directory: Path, level: int = 0):
            for p in sorted(directory.iterdir(), key=lambda x: x.name.lower()):
                if should_exclude(p):
                    continue
                indent = "    " * level
                if p.is_dir():
                    lines.append(f"{indent}{p.name}/")
                    traverse(p, level + 1)
                else:
                    lines.append(f"{indent}{p.name}")
                    if detailed and p.suffix.lower() in (".py", ".java", ".swift"):
                        for detail in self.parser.detailed_view(p):
                            lines.append(f"{indent}    {detail}")

        if root.exists():
            traverse(root, 0)
        return "\n".join(lines)
