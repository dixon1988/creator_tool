#!/usr/bin/env python
#coding:utf8
import sys
import os
import zipfile
import hashlib
import json
import datetime
import shutil
import tool

_cache = '_cache'

def CalcMD5(filepath):
    with open(filepath,'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        hash = md5obj.hexdigest()
        return hash

def process(root,output):
    for parent, subdirs, files in os.walk(root):
        for name in files:
            # print("file", name)
            if (name.endswith('.png') or name.endswith('.jpg')):
                
                filepath = os.path.join(parent,name)
                filepath = tool.path_replace(filepath)
                output.append(filepath)
                
def start(root_path):
    print('etc2.start:', root_path)
    
    # 备份所有文件
    tool.rmtree(0, root_path+_cache)
    tool.copydir(root_path, root_path+_cache)
    
    # 压缩文件到 etc2 cache中
    all_files = []
    process(root_path, all_files)
    for file_path in all_files:
        ret = convert(root_path, file_path)
        if ret==0:
            return False
    
    # 删除原始文件，将备份etc2替换到源文件
    shutil.rmtree(root_path)
    os.path.rename(root_path+_cache, root_path)
    
# 转换为etc2
def convert(root_path, filepath):
    
    directory = os.path.dirname(filepath)
    md5 = CalcMD5(filepath)
    cacheFilePath = os.path.join(cache_dir,md5)
    inCache = os.path.exists(cacheFilePath)
    pkmPath = os.path.join(directory,os.path.splitext(os.path.basename(filepath))[0]+".pkm")
    ppmPath = os.path.join(directory,os.path.splitext(os.path.basename(filepath))[0]+".ppm")
    targetPath = os.path.join(directory,os.path.basename(filepath))
    
    if inCache:
        print("copy cached ",pkmPath)
        f_in = open(cacheFilePath, 'rb')
        f_out = gzip.open(cacheFilePath+'.gz', 'wb')
        f_out.writelines(f_in)
        f_out.close()
        f_in.close()
        #os.remove(cacheFilePath)
        shutil.move(cacheFilePath+'.gz',targetPath)
    else:
        command = 'etcpack ' + path + ' ' + directory + ' -c etc2 -f RGBA8'
        os.system(command)
        shutil.copy(pkmPath,cacheFilePath)
        
        f_in = open(pkmPath, 'rb')
        f_out = gzip.open(pkmPath+'.gz', 'wb')
        f_out.writelines(f_in)
        f_out.close()
        f_in.close()
        os.remove(pkmPath)
        #os.remove(cacheFilePath)
        shutil.move(pkmPath+'.gz',targetPath)
        print("cache copyed ",targetPath)
    #os.remove(cache_dir)
    return 1

# test 直接调试
# E:/work/client168/Sup_ZhenJin_dev/build/jsb-link/res/raw-assets
# e:/work/tools/sup_105_2.0/Sup_ZhenJin_dev/etc2_cache
if __name__ == '__main__':
    
    start('E:/work/client168/Sup_ZhenJin_dev/build/jsb-link/res/raw-assets')
    
    print('etc2')