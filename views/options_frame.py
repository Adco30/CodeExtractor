from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QCheckBox, QComboBox, QLineEdit, QFrame

class OptionsFrame(QFrame):
    """Application options."""
    
    options_changed = pyqtSignal()
    exclusions_changed = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.setup_connections()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        title_label = QLabel("Options")
        title_label.setStyleSheet("color: gray")
        layout.addWidget(title_label)

        self.remove_imports_checkbox = QCheckBox("Remove Imports")
        self.remove_comments_checkbox = QCheckBox("Remove Comments")
        self.sort_combo = QComboBox()
        self.sort_combo.addItems([
            "File Name (Ascending)",
            "File Name (Descending)",
            "File Type"
        ])

        exclude_layout = QVBoxLayout()
        exclude_label = QLabel("Exclude Directories (comma-separated):")
        self.exclude_input = QLineEdit()
        self.exclude_input.setPlaceholderText("node_modules, venv")
        exclude_layout.addWidget(exclude_label)
        exclude_layout.addWidget(self.exclude_input)

        layout.addWidget(self.remove_imports_checkbox)
        layout.addWidget(self.remove_comments_checkbox)
        layout.addWidget(self.sort_combo)
        layout.addLayout(exclude_layout)

        self.setLayout(layout)

    def setup_connections(self):
        # Setup signal connections
        self.remove_imports_checkbox.stateChanged.connect(self.options_changed.emit)
        self.remove_comments_checkbox.stateChanged.connect(self.options_changed.emit)
        self.sort_combo.currentIndexChanged.connect(self.options_changed.emit)
        self.exclude_input.textChanged.connect(self.on_exclusions_changed)

    def apply_config(self, config):
        # Apply configuration settings
        exclusions = config.get("exclusions", [])
        self.exclude_input.setText(", ".join(exclusions))
        options = config.get("options", {})
        self.remove_imports_checkbox.setChecked(options.get("remove_imports", False))
        self.remove_comments_checkbox.setChecked(options.get("remove_comments", False))
        self.sort_combo.setCurrentIndex(options.get("sort_index", 0))

    def on_exclusions_changed(self):
        # Handle exclusions change
        exclusions = self.get_exclusions()
        self.exclusions_changed.emit(exclusions)

    def get_options(self):
        # Get current options
        return {
            'remove_imports': self.remove_imports_checkbox.isChecked(),
            'remove_comments': self.remove_comments_checkbox.isChecked(),
            'sort_index': self.sort_combo.currentIndex()
        }

    def get_exclusions(self):
        # Get exclusion list
        return [item.strip() for item in self.exclude_input.text().split(',') if item.strip()]

    def set_exclusions(self, exclusions):
        # Set exclusion list
        self.exclude_input.setText(", ".join(exclusions))