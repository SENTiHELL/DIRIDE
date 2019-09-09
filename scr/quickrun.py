import sys
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QFrame, QPushButton,QShortcut, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
import re

class qrun(QWidget):
    history_command = ['']
    key_history = 0
    def __init__(self, parent=None):
        super(qrun, self).__init__(parent)
        self.parent = parent


        self.init()
    def init(self):
        sys.modules['m'].callbackResize.append(self.res)
        self.hk = sys.modules['scr.hotkey'].hotkey


        self.m = sys.modules['m']
        self.main = QWidget(self.m)

        self.textInput = QLineEdit(self.main)
        self.textInput.setFrame(False)

        self.main.setStyleSheet("""
            
            background-color: rgba(0,0,0,.2)
            """)

        self.textInput.setStyleSheet("""
            background: #031224;
            color: white; 
            border-radius: 5px; 
            padding-left: 10px
            """)


        #Resize event




        #sys.modules['m'].mousePressEvent = self.MPE
        #self.mousePressEvent = self.MPE
        #self.main.mousePressEvent = self.MPE

        self.toggle()

    def res(self):
        self.exploreGeo = self.m.fw.geometry()

        w = self.parentWidget().window.width()
        h = self.parentWidget().scroll.height()
        #print(h)

        self.textInput.move(self.exploreGeo.x()+5, self.m.size().height()-self.textInput.size().height()-5)



        self.main.setFixedSize(sys.modules['m'].size())
        self.textInput.setFixedSize( w-25,40)

        #self.setGeometry(self.main.geometry())
        #self.move(5,h-45)

        self.main.mousePressEvent = self.MPE

    def MPE(self,e):
        self.toggle()

    def toggle(self):
        print("TOGGLE")
        main = sys.modules['m'] #main class
        print('de')


        if self.main.isHidden():
            self.main.show()
            self.textInput.setFocus()
            self.textInput.setText('')


            self.hk.lock = True
            self.hk.reassing(self.hk, 'enter', self.qr_press)
            self.hk.reassing(self.hk, 'return', self.qr_press)

            self.hk.reassing(self.hk, 'up', lambda: self.keyArrow('up'))
            self.hk.reassing(self.hk, 'down', lambda: self.keyArrow('down'))

            self.hk.reassing(self.hk, 'esc', lambda: self.toggle())
            """
            setkey('keyup', lambda: self.keyArrow('up'))
            setkey('keydown', lambda: self.keyArrow('down'))
            
            """
            print('LOCK')
        else:
            self.hk.lock = False
            self.main.hide()
            self.setFocus()
            self.hk.restore(self.hk)
            #self.hk.update(self.hk)


            print('unlock')
    def keyArrow(self, key):
        self.update()
        if key == 'down':
            self.key_history +=1
            if self.key_history > len(self.history_command)-1:
                self.key_history = 0

        elif key == 'up':
            self.key_history -=1
            if self.key_history <= 0:
                self.key_history = len(self.history_command)-1

        #print(self.key_history)
        self.textInput.setText(self.history_command[self.key_history])

    def qr_press(self):
        selectFile = sys.modules['explore'].selectFiles()

        sFile = ''.join([' "'+e+'"' for e in selectFile])

        text = self.textInput.text() + ' '
        text = re.sub(' @ ', ' '+sFile+' ', text)
        sys.modules['explore'].cmd_run(text)

        self.history_command.append(self.textInput.text())
        self.toggle()