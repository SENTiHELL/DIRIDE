#!/bin/python

import sys, os
from PyQt5.QtWidgets import QMainWindow, QWidget, QLineEdit, QPushButton, QHBoxLayout, QStyleFactory
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QResizeEvent, QIcon, QValidator

from scr import explore, leftPanel
from scr.history import history
from scr.module import module
from scr.hotkey import hotkey, initKey

from pprint import pprint

from scr.about import about

class qt_gui(QMainWindow):
    programName = None

    windowfocus = True

    callbackResize = []
    def __init__(self):
        super().__init__()

        self.initUI()
        ###
    def keybind_load(self):
        self.hotkey.load()
        self.hotkey.update()
        #self.hotkey.createConfig()
    def setProgramName(self, name):
        self.setWindowTitle(name)
    def initUI(self):
        self.setGeometry(300, 300, 815, 525)

        fixedSize = QSize(360,240)

        #self.setMaximumSize(fixedSize)
        #self.setMinimumSize(fixedSize)

        self.setWindowIcon(QIcon(sys.modules['basedir']+'/ui/dirride.png'))

        self.module = module()

        #GLOBAL LINK
        sys.modules['m'] = self

        #self.setWindowFlags(Qt.CustomizeWindowHint)
        self.main = QWidget(self)
        #self.main.setStyleSheet("background: gray")

        self.history = history()

        self.menu()
        self.addressbar()
        self.filewindow()
        self.leftPanel()#Only last
        self.show()
        self.setFocusPolicy(Qt.StrongFocus)

        self.resizeEvent(QResizeEvent) #Fix geometry on start app

        self.hotkey = hotkey()

        timer = QTimer(self)
        timer.setSingleShot(True)
        timer.timeout.connect(self.keybind_load)
        timer.start(0)

    def addressbar(self):

        self.addrborder = QWidget(self)
        hbox = QHBoxLayout(self.addrborder)
        hbox.setSpacing(0)

        self.loader = QWidget(self.addrborder)
        self.address = QLineEdit(self.addrborder)

        fact = QStyleFactory.create("Fusion")
        self.address.setStyle(fact)

        self.btn_undo = QPushButton(self.addrborder)
        self.btn_redo = QPushButton(self.addrborder)
        self.btn_back = QPushButton(self.addrborder)

        self.btn_undo.setText('<')
        self.btn_redo.setText('>')
        self.btn_undo.setFixedSize(28,25)
        self.btn_redo.setFixedSize(28,25)
        self.btn_back.setFixedSize(28,25)
        self.address.setFixedHeight(25)

        self.btn_back.setStyleSheet("background: red")
        self.btn_back.setText('..')
        self.btn_undo.pressed.connect(self.undo_btn_event)
        self.btn_redo.pressed.connect(self.redo_btn_event)
        self.btn_back.pressed.connect(self.back_btn_event)

        #self.address.move(3,3)
        hbox.addWidget(self.btn_undo)
        hbox.addWidget(self.btn_redo)
        hbox.addWidget(self.btn_back)
        hbox.addWidget(self.address)

        self.loader.setStyleSheet("background: rgba(100,20,155,.5)")

        self.address.returnPressed.connect(self.address_key_enter)



    def setAddr(self, address):
        self.address.setText(address)
    def address_key_enter(self):
        normalPath = os.path.normpath(self.address.text())
        self.fw.setDir(normalPath)
        self.history.set(normalPath, 0)
    def filewindow(self):
        self.fw = explore.explore(self.main)

        home = os.path.expanduser('~')
        if  len(sys.argv) > 1:
            dir =  sys.argv[1]
        else:
            dir = home
        self.fw.setDir(dir)
        self.history.set(dir, self.fw.scroll_pos)

        self.fw.setFocus()


    def leftPanel(self):
        self.lPaenl = QWidget(self.main)
        self.lPaenl.move(0, 20)
        self.lPaenl.setStyleSheet('background: #222222')
        self.lp = leftPanel.leftPanel(self.lPaenl)

    def menu(self):
        self.bar = self.menuBar()

        self.bar.setNativeMenuBar(False)

        file = self.bar.addMenu("File")

        for i in ['New Tab', 'Create Folder', 'Preferenses', 'Exit']:
            p = file.addAction(i)
            p.value = i
            p.triggered.connect(self.menu_button)

        edit = self.bar.addMenu("Edit")
        for i in ['Undo', 'Redo', 'Paste', 'Cut', 'Paste', 'Move', 'Rename']:
            p = edit.addAction(i)
            p.value = i
            p.triggered.connect(self.menu_button)

        help = self.bar.addMenu("Bookmarks")

        help = self.bar.addMenu("help")
        for i in ['About', 'Donate', 'All Topics']:
            p = help.addAction(i)
            p.value = i
            p.triggered.connect(self.menu_button)

    def menu_button(self):
        name = self.sender().value

        mn = {
            'About': lambda: about(self),
            'Exit': sys.exit
        }
        self.e = mn[name]()

        #try:
        #    self.e = mn[name]()
        #except:
        #    print('"'+name + '" not correcty or not exist function or errors on widget')
    def resizeEvent(self, QResizeEvent):
        for e in self.callbackResize:
            e()

        widget = self.geometry()

        self.main.setFixedSize(widget.width(), widget.height())


        self.lPaenl.setFixedSize(200,widget.height())
        self.lp.setFixedSize(self.lPaenl.size())

        self.addrborder.setGeometry(self.lPaenl.width(),
                                    self.bar.geometry().height(),
                                    (self.width() - (self.lPaenl.geometry().x() + self.lPaenl.geometry().width())),
                                    40)

        """
        self.btn_back.move(3,3)
        self.address.setFixedWidth(self.addrborder.width()- 9 - self.btn_back.width())
        self.address.move(self.btn_back.x() + self.btn_back.width() + 3, 3)
        self.address.setStyleSheet('background')
        """


        #self.loader.setGeometry(self.address.geometry())



        self.fw.move(self.lPaenl.geometry().x() + self.lPaenl.geometry().width(),
                     self.addrborder.geometry().y() + self.addrborder.geometry().height())
        self.fw.setSize(self.main.width() - self.lPaenl.geometry().width(),
                        self.size().height() - self.addrborder.geometry().height())

    def setLoadPercent(self, perc):
        self.loader.setFixedWidth(self.addrborder.width() / 100 * perc)
        self.loader.setFixedHeight(self.addrborder.size().height())
        self.loader.show()
    def hideLoader(self):
        self.loader.hide()

    def redo_btn_event(self):
        self.fw.redo()
    def undo_btn_event(self):
        self.fw.undo()
    def back_btn_event(self):
        addr = self.address.text().split("/")
        del addr[-1]
        redir = "/".join(addr)

        if len(redir):
            self.fw.setDir(redir)
            self.history.set(redir, self.fw.scroll_pos)
        else:
            self.fw.setDir('/')
            self.history.set('/', 0)

