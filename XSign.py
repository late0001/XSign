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


class mywindow(QMainWindow, Ui_MainWindow):
    def  __init__ (self):
        super(mywindow, self).__init__()
        self.setupUi(self)
        self.pushButton1 = Button(self.centralwidget)
        self.pushButton1.setGeometry(QtCore.QRect(20, 440, 751, 101))
        self.pushButton1.setObjectName("pushButton1")
        self.pushButton1.setText("Oj8K")
        self.pushButton1.RecvFileSignal.connect(self.dealRecvFile)
        
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
        for it in ic:
            print(it)
            item = QListWidgetItem() # 创建QListWidgetItem对象
            item.setSizeHint(QSize(300, 60)) # 设置QListWidgetItem大小
            widget = get_item_wight(it)
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

def getFileInfo(filename):
    """获取文件的图片和名字"""
    fileInfo = QFileInfo(filename)
    fileIcon = QFileIconProvider()
    icon = QtGui.QIcon(fileIcon.icon(fileInfo))
    name = QtCore.QFileInfo(filename).fileName()
    return icon, name
        
def get_item_wight(data):
    # 读取属性
    filename = data['filename']
    status = data['status']
    isX64 = data['isX64']
    ship_star = 3 #data['ship_star']
    
    fileInfo = QFileInfo(filename)
    fileIcon = QFileIconProvider()
    name = QtCore.QFileInfo(filename).fileName()
    
    # 总Widget
    wight = QWidget()
    # 总体横向布局
    layout_main = QHBoxLayout()
    map_l = QLabel() # 头像显示
    #map_l.setFixedSize(40, 25)
    #maps = QPixmap(ship_photo).scaled(40, 25)
    icon = QIcon(fileIcon.icon(fileInfo))# 头像显示
    pixmap = icon.pixmap(QSize(22, 22), QIcon.Normal, QIcon.On)
#                                    isEnabled() ? QIcon::Normal
#                                                : QIcon::Disabled,
#                                    isChecked() ? QIcon::On
#                                                : QIcon::Off);
    map_l.setPixmap(pixmap)
    
    # 右边的纵向布局
    layout_right = QVBoxLayout()
    # 右下的的横向布局
    layout_right_down = QHBoxLayout() # 右下的横向布局
    layout_right_down.addWidget(QLabel(name))
    layout_right_down.addWidget(QLabel("X64" if isX64 > 0 else "X86"))
    layout_right_down.addWidget(QLabel(str(ship_star) + "星"))
    layout_right_down.addWidget(QLabel("------"))
    # 按照从左到右, 从上到下布局添加
    layout_main.addWidget(map_l) # 最左边的头像
    layout_right.addWidget(QLabel(filename)) # 右边的纵向布局
    layout_right.addLayout(layout_right_down) # 右下角横向布局
    layout_main.addLayout(layout_right) # 右边的布局
    wight.setLayout(layout_main) # 布局给wight
    return wight # 返回wight
        
if __name__== "__main__":
    app=QtWidgets.QApplication(sys.argv)
    ui = mywindow()    
    ui.show()
    #ui.loginToLCSC()
    sys.exit(app.exec_())