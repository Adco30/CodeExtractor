import re
from pathlib import Path

from constants import logger


class SwiftParser:
    def parse(self, file_path: Path) -> list[str]:
        try:
            lines = file_path.read_text(encoding="utf-8").splitlines()
            entity_pattern = re.compile(r'^\s*(class|struct|enum)\s+(\w+)')
            member_pattern = re.compile(r'^\s*func\s+(\w+)')
            details = []
            for line in lines:
                m = entity_pattern.match(line)
                if m:
                    details.append(f"{m.group(1)} {m.group(2)}")
                m2 = member_pattern.match(line)
                if m2:
                    details.append(f"func {m2.group(1)}()")
            return details
        except IOError as e:
            logger.error(f"SwiftParser failed on {file_path}: {e}")
            return []
