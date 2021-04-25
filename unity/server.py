import json
import logging
from websocket_server import WebsocketServer


data={
    "Type":"init",
    "Data":{
        "Title":"Test",
        "Team":[
            {
                "Id":1,
                "Name":"team1",
                "Score":"100",
                "Rank":"100",

            },
            {
                "Id":2,
                "Name":"team2",
                "Score":"100",
                "Rank":"100",

            },
            {
                "Id":3,
                "Name":"team3",
                "Score":"100",
                "Rank":"100",

            }
        ],
        "Time":"100",
        "Round":"10",
    }
}
def new_client(client, server):
    print("Client(%d) has joined." % client['id'])


def client_left(client, server):
    print("Client(%d) disconnected" % client['id'])


def message_back(client, server, message):
    # 这里的message参数就是客户端传进来的内容
    print("Client(%d) said: %s" % (client['id'], message))
    # 这里可以对message进行各种处理
    # result = "服务器已经收到消息了..." + message
    # 将处理后的数据再返回给客户端
    server.send_message(client, bytes(repr(json.dumps(data)).encode('utf-8')))


# 新建一个WebsocketServer对象，第一个参数是端口号，第二个参数是host
# 如果host为空，则默认为本机IP
server = WebsocketServer(19999, host='127.0.0.1')
# 设置当有新客户端接入时的动作
server.set_fn_new_client(new_client)
# 设置当有客户端断开时的动作
server.set_fn_client_left(client_left)
# 设置当接收到某个客户端发送的消息后的操作
server.set_fn_message_received(message_back)
# 设置服务一直运行
server.run_forever()