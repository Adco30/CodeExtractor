from PyQt5.QtWidgets import QHBoxLayout, QFrame, QLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import pyqtSignal

class DashboardFrame(QFrame):
    """Frame for workspace dashboard controls."""
    
    workspace_changed = pyqtSignal(str)
    update_clicked = pyqtSignal()
    reset_clicked = pyqtSignal()
    interrupt_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.setup_connections()

    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSizeConstraint(QLayout.SetMinAndMaxSize)

        workspace_label = QLabel("Eclipse Workspace:")
        self.workspace_input = QLineEdit("/path/to/folder")
        self.update_button = QPushButton("Update")
        self.reset_button = QPushButton("Reset Settings")
        self.interrupt_button = QPushButton("Interrupt")
        layout.addWidget(workspace_label)
        layout.addWidget(self.workspace_input, 1)
        layout.addWidget(self.update_button)
        layout.addWidget(self.reset_button)
        layout.addWidget(self.interrupt_button)
        self.setLayout(layout)
        self.adjustSize()

    def setup_connections(self):
        # Setup signal connections
        self.update_button.clicked.connect(self.update_clicked.emit)
        self.reset_button.clicked.connect(self.reset_clicked.emit)
        self.interrupt_button.clicked.connect(self.interrupt_clicked.emit)
        self.workspace_input.returnPressed.connect(self.update_clicked.emit)

    def get_workspace(self):
        # Get workspace path
        return self.workspace_input.text()

    def set_workspace(self, path):
        # Set workspace path
        self.workspace_input.setText(path)

    def apply_config(self, config):
        # Apply configuration settings
        if 'workspace_path' in config:
            self.set_workspace(config['workspace_path'])