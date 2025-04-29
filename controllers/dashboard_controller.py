from mixins.configurable_mixin import ConfigurableMixin


class WorkspaceDashboardController:
    """Controller for workspace dashboard functionality."""
    
    def __init__(self, view, app):
        self.view = view
        self.app = app
        self._connect_signals()

    def _connect_signals(self):
        # Connect view signals to controller methods
        self.view.update_clicked.connect(self.app.update_workspace)
        self.view.reset_clicked.connect(self.app.reset_settings)
        self.view.interrupt_clicked.connect(self.app.interrupt_processing)

    def apply_config(self, config):
        # Apply configuration settings
        if "workspace_path" in config:
            self.view.set_workspace(config["workspace_path"])

    def get_workspace_path(self):
        # Get current workspace path
        return self.view.get_workspace()

    def set_workspace(self, path):
        # Set workspace path and save config
        self.view.set_workspace(path)
        self.app.config["workspace_path"] = path
        self.app.save_config()