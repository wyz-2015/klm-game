import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
import time

from core.img_viewer import *
from core.buttons import *
from core.ruler import *
from core.stage import *
from core.save import *
from core.key_settings import *

class Main(QWidget):
    def __init__(self):
        super(Main,self).__init__() 

        self.setWindowTitle("K&L&M 反应测试游戏")

        #self.v_layout=QVBoxLayout()
        self.img_viewer=Img_viewer()
        self.first_launch=True#这已经是第3个为了控制流程设计的is_first变量了……
        self.first_load()
        #self.reset(is_first=True)
        self.rounds=None#为了交互界面中设定游戏次数使用的变量

    def reset(self,is_first=False):
        self.ruler=Ruler()
        self.ruler.set_test_time(self.rounds)
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

        #self.img_viewer=Img_viewer("ms_cs")
        if(self.img_viewer.stage):
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
        
        self.k_s_window=K_s_window()
        self.k_s_window.signal.connect(self.sync_keys)

    def change_img(self,c):#核心方法之一，切换图片并记录游戏数据
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

        #测试版使用此段代码展示游戏结果——但是现在“转正”了~
        if(self.test_time==0):
            self.ruler.timer_end()
            
            result="玩家：{5:s}\n作答：{0}\n答案：{1}\n得分：{2}\n总分：{3:n}\t用时：{4:.9f} s".format(\
                    self.ruler.choice_list,\
                    self.ruler.make_answers(),\
                    self.ruler.total(),\
                    sum(self.ruler.total()),\
                    self.ruler.total_time(),\
                    self.player_name\
                    )

            self.saver=Saver()#TODO:要能自定义存档位置
            t=time.localtime()
            #(玩家ID,选用模组,正确数,总题数,用时,rating,日期,时间)
            data_tuple=(\
                        self.player_name,\
                                self.img_viewer.stage,\
                                sum(self.ruler.total()),\
                                self.ruler.test_time,\
                                round(self.ruler.total_time(),9),\
                                round(sum(self.ruler.total())/self.ruler.total_time(),5),\
                                time.strftime("%Y-%m-%d",t),\
                                time.strftime("%H:%M:%S",t)\
                                )

            self.saver.add_score(data_tuple)

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
        elif(signal=="load"):
            #self.first_load()
            self.load_window.show()
        elif(signal=="option"):
            self.k_s_window.show()
            
    def first_load(self):#开启程序时首先提示加载何模组
        self.load_window=Stage()        
        self.load_window.signal.connect(self.load_window_func)
        self.load_window.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.load_window.show()

    def load_window_func(self,message):#接受信号中的信息，备写入分数存档中。
        print(message,bool(message))
        self.img_viewer.set_stage_name(message[1])
        self.player_name=message[0]
        self.rounds=message[2]
        print(self.img_viewer.stage)

        self.reset(is_first=self.first_launch)
        self.first_launch=False

    def sync_keys(self):#同步新键位设定
        self.btns1.sync_keys()
        self.btns2.sync_keys()

if(__name__=="__main__"):
    app=QApplication(sys.argv)
    main=Main()
    main.show()
    sys.exit(app.exec())
