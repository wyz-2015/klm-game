import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os

from core.img_viewer import *
from core.buttons import *
from core.ruler import *

class Main(QWidget):
    def __init__(self):
        super(Main,self).__init__()
    
        #self.v_layout=QVBoxLayout()
        self.reset(is_first=True)

    def reset(self,is_first=False):
        self.ruler=Ruler()
        self.ruler.set_test_time(3)
        self.test_time=self.ruler.test_time#实际上应为用户该作答的次数，默认15次

        if(not is_first):#非首轮游戏时，每轮游戏前清空v_layout内所有控件。
            #self.v_layout.removeWidget(self.img_viewer)
            #input("pause")
            #print("self.v_layout.removeWidget(self.img_viewer)")
            #self.v_layout.removeWidget(self.btns2)
            #input("pause")
            #print("self.v_layout.removeWidget(self.btns2)")
            while(self.v_layout.count()):#Thanks for 文心一言
                widget=self.v_layout.takeAt(0).widget()
                print(widget)
                if(widget):
                    widget.setParent(None)

        self.img_viewer=Img_viewer("ms_cs")
        choice=self.img_viewer.choose_one()
        self.ruler.img_read(choice)
        print(choice)
        self.img_viewer.play(choice)
        
        self.isFirst=True#由于首次展示图片较为特殊，需要引入此变量标识为首次使用。

        self.btns2=Menu_buttons()
        self.btns2.signal.connect(self.btns2_func)

        self.btns1=KLM_buttons()
        self.btns1.signal.connect(self.change_img)

        #for i in range(self.layout().count()):self.layout().takeAt(0).widget().setParent(None)
        #self.v_layout.takeAt(0).widget().setParent(None)
        if(is_first):
            self.v_layout=QVBoxLayout()
            self.setLayout(self.v_layout)
        self.v_layout.addWidget(self.img_viewer)
        self.v_layout.addWidget(self.btns2)
        print("self.layout().count()={0}".format(self.layout().count()))

    def change_img(self,c):
        print(self.test_time)

        choice=self.img_viewer.choose_one()
        print(choice)
        self.ruler.img_read(choice)
        self.img_viewer.play(choice)
        
        if(self.isFirst):
            self.isFirst=False
        else:
            self.test_time-=1
            self.ruler.choice_read(c)

        #测试版使用此段代码展示游戏结果
        if(self.test_time==0):
            self.ruler.timer_end()
            
            result="作答：{0}\n答案：{1}\n得分：{2}\n总分：{3:n}\t用时：{4:.9f} s".format(self.ruler.choice_list,\
                    self.ruler.make_answers(),\
                    self.ruler.total(),\
                    sum(self.ruler.total()),\
                    self.ruler.total_time())
            QMessageBox.information(self,"本局游戏结果",result)
            #sys.exit()
            self.reset(is_first=False)

    def btns2_func(self,signal):
        if(signal=="start"):
            print("start")
            #self.v_layout.removeWidget(self.btns2)
            #self.v_layout.addWidget(self.btns1)
            self.v_layout.replaceWidget(self.btns2,self.btns1)
            self.btns1.setFocus()#在切换控件btn1后，主动加入焦点，否则焦点将停留在btns2，使得KLM热键失效。
            self.change_img(None)
            self.ruler.timer_start()

if(__name__=="__main__"):
    app=QApplication(sys.argv)
    main=Main()
    main.show()
    sys.exit(app.exec())
