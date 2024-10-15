from PyQt5.QtWidgets import QApplication
from app import MainWindow
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    with open("static/style.qss", "r") as f:
        stylesheet = f.read()
    app.setStyleSheet(stylesheet)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
