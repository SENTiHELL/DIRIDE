
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QIcon, QPainter, QColor, QFont, QPixmap, QPainterPath, QFontMetrics
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QRect, QRectF


"""
БРИФИНГ
ТЕКСТ СЪЕЖАЕТ В ЛЕВЕЕ
РАЗБИВКА ТЕКСТА НЕ КОРРЕКТНО

"""
class object_file(QWidget):
    size = QSize(100,100)
    iconSize = QSize(64, 64)
    rowPos = 40#percent

    value = date = ''

    opacity = .5
    mouseHover = pyqtSignal()
    clicked = pyqtSignal()

    select = None
    hover = None
    selectBtn = None

    btn_update = False

    last_time_edit = 0

    def __init__(self, parent=None):
        super(object_file, self).__init__(parent)
        self.main = QWidget(self)
        self.main.setStyleSheet('background: rgba(0,0,0,0)')

        self.icon = QLabel(self.main)
        self.text = QLabel(self.main)
        #self.icon.setStyleSheet('background: green')
        self.hide()
    def init(self):

        #self.text.setFixedSize(self.size.width(), self.size.height() / 100 * self.rowPos)

        #self.text.setFixedWidth(self.size.width())
        self.text.setWordWrap(True)
        self.text.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        self.text.setObjectName('text')

        self.iconPix = QPixmap(self.size.width(), self.iconSize.width())

        #self.text.move(self.size.width()/2 - self.text.width()/2, self.icon.height())

        self.show()
        self.btn_update = True
        self.setMouseTracking(True)
        #self.main.setMouseTracking(True)

        self.main.mouseMoveEvent = self.mouseMoveEvent
    def mouseMoveEvent(self, QMouseEvent):
        #print('de')
        super(object_file, self).mouseMoveEvent(QMouseEvent)
    def paintEvent(self, event):
        if self.btn_update:

            qp = QPainter()
            self.iconPix.fill(Qt.transparent)
            qp.begin(self.iconPix)
            self.text.setStyleSheet("#text { background: none; } ")
            self.text.setStyleSheet("#text { background: rgba(255,150,100, 0); text-align: center; border-radius: 5px;} ")
            if self.select:
                qp.setOpacity(.2)
                qp.setPen(Qt.NoPen)
                qp.setBrush(QColor(200, 0, 0))
                #qp.drawRect(0,0, self.width(), self.height())

                path = QPainterPath()
                path.addRoundedRect(QRectF(self.width()/2-self.iconSize.width()/2,
                                           0,
                                           self.width()/2+5,
                                           self.height()/2+5
                                           ), 10, 10)
                qp.drawPath(path)
                self.text.setStyleSheet("#text { background: rgba(255,150,100, 0.5); text-align: center; border-radius: 5px;} ")
            qp.setOpacity(self.opacity)

            self.drawIcon(event, qp)



            self.icon.setPixmap(self.iconPix)

            qp.end()
            self.btn_update = False
    def drawIcon(self, event, qp):
        #qp.setFont(QFont('Decorative', 10))

        qp.drawPixmap(QRect(self.width()/2-self.iconSize.width()/2,
                            0,
                            self.iconSize.width(),
                            self.iconSize.height()),
                      self.icon_ft)

    def setIconFromTheme(self, name):
        self.icon_ft = QIcon.fromTheme(name).pixmap(QSize(64, 64))
        self.btn_update = True
        self.update()
    def setIcon(self, icon):
        self.icon_ft = icon.pixmap(QSize(64, 64))
    def setText(self, txt):


        #ОЧЕНЬ КРИВО
        self.text.setText(self.getTextSplit(txt))
        QF = QFont()
        QFM = QFontMetrics(QF)
        bound = QFM.boundingRect(0,0, 64, 300, Qt.TextWordWrap | Qt.AlignCenter,self.getTextSplit(txt))

        self.text.move(self.size.width()/2 - (bound.width()+15)/2, self.icon.height())
        if bound.size().width() > 100:
            self.text.setFixedSize(100, bound.size().height()+2)
        else:
            self.text.setFixedSize(bound.size().width()+15, bound.size().height()+2)


        #print(bound.width())
    def setFileSize(self, *size):
        self.size = QSize(*size)
        self.main.setFixedSize(*size)
        self.icon.setFixedSize(self.size.width(), self.size.height() / 100 * (100 - self.rowPos))
        #self.text.setFixedSize(self.size.width(), self.size.height() / 100 * self.rowPos)

        #self.icon.move((self.icon.width()/2) - (self.iconSize.width() / 2), 0)
    def enterEvent(self, event):
        self.hover = True
        self.mouseHover.emit()
        self.opacity = 1
        self.btn_update = True
        self.update()

    def leaveEvent(self, event):
        self.hover = False
        self.mouseHover.emit()
        self.opacity = 0.5
        self.btn_update = True

        self.update()
    #def mouseMoveEvent(self, QMouseEvent):

    def selected(self):

        self.select = True
        self.update()
    def unselected(self):

        self.select = None
        try:
            self.update()
        except:
            pass
    def mouseReleaseEvent(self, event):
        self.target = 'None'
        gcoord = event.globalPos()
        lcoord = event.pos()

        leftPad = self.icon.geometry().x()
        rightPad = self.icon.geometry().width() - self.icon.geometry().x()
        topPad = (self.icon.height() / 2 - self.iconSize.height() / 2)

        if lcoord.x() > leftPad and lcoord.x() < rightPad and \
            lcoord.y() > topPad and lcoord.y() < topPad+self.iconSize.height():
                self.target = 'icon'

        if lcoord.y() > self.text.y():
            self.target = 'text'

        self.globalPos = gcoord
        self.type = event.button()
        self.clicked.emit()

        self.btn_update = True

        self.update()
        self.parent().mouseReleaseEvent(event)

    def getTextSplit(self, text):
        #НЕ КОРРЕКТНО
        mw = self.size.width()-20

        def width(t):
            return self.text.fontMetrics().boundingRect(t).width()
        #Array words by space
        spl = text.split(' ') #Разбивка по пробелам



        group = ''

        for item in spl:
            if width(item) > mw:
                i = 0
                w = 0  #Проверка длины для новой строки
                letter = ''

                while True:
                    w = w + width(item[i])

                    if w > mw:
                        w = 0
                        letter += ' ' + item[i]
                    elif (item[i] == '-' or item[i] == '_') and w > mw/2:
                        w = 0
                        letter += item[i] + ' '
                    else:
                        letter += item[i]


                    i = i + 1
                    if i == len(item):
                        break

                group += letter + ' '
            else:
                group += item + ' '

        return group

    def unset(self):
        try:
            self.deleteLater()
        except:
            pass