import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from pathlib import Path
import os
import random

META_DIR=Path(os.path.abspath("./"))

class Img_viewer(QWidget):
    def __init__(self,stage_name=None):#初始化时需要传入stage名一次 ——现在不需要了，允许类现在允许先实例化再“set_stage_name”。2024-01-31 02:19:22
        super(Img_viewer,self).__init__()

        self.META_DIR=META_DIR
        self.META_IMG_DIR=self.META_DIR / "stages"
        self.stage=stage_name
        if(self.stage):self.play_list=self.make_play_list()
        
        self.lb1=QLabel()
        v_layout=QVBoxLayout()
        v_layout.addWidget(self.lb1)
        self.setLayout(v_layout)

        self.lb1.setFixedSize(800,600)#控件固定大小800x600 TODO:可以在设置里调节lb1大小。
        #self.lb1.setScaledContents(True)
        self.lb1.setAlignment(Qt.AlignCenter)#内容中置

    def set_stage_name(self,stage_name):#传入stage名
        self.stage=stage_name
        if(self.stage):self.play_list=self.make_play_list()
     
    def make_play_list(self):#解析stage中信息
        stg_dir=self.META_IMG_DIR / self.stage
        plist=[]

        #default
        default_img=list(stg_dir.glob("./default.*"))
        data_tuple=(self.stage,"default",str(default_img[0]))#(stage名,stage内组别,图片绝对路径)
        #print(default_img,data_tuple)
        plist.append(data_tuple)

        #其他组
        dirs=[i for i in stg_dir.iterdir() if(i.is_dir())]
        #print(dirs)
        for i in dirs:
            imgs=[x for x in i.iterdir() if(x.is_file())]
            for j in imgs:
                data_tuple=(self.stage,i.name,str(j))#(stage名,stage内组别,图片绝对路径)
                plist.append(data_tuple)
        
        return plist

    def play(self,input_data_tuple):
        pixmap=QPixmap(input_data_tuple[2])
        #if(pixmap.height()>self.lb1.height()):
        #   pixmap.scaledToHeight(self.lb1.height())#随高度变化
        #elif(pixmap.width()>self.lb1.width()):
        #    pixmap.scaledToWidth(self.lb1.width())#随宽度变化
        pixmap.scaled(QSize(self.lb1.width(),self.lb1.height()),aspectRatioMode=Qt.KeepAspectRatio)#尽可能让图片适应窗lb1大小
        self.lb1.setPixmap(pixmap)

    def choose_one(self):#在play_list中选择一张图片备展示，并返回信息元组。在外部使用时应先保存此信息元组，再传入play()方法使用。
        return random.choice(self.play_list)

# for test
if(__name__=="__main__"):
    META_DIR=Path(os.path.abspath("./")).parent

    app=QApplication(sys.argv)
    a=Img_viewer("default")
    #a.set_stage_name("default")
    play_img=a.choose_one()
    print(play_img)#for Dubug
    a.play(play_img)
    a.show()
    sys.exit(app.exec())
