from PyQt5.QtWidgets import QWidget
class mod(QWidget): #название класса не долежн быть другим
    p = 'pkaa'

    def __init__(self, parent=None):
        super(mod, self).__init__(parent)
        return
    def decode(self, dir):
        #dir = dir + 'SMB FILTERED'
        return dir
    def encode(self, dir):
        #dir = dir + 'SMB FILTERED'
        return dir

    def panel(self):
        pass