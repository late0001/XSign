from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QSize
from PyQt5.QtCore import QFileInfo
from PyQt5.QtWidgets import QFileIconProvider
from PyQt5.QtGui import QIcon
from uListItemui import Ui_ListWidgetItem

def getFileInfo(filename):
    """获取文件的图片和名字"""
    fileInfo = QFileInfo(filename)
    fileIcon = QFileIconProvider()
    icon = QtGui.QIcon(fileIcon.icon(fileInfo))
    name = QtCore.QFileInfo(filename).fileName()
    return icon, name

class MyListWidgetItem(QWidget, Ui_ListWidgetItem):
    def __init__(self, parent= None):
        super(MyListWidgetItem, self).__init__(parent)
        self.setupUi(self)
        
    def initData(self, data):
        # 读取属性
        filename = data['filename']
        status = data['status']
        isX64 = data['isX64']
        ship_star = 3 #data['ship_star']
        
        icon, name = getFileInfo(filename)
        

        #maps = QPixmap(ship_photo).scaled(40, 25)
    
        pixmap = icon.pixmap(QSize(40, 40), QIcon.Normal, QIcon.On)
    #                                    isEnabled() ? QIcon::Normal
    #                                                : QIcon::Disabled,
    #                                    isChecked() ? QIcon::On
    #                                                : QIcon::Off);
        self.map_l.setPixmap(pixmap)
        
        self.label_name.setText(name)
        self.label_fullpath.setText(filename)
        self.label_arch.setText("X64" if isX64 > 0 else "X86")
        self.label_5.setText(str(ship_star) + "星")
        self.label_status.setText("------")
        return  # 