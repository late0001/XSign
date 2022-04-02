from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtCore import QSize
from PyQt5.QtCore import QFileInfo
from PyQt5.QtWidgets import QFileIconProvider
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel 
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from XSignWinui import Ui_MainWindow
import sys
from ud_zip import ZFile
from uListItem import MyListWidgetItem

class mywindow(QMainWindow, Ui_MainWindow):
    def  __init__ (self):
        super(mywindow, self).__init__()
        self.setupUi(self)
        self.pushButton1 = Button(self.centralwidget)
        self.pushButton1.setGeometry(QtCore.QRect(20, 440, 751, 101))
        self.pushButton1.setObjectName("pushButton1")
        self.pushButton1.setText("Oj8K")
        self.pushButton1.RecvFileSignal.connect(self.dealRecvFile)
        self.btnExtract.clicked.connect(self.btnExtractClicked)
    
    def btnExtractClicked(self):
        for it in self.ic:
            extractZip( it["filename"], "./temp")
    
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
            #widget = get_item_wight(it)
            widget = MyListWidgetItem()
            widget.initData(it)
            self.listWidget.addItem(item) # 添加item
            self.listWidget.setItemWidget(item, widget) # 为item设置widget
            
class Button(QPushButton):
    RecvFileSignal = QtCore.pyqtSignal(list)
    def __init__(self, parent):
        super(Button, self).__init__(parent)
        self.setAcceptDrops(True)
        #self.setDragDropMode(QAbstractItemView.InternalMove)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super(Button, self).dragEnterEvent(event)
    
    def dragMoveEvent(self, event):
        super(Button, self).dragMoveEvent(event)
    
    def dropEvent(self, event):
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