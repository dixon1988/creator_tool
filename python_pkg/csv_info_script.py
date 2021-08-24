#!/usr/bin/env python
#coding:utf8
import os,sys,codecs,json,re,shutil

#获取渠道信息
def load_channel_list(csv_path):
    temp_list = list()

    fp = codecs.open(csv_path, 'rb+', 'utf-8')
    read_num = 0
    while True:
        lines = fp.readline()
        if not lines:
            break

        lines.replace("\r\n","")
        temp_info = lines.split(',')
        
        read_num += 1
        if read_num == 1:
            continue

        print(temp_info)
        temp_list.append(temp_info)
    fp.close()
    
    return temp_list

# 获取id信息
def get_channel_info(csv_info, channel_id):
    for temp_info in csv_info:
        if temp_info[0]==channel_id:
            return temp_info
    return -1

# 获取info中组件
def get_info_idx_key(channel_info, key):
    idc_temp=0
    for tpInfo in channel_info:
        if tpInfo==key:
            return idc_temp
        idc_temp += 1
    return -1

# 直接获取 exkey-info
def get_info_idx_info(info_list, channel_id, key):

    tp_main_id = channel_id[0:3] + '000'

    # 获取子渠道
    ex_info = get_channel_info(info_list, channel_id)
    if ex_info == -1:
        ex_info = get_channel_info(info_list, tp_main_id)

    # 通用配置
    ex_main_info = get_channel_info(info_list, '0')
    if ex_info == -1:
        ex_info = ex_main_info
    
    # 扩展-key
    idx_key = get_info_idx_key(ex_info, key)
    info_array = []
    if idx_key!=-1:
        if len(ex_info)>idx_key+0:
            info_array.append(ex_info[idx_key+0])
        if len(ex_info)>idx_key+1:
            info_array.append(ex_info[idx_key+1])
        if len(ex_info)>idx_key+2:
            info_array.append(ex_info[idx_key+2])
        if len(ex_info)>idx_key+3:
            info_array.append(ex_info[idx_key+3])
        if len(ex_info)>idx_key+4:
            info_array.append(ex_info[idx_key+4])

    return info_array
