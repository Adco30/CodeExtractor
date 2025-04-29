import re
from .code_filter import CodeFilter

class CLikeFilter(CodeFilter):
    def apply(self, code: str) -> str:
        # reuse JavaFilter logic for all C-like languages
        from .java_filter import JavaFilter
        return JavaFilter().apply(code)
