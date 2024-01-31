from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import os
from pathlib import *

META_DIR=Path(os.path.abspath("./"))
#META_IMG_DIR

class Stage(QWidget):
    signal=pyqtSignal(tuple)
    def __init__(self):
        self.META_IMG_DIR=META_DIR / "stages"
        super(Stage,self).__init__()
        self.setWindowTitle("选择模组")

        self.btn1=QPushButton("确定")
        self.btn1.clicked.connect(self.btn1_func)

        self.lb3=QLabel(self.stage_check("default"))
        
        self.combo_box=QComboBox()
        self.stage_list=self.get_stage_list()
        self.combo_box.addItems(self.stage_list)
        #self.signal.emit(("Nameless","default"))#初始化时先传出一个default,列表中的第0项
        self.combo_box.textActivated.connect(lambda:self.lb3.setText(self.stage_check(self.combo_box.currentText())))

        self.lb1=QLabel("请选择要用于游戏的图片模组：\n(它们都应以目录形式存放于“stages”目录中。)")

        self.lb2=QLabel("玩家ID：")
        self.name_line_edit=QLineEdit()
        self.name_line_edit.setText("Nameless")
        #self.name_line_edit.textEdited.connect(self.send_message)
        h_layout=QHBoxLayout()
        h_layout.addWidget(self.lb2)
        h_layout.addWidget(self.name_line_edit)

        v_layout=QVBoxLayout()
        v_layout.addLayout(h_layout)
        v_layout.addWidget(self.lb1)
        v_layout.addWidget(self.combo_box)
        v_layout.addWidget(self.lb3)
        v_layout.addWidget(self.btn1)
        self.setLayout(v_layout)

    def get_stage_list(self):
        stage_list=[i.name for i in self.META_IMG_DIR.iterdir() if(i.is_dir() and i.name!="default")]
        stage_list=["default"]+stage_list#这样保证default在第0项。
        return stage_list

    def send_message(self):
        player_name=self.name_line_edit.text()
        stage_name=self.combo_box.currentText()
        message=(player_name,stage_name)
        print(message)
        self.signal.emit(message)

    def btn1_func(self):
        self.send_message()
        self.close()

    def stage_check(self,stage_name):#检查所选关卡是否适合游戏
        stage_dir=self.META_IMG_DIR / stage_name
        categories=[i.name for i in stage_dir.iterdir() if(i.is_dir())]
        image_full_list=[]
        for i in categories:
            _dir=stage_dir / i
            images=list(_dir.glob("*"))
            image_full_list.append(images)
        print(image_full_list)
        
        def too_less():
            for i in image_full_list:
                if(len(i)<2):
                    return True
                else:
                    return False

        def have_default():
            return ("default" in [i.stem for i in stage_dir.iterdir() if(i.is_file())])

        if(not have_default()):
            self.btn1.setEnabled(False)
            return '<span style="color:red">这个模组不能进行游戏，模组内缺少特殊(default)图片。</span>'
        elif(len(categories)<2 or too_less()):
            self.btn1.setEnabled(True)
            return '<span style="color:orange">这个模组可能不适合游戏，图片分类过少或者某个分类里的图片过少。</span>'
        else:
            self.btn1.setEnabled(True)
            return '<span style="color:green">这个模组适合游戏。</span>'

if(__name__=="__main__"):
    META_DIR=Path(os.path.abspath("./../"))
    app=QApplication(sys.argv)
    a=Stage()
    a.show()
    print(a.get_stage_list())
    sys.exit(app.exec())
