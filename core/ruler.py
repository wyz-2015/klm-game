#实现游戏规则的类与函数
#from PyQt
import time

class Ruler():
    def __init__(self):
        self.img_list=[]
        self.choice_list=[None]#对于第1张图无需记载其KLM选项
        self.test_time=15#测试次数,默认15
        
        self.start_time=None
        self.end_time=None

    def choice_read(self,choice):#用户在KLM中作选择的记录
        self.choice_list.append(choice)

    def img_read(self,data_tuple):
        self.img_list.append(data_tuple[1])

    def set_test_time(self,time):#设置测试次数
        self.test_time=time

    def make_answers(self):
        answers=[None]
        for i in range(1,len(self.img_list)-1):#不知为何需要-1
            if(self.img_list[i]=="default"):
                answers.append("M")
                continue
            elif(self.img_list[i]==self.img_list[i-1]):
                answers.append("K")
            else:
                answers.append("L")

        return answers

    def total(self):
        total_list=[]
        answers=self.make_answers()
        #print("{0}\n{1}".format(answers,self.choice_list))
        for i in range(1,len(answers)):
            if(answers[i]==self.choice_list[i]):
                total_list.append(1)
            else:
                total_list.append(0)

        #return (total_list,sum(total_list))
        return total_list
    
    def timer_start(self):#计时器开始计时
        self.start_time=time.monotonic_ns()/1e9#转化为s作单位

    def timer_end(self):
        self.end_time=time.monotonic_ns()/1e9

    def total_time(self):
        return self.end_time-self.start_time
