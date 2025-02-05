from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon, QPixmap, QPainter
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtCore import QSize, Qt

from app.ui import static_path


class UploadButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        icon = QIcon()
        svg_renderer = QSvgRenderer(static_path+'/upload_icon.svg')
        pixmap = QPixmap(24, 24)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        svg_renderer.render(painter)
        painter.end()
        icon.addPixmap(pixmap)

        self.setIcon(icon)
        self.setIconSize(QSize(24, 24))
        self.setStyleSheet("text-align: center;")
