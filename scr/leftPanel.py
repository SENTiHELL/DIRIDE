from PyQt5.QtWidgets import QWidget, QLabel

class leftPanel(QWidget):

    def __init__(self, parent=None):
        super(leftPanel, self).__init__(parent)
        self.parent =  parent
        self.init()
        pass
    def init(self):
        self.bg = QWidget(self)
        self.module = self.parent.parent().parent().module
        #self.mod = self.parent.parent().module
        #print(self.module.panel(), 'eeee')
        try:
            self.module.panel(self)
        except:
            pass
        self.bg.setFixedSize(100,100)
    def resizeEvent(self, QResizeEvent):
        self.bg.setFixedSize(self.parent.size())
    def setStyleSheet(self, p_str):
        self.bg.setStyleSheet(p_str)