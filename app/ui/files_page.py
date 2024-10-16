from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox, QSizePolicy, \
    QHeaderView
from app.db.controller import FileController
from app.ui.components.delete_button import DeleteButton
from app.ui.components.upload_button import UploadButton
from app.ui.upload_dialog import FileUploadDialog


class FilesPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["File Name", ""])

        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table.setFocusPolicy(Qt.NoFocus)

        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)
        self.table.setColumnWidth(1, 80)


        self.refresh_table()

        self.table.cellDoubleClicked.connect(self.open_find_page)

        self.upload_button = UploadButton()
        self.upload_button.clicked.connect(self.open_upload_dialog)

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(self.upload_button)
        layout.setStretch(0, 1)
        layout.setStretch(1, 0)

        self.setLayout(layout)

    def open_find_page(self, row, column):
        if column == 0:
            filename = self.table.item(row, column).text()
            file_id = self.files[row][0]

            self.main_window.show_find_page(filename, file_id)

    def delete_file(self, row, file_id):
        confirm = QMessageBox.question(self, "Confirm Deletion", "Are you sure you want to delete this file?",
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.table.removeRow(row)
            FileController.delete_file(file_id)

    def open_upload_dialog(self):
        dialog = FileUploadDialog(self)
        dialog.finished.connect(self.refresh_table)
        if dialog.exec_():
            self.refresh_table()

    def refresh_table(self):
        self.table.setRowCount(0)

        self.files = FileController.get_files()

        for file_id, filename in self.files:
            row_count = self.table.rowCount()
            self.table.insertRow(row_count)
            item = QTableWidgetItem(filename)
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row_count, 0, item)

            delete_button = DeleteButton()
            delete_button.clicked.connect(lambda row=row_count, f_id=file_id: self.delete_file(row, f_id))
            self.table.setCellWidget(row_count, 1, delete_button)
        self.adjust_column_widths()

    def adjust_column_widths(self):
        self.table.setColumnWidth(1, 80)

