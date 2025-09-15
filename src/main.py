from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize
from variables import WINDOW_ICON_PATH
from main_window import MainWindow
from display import Display
from info import Info
from style import setupTheme
from buttons import ButtonsGrid, HistoryButton
from history import HistoryFrame, HistoryList
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    
    icon = QIcon(str(WINDOW_ICON_PATH))
    app.setWindowIcon(icon)
    window.setWindowIcon(icon)

    historyList = HistoryList()
    painel = HistoryFrame(window.cW)
    display = Display()
    info = Info('')
    historyButton = HistoryButton(painel, display, window.cW)
    buttonsGrid = ButtonsGrid(display, info, window, historyList)
    
    painel.addWidgetToVLayout(historyList)
    window.addWidgetToHLayout(historyButton)
    window.addWidgetToHLayout(info)
    window.addWidgetToVLayout(display)
    window.addLayoutGridToVLayout(buttonsGrid)
    
   
    window.ajustFixedSize()
    window.show()
    setupTheme(app)
    app.exec()