#!/usr/bin/env python
#coding:utf8
import os,sys,codecs,re,linecache,json,shutil,time,datetime,platform

platform_name=platform.platform()
IsWds=platform_name.find("Windows")==0
IsIos = not( IsWds )

import start_path

def do_path_replace(path):
    return path.replace('\\','/')

#分析路径
s_analy_root=''
s_analy_path=''
s_analy_file=''

#结果路径
s_copy_root=''
s_copy_path=''

s_file_list = []

def start(bake_path, build_path, texture, resources):

    global s_analy_root
    global s_analy_path
    global s_analy_file

    global s_copy_root
    global s_copy_path

    global s_file_list

    s_analy_root = bake_path

    s_analy_path = s_analy_root + start_path.root_res
    s_analy_file = s_analy_root + "/uuid-to-mtime.json"

    s_copy_root = build_path
    s_copy_path = build_path + start_path.root_res

    s_file_list = []
    s_file_list.append(texture)
    s_file_list.append(resources)

    print("需要保留资源路径")
    print("\n".join(s_file_list))

    print("开始处理")

    startLogicFilePath(s_analy_path)

    print("分析路径:%s"%(s_analy_root))
    print("结果路径:%s"%(s_copy_path))
     

def CanCopyFile(file):
    for temp_path in s_file_list:
        if(file.find(temp_path)==0):
            return temp_path
    return 0

def mkdir(path):
    if not os.path.isdir(path):
        mkdir(os.path.split(path)[0])
    else:
        return
    os.mkdir(path)

#uuid文件分析
def readLibraryAnalyFile(uuid_file):
    fp = codecs.open(s_analy_file,'r+','utf-8')
    load_dict=fp.read()
    fp.close()

    # print("load_dict%s",load_dict)

    analy_content = json.loads(load_dict)
    return analy_content

#处理路径
def startLogicFilePath(folder):

    #获取分析文件
    analy_content=readLibraryAnalyFile(s_analy_file)

    #操作数据
    copy_count=0

    #处理路径
    for maindir, subdir, file_name_list in os.walk(folder):
        for filename in file_name_list:
    
            #完整路径
            apath = os.path.join(maindir, filename)
            apath = do_path_replace(apath)

            #后缀
            ext = os.path.splitext(apath)[1]

            #文件名
            file_key = os.path.splitext(filename)[0]
            new_key = file_key

            arr_path = apath.split("/")

            temp_key = arr_path[len(arr_path)-2]
            new_tpkey = temp_key

            if( file_key.find('.')!=-1 ):
                new_key=file_key.split('.')[0]

            if( new_tpkey.find('.')!=-1 ):
                new_tpkey=new_tpkey.split('.')[0]

            file_json = ""
            relativePath = ""
            bFind = False
            if (new_key in analy_content):
                file_json = analy_content[new_key]
                relativePath = file_json["relativePath"]
                relativePath = do_path_replace(relativePath)
                bFind = True

            if bFind==False and new_tpkey in analy_content:
                temp_json = analy_content[new_tpkey]
                relativePath = temp_json["relativePath"]
                relativePath = do_path_replace(relativePath)
                bFind = True

            if bFind==False:
                # print("warning:", apath)
                continue
            

            
            # 是否拷贝资源
            result=CanCopyFile(relativePath)
            
            if( result!=0 ):
                # 路径替换
                targetDir=apath.replace(s_analy_root,s_copy_root)
                # print("apath:%s"%(apath))

                # 拷贝路径
                targetDir=os.path.abspath(os.path.dirname(targetDir))
                # print("targetDir:%s"%(targetDir))

                # 创建目录
                mkdir(targetDir)

                # 执行拷贝
                shutil.copy(apath, targetDir)

                copy_count+=1

                # print("file:%s"%(filename))

    print("拷贝数量:%d"%(copy_count))

if __name__ == '__main__':
    print('file_analy')