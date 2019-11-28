import socket  # 导入 socket 模块
import threading
import json
import time

from Exam import Exam

from cmd import Cmd

ip='127.0.0.1'
port = 8712

exams=[]

__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
__id = None
__nickname = None
__address=(ip,port)


def start():
    """
    socket连接
    """
    __socket.connect(__address)

def login(get_nickname):
    """
    登录考试系统

    """
    nickname = get_nickname

    # 将昵称发送给服务器，获取用户id
    __socket.send(json.dumps({
        'type': 'login',
        'nickname': nickname
    }).encode())
    # 尝试接受数据
    # noinspection PyBroadException
    try:
        buffer =__socket.recv(1024).decode()
        obj = json.loads(buffer)
        if obj['id']:
            global __nickname
            global __id
            __nickname = nickname
            __id = obj['id']
            print('[Client] 成功登录到考试系统')

            # 开启子线程用于接受数据
            thread = threading.Thread(target=__receive_message_thread,args=(exams,))
            thread.setDaemon(True)
            thread.start()
        else:
            print('[Client] 无法登录到考试系统')
    except Exception:
        print('[Client] 无法从服务器获取数据（服务器故障）')


def startexam():
    '''
    开始考试
    :param arg:
    :return:
    '''
    print("即将开始考试，读取试卷内容中。")
    __socket.send(json.dumps({
        'type': 'startexam',
        'sender_id': __id,
        'message': 'startexam'
    }).encode())

    while  exams==[]:

        time.sleep(1)


def okexam(answers):
    """
    提交试卷
    :param answers: 选项
    :return: 分数
    """

    score=0


    for i in range(len(answers)):
        if (answers[i] == exams[i].Answer):
            score = score + 100 / len(exams)

    print(score)
    __socket.send(json.dumps({
        'type': 'examscore',
        'sender_id': __id,
        'message': score
    }).encode())

    return score


def __receive_message_thread(exams):
    """
    接受消息线程
    """
    while True:
        # noinspection PyBroadException
        try:
            buffer = __socket.recv(102400).decode()

            objs = json.loads(buffer)

            if (objs['type'] == 'exam'):

                for obj in objs['message']:
                    exam = Exam(str(obj['Text']),
                               str(obj['A']),
                               str(obj['B']),
                               str(obj['C']),
                               str(obj['D']),
                               str(obj['Answer']))
                    exams.append(exam)
                    #print(str(obj['Text']+obj['A']+obj['B']+obj['C']+obj['D']+obj['Answer']))


            elif (objs['type'] == 'paper'):
                print("收到试卷内容")
                print(objs['message']["Title"])
        except Exception:
            print('[Client] 无法从服务器获取数据(接收的message格式有问题)')