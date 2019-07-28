from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.QtCore import  Qt, QRect
from PyQt5.QtGui import QPainter, QFont, QColor, QPen, QIcon, QCursor
import sys


class menuitem:
    name = None
    path = None
    icon = None
    press = None
    icon_press = None

class indexitem:
    name = None
    call = None

class menu(QWidget):
    mouse = [-1, -1]

    line = -1
    clicked = None

    draw_object = []

    index = {} #local database buttons
    items = []
    def __init__(self, parent=None):
        super(menu, self).__init__(parent)
        self.setMouseTracking(True)
        self.setFixedSize(200, 300)



    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()

    def mouseMoveEvent(self, QMouseEvent):
        self.mouse = [QMouseEvent.x(), QMouseEvent.y()]
        self.update()

        n = self.collision()
        if n:
            self.setCursor(Qt.PointingHandCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

    def leaveEvent(self, event):
        self.mouse = [-1,-1]
        self.update()

    def mousePressEvent(self, QMouseEvent):
        n = self.collision()
        if n:
            self.index[n].call()

            #self.index[n]['press']()
    def collision(self):
        for e in self.draw_object:
            if e['x'] > self.mouse[0] - e['w'] and e['x'] < self.mouse[0]:
                if e['y'] > self.mouse[1] - e['h'] and e['y'] < self.mouse[1]:
                    return e['target']



    def add_collision(self, x, y, w, h, target):
        self.draw_object.append({'x': x, 'y': y, 'w': w, 'h':h, 'target': target})

    def func(self):
        print('plivet')

    def drawWidget(self, qp):
        pen = QPen(QColor(220, 220, 220), 1,
                   Qt.SolidLine)

        for e in range(len(self.items)):
            m = 10
            h = 20
            p = 4

            qp.setPen(Qt.NoPen)
            qp.setBrush(Qt.NoBrush)

            hb = m+(h+p)*e
            if hb > self.mouse[1]-h and hb < self.mouse[1]:
                qp.setBrush(Qt.black)
                self.line = int(hb/(h+p))

            qp.setOpacity(.2)
            qp.drawRect(m, hb-2, 180, h+4)

            qp.setOpacity(1)
            self.add_collision(m+40, hb, 140, h,'btn'+str(e))

            item = indexitem()
            item.name = 'btn'+str(e)
            item.call = self.items[e].press

            self.index['btn'+str(e)] = item #Database

            #qp.setBrush(Qt.black)
            #qp.drawRect(20, hb, 20, h)


            #ВРЕМЕННАЯ
            ico = self.items[e].icon
            if ico:
                icon = QIcon().fromTheme(ico)
            else:
                icon = QIcon().fromTheme("window-close")

            pix = icon.pixmap(20, 20)
            qp.drawPixmap(QRect(15, hb, 20, 20), pix)

            #print(img)
            #qp.drawPixmap(icon.pixmap)


            item = indexitem()
            item.name = 'subbtn' + str(e)
            item.call = self.items[e].icon_press
            self.index['subbtn'+str(e)] = item  # Database
            self.add_collision(15, hb, 20, 20, 'subbtn' + str(e))


            qp.setPen(pen)
            font = QFont()
            font.setBold(True)
            qp.setFont(font)
            qp.drawText(30+m+p,((m*2+(h/3))+(h+p)*e)-1, self.items[e].name)

    def add(self, menuitem):
        self.items.append(menuitem)
    def clear(self):
        self.items = []
    def remove(self, Name=None):
        #Does not work
        if Name == None:
            return

