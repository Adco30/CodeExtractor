from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QFrame, QVBoxLayout, QHBoxLayout, QLabel, QToolButton, QTextEdit, QPushButton

class MarkdownFrame(QFrame):
    """Frame for displaying markdown content."""

    def __init__(self, parent):
        super().__init__(parent)
        self.init_ui()
        self.setup_connections()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        header_layout = QHBoxLayout()
        title_label = QLabel("Markdown")
        title_label.setStyleSheet("color: gray")

        font_control_layout = QHBoxLayout()
        self.increase_font_btn = QToolButton()
        self.increase_font_btn.setText("+")
        self.increase_font_btn.setFixedSize(QSize(20, 20))

        self.decrease_font_btn = QToolButton()
        self.decrease_font_btn.setText("-")
        self.decrease_font_btn.setFixedSize(QSize(20, 20))

        font_control_layout.addWidget(self.decrease_font_btn)
        font_control_layout.addWidget(self.increase_font_btn)

        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addLayout(font_control_layout)

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setLineWrapMode(QTextEdit.NoWrap)
        jetbrains_mono = QFont("JetBrains Mono", 10)
        self.text_edit.setFont(jetbrains_mono)

        self.copy_button = QPushButton("Copy Code")

        layout.addLayout(header_layout)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.copy_button)

        self.setLayout(layout)

    def update_content(self, markdown):
        # Update markdown content
        self.text_edit.setPlainText(markdown)

    def setup_connections(self):
        # Setup signal connections
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        self.increase_font_btn.clicked.connect(self.increase_font_size)
        self.decrease_font_btn.clicked.connect(self.decrease_font_size)

    def copy_to_clipboard(self):
        # Copy content to clipboard
        QApplication.clipboard().setText(self.text_edit.toPlainText())

    def increase_font_size(self):
        # Increase font size
        font = self.text_edit.font()
        font.setPointSize(font.pointSize() + 1)
        self.text_edit.setFont(font)

    def decrease_font_size(self):
        # Decrease font size
        font = self.text_edit.font()
        if font.pointSize() > 1:
            font.setPointSize(font.pointSize() - 1)
            self.text_edit.setFont(font)