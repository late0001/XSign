from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QPushButton, QListWidgetItem, QLabel, QFileIconProvider, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import QSize, QFileInfo, Qt
from PyQt5.QtGui import QIcon, QColor 
from XSignWinui import Ui_MainWindow
import sys
from ud_zip import ZFile
from uListItem import MyListWidgetItem
from tSign import TSign
from selenium.common.exceptions import NoSuchElementException   
import operator as op
import os
from ExThd import WorkThread 
from XConfig import XConfig

class mywindow(QMainWindow, Ui_MainWindow):
    ConvertSignal = QtCore.pyqtSignal(str)
    
    def  __init__ (self):
        super(mywindow, self).__init__()
        self.setupUi(self)
        self.pushButton1 = Button(self.centralwidget, self)
        self.pushButton1.setGeometry(QtCore.QRect(20, 440, 751, 101))
        self.pushButton1.setObjectName("pushButton1")
        self.pushButton1.setText("Drag file to here")
        self.pushButton1.RecvFileSignal.connect(self.dealRecvFile)
        self.btnExtract.clicked.connect(self.btnExtractClicked)
        self.btnRtkSign.clicked.connect(self.btnRtkSignClicked)
        self.btnMSSign.clicked.connect(self.btnMSSignClicked)
        self.pb_stripdir.clicked.connect(self.btnStripDirClicked)
        self.pb_peel.clicked.connect(self.btnPeelClicked)
        cfg = XConfig()
        cfg.getAccConfig()
        cfg.getBuildEnvConfig()
        self.tracefmt = cfg.tracefmt
        self.cfg = cfg
        self.tSign = TSign(cfg)
        
    
    def btnStripDirClicked(self):
        str1 = self.te_pdb.toPlainText()
        idx = str1.rfind("/")
        if(idx >-1 ):
            str1 = str1[0: idx]
            print(str1)
            self.te_pdb.setText(str1)
    
    def thread_decode_over(self):
        self.pb_peel.setEnabled(True)
        
    def btnPeelClicked(self):
        self.pb_peel.setEnabled(False)
        etl = self.te_etl.toPlainText()
        pdb = self.te_pdb.toPlainText()
        ofile = etl[0:-4] + ".txt"
        cmd = self.tracefmt 
        if(os.path.isdir(pdb)):
            cmd = cmd + " " + etl + " -r " + pdb + " -o " + ofile
        else:
            cmd = cmd + " " + etl + " -pdb " + pdb + " -o " + ofile
        self.decodethread = WorkThread(cmd)    
        self.decodethread.signal_over.connect(self.thread_decode_over)  
        self.decodethread.start()  # 启动线程

        

        
            
    def btnRtkSignClicked(self):
        self.tSign.signFiles(self.ic)
        
    def btnExtractClicked(self):
        for it in self.ic:
            extractZip( it["filename"], "./temp")
    
    def btnMSSignClicked(self):
        self.tSign.MSSign(self.ic)

    def dealRecvFile(self, fileList):
        print ("*"*80)
        print (fileList)
        
        ic = []
        for f in fileList:
            c = {}
            c["filename"] = f
            c["isX64"] = 0
            if (f.lower().find("x64") != -1):
                c["isX64"] = 1
            c["status"] = ""
            ic.append(c)
        print ("*"*80)
        self.ic = ic
        for it in ic:
            print(it)
            item = QListWidgetItem() # 创建QListWidgetItem对象
            item.setSizeHint(QSize(300, 80)) # 设置QListWidgetItem大小
            widget = MyListWidgetItem()
            widget.initData(it)
            self.listWidget.addItem(item) # 添加item
            self.listWidget.setItemWidget(item, widget) # 为item设置widget
        
        for it in ic:
            print("ic=>", ic)

class Button(QPushButton):
    RecvFileSignal = QtCore.pyqtSignal(list)

    def __init__(self, parent, mf):
        super(Button, self).__init__(parent)
        self.setAcceptDrops(True)
        self.mf = mf
        #self.setDragDropMode(QAbstractItemView.InternalMove)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super(Button, self).dragEnterEvent(event)
    
    def dragMoveEvent(self, event):
        super(Button, self).dragMoveEvent(event)
    
    def dropEvent(self, event):
        idx = self.mf.tabWidget.currentIndex()
        print("idx = ", idx)
        if(idx == 0):
            ilist = []
            if event.mimeData().hasUrls():
                for url in event.mimeData().urls():
                    path = str(url.toLocalFile())
                    print (path)
                    ilist.append(path)
                self.RecvFileSignal.emit(ilist)
                event.acceptProposedAction()
            else:
                super(Button,self).dropEvent(event)
        elif (idx == 1):
            if event.mimeData().hasUrls():
                for url in event.mimeData().urls():
                    path = str(url.toLocalFile())
                print (path)
                if(path[-4:] == ".etl"):
                    self.mf.te_etl.setText(path)
                else:
                    print("not bat")
                    self.mf.te_pdb.setText(path)
                event.acceptProposedAction()
            else:
                super(Button,self).dropEvent(event)
        

#解压缩Zip到指定文件夹
def extractZip(zfile, path):
    z = ZFile(zfile)
    z.extract_to(path)
    z.close()
        

if __name__== "__main__":
    app=QtWidgets.QApplication(sys.argv)
    ui = mywindow()    
    ui.show()
    #ui.loginToLCSC()
    sys.exit(app.exec_())