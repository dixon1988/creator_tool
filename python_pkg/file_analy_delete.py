#!/usr/bin/env python
#coding:utf8
import os,sys,codecs,re,linecache,json,shutil,time,datetime,platform

import tool

platform_name=platform.platform()
IsWds=platform_name.find("Windows")==0
IsIos = not( IsWds )

# 分析路径
s_analy_root=''
s_analy_file=''
s_del_list=''

# 处理路径
s_logic_path = ''

def start(build_path, res_del_list):
    global s_analy_root
    global s_analy_file
    global s_del_list
    global s_logic_path

    s_analy_root = build_path
    s_analy_file = s_analy_root+"/uuid-to-mtime.json"
    s_del_list = res_del_list
    s_logic_path = '/res'

    if not os.path.exists(s_analy_root+s_logic_path):
        s_logic_path = '/assets'

    print("分析路径:%s"%(s_analy_root))
    print("分析文件:%s"%(s_analy_file))
    print("开始处理")

    startLogicFilePath()

    print("删除分析完成")

#uuid文件分析
def readLibraryAnalyFile(uuid_file):
    fp = codecs.open(s_analy_file,'r+','utf-8')
    load_dict=fp.read()
    fp.close()

    analy_content = json.loads(load_dict)
    return analy_content

# 是否删除
def canDelFile(uuid_file_path):
    for del_path in s_del_list:
        if(uuid_file_path.find(del_path)==0):
            return del_path
    return 0

#处理路径
def startLogicFilePath():
    
    # 删除数量
    del_count = 0
    all_count = 0

    # 获取分析文件
    analy_content=readLibraryAnalyFile(s_analy_file)

    # 分析文件夹
    del_root_path = s_analy_root + s_logic_path
    
    #处理路径
    for maindir, subdir, file_name_list in os.walk(del_root_path):
        for filename in file_name_list:
            
            all_count = all_count + 1

            #完整路径
            apath = os.path.join(maindir, filename)
            apath = tool.path_replace(apath)

            #后缀
            #ext = os.path.splitext(apath)[1]

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
                relativePath = tool.path_replace(relativePath)
                bFind = True

            if bFind==False and new_tpkey in analy_content:
                temp_json = analy_content[new_tpkey]
                relativePath = temp_json["relativePath"]
                relativePath = tool.path_replace(relativePath)
                bFind = True

            if bFind==False:
                continue
            
            # 是否拷贝资源
            result=canDelFile(relativePath)
            if( result!=0 ):
                if os.path.exists( apath ):
                    os.remove( apath )
                    del_count+=1
    tool.out_warning('file_analy_delete: all_count=' + str(all_count) + ',del_cout=' + str(del_count))
    return del_count

if __name__ == '__main__':
    print('file_analy_delete')
    