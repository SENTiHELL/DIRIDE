from PyQt5.QtWidgets import QWidget
import os

class mod(QWidget):  #Only this name class for working
    mtp_dir = ''
    p = 'papka'
    def __init__(self, parent=None):
        super(mod, self).__init__(parent)
        self.mtp_dir = '/run/user/'+str(os.getuid())+'/gvfs/mtp.py:host='
        return
    def decode(self, dir):
        dir = dir.replace('mtp.py:/', self.mtp_dir)
        return dir
    def encode(self, dir):
        dir = dir.replace(self.mtp_dir, 'mtp.py:/')
        return dir
    def panel(self):
        pass