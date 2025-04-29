import re
from .code_filter import CodeFilter

class PythonFilter(CodeFilter):
    def apply(self, code: str) -> str:
        # remove triple-quoted blocks
        code = re.sub(r'("""|\'\'\')(?:.|\n)*?\1', '', code)
        # remove single-line comments
        code = re.sub(r'#.*', '', code)
        # collapse multiple blank lines
        code = re.sub(r'\n{3,}', '\n\n', code)
        return code
