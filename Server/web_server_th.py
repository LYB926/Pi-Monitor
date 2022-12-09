# 后端Flask使用库
from flask import Flask, render_template
from pyecharts import options as opts
from pyecharts.charts import Line, Grid
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
    # AF_INET表示网络层使用IP协议，SOCK_STREAM表示传输层使用TCP协议
    listenSocket = socket(AF_INET, SOCK_STREAM)
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
        global msg_temp
        global msg_humi
        msg = recv_msg.decode()             # 将收到的消息解码为字符串

        temp_msg = msg.split(',')
        msg_eCO2 = float(temp_msg[0])
        msg_TVOC = float(temp_msg[1])
        msg_temp = float(temp_msg[2])
        msg_humi = float(temp_msg[3])
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
data_temp = [0 for _ in range(32)]
data_humi = [0 for _ in range(32)]


def get_grid():
    timeIndex = strftime('%H:%M:%S')
    timeList.pop(0)
    timeList.append(timeIndex)

    dataNext_eCO2 = msg_eCO2
    data_eCO2.pop(0)
    data_eCO2.append(dataNext_eCO2)
    dataNext_TVOC = msg_TVOC
    data_TVOC.pop(0)
    data_TVOC.append(dataNext_TVOC)

    dataNext_temp = msg_temp
    data_temp.pop(0)
    data_temp.append(dataNext_temp)
    dataNext_humi = msg_humi
    data_humi.pop(0)
    data_humi.append(dataNext_humi)

    chartVOC = (
        Line()
        .add_xaxis(timeList)
        .add_yaxis("CO2EQ(ppm)", data_eCO2)
        .add_yaxis("TVOC(ppb)", data_TVOC)
        .set_global_opts(title_opts=opts.TitleOpts(title="eCO2 and TVOC", subtitle="空气中可挥发性有机物实时数据"))
    )
    chartTAH = (
        Line()
        .add_xaxis(timeList)
        .add_yaxis("Temperature(­°C)", data_temp)
        .add_yaxis("Humidity(%)", data_humi)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="环境温度和湿度", subtitle="温度湿度实时数据", pos_top="48%"),
            legend_opts=opts.LegendOpts(pos_top="48%"))
    )

    grid = (
        Grid()
        .add(chartVOC, grid_opts=opts.GridOpts(pos_bottom="60%"))
        .add(chartTAH, grid_opts=opts.GridOpts(pos_top="60%"))
        #.render("grid_vertical.html")
    )
    return grid

# def Line_base() -> Line:
#     timeIndex = strftime('%H:%M:%S')
#     timeList.pop(0)
#     timeList.append(timeIndex)

#     dataNext_eCO2 = msg_eCO2
#     data_eCO2.pop(0)
#     data_eCO2.append(dataNext_eCO2)

#     dataNext_TVOC = msg_TVOC
#     data_TVOC.pop(0)
#     data_TVOC.append(dataNext_TVOC)

#     c = (
#         Line()
#         .add_xaxis(timeList)
#         .add_yaxis("CO2EQ(ppm)", data_eCO2)
#         .add_yaxis("TVOC(ppb)", data_TVOC)
#         .set_global_opts(title_opts=opts.TitleOpts(title="eCO2 and TVOC", subtitle="空气中可挥发性有机物实时数据"))
#     )
#     return c


# def Line_base2() -> Line:
#     timeIndex = strftime('%H:%M:%S')
#     timeList.pop(0)
#     timeList.append(timeIndex)

#     dataNext_temp = msg_temp
#     data_temp.pop(0)
#     data_temp.append(dataNext_temp)

#     dataNext_humi = msg_humi
#     data_humi.pop(0)
#     data_humi.append(dataNext_humi)

#     c = (
#         Line()
#         .add_xaxis(timeList)
#         .add_yaxis("Temperature(­°C)", data_temp)
#         .add_yaxis("Humidity(%)", data_humi)
#         .set_global_opts(title_opts=opts.TitleOpts(title="环境温度和湿度", subtitle="温度湿度实时数据"))
#     )
#     return c


@app.route("/")
def index():
    return render_template("index_th.html")

@app.route("/updateChart")
def get_grid_upd():
    c = get_grid()
    return c.dump_options_with_quotes()

# @app.route("/updateChart")
# def get_Line_chart():
#     c = Line_base()
#     return c.dump_options_with_quotes()

if __name__ == "__main__":
    app.run()
