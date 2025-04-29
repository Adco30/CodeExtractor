from abc import ABC, abstractmethod

class CodeFilter(ABC):
    # Strategy interface for filtering code (comments, imports, etc.).
    @abstractmethod
    def apply(self, code: str) -> str:
        ...
