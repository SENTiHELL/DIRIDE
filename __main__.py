#!/bin/python
import os, sys
from scr import qt_gui, hotkey

programName='Dirride'
ver='0.0.2a'

from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QFrame,
    QSplitter, QStyleFactory, QApplication)


def program():
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)

    main = qt_gui.qt_gui()
    main.setProgramName(programName)
    sys.exit(app.exec_())


if __name__ == "__main__":
    realpath =  os.path.realpath(sys.argv[0])

    #fix dot directory
    if os.path.isdir(realpath):
        realpath = realpath + '/__main__.py'

    sys.modules['mainfile'] = realpath
    sys.modules['basedir'] = os.path.dirname(realpath)
 
    for i in sys.argv:
        if i == '--version':
            print(programName+' version: ' + ver)
            exit()

    program()
   