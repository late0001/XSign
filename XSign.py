from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton
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

class Button(QPushButton):
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
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                path = str(url.toLocalFile())
                print (path)
            event.acceptProposedAction()
        else:
            super(Button,self).dropEvent(event)
        
if __name__== "__main__":
    app=QtWidgets.QApplication(sys.argv)
    ui = mywindow()    
    ui.show()
    #ui.loginToLCSC()
    sys.exit(app.exec_())