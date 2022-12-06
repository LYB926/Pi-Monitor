# ===Pi-Monitor TCP Client ===
from socket import *
import time
from random import randrange

# 使用SGP30传感器库
import RTrobot_SGP30

# Socket和传感器的参数设置
IP = '127.0.0.1'
SERVER_PORT = 50000
BUFLEN = 512
SENSOR = RTrobot_SGP30.RTrobot_SGP30()

# 传感器初始化
eCO2 = 0
TVOC = 0
SGP30_Serial_ID = SENSOR.SGP30_Init()
if SGP30_Serial_ID == False:
    print("Fatal error: SGP30 sensor initialization failed.")
else:
    print("SGP30 sensor initialization register finished.")
    print("Ready to start data transfer via Socket...")
time.sleep(0.1)

# 实例化Socket对象，指名协议
dataSocket = socket(AF_INET, SOCK_STREAM)

# 连接Server端的Socket
dataSocket.connect((IP, SERVER_PORT))

while True:
    sensorResult = SENSOR.SGP30_Measure_Air_Quality()
    if sensorResult != False:
        eCO2 = sensorResult[0]
        TVOC = sensorResult[1]
        print("eCO2:%dppm\r\nTVOC:%dppb\r\n"%(sensorResult[0], sensorResult[1]))
    else:
        eCO2 = 0
        TVOC = 0
        print("Warning: Incorrect sensor data.")
    #toSendMsg = input('>>>' )            # 从终端读取用户输入
    #toSendMsg = str(randrange(0, 20))
    toSendMsg = str(eCO2)
    if toSendMsg == '114514':
        break
    dataSocket.send(toSendMsg.encode())  # 编码发送消息
    time.sleep(1)
    # recvMsg = dataSocket.recv(BUFLEN)    # 接收Server返回的消息
    # if not recvMsg:
    #    break
    # print(recvMsg.decode())              # 打印读取到的消息

dataSocket.close()