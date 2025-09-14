from PySide6.QtWidgets import QPushButton, QGridLayout, QWidget
from variables import MEDIUM_FONT_SIZE, HISTORY_ICON_PATH
from utils import isNumOrDot, isEmpty, isValidNumber, convertToNumber, replaceCaretWithPow
from PySide6.QtCore import Slot, QSize, QModelIndex, QPropertyAnimation, QEasingCurve, QRect
from display import Display
from info import Info
from main_window import MainWindow
from PySide6.QtGui import QIcon, QResizeEvent
from history import HistoryFrame, HistoryList

class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()  
    
    def configStyle(self):
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(75, 75)


class ButtonsGrid(QGridLayout):
    def __init__(self, display: Display, info: Info, window: MainWindow, historyList: HistoryList, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._gridMask = [
            ['C', '◀', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['N',  '0', '.', '='],
        ]
        self.display = display
        self.info = info
        self.window = window
        self._equation = ''
        self._equationInitialValue = ''
        self._last_number = ''
        self._op = None
        self._history = {}
        self._expression = self._equationInitialValue
        self.equation = self._equationInitialValue
        self._result = ''
        self.historyList = historyList
        self.historyList.clicked.connect(self.changeExpression)
        self._makeGrid()
    
    @property
    def equation(self):
        return self._equation

    @equation.setter
    def equation(self, value):
        self._equation = value
        self.info.setText(value)

    def _makeGrid(self):
        self.display.eqPressed.connect(self._eq)
        self.display.delPressed.connect(self._backspace)
        self.display.clearPressed.connect(self._clear)
        self.display.inputPressed.connect(self._insertToDisplay) 
        self.display.operatorPressed.connect(self._configLeftOp)
        
        for x, row_number in enumerate(self._gridMask):
            for y, col_number in enumerate(row_number):
                button = Button(col_number)

                if not isNumOrDot(col_number) and not isEmpty(col_number):
                    button.setProperty("cssClass", "specialButton")
                    self._configSpecialButton(button)

                self.addWidget(button, x, y)
                slot = self._makeSlot(
                    self._insertToDisplay,
                    col_number,
                )
                self._connectButtonClicked(button, slot)

    def _connectButtonClicked(self, button, slot):
        button.clicked.connect(slot)

    def _configSpecialButton(self, button):
        text = button.text()
       
        if text == 'C':
            self._connectButtonClicked(button, self._clear)
        
        if text == '◀':
            self._connectButtonClicked(button, self.display.backspace)
        
        if text == 'N':
            self._connectButtonClicked(button, self._invertNumber)

        if text in '+-/*^':
            self._connectButtonClicked(button, 
                self._makeSlot(self._configLeftOp, text)
                )
            
        if text in '=':
            self._connectButtonClicked(button, 
                self._makeSlot(self._eq)
                )

    def _makeSlot(self, func, *args, **kwargs):
        @Slot(bool)
        def realSlot(_):
            func(*args, **kwargs)
        return realSlot

    @Slot()
    def _invertNumber(self):
        displayText = self.display.text()

        if not isValidNumber(displayText):
            return
        
        newNumber = convertToNumber(displayText) * -1
        self.display.setText(str(newNumber))

    @Slot()
    def _insertToDisplay(self, text):
        newDisplayValue = self.display.text() + text
        self.display.setFocus()

        if not isValidNumber(newDisplayValue):
            return
    
        if self._expression != "" and self._expression[-1] not in '+-/*^':
            self._clear()

        self.display.insert(text)
        

    @Slot()
    def _clear(self):
        self._op = None
        self._expression = self._equationInitialValue
        self.equation = self._equationInitialValue
        self.display.clear()
        self.display.setFocus()

    @Slot()
    def _configLeftOp(self, text):
        self._op = text
        if not self.display.text() or not self.display.text().strip():

            if self._expression != "" and self._expression[-1] in '+-/*^':
                self._expression = self._expression[:-1] + self._op

            elif self._expression == "":
                self._expression = f'0 {self._op}'

            self.info.setText(self._expression)
            self._checkEquation()
            return
            
        displayText = self.display.text()
        self.display.clear()
        self.display.setFocus()

        if not isValidNumber(displayText) and self._expression == '':
            return
        
        if displayText == self._expression:
            self._expression += f' {self._op}'
        else:
            self._expression += f' {displayText} {self._op}'
            
        self.info.setText(self._expression)
        self._checkEquation()
    
    @Slot()
    def _eq(self):
        if self.display.text() != self._expression:
            self._last_number = self.display.text()
        self.display.setFocus()

        if not isValidNumber(self._last_number) or self._expression == '':
            self._showError("Erro: Conta incompleta")
            return
        
        if self._expression == self.display.text():
            self._expression += f' {self._op} {self._last_number}'
        else:
            self._expression += f' {self._last_number}'
        
        self._result = 'error'

        try:
            self._result = eval(replaceCaretWithPow(self._expression))
        except ZeroDivisionError:
            self._showError("Erro: Divisão por zero")
        except OverflowError:
            self._showError("Erro: Número muito grande")
        except ValueError:
            self._showError("Erro: Valor inválido")
        except TypeError:
            self._showError("Erro: Operação inválida")
        except SyntaxError:
            self._showError("Erro: Sintaxe inválida")
        except Exception as e:
            self._showError(f"Erro: {type(e).__name__}")
        
        self.info.setText(f'{self._expression} = {self._result}')
        history_item = {'expr': self.info.text(), 'result': str(self._result), 'last_number': self._last_number, 'op': self._op}
        self.historyList.expressions.add_history_item(history_item)
        self._expression = str(self._result)
        self.display.setText(str(self._result))
 
        if self._result == 'error':
            self._expression = ''
            self._clear()

    @Slot()
    def _backspace(self):
        self.display.backspace()
        self.display.setFocus()

    def _showError(self, text):
        msgBox = self.window.makeMsgBox()
        msgBox.setText(text)
        msgBox.setIcon(msgBox.Icon.Critical)
        msgBox.exec()

    def _checkEquation(self):
        try:
            if self._expression[-1:] == '^':
                self._result = eval(replaceCaretWithPow(self._expression)[:-2])
            else:
                self._result = eval(replaceCaretWithPow(self._expression)[:-1])
        except ZeroDivisionError:
            self._showError("Erro: Divisão por zero")
            self._clear()
        except OverflowError:
            self._showError("Erro: Número muito grande")
            self._clear()
        except ValueError:
            self._showError("Erro: Valor inválido")
            self._clear()
        except TypeError:
            self._showError("Erro: Operação inválida")
            self._clear()
        except SyntaxError:
            self._showError("Erro: Sintaxe inválida")
            self._clear()
        except Exception as e:
            self._showError(f"Erro: {type(e).__name__}")
            self._clear()
    
    def changeExpression(self, index: QModelIndex):
        history_item = self.historyList.expressions._data[index.row()]
        result = history_item['result']
        full_expression = history_item['expr']
        last_number = history_item['last_number']
        last_op = history_item['op']

        self._expression = result
        self._last_number = last_number
        self._op = last_op
        self.info.setText(full_expression)
        self.display.setText(self._expression)
        

    
class HistoryButton(QPushButton):
    def __init__(self, frame: HistoryFrame, display: Display, widget: QWidget,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()  
        self.adjustSize()
        self.setIcon(QIcon(str(HISTORY_ICON_PATH)))
        self.setIconSize(QSize(30, 30))
        self.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: #104961;
            }
            QPushButton:pressed {
                background-color: #0B3547;
            }
            """)
        self.frame = frame
        self.display = display
        self.widget = widget
        self.clicked.connect(self.toggleHistory)

        self.animation = QPropertyAnimation(self.frame, b"geometry")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutCubic)  
        self.animation.finished.connect(self.onAnimationFinished)

    def configStyle(self):
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        self.setFixedSize(40,40)
    
    def onAnimationFinished(self):
        if self.animation.direction() == QPropertyAnimation.Direction.Backward:
            self.frame.hide()


    def toggleHistory(self):
        self.uptadeHistoryFrameGeometry()

        if self.frame.isVisible():
            self.animation.setDirection(QPropertyAnimation.Direction.Backward)
        else:
            self.frame.show()
            self.frame.raise_()
            self.animation.setDirection(QPropertyAnimation.Direction.Forward)
    
        self.animation.start()

    def uptadeHistoryFrameGeometry(self):
        margem = 6

        endPosX = margem
        endPosY = self.display.y() + self.display.height() + margem
        endWidth = self.widget.width() - (2 * margem)
        endHeight  = self.widget.height() - endPosY - margem
        endGeometry = QRect(endPosX, endPosY, endWidth, endHeight)
        startGeometry = QRect(endPosX, endPosY, endWidth, 0)

        self.animation.setStartValue(startGeometry)
        self.animation.setEndValue(endGeometry)

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)

        self.uptadeHistoryFrameGeometry()