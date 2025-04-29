from PyQt5.QtGui import QTextOption
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QTextEdit, QHBoxLayout, QCheckBox, QPushButton, QApplication
from PyQt5.QtCore import pyqtSignal

class IndentedViewFrame(QFrame):
    """Frame for displaying indented file view."""
    
    options_changed = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.main_app = parent
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel("Indented View")
        label.setStyleSheet("color: gray")

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setWordWrapMode(QTextOption.NoWrap)
        self.text_edit.setStyleSheet("background-color: #f0f0f0; font-family: Courier;")

        checkbox_layout = QHBoxLayout()
        self.show_dotfiles_checkbox = QCheckBox("Show dotfiles")
        self.detailed_view_checkbox = QCheckBox("Detailed View")
        checkbox_layout.addWidget(self.show_dotfiles_checkbox)
        checkbox_layout.addWidget(self.detailed_view_checkbox)

        self.copy_button = QPushButton("Copy Treemap")

        layout.addWidget(label)
        layout.addWidget(self.text_edit)
        layout.addLayout(checkbox_layout)
        layout.addWidget(self.copy_button)

        self.setLayout(layout)
        self.setup_connections()

    def setup_connections(self):
        # Setup signal connections
        self.show_dotfiles_checkbox.stateChanged.connect(self.options_changed.emit)
        self.detailed_view_checkbox.stateChanged.connect(self.options_changed.emit)
        self.copy_button.clicked.connect(self.copy_to_clipboard)

    def set_content(self, text):
        # Set text content
        self.text_edit.setPlainText(text)

    def get_options(self):
        # Get current options
        return {
            'show_dotfiles': self.show_dotfiles_checkbox.isChecked(),
            'detailed_view': self.detailed_view_checkbox.isChecked()
        }

    def copy_to_clipboard(self):
        # Copy content to clipboard
        QApplication.clipboard().setText(self.text_edit.toPlainText())