# Pi-Monitor
![Pi-Monitor.png](http://wisp.fun/wp-content/uploads/2022/12/Pi-Monitor.png)
## 简介
Pi-Monitor 使用安装在树莓派上的 SGP30 气体传感器收集当前环境空气中的 VOC（挥发性有机化合物）和 CO<sub>2</sub>EQ（二氧化碳当量）数据，并且将这些数据经由 Socket 实时发送到服务器，服务器端使用 [Flask](https://github.com/pallets/flask) 框架和 [pyecharts](https://github.com/pyecharts/pyecharts) 库实时显示空气质量数据。
## 安装和使用
### 服务器端
安装所需依赖：
```
pip3 install -r requirements.txt
```
#### 本地部署
修改`Server/templates/index.html`中`fetchData()`函数的`url`为`http://localhost/updateChart`。

运行`server.py`使 Flask 服务在5000端口运行，现在只需要访问 http://localhost:5000 即可查看数据展示页面。
#### 服务器部署
假定服务器的域名为`somedomain.com`：

修改`Server/templates/index.html`中`fetchData()`函数的`url`为`"http://somedomain.com/updateChart"`，访问 http://somedomain.com:5000 即可查看数据展示页面。

如果不想通过域名+端口的方式访问或者服务器只能开放80端口为 HTTP 端口，可以使用反向代理将 Flask 服务代理到指定 URL，以 Debian/Apache2 为例：

首先，启用 Apache 的 HTTP 代理模块：
```
sudo a2enmod proxy proxy_http
```
编辑 Apache 的配置文件`/etc/apache2/apache2.conf`，在文件末尾增加代理设置将 localhost:5000 的 Flask 服务代理到 somedomain.com/monitor：
```
ProxyPass /monitor http://localhost:5000
ProxyPassReverse /monitor http://localhost:5000  
ProxyPass /updateChart http://localhost:5000/updateChart 
ProxyPassReverse /updateChart http://localhost:5000/updateChart  
```
重新启动 Apache 服务：
```
sudo service apache2 restart
```
访问 http://somedomain.com/monitor 即可查看数据展示页面。
### 树莓派端
SGP30 传感器使用 I2C 总线与树莓派连接，接线如下：
|  Raspberry Pi Board GPIO  | SGP30 Sensor  |
|  ----  | ----  |
| GPIO.3(SDA)  | SDA |
| GPIO.4(5V)  | VCC |
| GPIO.5(SCL)  | SCL |
| GPIO.6(GND)  | GND |

并且在树莓派上安装I2C包：
```
sudo apt-get install -y python3-smbus
sudo apt-get install -y i2c-tools
```
修改`Client/client.py`中第9行的服务器IP为你服务器的IP地址，运行即可：
```
python3 client.py
```
在运行代码时，请确保先运行服务器端，再运行树莓派端。