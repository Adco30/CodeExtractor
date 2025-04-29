import os
import fnmatch
from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QFileSystemModel

class FileModel:
    """Model for file system operations."""
    
    def __init__(self):
        self.file_model = QFileSystemModel()
        self.file_model.setFilter(QDir.AllEntries | QDir.NoDotAndDotDot)
        self.current_path = ""

    def get_file_extensions(self, path, excluded_items=None):
        # Get file extensions in directory
        if not os.path.exists(path):
            return set()
        extensions = set()
        excluded_dirs = [item for item in (excluded_items or []) if '*' not in item and '.' not in item]
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d not in excluded_dirs]
            for file in files:
                _, ext = os.path.splitext(file)
                if ext:
                    extensions.add(ext)
        return extensions

    def get_files_in_directory(self, path, excluded_items=None, excluded_extensions=None, show_dotfiles=False):
        # Get files in directory with filters
        if not os.path.exists(path):
            return []

        files_found = []
        excluded_dirs = [item for item in (excluded_items or []) if '*' not in item and '.' not in item]
        excluded_files = [item for item in (excluded_items or []) if '*' in item or '.' in item]

        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d not in excluded_dirs]
            for file in files:
                if not show_dotfiles and file.startswith('.'):
                    continue
                if any(fnmatch.fnmatch(file, pattern) for pattern in excluded_files):
                    continue
                file_path = os.path.join(root, file)
                _, ext = os.path.splitext(file)
                if excluded_extensions and ext in excluded_extensions:
                    continue
                rel_path = os.path.relpath(file_path, path)
                if any(part in excluded_dirs for part in rel_path.split(os.sep)):
                    continue
                files_found.append(file_path)

        return files_found

    def set_root(self, path):
        # Set root path for file model
        if os.path.exists(path):
            self.current_path = path
            self.file_model.setRootPath(path)
            return self.file_model.index(path)
        return None

    def get_file_path(self, index):
        # Get file path from model index
        return self.file_model.filePath(index)