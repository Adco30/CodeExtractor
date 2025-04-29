import os
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QScrollArea, QWidget, QGridLayout, QCheckBox

def should_be_checked(extension, project_preferences):
    if not project_preferences:
        return False
    return extension in project_preferences.get("extensions", {})

class FileTypeCheckboxesFrame(QScrollArea):
    """Widget for file type selection checkboxes."""
    
    selection_changed = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.checkboxes = {}
        self.init_ui()

    def init_ui(self):
        self.setWidgetResizable(True)
        container = QWidget()
        self.grid_layout = QGridLayout()
        container.setLayout(self.grid_layout)
        self.setWidget(container)

    def update_for_project(self, file_extensions, project_preferences=None):
        # Update checkboxes for current project
        for checkbox in self.checkboxes.values():
            self.grid_layout.removeWidget(checkbox)
            checkbox.deleteLater()
        self.checkboxes.clear()

        sorted_extensions = sorted(file_extensions)
        row, col = 0, 0
        for ext in sorted_extensions:
            checkbox = QCheckBox(ext)
            checkbox.setChecked(should_be_checked(ext, project_preferences))
            checkbox.stateChanged.connect(lambda state, e=ext: self.on_checkbox_changed(e, state))
            self.grid_layout.addWidget(checkbox, row, col)
            self.checkboxes[ext] = checkbox
            col += 1
            if col == 3:
                col = 0
                row += 1

    def on_checkbox_changed(self, extension, state):
        # Handle checkbox state change
        self.selection_changed.emit(self.get_selected_extensions())

    def get_selected_extensions(self):
        # Get list of selected extensions
        return [ext for ext, checkbox in self.checkboxes.items() if checkbox.isChecked()]