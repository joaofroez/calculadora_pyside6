from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt
from variables import SMALL_FONT_SIZE

class Info(QLabel):
    def __init__(self, text, parent = None, *args, **kwargs):
        super().__init__(text, parent, *args, **kwargs)
        self.configStyle()

    def configStyle(self):
        self.setStyleSheet(f'font-size: {SMALL_FONT_SIZE+5}px;')
        self.setAlignment(Qt.AlignmentFlag.AlignRight)