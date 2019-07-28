from os.path import dirname, basename, isfile
import glob, importlib, sys
from PyQt5.QtWidgets import QWidget

class module(QWidget):
    mod_load = []
    def __init__(self):
        super().__init__()



        modules = glob.glob(dirname(__file__) + "/Module/*.py")
        self.fscr = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]
        for i in self.fscr:
            self.mod_load.append(importlib.import_module('scr.Module.' + i))
    """
    def dec(self, dir):
        for i in self.mod_load:
            scr = i.dirFilter()
            dir = scr.decode(dir)
        return dir
    def enc(self, dir):
        for i in self.mod_load:
            scr = i.dirFilter()
            dir = scr.encode(dir)
        return dir
"""
    def panel(self, parent=None):

        for i in self.mod_load:
            cls = i

            cls = cls.mod(self)
            cl = cls.panel()



"""
d = dirFilter()
w = d.enc('/run/user/1000/gvfs/mtp.py:host=Pegatron_Cintiq_Companion_Hybrid_13HD_2n21231hg000000vo0q0/anal/karnaval/')
f = d.dec(w)
print(f)
"""