#!/usr/bin/env python
#coding:utf8
#ftp 上传服务
import os
import sys
import time
import ftplib

# import path
fatherdir = os.path.dirname(os.path.abspath(__file__))
fatherdir = os.path.abspath(os.path.join(fatherdir, ".."))
sys.path.append(fatherdir+'\\python_pkg')

import tool
self_path = tool.path_replace(fatherdir)

from ftplib import FTP

class ftp_info:
    ftp=None
    server=''
    username=''
    password=''
    remotepath=''
    ftp_finder=[]

# ftp 链接
def ftpconnect(host, username, password):
    ftp = FTP()
    ftp.set_debuglevel(2)
    ftp.connect(host, 21)
    ftp.login(username, password)
    return ftp

# 从ftp下载文件
def downloadfile(ftp, remotepath, localpath):
    bufsize = 1024
    fp = open(localpath, 'wb')
    ftp.retrbinary('RETR ' + remotepath, fp.write, bufsize)
    ftp.set_debuglevel(0)
    fp.close()

# 创建远程目录
def remotepath_mkdir(ftp, path):
    global ftp_info
    if path in ftp_info.ftp_finder:
        return True
    try:
        ftp.mkd(path)
    except Exception as error:
        code = str(error).split(',')
        if code[0][0:3]=='550':
            ftp_info.ftp_finder.append(path)
        print(error)

    # 记录创建成功
    ftp_info.ftp_finder.append(path)
    return True

# 从本地上传文件到ftp
def uploadfile(ftp, localpath, remotepath):
    print( 'uploadfile '+localpath )
    bufsize = 1024*4
    fp = open(localpath, 'rb')
    try:
        ftp.set_debuglevel(0)
        ftp.storbinary('STOR ' + remotepath, fp, bufsize)
        fp.close()
    except Exception as error:
        return error
    return True

# 失败文件处理
def uploadfailure(ftp, upload_failure, remotepath):
    if len(upload_failure)==0:
        print('ftp上传完成') 
        return True

    time.sleep(5)
    failure = []
    print('failure len-' + str(len(upload_failure)) + ' 重试中============================')
    print(upload_failure)
    for file in upload_failure:
        tail = file.split(remotepath)[-1]
        remotefile = remotepath + tail
        
        file_full = remotefile.split('/')[-1]
        parent_path = remotefile.split('/'+file_full)[0]
        remotepath_mkdir(ftp, parent_path)
        
        ret=uploadfile(ftp, file, remotefile)
        
        # 记录失败文件
        if ret!=True:
            print(type(ret))
            type_of = type(ret)
            if type_of==ftplib.error_temp:
                print(type_of)
            
            if type_of==ConnectionAbortedError:
                print('ConnectionResetError:'+str(ret.errno))
                if ret.errno==10053:
                    ftp=ftp_reconnect()
                    
            if type_of==ConnectionResetError:
                print('ConnectionResetError:'+str(ret.errno))
                if ret.errno==10054:
                    ftp=ftp_reconnect()
            failure.append(file)
            
    return uploadfailure(ftp, failure, remotepath)
    
# dir上传
def uploaddir(ftp, localpath, remotepath):
    print('开始上传')
    
    failure = []
    upload_list = []
    for maindir, subdir, file_list in os.walk(localpath):
        for filename in file_list:
            apath = os.path.join(maindir, filename)
            apath = apath.replace('\\','/')
            upload_list.append(apath)
    
    # 上传文件
    for file in upload_list:
        tail = file.split(remotepath)[-1]
        remotefile = remotepath + tail
        
        file_full = remotefile.split('/')[-1]
        parent_path = remotefile.split('/'+file_full)[0]
        
        remotepath_mkdir(ftp, parent_path)
        ret=uploadfile(ftp, file, remotefile)
        
        # 记录失败文件
        if ret!=True:     
            failure.append(file)
            # if ret.errno==10053 or ret.errno==10054:
                # ftp_reconnect()
    
    return uploadfailure(ftp, failure, remotepath) 

# ftp重连
def ftp_reconnect():
    global ftp_info
    print('ftp_reconnect')
    ftp = ftpconnect(ftp_info.server, ftp_info.username, ftp_info.password)
    ftp_info.ftp = ftp
    return ftp

# 开始执行
# if __name__ == "__main__":
def start_hotUpdate(task_dict, localpath):
    global ftp_info
    
    server_info = tool.get_server_info()
    server_name = task_dict['server_name']
    
    ftp_name = 'cs_ftp'
    if server_name=='public':ftp_name = 'zs_ftp'
    if server_name=='test':ftp_name = 'cs_ftp'
    if server_name=='local':ftp_name = 'nc_ftp'
    
    ftpinfo = server_info[ftp_name]
    server = ftpinfo['address']
    accounts = ftpinfo['accounts']
    password = ftpinfo['password']
    if server=='':return '未配置上传ftp地址'
    
    remotepath2 = localpath.split('/')[-2]
    remotepath1 = localpath.split('/')[-1]
    remotepath = remotepath2 + '/' + remotepath1
    
    ftp_info.server = server
    ftp_info.username = accounts
    ftp_info.password = password
    
    ftp = ftpconnect(server, accounts, password)
    ftp_info.ftp = ftp
    ftp_info.remotepath=remotepath
    ftp_info.ftp_finder.clear()
    rp_ret = uploaddir(ftp, localpath, remotepath)
    ftp_info.ftp.quit()
    return rp_ret

# if __name__ == "__main__":
#     # global ftp_info
    
#     server_info = tool.get_server_info()
#     ftpinfo = server_info['cs_ftp']
    
#     remote_root = 'home/opt/web/update/hotupdate'
#     localpath = self_path + '/hs2020/skip0/1.0.100'
#     remotepath = 'home/opt/web/update/hotupdate'
    
#     # ftp = ftpconnect("47.244.35.121", "download", "download")
#     # uploadfile(ftp, localpath, "D:/download/Ranxiangfei/2.jpg")
#     # downloadfile(ftp, "D:/download/Ranxiangfei/svn/V2.0.xxx.171030_Alpha/xzrs.tar.gz","/home/rxf/svn/V2.0.xxx.171030_Alpha/xzrs.tar.gz")
#     # ftp.quit()

#     ftp = ftpconnect("47.244.35.121", "dltftp", "dlt-ftp123")
#     ftp_info.ftp = ftp;
#     ftp_info.remotepath = remotepath
#     ftp_info.ftp_finder.clear()
#     rp_ret = uploaddir(ftp, localpath, remotepath)
#     ftp_info.ftp.quit()