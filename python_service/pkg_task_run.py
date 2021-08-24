#!/usr/bin/env python
#coding:utf8

import os
import sys
import json
import time
import threading
import pkg_cmd

# import path
fatherdir = os.path.dirname(os.path.abspath(__file__))
fatherdir = os.path.abspath(os.path.join(fatherdir, ".."))
sys.path.append(fatherdir+'/python_pkg')

import tool
import start_pkg
import start_path
import start_config

# 当前打包配置
g_pk_config = 0

# pkg_run
def pkg_run(task_dict, config_id, pk_config):
    
    # 初始化环境变量
    start_config.on_read_config(start_pkg, config_id)
    
    # 打包命令
    task_cmd = task_dict['pkg_cmd']
    
    # pk_apk
    if task_cmd==pkg_cmd.CMD_PK_APK:
        start_pkg.g_platform_name = start_path.pkg_type_android
        pkg_ret = start_pkg.do_pkg_platform()
        return pkg_ret
    
    # pk_ipa
    if task_cmd==pkg_cmd.CMD_PK_IPA:
        start_pkg.g_platform_name = start_path.pkg_type_ios
        pkg_ret = start_pkg.do_pkg_platform()
        return pkg_ret
    
    # PK_WEB-
    if task_cmd==pkg_cmd.CMD_PK_WEB:
        start_pkg.g_platform_name = start_path.pkg_type_web
        pkg_ret = start_pkg.do_pkg_platform()
        return pkg_ret
    
    # pk_hotupdate
    if task_cmd==pkg_cmd.CMD_PK_HOTUPDATE:
        version = start_pkg.g_update_hot_version.split('.')
        version[2] = str( int(version[2]) + 1 ); 
        start_pkg.g_update_hot_version = '.'.join(version)
        start_pkg.g_platform_name = start_path.pkg_type_hotUpdate
        
        # pk-server 由server来执行上传任务
        start_pkg.g_update_oss_upload = 0
        pkg_ret = start_pkg.do_build_hotUpdate()
        
        # 处理成功，保存配置
        if pkg_ret:
            start_config.on_save_config(start_pkg, config_id)
        return pkg_ret
    
    print('无效打包命令')

# pk_测试
def pkg_test():
    time.sleep(15)

# svn更新-为了避免更新时冲突，svn目录、禁止打包
# "pf-root":"E:/work/client168/Sup_ZhenJin_dev",
def svn_check_update(task_dict, config_id, pk_config):
    
    # 更新svn
    pj_root = pk_config['g_project_root']
    svn = tool.get_server_conf('svn_account')
    username = svn['username']
    password = svn['password']

    cmd_param = 'svn update ' + pj_root + ' --username=' + username + ' --password=' + password
    tool.out_cmd(cmd_param)
    os.system(cmd_param)

    tool.out_green('svn update done!')
    return True

# 打包处理
def pkg(task_dict):
    global g_pk_config;
    
    g_is_svn_update = task_dict['g_is_svn_update']
    g_is_share_up = task_dict['g_is_share_up']
    g_is_ftp_up = task_dict['g_is_ftp_up']
    g_config_id = task_dict['g_config_id']
    
    # 打包配置
    g_pk_config = start_config.get_conf_obj(g_config_id)
    
    task_dict['g_config_id'] = g_pk_config['g_config_id']
    task_dict['g_version'] = g_pk_config['g_version']
    task_dict['g_update_hot_version'] = g_pk_config['g_update_hot_version']
    
    # svn更新
    if g_is_svn_update==1:
        svn_check_ret = svn_check_update(task_dict, g_config_id, g_pk_config)
        if svn_check_ret!=True:
            return svn_check_ret
        
    # 运行打包
    pkg_run(task_dict, g_config_id, g_pk_config)
    # pkg_test()

    return True