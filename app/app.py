from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QDesktopWidget
from ui.files_page import FilesPage
from ui.find_page import FindPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AiLookUp")
        self.setWindowIcon(QIcon('static/logo.ico'))

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.files_page = FilesPage(self)
        self.find_page = FindPage(self)

        self.stacked_widget.addWidget(self.files_page)
        self.stacked_widget.addWidget(self.find_page)

        self.stacked_widget.setCurrentWidget(self.files_page)
        self.set_window_size()

    def show_find_page(self, filename, file_id):
        self.find_page = FindPage(self, filename=filename, file_id=file_id)
        self.stacked_widget.addWidget(self.find_page)
        self.stacked_widget.setCurrentWidget(self.find_page)

    def set_window_size(self):
        screen = QDesktopWidget().screenGeometry()
        screen_width = screen.width()
        screen_height = screen.height()

        new_width = int(screen_width * 0.9)
        new_height = int(screen_height * 0.9)

        self.resize(new_width, new_height)

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
