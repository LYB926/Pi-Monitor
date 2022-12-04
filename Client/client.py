# === TCP Client ===
from socket import *
import time
from random import randrange

IP = '139.224.246.156'
SERVER_PORT = 50000
BUFLEN = 512

# 实例化Socket对象，指名协议
dataSocket = socket(AF_INET, SOCK_STREAM)

# 连接Server端的Socket
dataSocket.connect((IP, SERVER_PORT))

while True:
    #toSendMsg = input('>>>' )            # 从终端读取用户输入
    toSendMsg = str(randrange(0, 20))
    if toSendMsg == '114514':
        break
    dataSocket.send(toSendMsg.encode())  # 编码发送消息
    time.sleep(1)
    # recvMsg = dataSocket.recv(BUFLEN)    # 接收Server返回的消息
    # if not recvMsg:
    #    break
    # print(recvMsg.decode())              # 打印读取到的消息

dataSocket.close()