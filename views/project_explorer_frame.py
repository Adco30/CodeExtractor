from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QTreeView, QHeaderView

class ProjectExplorerFrame(QFrame):
    """Frame for project file explorer."""
    
    project_selected = pyqtSignal(object)
    column_clicked = pyqtSignal(int, int)
    columnResized = pyqtSignal(int, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.setup_connections()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        title_label = QLabel("Project Explorer")
        title_label.setStyleSheet("color: gray")

        self.file_tree = QTreeView()
        header = self.file_tree.header()
        header.setSectionResizeMode(QHeaderView.Interactive)
        header.setStretchLastSection(False)
        header.setSortIndicatorShown(True)
        header.setSectionsClickable(True)
        self.file_tree.setSortingEnabled(True)
        self.file_tree.setAlternatingRowColors(True)

        self.file_tree.setColumnWidth(0, 200)
        self.file_tree.setColumnWidth(1, 100)
        self.file_tree.setColumnWidth(2, 100)
        self.file_tree.setColumnWidth(3, 150)

        header.sectionResized.connect(self.on_section_resized)

        self.selected_path_label = QLabel()
        layout.addWidget(title_label)
        layout.addWidget(self.file_tree)
        layout.addWidget(self.selected_path_label)
        self.setLayout(layout)

    def setup_connections(self):
        # Setup signal connections
        self.file_tree.clicked.connect(self.on_item_clicked)
        self.file_tree.header().sectionClicked.connect(self.on_header_clicked)

    def on_section_resized(self, logicalIndex, oldSize, newSize):
        # Handle column resize event
        self.columnResized.emit(logicalIndex, newSize)

    def set_model(self, model):
        # Set tree view model
        self.file_tree.setModel(model)

    def set_root_index(self, index):
        # Set root index for tree view
        self.file_tree.setRootIndex(index)

    def set_selected_path(self, path):
        # Set selected path label
        self.selected_path_label.setText(path)

    def get_selected_path(self):
        # Get selected path
        return self.selected_path_label.text()

    def get_column_index(self, column_name):
        # Get column index from name
        model = self.file_tree.model()
        if model:
            for i in range(model.columnCount()):
                if model.headerData(i, Qt.Horizontal, Qt.DisplayRole) == column_name:
                    return i
        return 0

    def on_item_clicked(self, index):
        # Handle item click event
        self.project_selected.emit(index)

    def on_header_clicked(self, logical_index):
        # Handle header click for sorting
        current_sort_column = self.file_tree.header().sortIndicatorSection()
        current_sort_order = self.file_tree.header().sortIndicatorOrder()
        if logical_index == current_sort_column:
            new_order = Qt.DescendingOrder if current_sort_order == Qt.AscendingOrder else Qt.AscendingOrder
        else:
            new_order = Qt.AscendingOrder
        self.file_tree.setSortingEnabled(False)
        self.file_tree.sortByColumn(logical_index, new_order)
        self.file_tree.setSortingEnabled(True)
        self.file_tree.header().setSortIndicator(logical_index, new_order)
        self.file_tree.header().setSortIndicatorShown(True)
        self.column_clicked.emit(logical_index, new_order)

    def set_preferred_sort(self, column_index, sort_order):
        # Set preferred sorting
        if column_index is not None and sort_order is not None:
            self.file_tree.sortByColumn(column_index, sort_order)

    def apply_config(self, config):
        # Apply configuration settings
        if "column_widths" in config:
            model = self.file_tree.model()
            if model:
                for i in range(model.columnCount()):
                    header_text = model.headerData(i, Qt.Horizontal, Qt.DisplayRole)
                    if header_text in config["column_widths"]:
                        self.file_tree.setColumnWidth(i, config["column_widths"][header_text])