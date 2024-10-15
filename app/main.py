from PyQt5.QtWidgets import QApplication
from app.app import MainWindow
import sys
import os

if __name__ == "__main__":
    app = QApplication(sys.argv)
    with open("app/static/style.qss", "r") as f:
        stylesheet = f.read()
    app.setStyleSheet(stylesheet)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
