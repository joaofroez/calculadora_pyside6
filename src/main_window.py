from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget, QMessageBox, QHBoxLayout, QFrame, QGridLayout
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self, /, parent: QWidget | None = None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs) 
        self.cW = QWidget()
        self.VLayout = QVBoxLayout()
        self.HLayout = QHBoxLayout()
        self.VLayout.addLayout(self.HLayout)
        self.cW.setLayout(self.VLayout)
        self.setCentralWidget(self.cW)
        self.setWindowTitle('Calculadora')

    def ajustFixedSize(self):
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())

    def addWidgetToVLayout(self, widget: QWidget):
        self.VLayout.addWidget(widget)

    def addWidgetToHLayout(self, widget: QWidget):
        self.HLayout.addWidget(widget)

    def addLayoutGridToVLayout(self, layout: QGridLayout):
        self.VLayout.addLayout(layout)

    def makeMsgBox(self):
        return QMessageBox(self)
        
