# ===Pi-Monitor TCP Client ===
from socket import *
import time
from random import randrange

# 读取传感器信息
import threading
import RTrobot_SGP30

# Socket和传感器的参数设置
IP = '127.0.0.1'
SERVER_PORT = 50000
BUFLEN = 512
SENSOR = RTrobot_SGP30.RTrobot_SGP30()

# 传感器初始化
SGP30_Serial_ID = SENSOR.SGP30_Init()
if SGP30_Serial_ID == False:
    print("Fatal error: SGP30 sensor initialization failed.")
else:
    print("SGP30 sensor initialization register finished.")
    print("Ready to start data transfer via Socket.")
time.sleep(0.1)

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