import os
from PyQt5.QtWidgets import QSplitter, QWidget, QVBoxLayout, QFrame, QSizePolicy
from PyQt5.QtCore import Qt

from controllers.dashboard_controller import WorkspaceDashboardController
from controllers.explorer_controller import ExplorerController
from controllers.markdown_controller import MarkdownController
from models.config_manager import ConfigManager
from models.file_model import FileModel
from services.markdown_service import ThreadManager
from views.dashboard_frame import DashboardFrame
from views.file_type_checkboxes_frame import FileTypeCheckboxesFrame
from views.indented_view_frame import IndentedViewFrame
from views.markdown_frame import MarkdownFrame
from views.options_frame import OptionsFrame
from views.project_explorer_frame import ProjectExplorerFrame

class CodeExplorer(QWidget):
    """Main application controller"""
    
    def __init__(self):
        super().__init__()
        self.thread_manager = ThreadManager()
        self.config = ConfigManager.load()
        self.file_system_model = FileModel()

        self.setWindowTitle("Project Explorer")
        self.setGeometry(100, 100, 1200, 800)

        self.setup_ui()
        self.init_controllers()
        self.load_config()
        self.update_workspace()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.dashboard_frame = DashboardFrame(self)
        main_layout.addWidget(self.dashboard_frame)

        self.project_explorer_frame = ProjectExplorerFrame(self)
        self.markdown_frame = MarkdownFrame(self)
        self.indented_view_frame = IndentedViewFrame(self)
        self.options_frame = OptionsFrame(self)
        self.file_type_checkboxes_frame = FileTypeCheckboxesFrame(self)

        vertical_splitter = QSplitter(Qt.Vertical)
        vertical_splitter.setChildrenCollapsible(False)
        
        top_splitter = QSplitter(Qt.Horizontal)
        top_splitter.setChildrenCollapsible(False)
        
        bottom_splitter = QSplitter(Qt.Horizontal)
        bottom_splitter.setChildrenCollapsible(False)

        self.project_explorer_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.markdown_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.indented_view_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        top_splitter.addWidget(self.project_explorer_frame)
        top_splitter.addWidget(self.markdown_frame)

        combined_frame = QFrame()
        combined_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        combined_layout = QVBoxLayout(combined_frame)
        combined_layout.setContentsMargins(0, 0, 0, 0)
        combined_layout.addWidget(self.file_type_checkboxes_frame)
        combined_layout.addWidget(self.options_frame)

        bottom_splitter.addWidget(self.indented_view_frame)
        bottom_splitter.addWidget(combined_frame)

        vertical_splitter.addWidget(top_splitter)
        vertical_splitter.addWidget(bottom_splitter)

        vertical_splitter.setSizes([400, 400])
        top_splitter.setSizes([600, 600])
        bottom_splitter.setSizes([600, 600])

        main_layout.addWidget(vertical_splitter)
        self.setLayout(main_layout)

        self.project_explorer_frame.set_model(self.file_system_model.file_model)

    def init_controllers(self):
        # Initialize controllers
        self.dashboard_controller = WorkspaceDashboardController(self.dashboard_frame, self)
        self.explorer_controller = ExplorerController(
            self.project_explorer_frame,
            self.indented_view_frame,
            self.file_type_checkboxes_frame,
            self.file_system_model,
            self
        )
        self.markdown_controller = MarkdownController(
            self.markdown_frame,
            self.options_frame,
            self.file_type_checkboxes_frame,
            self.thread_manager,
            self
        )

    def load_config(self):
        # Load configuration settings
        self.dashboard_controller.apply_config(self.config)
        self.explorer_controller.apply_config(self.config)
        self.options_frame.apply_config(self.config)
        if "exclusions" in self.config:
            self.options_frame.set_exclusions(self.config["exclusions"])

    def save_config(self):
        # Save configuration settings
        self.config["frame_dimensions"] = {
            "project_explorer": {"width": self.project_explorer_frame.width(), "height": self.project_explorer_frame.height()},
            "indented_view": {"width": self.indented_view_frame.width(), "height": self.indented_view_frame.height()},
            "markdown": {"width": self.markdown_frame.width(), "height": self.markdown_frame.height()},
            "options": {"width": self.options_frame.width(), "height": self.options_frame.height()}
        }
        ConfigManager.save(self.config)

    def update_workspace(self):
        # Update workspace path
        workspace_path = self.dashboard_frame.get_workspace()
        if os.path.exists(workspace_path):
            index = self.file_system_model.set_root(workspace_path)
            self.project_explorer_frame.set_root_index(index)
            self.config["workspace_path"] = workspace_path
            self.save_config()

    def reset_settings(self):
        # Reset application settings
        self.config = ConfigManager.load()
        self.load_config()
        self.update_workspace()

    def get_excluded_items(self):
        # Get excluded items from options
        return self.options_frame.get_exclusions()

    def interrupt_processing(self):
        # Interrupt current processing thread
        self.thread_manager.interrupt_current()

    def on_project_selected(self, path):
        # Handle project selection
        if os.path.isdir(path):
            self.project_explorer_frame.set_selected_path(path)
            self.explorer_controller.update_file_type_checkboxes(path)
            self.explorer_controller.update_indented_view()
            self.markdown_controller.refresh()
        elif os.path.isfile(path):
            self.project_explorer_frame.set_selected_path(path)
            self.explorer_controller.update_indented_view()
            self.markdown_controller.refresh()

    def on_column_sort_preference_update(self, column_name, order_key):
        # Update column sort preferences
        if column_name in self.config["column_sort_preferences"]:
            self.config["column_sort_preferences"][column_name][order_key] += 1
            self.save_config()

    def on_project_preferences_update(self, project_name, extension, checked):
        # Update project preferences
        if project_name not in self.config["project_preferences"]:
            self.config["project_preferences"][project_name] = {"extensions": {}}
        extensions = self.config["project_preferences"][project_name]["extensions"]
        if checked:
            extensions[extension] = extensions.get(extension, 0) + 1
        self.save_config()