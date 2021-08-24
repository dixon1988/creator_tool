#!/usr/bin/env python
#coding:utf8
import os
import sys
import tool
import platform
import json
import tkinter as tk
from tkinter import * 

# 平台持续类型
platform_name=platform.platform()
IsIos=platform_name.find("Darwin")==0
IsWds=platform_name.find("Windows")==0

self_path = os.path.split(os.path.realpath(__file__))[0]
self_path = tool.path_replace(self_path)
os.chdir(self_path)
os.system('cd '+self_path)

self_out_path = os.path.abspath(os.path.join(self_path, ".."))
self_out_path = tool.path_replace(self_out_path)

g_config_id = "" # 配置编号

def get_conf_file(config_id):
    return self_path + "/conf/channel_" + str(config_id) + '.conf'

def get_conf_id_file():
    return self_path + '/conf/channel_d.conf'

def get_conf_obj(config_id):
    conf_file = get_conf_file(config_id)
    conf_obj = {}
    if not os.path.exists(conf_file):
        return 0;
    else:
        conf_obj = tool.read_file_json(conf_file);
    return conf_obj

def has_conf_obj(config_id):
    conf_file = get_conf_file(config_id)
    return os.path.exists(conf_file)

def get_config_id():
    conf_file = get_conf_id_file()
    id_conf = {'id':0}
    if os.path.exists(conf_file):
        id_conf = tool.read_file_json(conf_file);
    return id_conf

def set_config_id(conf_id):
    conf_file = get_conf_id_file()
    id_conf = {'id':conf_id}
    tool.write_file_json(conf_file, id_conf)

# 配置读取
def on_read_config_by_ui( obj, get_conf_id=-1 ):
    
    # 获取配置id
    id_obj = get_config_id()
    if id_obj==0:return 1

    # 获取id配置
    g_config_id = id_obj["id"];
    if get_conf_id!=-1:g_config_id = get_conf_id
    
    print("读取 配置id:", g_config_id)
    conf_obj = get_conf_obj(g_config_id);
    if conf_obj==0:return 1
    
    # 读取配置
    for name in dir(obj):
        if name.find('g_')==0:
            if name in conf_obj:
                tk = getattr(obj, name)
                value = conf_obj[name]
                tk.set(value)
            
# 配置读取
def on_read_config( obj, get_conf_id=-1 ):
    # 获取配置id
    id_obj = get_config_id()
    if id_obj==0:return 1

    # 获取id配置
    g_config_id = id_obj["id"];
    if get_conf_id!=-1:g_config_id = get_conf_id
    
    print("读取 配置id:", g_config_id)
    conf_obj = get_conf_obj(g_config_id);
    if conf_obj==0:return 1
    
    # 读取配置
    for name in dir(obj):
        if name.find('g_')==0:
            if name in conf_obj:
                value = conf_obj[name]
                setattr(obj, name, value)

# 保存配置
def on_save_config( obj, config_id ):
    conf_obj = {}
    
    # 读取配置
    for name in dir(obj):
        if name.find('g_')==0:
            value = getattr(obj, name)
            conf_obj[name]=value
    
    # 保存配置
    conf_path = get_conf_file(config_id)
    tool.write_file_json_indent4(conf_path, conf_obj)
    
    print("保存 配置id:", config_id)
    
# 保存配置
def on_save_config_by_ui( obj ):
    conf_obj = {}
    
    # 读取配置
    for name in dir(obj):
        if name.find('g_')==0:
            tk = getattr(obj, name)
            conf_obj[name]=tk.get()
    
    # 保存配置
    conf_id = getattr(obj, "g_config_id").get()
    conf_path = get_conf_file(conf_id)
    tool.write_file_json_indent4(conf_path, conf_obj)
    
    # 保存配置id
    set_config_id(conf_id)
    
    print("保存 配置id:", conf_id)