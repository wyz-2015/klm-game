import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os

from core.img_viewer import *
from core.buttons import *

class Main(QWidget):
    def __init__(self):
        super(Main,self).__init__()

        self.img_viewer=Img_viewer("default")
        choice=self.img_viewer.choose_one()
        print(choice)
        self.img_viewer.play(choice)

        self.btns1=KLM_buttons()
        self.btns1.signal.connect(self.change_img)

        v_layout=QVBoxLayout()
        v_layout.addWidget(self.img_viewer)
        v_layout.addWidget(self.btns1)
        self.setLayout(v_layout)

    def change_img(self):
        choice=self.img_viewer.choose_one()
        print(choice)
        self.img_viewer.play(choice)

if(__name__=="__main__"):
    app=QApplication(sys.argv)
    main=Main()
    main.show()
    sys.exit(app.exec())
