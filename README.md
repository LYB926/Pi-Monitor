# Pi-Monitor
![Pi-Monitor.png](http://wisp.fun/wp-content/uploads/2022/12/Pi-Monitor.png)

Pi-Monitor 使用安装在树莓派上的SGP30气体传感器收集当前环境空气中的VOC（挥发性有机化合物）和CO<sub>2</sub>EQ（二氧化碳当量）数据，并且将这些数据经由 Socket 实时发送到服务器，服务器端使用 [Flask](https://github.com/pallets/flask) 框架和 [pyecharts](https://github.com/pyecharts/pyecharts) 库实时显示空气质量数据。