from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem, QWidget, QVBoxLayout, QLineEdit, QTableWidget, QSizePolicy, QHeaderView, \
    QPushButton, QHBoxLayout

from app.db.controller import FileController
from app.ui.components.back_button import BackButton


class FindPage(QWidget):
    def __init__(self,main_window, filename=None, file_id=None):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Find Page")

        self.file_id = file_id
        self.filename = filename

        self.layout = QVBoxLayout(self)
        self.horizontal_layout = QHBoxLayout()

        self.back_button = BackButton()
        self.back_button.setFixedSize(60, 30)
        self.back_button.clicked.connect(self.go_back)
        self.horizontal_layout.addWidget(self.back_button)

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("What are you looking for?")
        self.search_input.returnPressed.connect(self.refresh_table)
        self.horizontal_layout.addWidget(self.search_input)

        self.layout.addLayout(self.horizontal_layout)

        self.table = QTableWidget(self)
        self.layout.addWidget(self.table)


        if self.filename:
            self.file_controller = FileController.find(self.filename)
            self.load_data()

    def load_data(self):
        self.display_data(self.file_controller.df)

    def display_data(self, df):
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table.setRowCount(df.shape[0])
        self.table.setColumnCount(df.shape[1])
        self.table.setHorizontalHeaderLabels(df.columns)

        for col in range(df.shape[1]):
            self.table.horizontalHeader().setSectionResizeMode(col, QHeaderView.Interactive)
            for row in range(df.shape[0]):
                item = QTableWidgetItem(str(df.iat[row, col]))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(row, col, item)

    def refresh_table(self):
        search_text = self.search_input.text()
        data = self.file_controller.similarity_rank(search_text)
        self.display_data(data)

    def go_back(self):
        self.main_window.stacked_widget.setCurrentWidget(self.main_window.files_page)
