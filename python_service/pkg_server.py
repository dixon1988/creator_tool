#!/usr/bin/env python
#coding:utf8
# pip3 install websocket-server
import os
import sys
import json

import websocket

import pkg_cmd
import pkg_task

from websocket_server import WebsocketServer
 
# import path
fatherdir = os.path.dirname(os.path.abspath(__file__))
fatherdir = os.path.abspath(os.path.join(fatherdir, ".."))
sys.path.append(fatherdir+'/python_pkg')

import tool
 
info = tool.get_server_info()
listen_ip = info['ip']
listen_port = info['port']
 
# 当新的客户端连接时会提示
def new_client(client, server):
    print( "new_client-id:%s " % client['id'] )
 
# 当旧的客户端离开
def client_left(client, server):
    print( "client %s leave"%(client['id']) )
 
# 接收客户端的信息。
def message_received(client, server, message):
    pkg_task.message_received(client, server, message)
    
# 启动服务
if __name__ == '__main__':
    server = WebsocketServer(listen_port, listen_ip)
    server.set_fn_new_client(new_client)
    server.set_fn_client_left(client_left)
    server.set_fn_message_received(message_received)
    server.run_forever()
