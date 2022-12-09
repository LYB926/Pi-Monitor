# ===Pi-Monitor TCP Client ===
from socket import *
import time
import threading

# 使用SGP30传感器库
import RTrobot_SGP30

# 使用UDP接收温度、湿度信息


def udp_sensor():
    #  1.创建socket套接字
    # AF_INET表示使用ipv4,默认不变，SOCK_DGRAM表示使用UDP通信协议
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    #  2.绑定端口port
    local_addr = ("169.254.76.130", 1234)  # 默认本机任何ip ，指定端口号7878
    udp_socket.bind(local_addr)  # 绑定端口

    #  3.收发数据
    while (1):
        recv_data = udp_socket.recvfrom(1024)  # 定义单次最大接收字节数
        #  4.打印数据
        recv_msg = recv_data[0]  # 接收的元组形式的数据有两个元素，第一个为发送信息
        send_addr = recv_data[1]  # 元组第二个元素为发信息方的ip以及port
        h0 = recv_msg[0]  # 湿度整数部分
        h1 = recv_msg[1]  # 湿度小数部分
        global humidity
        humidity = h0+0.1*h1
        # print("湿度为：",h)
        t0 = recv_msg[2]
        t1 = recv_msg[3] % 128
        global temperature
        temperature = t0+0.1*t1
        if recv_msg[3] >= 128:
            temperature = -temperature
        # print("温度为：",t)

    #  5.关闭套接字
    udp_socket.close()


udp_thread = threading.Thread(target=udp_sensor)
udp_thread.start()

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
        # print("eCO2:%dppm\r\nTVOC:%dppb\r\n" %
        #      (sensorResult[0], sensorResult[1]))
    else:
        eCO2 = 0
        TVOC = 0
        print("Warning: Incorrect sensor data.")

    toSendMsg = str(eCO2)+','+str(TVOC)+','+str(temperature)+','+str(humidity)
    print('Data: '+toSendMsg+' sent')
    if toSendMsg == '114514':
        break
    dataSocket.send(toSendMsg.encode())  # 编码发送消息
    time.sleep(1)
    # recvMsg = dataSocket.recv(BUFLEN)    # 接收Server返回的消息
    # if not recvMsg:
    #    break
    # print(recvMsg.decode())              # 打印读取到的消息

dataSocket.close()
