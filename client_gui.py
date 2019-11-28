import tkinter as tk  # 使用Tkinter前需要先导入
import threading
import time
import client_gui_core as client_core


"""
窗口创建以及窗口属性设置
"""
window = tk.Tk()

window.title('在线考试系统')

window.geometry('300x200')

gui_exams = [] #试卷题目列表
i = 0 #当前显示得题目的序号
answers=[] #保存答案
var = tk.StringVar()
examtime=0 #考试倒计时


def link():
    """
    socket连接
    按钮 连接 按下时触发
    """
    client_core.ip =str(e1.get())
    client_core.port=int(e3.get())
    client_core.start()


def login():
    """
    登录
    """
    var = e2.get()
    client_core.login(str(var))


def showexam(i, exams):
    """
    显示考题
    :param i: 题目序号
    :param exams: 题目数组

    """
    l1.config(text=exams[i].Text)
    r1.config(text=exams[i].A)
    r2.config(text=exams[i].B)
    r3.config(text=exams[i].C)
    r4.config(text=exams[i].D)
    l2.config(text=str(i+1)+"/"+str(len(gui_exams)))


def start_exam_time():
    """
    倒计时子线程
    :return:
    """
    while True:
        global examtime
        examtime=examtime-1
        l3.config(text=str(examtime))
        time.sleep(1)
        if examtime==0:
            #交卷
            ok()
            break


def startexam():
    """
    开始考试
    :return:
    """
    global i
    global gui_exams

    #发出考试请求
    client_core.startexam()

    #读取试卷信息
    gui_exams=client_core.exams

    showexam(i,gui_exams)
    window.geometry('300x350')

    #倒计时子线程
    global examtime
    examtime = len(gui_exams) * 30
    thread = threading.Thread(target=start_exam_time)
    thread.setDaemon(True)
    thread.start()

    e1.pack_forget()
    e3.pack_forget()
    b1.pack_forget()
    e2.pack_forget()
    b2.pack_forget()
    b3.pack_forget()

    #生成答案位
    for j in gui_exams:
        answers.append("")

def last():
    """
    上一题
    :return:
    """

    global i
    global gui_exams
    global answers
    a = str(var.get())

    answers[i] = a

    if i != 0:
        i = i-1

    showexam(i, gui_exams)

def next():
    """
    下一题
    :return:
    """

    global i
    global gui_exams
    global answers
    a = str(var.get())
    answers[i] = a

    if i != len(gui_exams)-1:
        i = i + 1

    showexam(i, gui_exams)


def print_selection():
    """
    按下选项
    :return:
    """
    global i
    global answers
    a=str(var.get())

    answers[i] = a


def ok():
    """
    提交试卷
    :return:
    """
    global answers
    score=client_core.okexam(answers)
    l_tip.config(text='你考了'+str(int(score)))
    b6.pack_forget()


v1 = tk.StringVar(window, value='127.0.0.1')
e1 = tk.Entry(window, show=None, font=('Arial', 12), textvariable=v1)

v3 = tk.StringVar(window, value='8712')
e3 = tk.Entry(window, show=None, font=('Arial', 12), textvariable=v3)

v2 = tk.StringVar(window, value='Jack')
e2 = tk.Entry(window, show=None, font=('Arial', 12), textvariable=v2)


b1 = tk.Button(window, text='连接', width=10,
               height=1, command=link)

b2 = tk.Button(window, text='登录', width=10,
               height=1, command=login)

b3 = tk.Button(window,text='开始考试', width=10,
               height=1, command=startexam)

b4 = tk.Button(window,text='上一题', width=10,
               height=1, command=last)

b5 = tk.Button(window,text='下一题', width=10,
               height=1, command=next)

b6 = tk.Button(window,text='交卷', width=10,
               height=1, command=ok)

l1 =  tk.Label(window, text=' ', font=('Arial', 12),  wraplength=200,
 anchor='w')
l2 =  tk.Label(window, text=' ', height=1, anchor='w')
l3 =  tk.Label(window, text=' ', height=1, anchor='w')


r1 = tk.Radiobutton(window, text='Option A', variable=var, value='A', command=print_selection)

r2 = tk.Radiobutton(window, text='Option B', variable=var, value='B', command=print_selection)

r3 = tk.Radiobutton(window, text='Option C', variable=var, value='C', command=print_selection)

r4 = tk.Radiobutton(window, text='Option D', variable=var, value='D', command=print_selection)


e1.pack()
e3.pack()
b1.pack()
e2.pack()
b2.pack()
b3.pack()
l3.pack()
l2.pack()
l1.pack()
r1.pack()
r2.pack()
r3.pack()
r4.pack()
b4.pack()
b5.pack()
b6.pack()

l_tip =  tk.Label(window, text='',  height=4, wraplength=200,
 anchor='w')
l_tip.pack()

window.mainloop()