from pathlib import Path
import fnmatch

class FileScannerService:
    
    def list_files(
        self,
        root: Path,
        exclude_patterns: list[str],
        include_exts: set[str] | None = None
    ) -> list[Path]:
        # List files with specified filters
        excluded_dirs = [p for p in exclude_patterns if "*" not in p and "." not in p]
        excluded_files = [p for p in exclude_patterns if "*" in p or "." in p]
        result = []
        for p in root.rglob("*"):
            if any(p.match(pat) for pat in excluded_files):
                continue
            if any(part in excluded_dirs for part in p.parts):
                continue
            if p.is_file():
                if include_exts and p.suffix not in include_exts:
                    continue
                result.append(p)
        return result