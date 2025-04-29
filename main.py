import sys
from PyQt5.QtWidgets import QApplication
from controllers.app_controller import CodeExplorer

if __name__ == "__main__":
    app = QApplication(sys.argv)
    explorer = CodeExplorer()
    explorer.show()
    sys.exit(app.exec_())