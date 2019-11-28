"""
题目：开发一个在线考试系统，要求如下：
a) 采用Ｃ／S模式架构
b) 服务器能够随机选题，分发试题，控制客户端的考试时间、统计成绩等。
c) 不同的客户端获取的试题不同，并在客户端显示考试成绩。
"""

import socket  # 导入 socket 模块
import threading
import json

import random
from Exam import Exam


ADDRESS = ('127.0.0.1', 8712)  # 绑定地址


class Server:
    """
    服务器类
    """
    def __init__(self):
        """
        构造
        """
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__connections = list()
        self.__nicknames = list()
        self.__userstatus=list()

    def __user_thread(self, user_id):
        """
        用户子线程
        :param user_id: 用户id
        """
        connection = self.__connections[user_id]
        nickname = self.__nicknames[user_id]
        print('[Server] 用户', user_id, nickname, '进入考试系统')


        # 侦听
        while True:
            # noinspection PyBroadException
            try:

                buffer = connection.recv(1024).decode()
                # 解析成json数据
                obj = json.loads(buffer)
                # 如果是广播指令
                if obj['type'] == 'broadcast':
                    print(str(obj['message']))
                    self.__broadcast(obj['sender_id'], obj['message'])
                elif obj['type'] == "startexam":
                    print('用户'+self.__nicknames[obj['sender_id']]+"请求开始考试")
                    exam1 = Exam('企鹅是什么颜色', '红色', '黑白', '绿色', '蓝色', 'B')
                    exam2 = Exam('万有引力是谁发现的', '牛顿', '爱因斯坦', '达芬奇', '哥德尔', 'A')
                    exam3 = Exam('太阳是什么颜色', '红色', '黑白', '黄色', '蓝色', 'C')
                    exams = [exam1.to_json(), exam2.to_json(), exam3.to_json()]
                    examss = [exam1.to_json(), exam2.to_json(), exam3.to_json()]
                    for i in range(0,100):
                        if i%4 == 0:
                            answer='A'
                        elif i%4 == 1:
                            answer='B'
                        elif i%4 == 2:
                            answer='C'
                        elif i%4 == 3:
                            answer='D'
                        exams.append(Exam('这是第'+str(i)+'道题题题题题题题题题题题题题题题题题题题题题题题题题',
                                          'A选项',
                                          'B选项',
                                          'C选项',
                                          'D选项',
                                          answer).to_json())

                    resultList = []  # 用于存放结果的List
                    A = 0  # 最小随机数
                    B = len(exams)-1  # 最大随机数
                    COUNT = 20
                    resultList = random.sample(range(A, B + 1), COUNT)
                    send_exams=[]
                    for i in resultList:
                        send_exams.append(exams[i])

                    self.__send_message(user_id=obj['sender_id'], message=send_exams, type="exam")


                elif obj['type'] == 'examscore':
                    print('用户' + self.__nicknames[obj['sender_id']] + "考了"+str(obj['message']))
                    self.__userstatus[int(obj['sender_id'])-1]['score']=int(obj['message'])
                else:
                    print('[Server] 无法解析json数据包:', connection.getsockname(), connection.fileno())
            except Exception:
                print('[Server] 连接失效:', connection.getsockname(), connection.fileno())
                self.__connections[user_id].close()
                self.__connections[user_id] = None
                self.__nicknames[user_id] = None

    def __broadcast(self, user_id=0, message=''):
        """
        广播
        :param user_id: 用户id(0为系统)
        :param message: 广播内容
        """
        for i in range(1, len(self.__connections)):
            if user_id != i:
                self.__connections[i].send(json.dumps({
                    'sender_id': user_id,
                    'sender_nickname': self.__nicknames[user_id],
                    'message': message
                }).encode())

    def __send_message(self, user_id=0, message=None, type="default"):
        """
        广播
        :param user_id: 接收message的用户id(0为系统)
        :param message: 广播内容
        :param type: 广播种类
        """
        if(type == "exam"):
            self.__connections[user_id].send(json.dumps({'message':message,'type':type}).encode())

    def __accept_client(self):

        # 开始侦听
        while True:
            connection, address = self.__socket.accept()
            print('[Server] 收到一个新连接', connection.getsockname(), connection.fileno())

            # 尝试接受数据
            # noinspection PyBroadException
            try:
                buffer = connection.recv(1024).decode()
                # 解析成json数据
                obj = json.loads(buffer)
                # 如果是连接指令，那么则返回一个新的用户编号，接收用户连接
                if obj['type'] == 'login':
                    self.__connections.append(connection)
                    self.__nicknames.append(obj['nickname'])
                    self.__userstatus.append({"userid":len(self.__connections) - 1,
                                              "exam":False,
                                              "score":0,
                                              "start_exam_time":30})
                    connection.send(json.dumps({
                        'id': len(self.__connections) - 1
                    }).encode())

                    # 开辟一个新的线程
                    thread = threading.Thread(target=self.__user_thread, args=(len(self.__connections) - 1,))
                    thread.setDaemon(True)
                    thread.start()
                else:
                    print('[Server] 无法解析json数据包:', connection.getsockname(), connection.fileno())
            except Exception:
                print('[Server] 无法接受数据:', connection.getsockname(), connection.fileno())


    def start(self):
        """
        启动服务器
        """
        # 绑定端口
        self.__socket.bind(ADDRESS)
        # 启用监听
        self.__socket.listen(10)
        print('[Server] 服务器正在运行......')

        # 清空连接
        self.__connections.clear()
        self.__nicknames.clear()
        self.__connections.append(None)
        self.__nicknames.append('System')

        # 新开一个线程，用于接收新连接
        thread = threading.Thread(target=self.__accept_client)
        thread.setDaemon(True)
        thread.start()

        #主线程
        while True:
            cmd=input("输入1：查看已进入考试系统人数\n"
                      "输入2：列出名单\n"
                      "输入3：成绩单\n"
                      "")
            if cmd == '1':
                print("--------------------------")
                print("当前在线人数：", len(self.__connections)-1)
                print("--------------------------")
            elif cmd == '2':
                print("--------------------------")
                for i in self.__nicknames:
                    print(i)
                print("--------------------------")
            elif cmd == '3':
                print("--------------------------")
                for i in self.__userstatus:
                   print(self.__nicknames[i['userid']]+"     "+str(i['score']))
                print("--------------------------")

