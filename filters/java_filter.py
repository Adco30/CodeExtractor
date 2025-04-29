import re
from .code_filter import CodeFilter

class JavaFilter(CodeFilter):
    def apply(self, code: str) -> str:
        # remove // comments
        code = re.sub(r'//.*', '', code)
        # remove /* ... */ blocks
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
        # collapse blank lines
        code = re.sub(r'\n{3,}', '\n\n', code)
        return code
