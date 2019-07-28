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
    sys.modules['mainfile'] = os.path.realpath(sys.argv[0])
    sys.modules['basedir'] = os.path.dirname(os.path.realpath(sys.argv[0]))

    for i in sys.argv:
        if i == '--version':
            print(programName+' version: ' + ver)
            exit()
    if toolkit == "QT":
        program()