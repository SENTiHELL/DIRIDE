from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QSizePolicy
from PyQt5.QtGui import QIcon, QPixmap, QPalette, QFontMetrics
from PyQt5.QtCore import Qt, QSize

import sys, re,__main__

class about(QWidget):

    def __init__(self, parent=None):
        super(about, self).__init__(parent)
        self.parent = parent

        self.init()
    def init(self):
        sys.modules['m'].callbackResize.append(self.res)

        #self.setStyleSheet("background: red") # temp
        self.background = QWidget(self)
        self.background.setStyleSheet("background: rgba(0,0,0,.2)")

        self.mainGeom = sys.modules['m'].geometry()
        self.setGeometry(0, 0, self.mainGeom.width(), self.mainGeom.height())
        self.setMaximumSize(self.size())
        self.setMinimumSize(self.size())
        self.setWindowIcon(QIcon(sys.modules['basedir']+'/ui/dirride.png'))
        self.setWindowTitle(__main__.programName + ' - About')

        c = sys.modules['m'].palette().color(QPalette.Background)
        arr = [c.red(), c.green(), c.blue()]

        mainBG = 'rgb(' + (','.join(str(x) for x in arr)) + ')'

        self.main = QWidget(self.background)
        self.main.setStyleSheet("background: "+ mainBG + "; border-radius: 10px")

        self.main.setFixedSize(400,240)

        #print(bgRGB)
        #self.setPalette()
        #rbg(c.red(), c.green(),c.blue())

        self.logo = QLabel(self.main)
        self.logoPix = QPixmap(sys.modules['basedir']+'/ui/logo_128.svg')
        self.logo.setPixmap(self.logoPix)
        self.logo.setFixedSize(128,128)

        self.ver = QLabel(self.main)
        self.setCenter(self.ver)
        self.ver.setText(__main__.ver)

        self.authors = QLabel(self.main)
        self.setCenter(self.authors)
        self.authors.setText('''Author <b>Manzhelievsky Alexey</b> (<a href="http://sentihell.com/">sentihell.com</a>)''')

        self.authors.setOpenExternalLinks(True)

        self.background.mousePressEvent = lambda e: self.pressBG(1)
        self.main.mousePressEvent = lambda e: self.pressBG(2)
        self.show()
        self.res()
    def pressBG(self, e):
        if e == 1:
            self.close()
    def boundText(self, qlabel):
        label = self.cleanhtml(qlabel.text())
        metrics = QFontMetrics(self.font())
        width = metrics.boundingRect(label).width()
        #width = metrics.boundingRect(label.text())#boundingRect(label.text()).width()
        #print(width)
        height = metrics.boundingRect(label).height()
        return QSize(width, height)
    def res(self):
        self.mainGeom = sys.modules['m'].geometry()
        self.setFixedSize(self.mainGeom.width(), self.mainGeom.height())
        self.background.setFixedSize(self.mainGeom.width(), self.mainGeom.height())

        self.main.move((self.width()/2)-(self.main.width()/2), (self.height()/2)-(self.main.height()/2))

        self.logo.move((self.main.width()-self.logo.width())/2, 15)

        self.ver.move((self.main.width()-self.ver.width())/2, 145)



        self.authors.move((self.main.size().width()/2) - (self.boundText(self.authors).width()/2), 190)
    def setCenter(self, o):
        o.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        o.setAlignment(Qt.AlignCenter)

    def cleanhtml(self, raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext