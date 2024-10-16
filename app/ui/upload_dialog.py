from PyQt5.QtWidgets import QDialog, QLineEdit, QFileDialog, QTableWidget, QHBoxLayout, QVBoxLayout, \
    QTableWidgetItem, QLabel, QSizePolicy, QHeaderView
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor
import pandas as pd

from app.db.controller import FileController
from app.ui.components.browse_button import BrowseButton
from app.ui.components.upload_button import UploadButton


class FileUploadDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Upload File")
        self.setMinimumSize(800, 600)
        self.layout = QVBoxLayout(self)

        self.file_path_edit = QLineEdit(self)
        self.browse_button = BrowseButton()
        self.browse_button.clicked.connect(self.browse_file)

        file_layout = QHBoxLayout()
        file_layout.addWidget(self.file_path_edit)
        file_layout.addWidget(self.browse_button)
        self.layout.addLayout(file_layout)

        legend = QLabel("Click to select descriptive columns", self)
        legend.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(legend)

        self.table = QTableWidget()
        self.table.horizontalHeader().sectionClicked.connect(self.handle_header_click)
        self.table.setSelectionMode(QTableWidget.NoSelection)
        self.layout.addWidget(self.table)

        self.upload_button = UploadButton()
        self.upload_button.clicked.connect(self.upload_file)
        self.layout.addWidget(self.upload_button)

        self.selected_columns = []

    def browse_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select File", "", "CSV Files (*.csv);;Excel Files (*.xlsx)")
        if file_name:
            self.file_path_edit.setText(file_name)
            self.read_file(file_name)

    def read_file(self, file_name):
        try:
            if file_name.endswith('.csv'):
                df = pd.read_csv(file_name)
            elif file_name.endswith('.xlsx'):
                df = pd.read_excel(file_name)
            else:
                raise ValueError("Unsupported file format")

            self.display_data(df.head(10))

        except Exception as e:
            print(f"Error reading file: {e}")

    def display_data(self, df):
        self.table.setRowCount(df.shape[0])
        self.table.setColumnCount(df.shape[1])
        self.table.setHorizontalHeaderLabels(df.columns)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table.setFocusPolicy(Qt.NoFocus)

        for col in range(df.shape[1]):
            self.table.horizontalHeader().setSectionResizeMode(col, QHeaderView.Stretch)
            for row in range(df.shape[0]):
                self.table.setItem(row, col, QTableWidgetItem(str(df.iat[row, col])))
                item = self.table.item(row, col)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)

    def handle_header_click(self, col_index):
        if col_index in self.selected_columns:
            self.selected_columns.remove(col_index)
            self.set_column_color(col_index, "#3C3C3C")
        else:
            self.selected_columns.append(col_index)
            self.set_column_color(col_index, "#524444")

    def set_column_color(self, col_index, color):
        header_item = self.table.horizontalHeaderItem(col_index)
        if header_item:
            header_item.setBackground(QColor(color))

        for row in range(self.table.rowCount()):
            item = self.table.item(row, col_index)
            if item:
                item.setBackground(QColor(color))
            else:
                new_item = QTableWidgetItem()
                new_item.setBackground(QColor(color))
                self.table.setItem(row, col_index, new_item)

    def upload_file(self):
        file_path = self.file_path_edit.text()
        if not file_path:
            print("Error: No file selected.")
            return

        if not self.selected_columns:
            print("Error: No columns selected.")
            self.upload_button.setStyleSheet("background-color: red;")
            QTimer.singleShot(2000, lambda: self.upload_button.setStyleSheet(""))
            return

        self.upload_button.setStyleSheet("")

        selected_columns_names = [self.table.horizontalHeaderItem(i).text() for i in self.selected_columns]

        f = FileController.new(file_path, selected_columns_names)
        f.save()

        self.close()
