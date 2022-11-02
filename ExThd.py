from PyQt5.QtCore import QThread, pyqtSignal
import os

class WorkThread(QThread):
    # 使用信号和UI主线程通讯
    signal_over = pyqtSignal(list)   #给主线程传递函数执行结束的返回值，list表示返回值类型是列表
 
    def __init__(self, cmd_str='', parent=None):     
        super(WorkThread, self).__init__(parent)
        self.cmd_str = cmd_str     
 
    def run(self):   #固定函数，不可变，线程开始自动执行run函数
        print(self.cmd_str)
        os.system(self.cmd_str)
        li = []  #将返回值添加到列表
        self.signal_over.emit(li)  #发射列表信号，表示线程结束
        return 
