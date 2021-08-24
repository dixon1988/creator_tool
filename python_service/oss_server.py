#!/usr/bin/env python
#coding:utf8
#ftp 上传服务
import os
import sys
import threading
sys.setrecursionlimit(10000000)

# import path
fatherdir = os.path.dirname(os.path.abspath(__file__))
fatherdir = os.path.abspath(os.path.join(fatherdir, ".."))
sys.path.append(fatherdir+'\\python_pkg')

import tool
self_path = tool.path_replace(fatherdir)

# coding=utf-8
import datetime,string,random
import time
import oss2

oss2_auth = None
oss2_bucket = None

g_root_path = ""
g_upload_count = 0    # 总上传数量
g_succee_count = 0    # 成功数量
g_upload_list = []    # 上传列表
g_thread_max = 50   # 最大上传线程
g_thread_lock = None # 线程锁

class CFileInfo:
    def __init__(self, local_file, cloud_name):
        self.local_file = local_file
        self.cloud_name = cloud_name
        self.count = 0 # 0：无效状态 1：上传中
        
# 文件上传
def uploadfile(file_info):
    global oss2_bucket
    global g_succee_count
    try:
        with open(oss2.to_unicode(file_info.local_file), 'rb') as fp:
            oss2_bucket.put_object(file_info.cloud_name, fp)
        meta = oss2_bucket.get_object_meta(file_info.cloud_name)
        
        # 上传成功->next
        if meta:
            print("上传成功:" + file_info.local_file)
            g_succee_count += 1
            return True
        
        # 上传失败
        uploadfileRetry(file_info)
        return False
    
    # catch 失败
    except Exception as error:
        uploadfileRetry(file_info)
        return False
    
    # 默认失败
    uploadfileRetry(file_info)
    return False

# 重新上传
def uploadfileRetry(file_info):
    time.sleep(1)
    uploadfile(file_info)

# 文件上传
def uploadThread(file_info):
    global oss2_bucket
    global g_succee_count
    global g_thread_lock
    
    try:
        local_file = file_info.local_file
        cloud_name = file_info.cloud_name
        result = oss2_bucket.put_object_from_file(cloud_name, local_file)
        if result.status == 200:
            
            g_thread_lock.acquire()
            print("成功上传: " + str(g_succee_count) + "=" + local_file)
            g_succee_count += 1
            g_thread_lock.release()
            
            start_next_thread()
            return True
        
        # 上传失败
        start_retry_thread(file_info)
        return False
    
    # catch 失败
    except Exception as error:
        start_retry_thread(file_info)
        return False
    
    # 默认失败
    start_retry_thread(file_info)
    return False

# 开启上传线程
def start_next_thread():
    global g_thread_lock
    global g_upload_list
    
    g_thread_lock.acquire()
    count = len(g_upload_list)
    file_info = None
    if count>0:
        file_info = g_upload_list.pop()
        # print("开始上传:",file_info.local_file)
    g_thread_lock.release()
    
    if file_info:
        uploadThread(file_info)

def start_new_thread():
    global g_thread_lock
    global g_upload_list
    
    g_thread_lock.acquire()
    count = len(g_upload_list)
    file_info = None
    if count>0:
        file_info = g_upload_list.pop()
        # print("开始上传:",file_info.local_file)
    g_thread_lock.release()
    
    if file_info:
        # 创建
        t = threading.Thread(target=uploadThread, args=[file_info])
        # 不阻塞
        t.setDaemon(True)
        # 启动
        t.start()
        return t
    return None

# 失败线程，重新上传，成功为止
def start_retry_thread(file_info):
    # 1秒后重试
    time.sleep(1)
    g_thread_lock.acquire()
    file_info.count += 1
    print('重试:' + str(file_info.count)  + '次: ' + file_info.local_file)
    g_thread_lock.release()
    uploadThread(file_info)

# 开始上传
def startUpload(local_root, upload_root):
    global g_thread_lock
    global g_thread_max
    global g_root_path
    global g_upload_list
    global g_upload_count
    global oss2_bucket
    global oss2_auth
    global g_succee_count
    
    g_root_path = local_root
    print('上传路径:' + g_root_path)
    print('文件根路径:' + upload_root)

    server_info = tool.get_server_info()
    ossinfo = server_info['ossinfo']
    
    accessKey = ossinfo['accessKey']
    accessKeySecret = ossinfo['accessKeySecret']
    endPoint = ossinfo['endpoint']
    bucket_name = ossinfo['bucket_name']

    oss2_auth = oss2.Auth(accessKey, accessKeySecret)
    oss2_bucket = oss2.Bucket(oss2_auth, endPoint, bucket_name)

    # 本地上传文件列表
    g_upload_list = []
    for maindir, subdir, file_list in os.walk(local_root):
        for filename in file_list:
            apath = os.path.join(maindir, filename)
            apath = apath.replace('\\','/')
            file_path = apath.replace(local_root,'')
            cloud_name = upload_root + file_path
            file_info = CFileInfo(apath, cloud_name)
            g_upload_list.append(file_info)
    
    g_upload_count = len(g_upload_list)
    
    # 多线程上传===========================================
    print( '开始上传: 文件数量=' + str(g_upload_count) )
    g_succee_count = 0
    start_time = time.time()
    
    # 最大上传线程
    g_thread_lock = threading.Lock()
    thread_list = []
    for i in range(g_thread_max):
        t = start_new_thread()
        if t:
            thread_list.append(t)
            
    for t in thread_list:
        t.join()
        
    # 上传完成
    end_time = time.time()
    print( '上传完成:' )
    print( '上传路径:', g_root_path )
    print( '上传数量:', g_upload_count )
    print( '成功数量:', g_succee_count )
    print( '上传耗时:', end_time-start_time )
    
    # 单线程上传===========================================
    # print( '开始上传:')
    # count = len(g_upload_list)
    # while count>0:
    #     file_info = g_upload_list.pop()
    #     uploadfile(file_info)
    # print( '结果日志:' )
    # print( '上传路径:', g_root_path )
    # print( '上传数量:', g_upload_count )
    # print( '成功数量:', g_succee_count )

# if __name__ == "__main__":
#     local_root = self_path + '/hs2020/'
#     upload_root = 'skin0/1.0.100/'
#     startUpload(local_root, upload_root)
#     print('main=test')
