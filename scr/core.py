#!/bin/python
import os, re, math, stat
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QDesktopWidget, QLabel
from PyQt5.QtGui import QPainter, QColor, QFont, QBrush, QPen
from PyQt5.QtCore import Qt, QTimer, QThread
from threading import Thread

import aiofiles

from time import sleep


"""
БРИФИНГ
НУЖНО РЕАЛИЗОВАТЬ ПРАВА И ЮЗЕР ПАПОК И ФАЙЛОВ

"""
class indicator(QWidget):
    frame = 0
    process = 0
    full_copy = 0

    pause_status = None

    tmp_bytes = 0
    tmp_bytes_array = []
    current_file_name = ''
    def __init__(self, sourcedir, arr, dest):
        super().__init__()
        self.arr = arr
        self.dest = dest
        self.sourceDir = sourcedir


        self.initUI()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setWindowOpacity(0.3)

        size = QApplication.primaryScreen().size() / 2 - self.size() / 2

        self.move(size.width(), 0)

        self.scanFiles()
        self.show()
    def initUI(self):
        self.setFixedSize(500, 60)

        self.cancel = QPushButton('cancel', self)
        self.cancel.move(5, 8)

        self.pause = QPushButton('P', self)
        self.pause.clicked.connect(self.pause_button)
        self.pause.setFixedSize(18,18)
        self.pause.move(2,41)

        self.cancel.clicked.connect(self.cancel_clicked)

        self.byteratetext = 'W: '
        self.byterate = QLabel(self.byteratetext, self)
        self.byterate.move(40, 40)
        self.byterate.setFixedSize(400,20)

        self.bytetimer = QTimer()
        self.bytetimer.timeout.connect(self.byterate_interval)
        self.bytetimer.start(1000)


        #ANIMATION
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1000/60)

    def pause_button(self):
        self.pause_status = True if not self.pause_status else None
        if self.pause_status:
            self.pause.setText('||')
        else:
            self.pause.setText('P')

    def bytestage(self, a):
        b = a
        p = 0
        step = 1024
        while a > step:
            p += 1
            a = a/step


        res = {p == 0: 'b/s',
            p == 1: 'kb/s',
            p == 2: 'mb/s',
            p == 3: 'gb/s',
            p == 4: 'tb/s',
            p == 5: 'pb/s',
            p == 6: 'eb/s',
            p == 7: 'zb/s',
            p == 8: 'yb/s'

            }[True]
        return  ['{:.1f}'.format( b / (step ** p )) , res]

    def byterate_interval(self):
        if self.pause_status:
            return
        #Soft number speed
        self.tmp_bytes_array.append(self.tmp_bytes)
        medium = 0
        for b in self.tmp_bytes_array:
            medium += b
        m = medium / len(self.tmp_bytes_array)
        if len(self.tmp_bytes_array) > 5:
            self.tmp_bytes_array.pop(0)

        #Convert format
        bs = self.bytestage(m)
        mb = str(bs[0]) + ' ' + bs[1]
        self.byterate.setText(self.byteratetext + mb + ' | ' + self.current_file_name)
        self.tmp_bytes = 0

    def cancel_clicked(self, e):
        self.close()

    def paintEvent(self, QPaintEvent):

        qp = QPainter()
        qp.begin(self)
        qp.setPen(Qt.NoPen)


        qp.setBrush(QColor(100, 20, 20))
        qp.drawRect(100, 17, 380, 5)

        a = ((math.sin(self.frame/10)+1)*80)
        qp.setBrush(QColor(255, 190-a, 80+(-a/2)))

        #process = (math.sin(self.frame/30) + 1)/2
        qp.drawRect(101, 18, 378*(self.process/100), 3)

        qp.end()

        self.frame = self.frame + 1
    def scanFiles(self):

        ###############################
        #НАДО РАЗОБРАТЬ

        files = []
        dirs = []

        for f in self.arr:
            if os.path.isdir(f):
                obj = self.getFilesFromFolder(f)
                files = files + obj[1]
                dirs = dirs + obj[0]
            elif os.path.isfile(f):
                files.append('/' + os.path.basename(f))

        #Create folders
        for d in dirs:
            try:
                os.mkdir(self.dest + d)
            except:
                print("Dir is exist")
            #print(self.dest + d)

        bytes = 0
        for f in files:
            print(self.sourceDir + f)
            s = os.path.getsize(self.sourceDir + f)
            bytes = bytes + s

        #self.setCopy(files, self.dest + '/' + os.path.basename(f))
        self.allBytes = bytes


        ######
        #DEST недостаточно, нужно еще папки прописать
        # self.destDIR + self.dest
        ######

        self.setCopy(files, self.sourceDir, self.dest)

    def getFilesFromFolder(self, dir):
        files = []
        dirs = []
        # r=root, d=directories, f = files
        for r, d, f in os.walk(dir):
            #cleanup files for destination
            dir = r[len(self.sourceDir):]
            dirs.append(dir)
            #print(dir)
            for file in f:
                files.append(os.path.join(r, dir+'/'+file))

        return [dirs, files]
        """
        for f in files:
            print('seq file: ',f)
        """

    def progressCopy(self):


        src = self.cpSource + self.cpFiles[self.countFinish-1]
        dest = self.cpDest + self.cpFiles[self.countFinish-1]
        #dest = self.cpDest +'/'+os.path.basename(src)

        self.copyfileobj(src=src,
                         dst=dest,
                         callback_progress=self.progress,
                         callback_copydone=self.copydone)

    def setCopy(self, files, srcs, dest):

        """
        for d in self.dir:
            print(self.dest + '/' + d)
            try:
                os.mkdir(self.dest + '/' + d)
            except:
                print(d, "file exists")
        """
        self.cpFiles = files
        self.cpSource = srcs
        self.cpDest = dest
        self.len = len(self.cpFiles)

        self.countFinish = 0

        self.progressCopy()
    def progress(self, fsrc, fdst, copied):

        self.full_copy += copied
        self.tmp_bytes += copied
        self.process = int(self.full_copy / self.allBytes * 100)

    def copydone(self, fsrc, fdst, copied):
        st = os.stat(fsrc.name)  # для получения текущих разрешений
        os.chmod(fdst.name, st.st_mode) #| stat.S_IEXEC) # Копирование разрешений
        print('fdst.name', fdst.name)

        self.countFinish += 1
        if self.countFinish == self.len:
            self.finish()
        else:
            self.progressCopy()

    def finish(self):
        print('COPY ALL FILES', self.full_copy, self.allBytes)

        self.bytetimer.stop()
        self.timer.stop()

        self.thr.quit()
        self.close()
    def getPause(self):
        return self.pause_status
    def copyfileobj(self, src, dst, callback_progress, callback_copydone, length=8 * 1024):
        print('START COPY FILE')
        self.current_file_name = os.path.basename(src)
        self.thr = io_thread()
        self.thr.args(src, dst, callback_progress, callback_copydone, length, lambda: self.getPause())
        self.thr.start()





class io_thread(QThread):


    def __init__(self, parent=None):
        QThread.__init__(self, parent)
    def args(self, src, dst, callback_progress, callback_copydone, length=8*1024, pause=None):
        self.src = src
        self.dst = dst
        self.callback_progress = callback_progress
        self.callback_copydone = callback_copydone
        self.length = length
        self.pause = pause
    def run(self):


        with open(self.src, 'rb') as fsrc:
            with open(self.dst, 'wb') as fdst:
                copied = 0
                while True:
                    if self.pause():
                        pass
                    else:

                        buf = fsrc.read(self.length)

                        if not buf:
                            break
                        fdst.write(buf)
                        copied += len(buf)

                        #if c == c_max:
                        self.callback_progress(fsrc=fsrc, fdst=fdst, copied=len(buf))


                self.callback_copydone(fsrc=fsrc, fdst=fdst, copied=len(buf))


class core:
    sort = None
    cp = None

    last_query_url = None



    def read_dir(self, url):

        try:
            files = os.listdir(os.path.realpath(url))
        except PermissionError:
            #print(PermissionError)
            print('PermissionError', '320 core.py')
        self.last_query_url = self.sort_list(files)
        return self.last_query_url

    def nat_keys(self, text):
        def atoi(let):
            return int(let) if let.isdigit() else let
            # ANALOG
            """
            if let.isdigit():
                return int(let)
            else:
                return let

            """
        return [atoi(c) for c in re.split(r'(\d+)', text)]
        ######
        # ANALOG
        # for c in re.split(r'(\d+)', text):
        #    return atoi(c)

    def sort_list(self, list):
        #abs123
        if self.sort == 'abs123':
            list.sort(key=self.nat_keys)

        #FORMAT
        #---
        #EXT
        #---
        #ALFAVIT


        return list


    def new_history(self):
        pass
    def get_history(self):
        pass
    def create_dir(self, url):
        pass
    def copy(self, SOURCEDIR, FROM, TO):
        self.cp = indicator(SOURCEDIR, FROM, TO)

    def symlink(self, FROM, TO):
        pass
    def type_file(self, file):
        if os.path.isdir(file):
            return 'folder'
        else:
            return 'file'