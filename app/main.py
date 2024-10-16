from app.app import MainWindow
import PyQt5.QtWidgets
import sys
import os

if __name__ == "__main__":
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    with open("app/static/style.qss", "r") as f:
        stylesheet = f.read()
    app.setStyleSheet(stylesheet)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
