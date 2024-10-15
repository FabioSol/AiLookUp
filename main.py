from PyQt5.QtWidgets import QApplication
from app import MainWindow
import sys
import os

from model.downloader import download
from db.build import build


if __name__ == "__main__":
    if not os.path.exists('model/model'):
        download()
    if not os.path.exists('db/data'):
        build()

    app = QApplication(sys.argv)
    with open("static/style.qss", "r") as f:
        stylesheet = f.read()
    app.setStyleSheet(stylesheet)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
