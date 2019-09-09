
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QIcon, QPainter, QColor, QFont, QPixmap, QPainterPath, QFontMetrics
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QRect, QRectF, QThread, QTimer, QEvent
import os
import textwrap
"""
БРИФИНГ
ТЕКСТ СЪЕЖАЕТ В ЛЕВЕЕ
РАЗБИВКА ТЕКСТА НЕ КОРРЕКТНО


----
Разработать предпросмотр jpg, png 
Class должен быть в треде

"""

class io_thumb(QThread):
    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.parent = parent
    def args(self, target, url):
        self.target = target
        self.url = url

    def run(self):
        """
        self.timeout = QTimer()
        self.timeout.setInterval(1000)
        self.timeout.setSingleShot(True)
        self.timeout.timeout.connect(self.push_thumb)
        self.timeout.start()
        """
        self.extension = os.path.splitext(self.url)[1]
        if self.extension == '.jpg' or self.extension == '.png' or self.extension == '.svg':
            print('IO thumb', self.target)
            pixmap = QPixmap(self.url)
            pixmap4 = pixmap.scaled(100, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            self.parent.icon_ft = pixmap4
            self.parent.update()

    def push_thumb(self):
        print('de')

class object_file(QWidget):
    size = QSize(100,100)
    iconSize = QSize(64, 64)
    rowPos = 40#percent

    value = date = ''

    opacity = .9
    mouseHover = pyqtSignal()
    clicked = pyqtSignal()

    select = None
    hover = None
    selectBtn = None

    btn_update = False

    last_time_edit = 0

    realfile = ''
    extension = ''
    sourceText = ''

    trigger = None
    def __init__(self, parent=None):
        super(object_file, self).__init__(parent)

        #временно для padding
        self.setFixedWidth(100)

        self.main = QWidget(self)
        self.main.setStyleSheet('background: rgba(0,0,0,0)')
        #print(self.realfile)
        self.icon = QLabel(self.main)
        self.text = QLabel(self.main)
        #self.icon.setStyleSheet('background: green')
        self.hide()
    def init(self):

        #self.text.setFixedSize(self.size.width(), self.size.height() / 100 * self.rowPos)

        self.text.setFixedWidth(self.size.width()-20)
        self.text.move(0, self.text.y()-6)
        self.text.setFixedHeight(self.size.height()*5)

        #self.text.setWordWrap(True)
        self.text.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        self.text.setObjectName('text')

        self.iconPix = QPixmap(self.size.width(), self.iconSize.height())

        #self.text.move(self.size.width()/2 - self.text.width()/2, self.icon.height())

        self.show()
        self.btn_update = True
        self.setMouseTracking(True)
        #self.main.setMouseTracking(True)

        self.main.mouseMoveEvent = self.mouseMoveEvent
        self.thumbnaizer()

    def thumbnaizer(self):
        """
        self.extension = os.path.splitext(self.realfile)[1]
        if self.extension == '.jpg' or self.extension == '.png' or self.extension == '.svg':
            pixmap = QPixmap(self.realfile)
            pixmap4 = pixmap.scaled(100, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            self.icon_ft = pixmap4
        """
        self.thumb_io = io_thumb(self)
        self.thumb_io.args(self.icon_ft, self.realfile)
        self.thumb_io.start()

    def mouseMoveEvent(self, QMouseEvent):
        #print('de')
        super(object_file, self).mouseMoveEvent(QMouseEvent)
    def paintEvent(self, event):
        if self.btn_update:

            qp = QPainter()
            self.iconPix.fill(Qt.transparent)
            qp.begin(self.iconPix)
            self.text.setStyleSheet("#text { background: none; } ")
            self.text.setStyleSheet("#text { background: rgba(155,150,100, 0); text-align: center; border-radius: 5px;} ")
            if self.select:
                qp.setOpacity(.1)
                qp.setPen(Qt.NoPen)
                self.text.setStyleSheet("#text { background: rgba(155,100,255, 0.5); text-align: center; border-radius: 5px;} ")
            qp.setOpacity(self.opacity)

            self.drawIcon(event, qp)



            self.icon.setPixmap(self.iconPix)

            qp.end()

            QF = QFont()
            QFM = QFontMetrics(QF)
            bound = QFM.boundingRect(0, 0, 100, 1000, Qt.TextWordWrap | Qt.AlignCenter, self.text.text())

            self.text.setFixedHeight(bound.height())
            self.btn_update = False
    def drawIcon(self, event, qp):
        #qp.setFont(QFont('Decorative', 10))
        #if self.extension == '.jpg' or self.extension == '.png':
        #else:


        self.icosize = self.icon_ft.size()

        qp.drawPixmap(QRect(self.width()/2-self.icosize.width()/2,
                            -5,
                            self.icosize.width(),
                            self.icosize.height()),
                      self.icon_ft)

    def setIconFromTheme(self, name):
        self.icon_ft = QIcon.fromTheme(name).pixmap(QSize(64, 64))
        self.btn_update = True
        self.update()
    def setIcon(self, icon):
        self.icon_ft = icon.pixmap(QSize(64, 64))
    def setText(self, txt):


        self.sourceText = self.getWordWrap(txt)

        self.text.setText(self.sourceText)

        QF = QFont()
        QFM = QFontMetrics(QF)
        elidedText = QFM.elidedText(self.sourceText, Qt.TextWordWrap | Qt.ElideRight, 50)
        self.text.setText(elidedText)
        #bound = QFM.boundingRect(0, 0, 64, 300, Qt.TextWordWrap | Qt.AlignCenter, self.getWordWrap(txt))

        self.text.move(0, self.icon.height())
        """
        if bound.size().width() > 100:
            self.text.setFixedSize(100, bound.size().height()+2)
        else:
            self.text.setFixedSize(bound.size().width()+15, bound.size().height()+2)
        """

        #print(bound.width())
        self.leaveEvent(None)
        self.update()
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

        self.text.setText(self.sourceText)

        QF = QFont()
        QFM = QFontMetrics(QF)
        bound = QFM.boundingRect(0, 0, 100, 0, Qt.TextWordWrap | Qt.AlignCenter, self.text.text())


        self.setFixedHeight(80 + bound.height())
        self.main.setFixedHeight(self.height()-5)
        self.text.setFixedHeight(bound.height())

        #self.setFixedHeight(320)
        self.raise_()

        self.update()
        self.triggering()

    def leaveEvent(self, event):

        self.hover = False
        self.mouseHover.emit()
        self.opacity = 0.9
        self.btn_update = True

        self.setFixedHeight(self.size.height())
        self.main.setFixedHeight(self.height())

        e = self.sourceText.split('\n')
        if len(e) > 3:
            self.text.setText('\n'.join(e[:3])+'\n...')

        self.update()


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
        topPad = 0#(self.icon.height() / 2 - self.iconSize.height() / 2)

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

    def getWordWrap(self, text):

        #РАЗДЕЛЯЮЩИЕ СИМВОЛЫ
        #   ! - / | ?

        mw = self.text.width()

        def width(t):
            return self.text.fontMetrics().boundingRect(t).width()

        #Разбивка текста по знакам
        def getSplit(text, symbols):
            arr = []
            let = ''
            for t in text:
                let += t
                if t in symbols:
                    arr.append(let)
                    let = ''
            arr.append(let)
            return arr

        spl = getSplit(text, ['!', '-', '/', '|', '?', ' ', '_']) #Разбивка по пробелам




        #BUILD
        self.group = ''
        self.f = ''

        #БУКВЫ
        def letSplit(text, st=0):
            start = st
            r = ''
            f = ''

            k=0
            while k < len(text):
                if width(r+text[k]) < (mw-5)-start:
                    r += text[k]

                else:
                    f += r + text[k] + '\n'
                    start = 0
                    r = ''
                k += 1

            f += r

            return f

        #СЛОВА
        i=0
        while i < len(spl):
            t = spl[i]
            i+=1
            #слова не дописываются
            if width(self.group + t) < mw:
                self.group += t
            else:
                #ЗДЕСЬ РАЗБИВКА ДЛИННОГО СЛОВА
                if width(t) > mw:
                    if not self.group:
                        self.group += letSplit(t)
                    else:
                        self.group += '\n' + letSplit(t)

                self.f += self.group
                #############################
                last_line = self.group.split("\n")[-1]
                #############################
                if width(last_line + t) > mw/2:
                    self.group = '\n' + t
                else:
                    self.group = '' + t
        self.f += self.group

        return self.f


    def unset(self):
        try:
            self.deleteLater()
        except:
            pass

    def setTrigger(self, signal):
        print('sign', signal)
        self.trigger = signal
    def triggering(self):
        if self.trigger:
            self.trigger()(self) #Send this button link
