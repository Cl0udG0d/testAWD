# import socket
# # 建立一个服务端
# server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# server.bind(('localhost',19999)) #绑定要监听的端口
# server.listen(5) #开始监听 表示可以使用五个链接排队
# while True:# conn就是客户端链接过来而在服务端为期生成的一个链接实例
#     conn,addr = server.accept() #等待链接,多个链接的时候就会出现问题,其实返回了两个值
#     print(conn,addr)
#     while True:
#         try:
#             data = conn.recv(1024)  #接收数据
#             print('recive:',data.decode()) #打印接收到的数据
#             conn.send(data.upper()) #然后再发送数据
#         except Exception as e:
#             print('关闭了正在占线的链接！')
#             print(e)
#             break
#     conn.close()

import socket
import json
sendData = {
  "Type":"INIT",
  "Data":{
          "Title":"aaa",
          "Team":[{}],
          "Time":1000,
          "Round":10,
    }
}
BUF_SIZE = 1024
host = 'localhost'
port = 19999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(1)  # 接收的连接数
client, address = server.accept()  # 因为设置了接收连接数为1，所以不需要放在循环中接收
while True:  # 循环收发数据包，长连接
    data = client.recv(BUF_SIZE)
    print(data.decode())  # python3 要使用decode
    # client.close() #连接不断开，长连接
    client.send(bytes(repr(json.dumps(sendData)).encode('utf-8')))