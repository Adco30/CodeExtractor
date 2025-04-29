import logging
from pathlib import Path

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("CodeExplorer")

DEFAULT_CONFIG = {
    "workspace_path": str(Path.home()),
    "exclusions": ["node_modules", "venv", ".git", ".idea", ".DS_Store", "*.pyc", "*.class"],
    "column_sort_preferences": {
        "Name": {"asc": 0, "desc": 0},
        "Size": {"asc": 0, "desc": 0},
        "Type": {"asc": 0, "desc": 0},
        "Date Modified": {"asc": 0, "desc": 0}
    },
    "project_preferences": {},
    "frame_dimensions": {
        "project_explorer": {"width": 0, "height": 0},
        "indented_view": {"width": 0, "height": 0},
        "markdown": {"width": 0, "height": 0},
        "options": {"width": 0, "height": 0}
    },
    "column_widths": {"Name": 200, "Size": 100, "Type": 100, "Date Modified": 150},
    "options": {"remove_imports": False, "remove_comments": False, "sort_index": 0}
}

CONFIG_PATH = Path("code_explorer_config.json")

# File extensions
C_LIKE_EXTENSIONS = ['.java', '.c', '.cpp', '.h', '.hpp', '.swift', '.js', '.kt', '.kts', '.cs', '.go', '.php']