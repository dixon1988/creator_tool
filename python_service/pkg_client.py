#!/usr/bin/env python
#coding:utf8
# pip3 install websocket-client
import websocket
import json
import pkg_cmd

# 校验数据
class pkg_info:
    ws_url = ''
    ip = ''
    port = ''
    accounts = ''
    password = ''
    tk_lab = None

# 客户端数据
class pkg_client:
    loop = None
    ws = None
    is_connect = False
    is_logon = False
    buf_list = []
    task_buf = '无'

# 初始化数据
def on_client_init():
    global pkg_client
    pkg_client.loop = None
    pkg_client.ws = None
    pkg_client.is_connect = False
    pkg_client.is_logon = False
    pkg_client.buf_list = []
    pkg_client.task_buf = '无'
    
# 设置UI显示反馈
def set_ui_Label(tips):
    print(tips)
    if pkg_info.tk_lab:
        pkg_info.tk_lab.config(text=tips)

# 认证后、消息处理
def on_message(event, message):
    global pkg_client
    global pkg_info
    
    cred_dict = json.loads(message)
    
    recv_cmd = cred_dict['cmd']
    
    # 校验通过
    if recv_cmd==pkg_cmd.CMD_LOGON_SUCCEED:
        pkg_client.is_logon = True
        set_ui_Label('检验通过')
        on_list_buf_flush()
        return

    # 请求失败
    if recv_cmd==pkg_cmd.CMD_REQUEST_FAILURE:
        logon_error = cred_dict['buffer']
        set_ui_Label(logon_error)
        return
    
    # 任务查询
    if recv_cmd==pkg_cmd.CMD_CHECK:
        task_status = cred_dict['buffer']
        print("当前配置：")
        print(task_status['config'])
        
        task_list = task_status['list']
        print("任务列表：", len(task_list))
        for task in task_list[:]:
            print(task)
        return
    
    # 完成通知
    if recv_cmd==pkg_cmd.CMD_TASK_DONE:
        task_notify = cred_dict['buffer']
        print("任务完成：")
        print(task_notify)
        return
    
    # 未知命令
    print('未知命令:'+cmd)

# 资料认证
def send_auth():
    auth_buf = pkg_cmd.get_cmd_logon_buf(pkg_info.accounts, pkg_info.password)
    ret = pkg_client.ws.send(auth_buf)
    if ret!=None:
        return ('ret:' + ret)

# 发送命令
def send_message(cmd, p_dict):
    if pkg_client.is_connect==False:return '服务未链接'
    if pkg_client.is_logon==False:return '资料未认证'
    logo_buf = pkg_cmd.get_cmd_buf(cmd, p_dict)
    ret = pkg_client.ws.send(logo_buf)
    if ret!=None:
        return ('ret:' + ret)
    
# 发送命令
def send_buffer(buf_txt):
    if pkg_client.is_connect==False:return '服务未链接'
    if pkg_client.is_logon==False:return '资料未认证'
    ret = pkg_client.ws.send(buf_txt)
    if ret!=None:
        return ('ret:' + ret)
    
# 刷新消息
def on_list_buf_flush():
    global pkg_client
    if pkg_client.is_logon==False:
        print('身份校验未通过')
        return;
    count = len(pkg_client.buf_list)
    while count!=0:
        buf = pkg_client.buf_list.pop(0)
        send_buffer(buf)
        count = len(pkg_client.buf_list)
    
def on_error(event, error):
    set_ui_Label(error)
    print('on_error')
    
def on_close(event):
    global pkg_client
    on_client_init()
    print('on_close')

def on_open(event):
    global pkg_client
    
    # 标记登陆
    pkg_client.is_connect = True

    # 发送资料验证
    send_auth()
    
    # 刷新消息
    on_list_buf_flush()
    
# 关闭客户端
def stop_client():
    global pkg_client
    if pkg_client.ws:pkg_client.ws.close()
    # print('stop_client')

# 设置信息
def set_client_info(ip, port, accounts, password, tk_lab, event=None):
    global pkg_info
    global pkg_client
    
    # 添加消息
    pkg_client.buf_list.append(event)
    
    # 未链接、发起连接
    if pkg_client.is_connect==False:
        pkg_info.ip = ip
        pkg_info.port = port
        pkg_info.accounts = accounts
        pkg_info.password = password
        pkg_info.tk_lab = tk_lab
        pkg_info.ws_url = 'ws://' + ip + ":" + port

        print(pkg_info.ws_url)
        set_ui_Label('连接中...')
        
        websocket.enableTrace(True)
        
        ws = websocket.WebSocketApp(pkg_info.ws_url)
        ws.on_message = on_message
        ws.on_error = on_error
        ws.on_close = on_close
        ws.on_open = on_open
        pkg_client.ws = ws
        ws.run_forever()

    else:
        on_list_buf_flush()

    return True
    