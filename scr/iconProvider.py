from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileIconProvider

class iconProvider(QFileIconProvider):
    def icon(self, fileInfo):
        if fileInfo.isDir():
            return QIcon("folder.png")
        return QFileIconProvider.icon(self, fileInfo)
