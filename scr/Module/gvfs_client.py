import os

from gi.repository import Gio, GObject, GLib

from PyQt5.QtWidgets import QWidget, QLabel,QTreeWidget, QTreeWidgetItem, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import pyqtSlot

from scr.ui.menu import menu, menuitem

import os, sys



class mod(QWidget):
    p = 'papka'
    dir = '/'


    menu = None
    def __init__(self, parent):
        super(mod, self).__init__(parent)

        #super().__init__()
        self.parent = parent

        #self.init()
        #self.lp = sys.modules['scr.leftPanel']
        aa = QPushButton('ANAL')
        aa.clicked.connect(self.panel_button_clicked)
        aa.move(40,100)
        aa.show()
        self.init()
        pass

    #Тот кто еще не примонтирован
    def mount_done_cb(self, obj, res, user_data):
        # print(obj, res, user_data)
        # obj.mount_enclosing_volume_finish(res)


        obj.mount_finish(res)

        #self.select_current_path = obj.get_mount().get_root().get_path()
        # print('done.')
        # print(1, obj.get_name(), obj.get_uuid(), obj.get_mount(), obj.get_drive())

        #print(2, obj.get_mount().get_uuid())
        # print(3, obj.get_mount().get_default_location().get_path())
        print(4,obj.get_name() ,obj.get_mount().get_root().get_path())

        #self.dir = obj.get_mount().get_root().get_path()
        # print(5, obj.get_mount().get_volume())
        # print(6, obj.get_mount().get_drive())
        user_data.quit()

        #######################################################
        icon_names = obj.get_icon().get_names()
        icon = None
        for x in icon_names:
            if 'usb' not in x and 'symbolic' in x:
                icon = x

                break
        if icon == None:
            icon = icon_names[0]

        #print(obj.get_icon)
        self.changeAttrByName(obj.get_name(), 'path', obj.get_mount().get_root().get_path())
        self.changeAttrByName(obj.get_name(), 'uuid', obj.get_uuid())
        self.changeAttrByName(obj.get_name(), 'icon_name', icon)

        """
            self.listDrive.append({'name': volume.get_name(),
            'path': mount.get_default_location().get_path(),
            'uuid': volume.get_uuid(),
            'icon_name': icon })
        """


    #УЖе примонтирован
    def mounted_done_cb(self, obj, res, user_data):

        # print(obj, res, user_data)
        # obj.mount_enclosing_volume_finish(res)
        #print('aga')


        #obj.mount_finish(res)


#######
        # print('done.')
        # print(1, obj.get_name(), obj.get_uuid(), obj.get_mount(), obj.get_drive())

        #print(2, obj.get_mount().get_uuid())
        # print(3, obj.get_mount().get_default_location().get_path())
        print(4,obj.get_name(), obj.get_mount().get_root().get_path())
#####################
        #self.dir = obj.get_mount().get_root().get_path()
        # print(5, obj.get_mount().get_volume())
        # print(6, obj.get_mount().get_drive())
        user_data.quit()

    def init(self):

        mo = Gio.MountOperation()
        mo.set_anonymous(True)

        vm = Gio.VolumeMonitor.get()
        # print(dir(vm))
        # print(vm.get_mount_for_uuid(VOLUME_UUID))
        # print(vm.get_volume_for_uuid(VOLUME_UUID))
        """
        loop = GLib.MainLoop()
        found = False
   
        for v in vm.get_volumes():
            name = v.get_name()
            #print(name)
            print(v.get_path())
            if name == 'wblack':
                mount = v.get_mount()
                print('select:', mo)
                #print(name, v.get_uuid(), v.get_mount(), v.get_drive())
                if not mount:

                    v.mount(0, mo, None, self.mount_done_cb, loop)
                    # print(name, v.get_uuid(), v.get_mount(), v.get_drive())
                    found = True
            v.mount(0, mo, None, self.mounted_done_cb, loop)
        if found:
            loop.run()
        """


        ######################
        self.listDrive = []

        volume_monitor = Gio.VolumeMonitor.get()

        for volume in vm.get_volumes():
            mount = volume.get_mount()
            if mount is not None:
                #print(mount.get_default_location().get_path())


                #print('1', volume.get_drive().get_icon().get_names())

                icon_names = volume.get_drive().get_icon().get_names()

                icon = None

                for x in icon_names:
                    if 'usb' not in x and 'symbolic' in x:
                        icon = x

                        break
                if icon == None:
                    icon = icon_names[0]
                self.listDrive.append({'name': volume.get_name(),
                                       'path': mount.get_default_location().get_path(),
                                       'uuid': volume.get_uuid(),
                                       'icon_name': icon })

            else:
                #print(volume.get_name())

                self.listDrive.append({'name': volume.get_name(),
                                       'path': None,
                                       'uuid': volume.get_uuid(),
                                       'icon_name': None})

        #paths = [volume.get_mount().get_default_location().get_path()
        #        for volume in vm.get_volumes() if volume.get_mount() is not None]
        #print(self.listDrive)

    def pressMenuLabel(self,e):
        print('dochlo!!!', e.path)

        sys.modules['m'].address.setText(e.path)
        sys.modules['m'].address_key_enter()

    def pressMenuIcon(self, e):
        print('ICON!!!', e['name'])
        #self.changeAttrByName(e['name'], 'icon_name', 'preferences-system-time-symbolic')
        self.menu.update()

        mo = Gio.MountOperation()
        mo.set_anonymous(True)

        vm = Gio.VolumeMonitor.get()
        # print(dir(vm))
        # print(vm.get_mount_for_uuid(VOLUME_UUID))
        # print(vm.get_volume_for_uuid(VOLUME_UUID))

        loop = GLib.MainLoop()
        found = False

        for v in vm.get_volumes():
            name = v.get_name()
            #print(name)
            if name == e['name']:
                mount = v.get_mount()



                #print(name, v.get_uuid(), v.get_mount(), v.get_drive())
                if not mount:

                    v.mount(0, mo, None, self.mount_done_cb, loop)

                    # print(name, v.get_uuid(), v.get_mount(), v.get_drive())
                    found = True
            #v.mount(0, mo, None, self.mounted_done_cb, loop)
        if found:
            loop.run()



    def changeAttrByName(self, name, attr, value):
        for x in range(len(self.listDrive)):
            if name in self.listDrive[x]['name']:
                self.listDrive[x][attr] = value
                break
        self.panel_ui_build()
    def panel_ui_build(self):
        if self.menu is not None:
            self.menu.clear()

        i = 0
        for e in self.listDrive:
            item = menuitem()
            item.name = e['name']
            item.icon = e['icon_name']
            item.path = e['path']
            item.press = lambda e=item: self.pressMenuLabel(e)
            item.icon_press = lambda e=e: self.pressMenuIcon(e)
            self.menu.add(item)

            i = i + 1

    def panel(self):
        self.lPanel = sys.modules['m'].lPaenl
        self.lPanel.setStyleSheet("background: #333")

        self.menu = menu(self.lPanel)
        self.panel_ui_build()
        """
        self.b = QPushButton(e['name'], self)
        self.b.clicked.connect(lambda a, p=e['path']: self.panel_button_clicked(p))
        if e['path'] == None:
            self.b.setDisabled(True)
        self.button.append(self.b)
        """




        """
        self.vboxLayout = QVBoxLayout(self.lPanel)
        self.hboxLayout = QHBoxLayout()
        self.treeWidget = QTreeWidget()

        self.vboxLayout.addWidget(self.treeWidget)
        self.treeWidget.setHeaderLabel("Quick menu")

        self.topLevelItem = QTreeWidgetItem()
        self.topLevelButton = QLabel("MTP")


        self.button = []
        i=0
        for e in self.listDrive:
            self.b = QPushButton(e['name'], self)
            self.b.clicked.connect(lambda a, p=e['path']: self.panel_button_clicked(p))
            if e['path'] == None:
                self.b.setDisabled(True)
            self.button.append(self.b)

            i = i + 1

        self.childItems = []
        for i in range(len(self.listDrive)):
            self.childItems.append(QTreeWidgetItem())
            self.topLevelItem.addChild(self.childItems[i])
        self.childItems.append(QTreeWidgetItem())
        self.treeWidget.addTopLevelItem(self.topLevelItem)
        self.treeWidget.setItemWidget(self.topLevelItem, i, self.topLevelButton)
        self.treeWidget.expandAll()
        i=0
        for e in self.button:
            self.treeWidget.setItemWidget(self.childItems[i], 0, e)
            i = i + 1
            pass

        self.treeWidget.setItemWidget(self.childItems[4], 0 , button2)




        self.lPanel.setLayout(self.vboxLayout)
        self.lPanel.move(0, 35)

        """




    def panel_button_clicked(self, path):
        sys.modules['m'].address_key_enter()
        pass

