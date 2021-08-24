#!/usr/bin/env python
#coding:utf8
#打包服务监听
import json

# 登陆命令
CMD_LOGON           = '100'
CMD_LOGON_SUCCEED   = '101'
CMD_REQUEST_FAILURE   = '102'
CMD_LOGON_FINISH    = '103'

# 打包命令
CMD_PK_APK          = '200'
CMD_PK_IPA          = '201'
CMD_PK_WEB          = '202'
CMD_PK_HOTUPDATE    = '203'
CMD_TASK_DONE       = '204'

CMD_PK_SUCCEED      = '210' # 打包成功 
CMD_PK_FAILURE      = '211' # 打包失败
CMD_PK_WAIT         = '212' # 打包任务 插入成功

# 查询任务状态
CMD_TEST            = '300'
CMD_CHECK           = '301'
CMD_DEL             = '302' # 删除任务

# 热更新批量处理
CMD_HOTUPDATE_BATCH = '400' # 批量处理

# 断开服务
CMD_EXIT            = '1100' # 退出

# 发送命令
def get_cmd_buf(cmd, buf_txt=''):
    cmd_buf = {'cmd':cmd}
    cmd_buf['buffer'] = buf_txt
    return json.dumps(cmd_buf)

# 获取登陆验证
def get_cmd_logon_buf(accounts, password):
    logon = {'accounts':accounts,'password':password}
    return get_cmd_buf(CMD_LOGON, logon)