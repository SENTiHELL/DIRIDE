import configparser, os



from pprint import pprint

class initKey:
    func = None
    key = None
"""
key['undo'].func = lambda: sys.modules['m'].main.undo()
"""

from PyQt5.QtWidgets import QMainWindow, QWidget, QShortcut
from PyQt5.QtGui import QKeySequence
import sys, __main__
class hotkey:
    db = {}
    name = None

    section = "Keyboard settings"
    def __init__(self):
        self.config_path = sys.modules['basedir']+'/config/settings.ini'
        self.config = self.__get_config()

    def setInitName(self, name=None):
        self.name = name
    def add(self, hk):
        if not self.name:
            print('error: no set init name for keymap')
            return

        if type(hk) == initKey:
            self.db[self.name] = hk
        else:
            print('Initkey not correcty')
    def remove(self, name):
        del db[self.name]
    def load(self):
        read = self.config.options(self.section)
        for e in read:
            try:
                self.db[e].key = str(self.__readConfig(e))
            except:
                print('Error: No correct key bind string in config/settings.ini')
    def update(self):
        main = sys.modules['m'] #main class


        for e in self.db:
            o = self.db[e]
            #print(o.func)
            if o.key:
                shortcut = QShortcut(QKeySequence(o.key.replace(" ", "")), main)
                shortcut.activated.connect(o.func)
    def list(self):
        for e in self.db:
            print('list', self.db[e].func)

    ######################################################
    #PRIVATE
    ######################################################
    def createConfig(self):
        "Create a config file"
        config = configparser.ConfigParser()

        config.add_section(self.section)
        for e in self.db:
            config.set(self.section, e, str(self.db[e].key))
        #print(__file__)
        with open(self.config_path, "w") as e: config.write(e)

    def __get_config(self):
        "Returns the config object"

        config = configparser.ConfigParser()

        config.read(self.config_path)

        return config

    def __readConfig(self, setting):

        value = self.config.get(self.section, setting)
        """
        msg = "{section} {setting} is {value}".format(
            section=section, setting=setting, value=value
        )
        """
        return value