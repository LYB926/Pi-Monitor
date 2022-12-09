# 后端Flask使用库
from flask import Flask, render_template
from pyecharts import options as opts
from pyecharts.charts import Line
from time import strftime
from flask_cors import CORS

# Socket库和配置 
import threading
from socket import *
# msg_eCO2 = 0
def socket_thr():
    IP = ''         # 主机地址为空，表示绑定本机所有网络接口IP地址
    PORT = 50000    # 服务端口号
    BUFLEN = 512    # Socket缓冲区大小
    # 实例化Socket对象
    listenSocket = socket(AF_INET, SOCK_STREAM) # AF_INET表示网络层使用IP协议，SOCK_STREAM表示传输层使用TCP协议
    listenSocket.bind((IP, PORT))               # 绑定IP和端口
    # 使Socket进入监听状态，最多接受8个等待连接的Client
    listenSocket.listen(8)
    print(f'Server listening at port {PORT}')

    dataSocket, addr = listenSocket.accept()
    print('Client connected:', addr)

    while True:
        recv_msg = dataSocket.recv(BUFLEN)  # 读取Client发送的消息
        if not recv_msg:                    # 如果消息为空表示连接已关闭，退出循环    
            break
        
        global msg_eCO2
        global msg_TVOC
        msg = recv_msg.decode()             # 将收到的消息解码为字符串

        #temp_msg = msg.split(',',1)
        temp_msg = msg.split(',')
        msg_eCO2 = float(temp_msg[0])
        msg_TVOC = float(temp_msg[1])
        print(f'Message received: {msg}')
        # 编码，向Client发送消息
        # dataSocket.send(f'Server message received: {msg}'.encode())

    # 调用close()关闭Socket
    dataSocket.close()
    listenSocket.close()

socket_thread = threading.Thread(target=socket_thr)
socket_thread.start()


# 后端工作函数
app = Flask(__name__, static_folder="templates")
CORS(app, resources=r'/*')
timeList = [strftime('%H:%M:%S') for __ in range(32)]
data_eCO2 = [0 for _ in range(32)]
data_TVOC = [0 for _ in range(32)]

def Line_base() -> Line:
    timeIndex = strftime('%H:%M:%S')
    timeList.pop(0)
    timeList.append(timeIndex)

    dataNext_eCO2 = msg_eCO2
    data_eCO2.pop(0)
    data_eCO2.append(dataNext_eCO2)

    dataNext_TVOC = msg_TVOC
    data_TVOC.pop(0)
    data_TVOC.append(dataNext_TVOC)

    c = (
        Line()
        .add_xaxis(timeList)
        .add_yaxis("CO2EQ(ppm)", data_eCO2)
        .add_yaxis("TVOC(ppb)", data_TVOC)
        .set_global_opts(title_opts=opts.TitleOpts(title="Pi-Monitor", subtitle="空气质量实时数据"))
    )
    return c


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/updateChart")
def get_Line_chart():
    c = Line_base()
    return c.dump_options_with_quotes()


if __name__ == "__main__":
    app.run()