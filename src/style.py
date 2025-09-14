# QSS - Estilos do QT for Python
# https://doc.qt.io/qtforpython/tutorials/basictutorial/widgetstyling.html
# Dark Theme
# https://pyqtdarktheme.readthedocs.io/en/latest/how_to_use.html

import qdarkstyle
from PySide6.QtWidgets import QApplication
from qdarkstyle.light.palette import LightPalette

from variables import (DARKER_PRIMARY_COLOR, DARKEST_PRIMARY_COLOR,
                       PRIMARY_COLOR)
 
qss = f"""
    QPushButton[cssClass="specialButton"] {{
        color: #fff;
        background: {PRIMARY_COLOR};
        border-radius: 5px;
    }}
    QPushButton[cssClass="specialButton"]:hover {{
        color: #fff;
        background: {DARKER_PRIMARY_COLOR};
    }}
    QPushButton[cssClass="specialButton"]:pressed {{
        color: #fff;
        background: {DARKEST_PRIMARY_COLOR};
    }}
"""
 
 
def setupTheme(app: QApplication):
    # Aplicar o estilo escuro do qdarkstyle
    app.setStyleSheet(qdarkstyle._load_stylesheet(qt_api='pyside6', palette=None))
 
    # Sobrepor com o QSS personalizado para estilização adicional
    app.setStyleSheet(app.styleSheet() + qss)