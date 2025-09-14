from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFrame, QListView, QAbstractItemView
from PySide6.QtCore import QRect, QSize, Qt, QMargins, QStringListModel, QAbstractListModel, QModelIndex

class HistoryFrame(QFrame):
    def __init__(self, /, parent: QWidget, *args, **kwargs):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setStyleSheet("background-color: #2b2b2b; color: white;border-radius: 1px;")
        self.setVisible(False)
        self.VLayout = QVBoxLayout(self)
        self.VLayout.addWidget(QLabel("Seu histórico aqui"))
        self.VLayout.addStretch()

    def addWidgetToVLayout(self, widget: QListView):
        self.VLayout.addWidget(widget)

class HistoryModel(QAbstractListModel):
    def __init__(self, data=None, parent=None):
        super().__init__(parent)
        self._data = data or []

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self._data)):
            return None

        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()]['expr'].strip()
        
        return None
    def add_history_item(self, item_dict):
        # Método para adicionar um novo item ao histórico
        row = self.rowCount()
        self.beginInsertRows(QModelIndex(), row, row)
        self._data.append(item_dict)
        self.endInsertRows()
        
    def clear_history(self):
        # Método para limpar o histórico
        self.beginRemoveRows(QModelIndex(), 0, self.rowCount() -1)
        self._data.clear()
        self.endRemoveRows()

class HistoryList(QListView):
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.expressions = HistoryModel()
        self.setModel(self.expressions)
        self.setFixedHeight(350)
        no_edit = QAbstractItemView.EditTrigger.NoEditTriggers
        self.setEditTriggers(no_edit) 
        self.setStyleSheet("""
            QListView {
                background-color: #2b2b2b; 
                border: 2px solid #444;
                font-size: 15px 
            }
            
            QListView::item {
                color: white;       
                padding: 5px;         
            }
            
            QListView::item:selected {
                background-color: #0078d7;
                color: white;            
            }
        """)

        






        
