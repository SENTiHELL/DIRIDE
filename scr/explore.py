import os, sys

from PyQt5.QtWidgets import QWidget, QLabel, QScrollArea, QFileIconProvider,QMenu,QWidgetAction, QLineEdit, QFrame
from PyQt5.QtCore import QTimer, QFileInfo, QPoint,  QMimeData, QUrl, Qt, QProcess
from PyQt5.QtGui import QIcon, QDrag, QKeySequence, QMouseEvent

from scr.core import core
from scr.hotkey import initKey

from scr.fileButton import object_file
from scr.iconProvider import iconProvider

from pprint import pprint

class explore(QWidget):
    files = None
    icon_size = 120
    hidden = False

    maxWidth = 1200

    scroll_pos_old = 0
    scroll_pos = 0

    btns = []
    targetType = None

    mouse = [0,0]
    collized = []

    #Print with hotkey
    keyPrint = None
    def __init__(self, parent=None):
        super(explore, self).__init__(parent)
        self.parent = parent
        self.setAcceptDrops(True)

        self.init()
    def prent(self):
        print('daaa')
    def init(self):
        self.core = core()
        self.keyPrint = lambda: (print(self.btns),
                                 print(len(self.btns),
                                 print('f:', self.files)))


        self.history = self.parent.parent().history
        self.scroll = QScrollArea(self)

        self.window = QWidget(self)
        self.window.setAcceptDrops(True)


        self.scroll.setWidget(self.window)


        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.scroll.verticalScrollBar().valueChanged.connect(self.wh_change)

        self.scroll.wheelEvent = self.wh

        #self.mousePressEvent = self.mousePressed

        #self.mods = self.parent.parent().module


        hk = sys.modules['scr.hotkey'].hotkey

        hk.setInitName(hk, 'redo')
        key = initKey()
        key.func = lambda: self.redo()
        hk.add(hk, key)

        hk.setInitName(hk, 'undo')
        key = initKey()
        key.func = lambda: self.undo()
        hk.add(hk, key)

        hk.setInitName(hk, 'selectall')
        key = initKey()
        key.func = lambda: self.selectAll()
        hk.add(hk, key)

        hk.setInitName(hk, 'deselectall')
        key = initKey()
        key.func = lambda: self.unSelectAll()
        hk.add(hk, key)



    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == 96:
            self.keyPrint()
    def mousePressed(self, e):
        #Надо пофиксить, глючит координация меню
        self.globalPos = e.globalPos()
        #print(e.globalPos())


    def wh_change(self, e):
        #print(e, self.scroll_pos, self.targetType)
        if self.targetType == None:
            self.scroll_pos = self.scroll_pos_old = e
    def wh(self, e):
        self.targetType = 'wheel'
        self.scroll_pos = self.scroll_pos - e.angleDelta().y()

        self.ani()
    def ani(self):

        self.anitimer = QTimer()
        self.anitimer.setInterval(1000/60)
        self.anitimer.timeout.connect(self.ani_func)
        self.anitimer.start()
        pass
    def ani_func(self):

        self.scroll_pos_old = self.scroll_pos_old - ( (self.scroll_pos_old - self.scroll_pos) / 5 )

        self.scroll.verticalScrollBar().setValue(self.scroll_pos_old)



        #MAX SCROLL LIMIT
        max = self.window.height() - self.scroll.height()
        if self.scroll_pos_old > max:
            self.scroll_pos = self.scroll_pos_old = max
            self.anitimer.stop()
            self.anitimer.deleteLater()
        if self.scroll_pos_old < 0:
            self.scroll_pos = self.scroll_pos_old = 0
            self.anitimer.stop()
            self.anitimer.deleteLater()

        if int(self.scroll_pos_old) == int(self.scroll_pos)-1:
            self.targetType = None
            self.anitimer.stop()
            self.anitimer.deleteLater()

    def setSize(self, *size):
        h,v = size

        self.window.setFixedWidth(h)

        self.setFixedSize(*size)
        self.scroll.setFixedSize(h, v-20)

        self.maxWidth = int(self.width() / self.icon_size) * self.icon_size
        self.reposition()

    def run_c(self, command):
        """Executes a system command."""

    def lm_cmd(self):
        cmd = self.lb.text() + ' ' + "'" + self.selectFile + "'"
        self.cmd_run(cmd)

    def rm_cmd(self):
        cmd = self.lb.text()
        self.cmd_run(cmd)

    def cmd_run(self, command):
        print(command)

        #subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        pros = QProcess(self)
        pros.finished.connect(self.proc_finish)

        str = "/bin/sh -c \""+command+"\""

        pros.start(str)
        self.mousemenu.close()

        #self.scroll.verticalScrollBar().setValue = self.scroll_pos
        #update

        pass
    def proc_finish(self):
        self.refresh()
    def lm_menu(self):
        self.mousemenu = QMenu(self)
        act = QWidgetAction(self)

        self.menuMain = QWidget(self)
        self.menuMain.setStyleSheet('background: #111')

        self.lb = QLineEdit(self.menuMain)
        self.lb.move(3, 3)
        self.lb.setFixedSize(194, 20)
        self.lb.setPlaceholderText('cmd')
        self.lb.setStyleSheet('background: white')


        self.lb.returnPressed.connect(self.lm_cmd)

        self.menuMain.setFixedSize(200, 100)
        act.setDefaultWidget(self.menuMain)
        self.mousemenu.addAction(act)
        self.mousemenu.exec_(self.globalPos)

    def contextMenuEvent(self, event):
        self.mousemenu = QMenu(self)
        act = QWidgetAction(self)

        self.menuSecond = QWidget(self)
        self.menuSecond.setStyleSheet('background: #511')

        self.lb = QLineEdit(self.menuSecond)
        self.lb.move(3, 3)
        self.lb.setFixedSize(194, 20)
        self.lb.setPlaceholderText('cmd')
        self.lb.setStyleSheet('background: white')

        self.lb.returnPressed.connect(self.rm_cmd)

        self.menuSecond.setFixedSize(200, 100)
        act.setDefaultWidget(self.menuSecond)
        self.mousemenu.addAction(act)
        self.mousemenu.exec_(self.globalPos)
    def btnsClear(self):
        if len(self.btns):
            for i in self.btns:
                i.deleteLater()
                del i
            del self.btns[:]
    def setDir(self, dir):
        dir = dir.replace("//", "/")


        #dir_enc = self.dFilter.enc(dir)
        #dir_dec = self.dFilter.dec(dir_enc)

        if os.path.isdir(dir) != True:

            if self.selectBtn.select != True:
                self.selectBtn.select = True
            return

        self.btnsClear()

        self.current_dir = dir.replace("//", "/")

        self.core.sort = 'abs123'

        self.files = self.core.read_dir(self.current_dir)


        #FILTER DIR
        self.parent.parent().address.setText(dir)


        os.chdir(dir)

        #self.history.set(self.current_dir)

        self.cycle = self.tmpL = 0
        self.asyncRender()

        self.refreshtime = QTimer()
        self.refreshtime.timeout.connect(self.refresh)
        self.refreshtime.start(1000)
    def redo(self):
        link = self.history.get(1)
        if link != None:
            self.setDir(link[1])
    def undo(self):
        link = self.history.get(-1)
        if link != None:
            self.setDir(link[1])
    def selectAll(self):
        #selectOn = next((x for x in self.btns if x.select == True), None)
        selectOn = [x for x in self.btns if x.select == True]

        if not len(selectOn) == len(self.btns):
            for b in self.btns:
                b.selected()
                b.leaveEvent(QMouseEvent)
        else:
            for b in self.btns:
                b.unselected()
                b.leaveEvent(QMouseEvent)
    def unSelectAll(self):



        for b in self.btns:
            b.unselected()
            b.leaveEvent(QMouseEvent)
    def asyncRender(self):

        self.renderTime = QTimer()
        self.renderTime.timeout.connect(self.render)
        self.renderTime.start(1000/60)

    def getTextSplit(self, text):
        def width(t):
            return label.fontMetrics().boundingRect(t).width()
        label = QLabel()
        mw = self.icon_size - 15
        spl = text.split(' ')

        group = ''
        for item in spl:
            if width(item) > mw:
                i = 0
                w = 0
                letter = ''
                while True:
                    w = w + width(item[i])
                    if w > mw:
                        w = 0
                        letter += ' ' + item[i]
                    elif item[i] == '-':
                        w = 0
                        letter += item[i] + ' '
                    else:
                        letter += item[i]


                    i = i + 1
                    if i == len(item):
                        break

                group += letter + ' '
            else:
                group += item + ' '
        return group

    def rebuild(self):
        btns_rebuild = []
        for f in self.btns:
            try:
                f.move(1, 1)
                btns_rebuild.append(f)
            except:
                pass
        self.btns = btns_rebuild
    def reposition(self):
        if self.btns == None:
            self.btns = []
        self.rebuild()
            #if f.value not in self.files:
            #    print(f.value)
                #self.create_button(f.value)
                #123
        i=0
        l=0


        for f in self.btns:

            count_hoz = int(self.maxWidth / self.icon_size)
            x = (self.icon_size * i) % self.maxWidth
            y = self.icon_size * l
            try:
                f.move(x, y)
            except:
                print('ERROR BTN', f)

            if i % count_hoz == count_hoz - 1:
                l = l + 1
            i = i + 1
        self.window.setFixedHeight((l+1) * self.icon_size)


    def dir_mod(self):
        self.refresh()

    def create_button(self, f):
        btn = object_file(self.window)
        realfile = self.current_dir + '/' + f

        if core.type_file(self, realfile) == 'folder':
            btn.setIconFromTheme('folder')
        else:
            ic = iconProvider()
            ic = ic.icon(QFileInfo(realfile))

            btn.setIcon(ic)

        btn.setFileSize(120, 120)
        btn.setText(f)
        btn.init()

        btn.value = f
        btn.clicked.connect(self.btn_press)

        self.btns.append(btn)

    def refresh(self):

        dir = self.current_dir

        #dir_dec = d.dec(dir)


        self.core.sort = 'abs123'

        #GET NEW LS`
        self.newfiles = self.core.read_dir(dir)


        l1 = set(self.files)
        l2 = set(self.newfiles)

        toDel = l1 - l2

        if len(toDel) > 0:

            for d in toDel:
                for btn in self.btns:
                    if d == btn.value:
                        btn.deleteLater()


        toAdd = l2 - l1

        unique = list(dict.fromkeys(toAdd))
        for f in unique:

            self.create_button(f)


        def btn_text(elem):
            return core.nat_keys(self, elem.value)[0]
        if self.btns != None:
            self.btns.sort(key=btn_text)

        self.btns = self.splitFolders(self.btns)
        self.files = self.newfiles

        self.reposition()

    def splitFolders(self, source_files):
        if source_files == None:
            return
        if len(source_files) == 0:
            return

        folders = []
        files = []

        if type(source_files[0]) is object_file:
            for file in source_files:
                realfile = self.current_dir + '/' + file.value

                if file.value[0] != '.' or self.hidden != True:
                    if core.type_file(self, realfile) == 'folder':
                        folders.append(file)
                    else:
                        files.append(file)

        else:
            for file in source_files:
                realfile = self.current_dir + '/' + file

                if file[0] != '.' or self.hidden != True:
                    if core.type_file(self, realfile) == 'folder':
                        folders.append(file)
                    else:
                        files.append(file)
        return folders+files
    def render(self):
        if len(self.files) == 0:
            return

        i = self.cycle
        l = self.tmpL

        combine = self.splitFolders(self.files)
        cycleAll = int(len(combine)/50)*50
        try:
            float_perc = self.cycle / cycleAll
        except ZeroDivisionError:
            float_perc = 0

        self.parent.parent().setLoadPercent(float_perc*100)
        if int(float_perc) == 1:
            self.parent.parent().hideLoader()


        for file in range(len(combine)):
            file = file + self.cycle
            btn = object_file(self.window)

            try:
                realfile = self.current_dir + '/' + combine[file]
            except:
                #print('no found file error')
                return

            if core.type_file(self, realfile) == 'folder':
                btn.setIconFromTheme('folder')
            else:
                ic = iconProvider()
                ic = ic.icon(QFileInfo(realfile))

                btn.setIcon(ic)

            btn.setFileSize(120,120)
            btn.setText(combine[file])
            btn.init()

            x = (self.icon_size * i) % self.maxWidth
            y = self.icon_size * l

            btn.move(x, y)

            count_hoz = int(self.maxWidth / self.icon_size)

            if file % count_hoz == count_hoz-1:
                l = l + 1
            i = i + 1

            btn.value = combine[file]
            try:
                btn.date = os.path.getctime(realfile)
            except:
                btn.date = 0

            btn.clicked.connect(self.btn_press)

            self.btns.append(btn)

            if i%50 == 0:
                self.cycle = i
                self.tmpL = l
                break
            elif file == len(combine)-1:
                self.renderTime = None
                self.cycle = -1
                break
        self.window.setFixedHeight((l+1) * self.icon_size)

        if self.cycle == -1:
            return
        self.asyncRender()

    def collision(self):
        iscoll = []

        for b in self.btns:
            e ={'x': b.pos().x()+50,
                'y': b.pos().y()+35,
                'w': b.pos().x()+8,
                'h': b.pos().y()+8}

            if e['x'] > self.select_rect_coll[0]  and e['x'] < self.select_rect_coll[2] and e['y'] > self.select_rect_coll[1] and e['y'] < self.select_rect_coll[3]:
                    iscoll.append(b)
        return iscoll

    def mousePressEvent(self, QMouseEvent):
        self.press = True
        self.globalPos = QMouseEvent.globalPos()
        self.windowMouseCoord = self.window.mapFromGlobal(QMouseEvent.globalPos())



        self.selection = QFrame(self.window)

        self.selection.setStyleSheet("""
            background: rgba(140,200,255,.0);
            border-radius: 10px;
            border-width: 1px;
            border-style: solid;
            border-color: rgba(0,0,0,.2);

        """)
        self.startCoord = QPoint(self.windowMouseCoord)

        #if abs(self.startCoord.x()) > 1 and abs(self.startCoord.y()) > 1:
        self.selection.setFixedSize(0,0)
        self.selection.move(5,5)
        self.selection.move(self.windowMouseCoord)
        self.selection.show()

        if self.collized:
            self.itemsSelection = True
        else:
            self.itemsSelection = None

    def mouseMoveEvent(self, QMouseEvent):



        if self.itemsSelection:

            url = []
            hover=None
            for e in self.collized:
                if e.hover:
                    hover = True

            if hover:

                self.mimeData = QMimeData()

                urls = []
                for e in self.collized:
                    urls.append(QUrl('file://'+self.current_dir + '/' +e.value))

                self.mimeData.setUrls(urls)
                self.drag = QDrag(self)
                self.drag.setMimeData(self.mimeData)

                ####################
                # ВОТ ЭТО ВАЖНО
                #self.drag.exec(Qt.LinkAction)
                self.drag.exec(Qt.CopyAction)


                if self.press:
                    pass
            else:
                for b in self.btns:
                    b.unselected()
                self.select_rect_coll = []
                self.collized = []
        else:
            if self.btns == None:
                return
            self.select_rect_coll = [self.selection.x(), self.selection.y(),
                                     self.selection.x() + self.selection.width(),
                                     self.selection.y() + self.selection.height()]
            for b in self.btns:
                b.unselected()
                b.leaveEvent(QMouseEvent)

            self.collized = self.collision()

            for b in self.collized:
                b.selected()
                b.leaveEvent(QMouseEvent)
                # b.clicked.emit()

            self.windowMouseCoord = self.window.mapFromGlobal(QMouseEvent.globalPos())
            self.mouse = [self.windowMouseCoord.x(), self.windowMouseCoord.y()]
            self.windowMouseCoord = self.window.mapFromGlobal(QMouseEvent.globalPos())
            movePoint = self.startCoord - self.windowMouseCoord

            invertmove = self.startCoord - movePoint

            if movePoint.x() > 0 and movePoint.y() > 0:
                self.selection.setFixedSize(abs(movePoint.x()), abs(movePoint.y()))
                self.selection.move(invertmove)
            elif movePoint.x() > 0:
                self.selection.setFixedSize(abs(movePoint.x()), abs(movePoint.y()))
                self.selection.move(invertmove.x(), self.startCoord.y())
            elif movePoint.y() > 0:
                self.selection.setFixedSize(abs(movePoint.x()), abs(movePoint.y()))
                self.selection.move(self.startCoord.x(), invertmove.y())
            else:
                self.selection.setFixedSize(abs(movePoint.x()), abs(movePoint.y()))
            #############################################################################

    def mouseReleaseEvent(self, QMouseEvent):
        self.press = False
        self.globalPos = QMouseEvent.globalPos()
        self.windowMouseCoord = self.window.mapFromGlobal(QMouseEvent.globalPos())
        if self.startCoord == QPoint(self.windowMouseCoord):

            self.select_rect_coll = []
        self.selection.deleteLater()
        pass

    def mimeTypes(self):
        mimetypes = super().mimeTypes()
        mimetypes.append('text/plain')
        return mimetypes

    def dropEvent(self, event):

        #print(event.dropAction() == Qt.CopyAction)
        url = QUrl()

        links = []
        for url in event.mimeData().urls():
            url = QUrl(url)
            links.append(url.toLocalFile())
        sys.modules['scr.core'].core.copy(sys.modules['scr.core'].core, links, os.getcwd())
        self.refresh()
            #path = url.toLocalFile().toLocal8Bit().data()
            #if os.path.isfile(path):
            #    print(path)
        #self.refresh()
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():

            event.accept()
        else:
            event.ignore()


    def btn_press(self):
        self.globalPos = self.sender().globalPos

        if self.sender().target == 'None':
            try:
                self.selectBtn.select = None
            except:
                print('none target')
                pass
        if self.sender().select and self.sender().target == 'icon':
            pass

        if self.sender().type == 1 and self.sender().target == 'icon':

            try:
                self.selectBtn.select = None
                self.selectBtn.btn_update = True
                self.selectBtn.update()
            except:
                pass

            self.selectBtn = self.sender()

            self.selectFile = os.path.normpath(self.current_dir + '/' +self.sender().value)
            #self.dFilter.dec(self.selectFile)

            if os.path.isdir(self.selectFile):
                self.setDir(self.current_dir + '/' + self.sender().value)
                self.history.set(self.current_dir)
            else:
                self.setDir(self.current_dir + '/' + self.sender().value)
                self.lm_menu()

