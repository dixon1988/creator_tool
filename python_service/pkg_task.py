#!/usr/bin/env python
#coding:utf8

import os
import sys
import json
import time
import threading
import logging
import shutil

import pkg_cmd
import pkg_task_run
import ftp_server
import oss_server
import start_pkg
import start_config

# import path
fatherdir = os.path.dirname(os.path.abspath(__file__))
fatherdir = os.path.abspath(os.path.join(fatherdir, ".."))
sys.path.append(fatherdir+'/python_pkg')

import tool

# 历史执行任务列表
g_lishi_list = []

# 任务列表，仅支持单任务
task_list = []
pkgtask_id = 0

# 执行列表上传
def on_ftp_upload(task):
    # task_channel = task['task_channel']
    print("暂未调试ftp上传，暂时不支持！")
    return;
    # cmd_pk = task['pkg_cmd']
    # out_root = task['ret_out_path']
    # out_root = 'e:/work/tools/zjdev_102/Sup_ZhenJin_dev/2.2.6/105011'
    
    # 压缩目录zip
    # out_file = out_root + '.zip'
    # tool.zip_dir(out_root, out_file)

    # ipa + apk 上传
    if cmd_pk==pkg_cmd.CMD_PK_APK or cmd_pk==pkg_cmd.CMD_PK_IPA:
        print("安装包 暂未上传ftp")
        return True

    # 热更上传
    if cmd_pk==pkg_cmd.CMD_PK_HOTUPDATE or cmd_pk==pkg_cmd.CMD_PK_WEB:
        up_ret = ftp_server.start_hotUpdate(task, out_root)
        if up_ret!=True:return up_ret
        
    return True
    
# oss上传
def on_oss_upload(task):
    print(task)
    
    cmd_pk = task['pkg_cmd']
    
    # 热更上传
    if cmd_pk==pkg_cmd.CMD_PK_HOTUPDATE or cmd_pk==pkg_cmd.CMD_PK_WEB:
        local_root = task['ret_out_path']
        upload_root = task['ret_path_root']
        up_ret = oss_server.startUpload(local_root, upload_root)
        if up_ret!=True:return up_ret
        
# 共享上传
def on_share_upload(task):
    pkg_json = tool.get_server_info()
    
    src_file_root = task['ret_out_path']
    src_path_root = task['ret_path_root']
    
    dst_file_root = pkg_json['win_share_path']
    dst_path_root = dst_file_root + '/' + src_path_root
    if tool.IsIos:dst_file_root = pkg_json['mac_share_path'];

    # copy 上传共享
    tool.copydir(src_file_root, dst_path_root)
    
    return True

# 执行打包
def on_pkg_start(event=None):
    global task_list
    global pkgtask_id
    
    task_dict = task_list[0]
    task_str_id = str(task_dict['pkgtask_id'])
    task_cmd = task_dict['pkg_cmd']
    print('task_start:pkgtask_id='+task_str_id+'===============================================')
    
    try:
        pkg_ret = pkg_task_run.pkg(task_dict)
        
        # 判定失败
        if pkg_ret!=True:
            task_dict['pkg_ret']='0'
            print('pkg_ret:'+pkg_ret)
            print('task_cmd:'+task_cmd+' failure')
        else:
            task_dict['pkg_ret']='1'
            task_dict['ret_out_path']=start_pkg.g_out_file_path
            task_dict['ret_path_root']=start_pkg.g_out_path_root
            print('task_cmd:'+task_cmd+' succeed')
        
    except Exception as error:
        task_dict['pkg_ret']='0'
        print(error)
        print('task_cmd:'+task_cmd+'-failure')
    
    # 打包完成
    on_pkg_doned(task_dict)

# 打包任务完成
def on_pkg_doned(task_dict):
    global g_lishi_list
    global task_list
    
    # 完成日志
    out_put = {}
    # 执行类型
    out_put['cmd'] = task_dict['pkg_cmd']
    
    # 完成日志
    if task_dict['pkg_ret']=='1':
        out_put['pkg_ret']='成功'
    else:
        out_put['pkg_ret']='失败'
        
    # 完成信息
    out_put['g_config_id'] = task_dict['g_config_id']
    out_put['g_version'] = task_dict['g_version']
    out_put['g_update_hot_version'] = task_dict['g_update_hot_version']
    out_put['pkgtask_id'] = task_dict['pkgtask_id']
        
    # 是否上传共享
    g_is_share_up = task_dict['g_is_share_up']
    if g_is_share_up==1:
        on_share_upload(task_dict)
        out_put['g_is_share_up:'] = 'shareup upload succeed'
        
    # 是否上传ftp
    g_is_ftp_up = task_dict['g_is_ftp_up']
    if g_is_ftp_up==1:
        on_ftp_upload(task_dict)
        out_put['g_is_ftp_up:'] = 'ftp upload succeed'
    
    # 是否上传oss
    g_is_oss_up = task_dict['g_is_oss_up']
    if g_is_oss_up==1:
        on_oss_upload(task_dict)
        out_put['g_is_oss_up:'] = 'oss upload succeed'
    
    # 移除任务
    task_list.clear()
    
    try:
        server = task_dict['server']
        client = task_dict['client']
        buf = pkg_cmd.get_cmd_buf(pkg_cmd.CMD_TASK_DONE, out_put)
        server.send_message(client, buf)
    except Exception as error:
        print(error)
        print('通知失败')
    print(out_put)

# 执行任务
def on_pkg_run(client, server, task_dict=None):
    global task_list
    global pkgtask_id

    # 添加任务
    if len(task_list)==0:
        if task_dict:
            is_task_add = task_dict['g_task_add']
            is_task_first = task_dict['g_task_first']
            task_dict['run']='0'
            task_dict['pkgtask_id']=pkgtask_id
            task_list.append(task_dict)
            if pkgtask_id>1000000:
                pkgtask_id=0
            else:
                pkgtask_id+=1
                
        # 执行任务
        task_0 = task_list[0]
        task_0['run']='1'
        t=threading.Thread(target=on_pkg_start, args=[])
        t.setDaemon(True)
        t.start()
    # 添加失败，已有任务执行
    else:
        buf = pkg_cmd.get_cmd_buf(pkg_cmd.CMD_REQUEST_FAILURE,'当前任务未结束，请稍后再试！')
        server.send_message(client, buf)
    
# 校验资料
def on_cmd_logon_ret(client, server, cred_dict):
    info = tool.get_server_info()
    conf_acct = info['accounts']
    conf_pass = info['password']
    
    logon = cred_dict['buffer']
    buf_acct = logon['accounts']
    buf_pass = logon['password']
    
    # 校验成功
    if buf_acct==conf_acct and buf_pass==conf_pass:
        buf = pkg_cmd.get_cmd_buf(pkg_cmd.CMD_LOGON_SUCCEED)
        server.send_message(client, buf)
        print('校验成功')
        
    # 校验失败
    else:
        buf = pkg_cmd.get_cmd_buf(pkg_cmd.CMD_REQUEST_FAILURE,'账号校验失败，请检查账号信息！')
        server.send_message(client, buf)
        
        handler=client['handler']
        handler.keep_alive=False
        print('校验失败')
        
# 获取任务列表
def get_task_sort(task_dict):
    task_statue = {}
    config_id = task_dict['g_config_id']
    pk_config = start_config.get_conf_obj(config_id)
    
    # 当前配置状态
    task_item = {}
    task_item['g_config_id'] = pk_config['g_config_id']
    task_item['g_version'] = pk_config['g_version']
    task_item['g_update_hot_version'] = pk_config['g_update_hot_version']
    task_statue['config'] = task_item;
    
    task_statue['list'] = []
    for task in task_list:
        pkgtask_id = str(task['pkgtask_id'])
        task_cmd = task['pkg_cmd']
        task_run = task['run']
        
        task_item = {}
        task_item['pkgtask_id'] = pkgtask_id
        task_item['run'] = task_run
        
        if task_cmd==pkg_cmd.CMD_PK_APK:task_item['cmd']='CMD_PK_APK'
        if task_cmd==pkg_cmd.CMD_PK_IPA:task_item['cmd']='CMD_PK_IPA'
        if task_cmd==pkg_cmd.CMD_PK_WEB:task_item['cmd']='CMD_PK_WEB'
        if task_cmd==pkg_cmd.CMD_PK_HOTUPDATE:task_item['cmd']='CMD_PK_HOTUPDATE'
        task_statue['list'].append(task_item)
        
    return task_statue

# 任务排序
def on_task_sort(cmd, task_dict):
    client = task_dict['client']
    server = task_dict['server']
    
    # 任务-任务查询
    if cmd==pkg_cmd.CMD_CHECK:
        task_sort = get_task_sort(task_dict)
        buf = pkg_cmd.get_cmd_buf(pkg_cmd.CMD_CHECK, task_sort)
        server.send_message(client, buf)
        return
        
    # 清理列表任务
    if cmd==pkg_cmd.CMD_DEL:
        # 执行中的任务，不允许删除
        for task in task_list[:]:
            task_run = task['run']
            if task_run=='1':continue
            task_list.remove(task)
        
        # 返回结果
        task_sort = get_task_sort(task_dict)
        buf = pkg_cmd.get_cmd_buf(pkg_cmd.CMD_CHECK, task_sort)
        server.send_message(client, buf)
        print('pkg_cmd.CMD_DEL')
        return

    print('无效命令:'+cmd)

# 接收客户端的信息。
def message_received(client, server, message):
    cred_dict = json.loads(message)     
    cmd = cred_dict['cmd']
    
    task_dict = cred_dict['buffer']
    task_dict['client']=client
    task_dict['server']=server
    task_dict['pkg_cmd']=cmd
    
    # 资料校验
    if cmd==pkg_cmd.CMD_LOGON:
        on_cmd_logon_ret(client, server, cred_dict)
        return
            
    # 任务-打包任务
    if cmd==pkg_cmd.CMD_PK_APK or cmd==pkg_cmd.CMD_PK_IPA or cmd==pkg_cmd.CMD_PK_WEB or cmd==pkg_cmd.CMD_PK_HOTUPDATE:
        on_pkg_run(client, server, task_dict)
        return
    
    # 任务-任务查询
    if cmd==pkg_cmd.CMD_CHECK:
        ret = on_task_sort(cmd, task_dict)
        return ret
        
    # 任务-删除任务
    if cmd==pkg_cmd.CMD_DEL:
        ret = on_task_sort(cmd, task_dict)
        return ret
         
    # 未知命令
    print('未知命令:'+cmd)