import os
import fnmatch
from PyQt5.QtCore import Qt

class ExplorerController:
    
    def __init__(self, explorer_view, indented_view, file_type_view, file_system_model, app):
        self.explorer_view = explorer_view
        self.indented_view = indented_view
        self.file_type_view = file_type_view
        self.file_system_model = file_system_model
        self.app = app
        self._connect_signals()

    def _connect_signals(self):
        # Connect view signals to controller methods
        self.explorer_view.project_selected.connect(self.on_project_selected)
        self.explorer_view.column_clicked.connect(self.on_column_clicked)
        self.explorer_view.columnResized.connect(self.on_column_resized)
        self.file_type_view.selection_changed.connect(self.on_file_type_selection_changed)
        self.indented_view.options_changed.connect(self.update_indented_view)

    def on_column_resized(self, index, new_size):
        # Handle column resize event
        model = self.explorer_view.file_tree.model()
        if model:
            header_text = model.headerData(index, Qt.Horizontal, Qt.DisplayRole)
            if "column_widths" not in self.app.config:
                self.app.config["column_widths"] = {}
            self.app.config["column_widths"][header_text] = new_size
            self.app.save_config()

    def on_file_type_selection_changed(self, selected_extensions):
        # Handle file type selection change
        project_path = self.explorer_view.get_selected_path()
        if project_path:
            project_name = os.path.basename(project_path)
            if project_name not in self.app.config["project_preferences"]:
                self.app.config["project_preferences"][project_name] = {"extensions": {}}
            prefs = self.app.config["project_preferences"][project_name]["extensions"]
            for ext in selected_extensions:
                prefs[ext] = prefs.get(ext, 0) + 1
            self.app.save_config()
            self.app.markdown_controller.refresh()

    def on_project_selected(self, index):
        # Handle project selection
        path = self.file_system_model.get_file_path(index)
        self.app.on_project_selected(path)

    def update_indented_view(self):
        # Update indented view content
        path = self.app.project_explorer_frame.get_selected_path()
        if not path:
            self.indented_view.set_content("")
            return

        if os.path.isfile(path):
            file_name = os.path.basename(path)
            output = [file_name]
            
            if self.indented_view.get_options().get('detailed_view', False):
                ext = os.path.splitext(file_name)[1]
                if ext in ['.java', '.py', '.swift']:
                    from services.markdown_service import DetailedViewParser
                    details = DetailedViewParser.parse_file(path)
                    for detail in details:
                        output.append(f"    {detail}")
            
            self.indented_view.set_content("\n".join(output))
            return
            
        excluded_items = self.app.get_excluded_items()
        options = self.indented_view.get_options()
        content = self.generate_indented_view(
            path,
            excluded_items,
            options.get('show_dotfiles', False),
            options.get('detailed_view', False)
        )

        self.indented_view.set_content(content)

    def generate_indented_view(self, path, excluded_items, show_dotfiles, detailed_view):
        # Generate indented directory view
        from services.markdown_service import DetailedViewParser
        if not os.path.exists(path):
            return ""
        output = []
        excluded_files = [pattern for pattern in excluded_items if '*' in pattern or '.' in pattern]
        excluded_dirs = [pattern for pattern in excluded_items if '*' not in pattern and '.' not in pattern]

        def should_exclude(item, relative_path):
            # Check if item should be excluded
            if not show_dotfiles and item.startswith('.'):
                return True
            if any(fnmatch.fnmatch(item, pattern) for pattern in excluded_files):
                return True
            if any(part in excluded_dirs for part in relative_path.split(os.sep)):
                return True
            return False

        def traverse_directory(directory, rel_path="", level=0):
            # Traverse directory recursively
            try:
                entries = sorted(os.listdir(directory))
                for entry in entries:
                    full_path = os.path.join(directory, entry)
                    cur_rel_path = os.path.join(rel_path, entry)
                    if should_exclude(entry, cur_rel_path):
                        continue
                    indent = "    " * level
                    if os.path.isfile(full_path):
                        output.append(f"{indent}{entry}")
                        if detailed_view:
                            _, ext = os.path.splitext(entry)
                            if ext in ['.java', '.py', '.swift']:
                                details = DetailedViewParser.parse_file(full_path)
                                for detail in details:
                                    output.append(f"{indent}    {detail}")
                    elif os.path.isdir(full_path):
                        output.append(f"{indent}{entry}/")
                        traverse_directory(full_path, cur_rel_path, level + 1)
            except PermissionError:
                pass
        traverse_directory(path)
        return "\n".join(output)

    def on_column_clicked(self, column, order):
        # Handle column click for sorting
        model = self.explorer_view.file_tree.model()
        header_text = model.headerData(column, Qt.Horizontal, Qt.DisplayRole)
        order_key = "desc" if order == Qt.DescendingOrder else "asc"
        if header_text in self.app.config["column_sort_preferences"]:
            self.app.config["column_sort_preferences"][header_text][order_key] += 1
        else:
            self.app.config["column_sort_preferences"][header_text] = {"asc": 0, "desc": 0}
            self.app.config["column_sort_preferences"][header_text][order_key] = 1
        self.app.save_config()

    def apply_config(self, config):
        # Apply configuration settings
        self.explorer_view.apply_config(config)

    def get_preferred_sort(self, config):
        # Get preferred sorting settings
        if "column_sort_preferences" not in config:
            return None
        preferences = config["column_sort_preferences"]
        max_count = 0
        preferred_sort = None
        for column_name, sort_orders in preferences.items():
            for order_type, count in sort_orders.items():
                if count > max_count:
                    max_count = count
                    column_index = self.explorer_view.get_column_index(column_name)
                    sort_order = Qt.DescendingOrder if order_type == "desc" else Qt.AscendingOrder
                    preferred_sort = (column_index, sort_order)
        return preferred_sort

    def update_file_type_checkboxes(self, path):
        # Update file type checkbox options
        excluded_items = self.app.get_excluded_items()
        file_extensions = self.file_system_model.get_file_extensions(path, excluded_items)
        project_preferences = self.app.config["project_preferences"].get(os.path.basename(path))
        self.file_type_view.update_for_project(file_extensions, project_preferences)