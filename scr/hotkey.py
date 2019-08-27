import configparser, os



from pprint import pprint

class initKey:
    func = None
    key = None
"""
key['undo'].func = lambda: sys.modules['m'].main.undo()
"""

from PyQt5.QtWidgets import QShortcut
from PyQt5.QtGui import QKeySequence
import sys, __main__
class hotkey:
    db = {}
    actives = [] #hotkey.activated arrays

    name = None
    lock = None

    restore_hk = []

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
                if not self.lock:
                    shortcut = QShortcut(QKeySequence(o.key.replace(" ", "")), main)
                    self.actives.append(shortcut)

                    shortcut.activated.connect(o.func)

    def reassing(self, key, callback):
        main = sys.modules['m']  # main class
        key = key.replace(" ", "")

        for act in range(len(self.actives)):
            if key.lower() == self.actives[act].key().toString().lower():
                k = key.lower()
                self.restore_hk.append( [k, self.getHotKey(self, k)] )
                #print(self.restore_hk)
                self.actives[act].activated.disconnect()
                self.actives[act].activated.connect(callback)
                break

    def getHotKey(self, skey):
        for e in self.db:
            o = self.db[e]
            if o.key == skey.lower():
                return o.func


    def restore(self):
        for e in self.restore_hk:
            for act in range(len(self.actives)):
                if e[0] == self.actives[act].key().toString().lower():
                    self.actives[act].activated.disconnect()
                    self.actives[act].activated.connect(e[1])
        #print(self.restore_hk)
        self.restore_hk = []

    def list(self):
        return self.db
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