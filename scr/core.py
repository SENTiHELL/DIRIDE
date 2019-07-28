import os, re, math, sys, asyncio
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QDesktopWidget, QLabel
from PyQt5.QtGui import QPainter, QColor, QFont, QBrush, QPen
from PyQt5.QtCore import Qt, QTimer, QThread
from threading import Thread

import aiofiles

from time import sleep

class indicator(QWidget):
    frame = 0
    process = 0
    full_copy = 0

    pause_status = None

    tmp_bytes = 0
    tmp_bytes_array = []
    current_file_name = ''
    def __init__(self, arr, dest):
        super().__init__()

        self.arr = arr
        self.dest = dest
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
        files = []
        for f in self.arr:
            if os.path.isdir(f):
                files = files + self.getFilesFromFolder(f)
            elif os.path.isfile(f):
                files.append(f)

        bytes = 0
        for f in files:
            s = os.path.getsize(f)
            bytes = bytes + s

        #self.setCopy(files, self.dest + '/' + os.path.basename(f))
        self.allBytes = bytes

        self.setCopy(files, self.dest)
        #mb = float('{:.1f}'.format(bytes/1024/1024))
        #print('SIZE_static:',mb, int(bytes))
    def getFilesFromFolder(self, dir):
        files = []
        # r=root, d=directories, f = files
        for r, d, f in os.walk(dir):
            for file in f:
                files.append(os.path.join(r, file))
        return files
        """
        for f in files:
            print('seq file: ',f)
        """

    def progressCopy(self):

        src = self.cpFiles[self.countFinish-1]
        dest = self.cpDest +'/'+os.path.basename(src)
        self.copyfileobj(src=src,
                         dst=dest,
                         callback_progress=self.progress,
                         callback_copydone=self.copydone)

    def setCopy(self, srcs, dest):

        self.cpFiles = srcs
        self.cpDest = dest
        self.len = len(self.cpFiles)

        self.countFinish = 0

        self.progressCopy()
    def progress(self, fsrc, fdst, copied):

        self.full_copy += copied
        self.tmp_bytes += copied
        self.process = int(self.full_copy / self.allBytes * 100)

    def copydone(self, fsrc, fdst, copied):

        self.countFinish += 1
        if self.countFinish == self.len:
            self.finish()
            return
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

        """
        old test
        delete this code 
        
        with open(self.reador_d, 'rb') as sr:

            while True:

                buf = sr.read(8 * 1024)
                print(buf)
                if not buf:
                    break

        """



class core:
    sort = None
    cp = None

    last_query_url = None











    def read_dir(self, url):

        files = os.listdir(os.path.realpath(url))

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
    def copy(self, FROM, TO):
        """
        def an():
            self.cp = indicator(FROM, TO)
        self.auto_start_timer = QTimer()
        self.auto_start_timer.timeout.connect(an)
        self.auto_start_timer.setSingleShot(True)
        self.auto_start_timer.start(0)
        """
        self.cp = indicator(FROM, TO)


        return
        if type(FROM) == list:
            for i in FROM:
                os.system('cp "'+i+'" "'+TO+'"')
        else:
            os.system('cp "'+FROM+'" "'+TO+'"')
    def symlink(self, FROM, TO):
        pass
    def type_file(self, file):
        if os.path.isdir(file):
            return 'folder'
        else:
            return 'file'