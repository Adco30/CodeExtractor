import json
from pathlib import Path

class ConfigManager:
    @staticmethod
    def load():
        config_file = Path("project_explorer_config.json")
        default_config = {
            "workspace_path": "/path/to/folder",
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
            "column_widths": {
                "Name": 200,
                "Size": 100,
                "Type": 100,
                "Date Modified": 150
            },
            "options": {
                "remove_imports": False,
                "remove_comments": False,
                "sort_index": 0
            }
        }
        if config_file.exists():
            try:
                with open(config_file) as f:
                    saved_config = json.load(f)
                for key, value in default_config.items():
                    if key not in saved_config:
                        saved_config[key] = value
                return saved_config
            except Exception as e:
                print("Error loading config:", e)
                return default_config
        else:
            with open(config_file, "w") as f:
                json.dump(default_config, f, indent=4)
            return default_config

    @staticmethod
    def save(config):
        with open("project_explorer_config.json", "w") as f:
            json.dump(config, f, indent=4)