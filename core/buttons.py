import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

if(__name__!="__main__"):from core.key_settings import *

#game_key=get_current_settings()

class KLM_buttons(QWidget):
    signal=pyqtSignal(str)
    def __init__(self):
        super(KLM_buttons,self).__init__()
        self.game_key=get_current_settings()
        #(self.bt_K,self.bt_L,self.bt_M,self.bt_Load,self.bt_Score,self.bt_About)=(QPushButton() for i in range(6))

        #bt_K
        #self.bt_K.setText("相似(&K)")
        #self.bt_K.setShortcut(Qt.Key_K)
        #self.bt_K.clicked.connect(lambda:print("K"))
        #self.

        #TODO:3个键要能在设置里自定义键位。
        self.bt_K=Btn(f"相似(&{self.game_key['K']})",KEYS[self.game_key["K"]])
        self.bt_K.signal.connect(lambda:self.signal.emit("K"))
        self.bt_L=Btn(f"不同(&{self.game_key['L']})",KEYS[self.game_key["L"]])
        self.bt_L.signal.connect(lambda:self.signal.emit("L"))
        self.bt_M=Btn(f"特殊(&{self.game_key['M']})",KEYS[self.game_key["M"]])
        self.bt_M.signal.connect(lambda:self.signal.emit("M"))

        h_layout=QHBoxLayout()
        h_layout.addWidget(self.bt_K)
        h_layout.addWidget(self.bt_L)
        h_layout.addWidget(self.bt_M)

        self.setLayout(h_layout)

    def keyPressEvent(self,event):#热键发送信号
        if(event.key()==KEYS[self.game_key["K"]]):
            self.signal.emit("K")
            print("K")
        elif(event.key()==KEYS[self.game_key["L"]]):
            self.signal.emit("L")
            print("L")
        elif(event.key()==KEYS[self.game_key["M"]]):
            self.signal.emit("M")
            print("M")

    def sync_keys(self):
        self.game_key=get_current_settings()#创建时刷新设置
        print(self.game_key)
        
class Btn(QPushButton):#KLM按钮通用模版封装
    signal=pyqtSignal(bool)
    def __init__(self,text,hot_key):
        super(Btn,self).__init__()
        #self.setText("相似(&K)")
        self.setText(text)
        self.hot_key=hot_key
        #self.setShortcut(Qt.Key_K)
        #self.setShortcut(hot_key)
        self.clicked.connect(lambda:self.signal.emit(True))#按下时发射信号
        
    #def keyPressEvent(self,event):#热键发射信号
    #    if(event.key()==self.hot_key):
    #        self.signal.emit(True)

class Menu_buttons(QWidget):
    signal=pyqtSignal(str)
    def __init__(self):
        super(Menu_buttons,self).__init__()
        #(self.btn_load,self.btn_start,self.btn_exit)=(QPushButton() for i in range(3))
        self.btn_load=QPushButton("载入")
        self.btn_start=QPushButton("开始(&Y)")
        self.btn_exit=QPushButton("设置")
        self.btn_load.clicked.connect(lambda:self.signal.emit("load"))
        self.btn_start.clicked.connect(lambda:self.signal.emit("start"))
        self.btn_exit.clicked.connect(lambda:self.signal.emit("option"))

        h_layout=QHBoxLayout()
        h_layout.addWidget(self.btn_load)
        h_layout.addWidget(self.btn_start)
        h_layout.addWidget(self.btn_exit)
        self.setLayout(h_layout)

    def keyPressEvent(self,event):#TODO:应加入自定义键位功能。
        if(event.key()==KEYS[self.game_key["Y"]]):self.signal.emit("start")

    def sync_keys(self):
        self.game_key=get_current_settings()#刷新设置
        print(self.game_key)

if(__name__=="__main__"):
    from key_settings import *
    app=QApplication(sys.argv)
    #a=Btn("KKKKKK",Qt.Key_K)
    #a.show()
    #a=KLM_buttons()
    a=Menu_buttons()
    a.show()
    sys.exit(app.exec())
