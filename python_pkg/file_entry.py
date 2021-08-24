#!/usr/bin/env python
#coding:utf8
import os,sys,codecs,re,linecache
import platform

import tool

platform_name=platform.platform()
IsWds=platform_name.find("Windows")==0
IsIos = not( IsWds )

#加密需要忽略的文件名
s_file_ignore = ''
s_logic_key = ''
s_len_key = ''
s_file_type = ''

#操作类型 0:解密 1:加密 
s_logic_type = ''

def start(res_raw_assets, logic_type):
    global s_logic_type
    global s_file_ignore
    global s_logic_key
    global s_len_key
    global s_file_type

    s_logic_type = logic_type

    s_file_ignore = tool.get_entry_ignore_list()
    s_logic_key = tool.get_tool_conf('entry_key')
    s_len_key = len(s_logic_key)
    s_file_type = tool.get_entry_file_type()
    print("忽略文件：",",".join(s_file_ignore))

    print("操作路径:%s"%(res_raw_assets))
    print("开始加密:startLogicFilePath")
    startLogicFilePath(res_raw_assets)

#文件头
# s_header_png=[0x89,0x50,0x4E,0x47]
# s_header_bmp=[0x42,0x4D]
# s_header_gif=[0x47,0x49,0x46]
# s_header_jpg=[0xFF,0xD8,0xFF,0xE0,0x00,0x10,0x4A,0x46,0x49,0x46]
# s_header_wave=[0x52,0x49,0x46,0x46]
# s_header_mp3=[0x49,0x44,0x33,0x03]
# s_header_mp3stream=[0xFF,0xFA,0x95,0x6C]

# #文件头长度
# s_len_png=len(s_header_png)
# s_len_bmp=len(s_header_bmp)
# s_len_gif=len(s_header_gif)
# s_len_jpg=len(s_header_jpg)
# s_len_wave=len(s_header_wave)
# s_len_mp3=len(s_header_mp3)
# s_len_mp3stream=len(s_header_mp3stream)

# def GetFileExtension(bytedata):
    # temp_ext="error"
    # if cmp(bytedata[0:s_len_png],s_header_png)==0:
    #     temp_ext='.png'
	# if cmp(bytedata[0:s_len_bmp],s_header_bmp)==0:
    #     temp_ext='.bmp'
	# if cmp(bytedata[0:s_len_gif],s_header_gif)==0:
	# 	temp_ext='.gif'
	# if cmp(bytedata[0:s_len_jpg],s_header_jpg)==0:
	# 	temp_ext='.jpg'
	# if cmp(bytedata[0:s_len_wave],s_header_wave)==0:
	# 	temp_ext='.wav'
	# if cmp(bytedata[0:s_len_mp3],s_header_mp3)==0:
	# 	temp_ext='.mp3'
	# if cmp(bytedata[0:s_len_mp3stream],s_header_mp3stream)==0:
	# 	temp_ext='.mp3'
	# return temp_ext

#需要处理的文件类型
def CanLogicFile(ext_type):
    for i in s_file_type:
        if(i==ext_type):
            return True
    return False

#是否需要忽略
def CanIgnoreFile(ignoreFile):
    for tempfile in s_file_ignore:
        if(ignoreFile.find(tempfile)!=-1):
            return True
    return False

#加密文件
def encryptFile(file):
    # 读取文件
    fp=open(file, "rb")
    data = fp.read()
    fp.close()

    # print(len(data))
    # print(data)
    
    len_data = len(data)
    
    # 已加密文件忽略
    if( data[0]==1 ):
        return 0

    new_data=bytearray(len_data+1)
    new_data[0]=1
    
    key_index=0

    i=1
    for i_byte in data:
        key_str=s_logic_key[key_index%s_len_key]
        key_asc=ord(key_str)

        data_data=(i_byte+key_asc)%256
        
        new_data[i]=data_data
        
        i+=1
        key_index+=1
        
    #重新写入密文
    refp=open(file, "wb")
    refp.write( new_data )
    refp.flush()
    refp.close()
    return 1

# #解密文件
def decryptFile(file):
    # 读取文件
    fp=open(file, "rb")
    data = fp.read()
    fp.close()

    len_data = len(data)

    #未加密文件忽略
    if( data[0]!=1 ):
        return 0

    new_data=bytearray(len_data-1)
    key_index=0
    i=0

    for i_byte in data:
        if(i==0):
            i+=1
            continue

        key_str=s_logic_key[key_index%s_len_key]
        key_asc=ord(key_str)

        data_data=(i_byte+256-key_asc)%256
        new_data[i-1]=data_data
        i+=1
        key_index+=1

    #重新写入密文
    refp=open(file, "wb+")
    refp.write( new_data )
    refp.close()

    # print(len(new_data))
    # print(new_data)
    return 1

#处理路径
def startLogicFilePath(folder):
    #操作数据
    entry_file=0
    entry_count=0

    #处理路径
    for maindir, subdir, file_name_list in os.walk(folder):
        for filename in file_name_list:
    
            #绝对路径
            apath = os.path.join(maindir, filename)
            ext = os.path.splitext(apath)[1]

            # 不是忽略文件
            if( False==CanIgnoreFile(apath)):
                #处理文件
                if( CanLogicFile(ext) ):
                    bResult=0
                    if(s_logic_type=='1'):
                        bResult=encryptFile(apath)
                    else:
                        bResult=decryptFile(apath)
                    if(bResult==1):
                        entry_count+=1
            entry_file+=1

    if(s_logic_type=='1'):
        print("加密数量:%d 文件数量:%d"%(entry_count,entry_file))
    else:
        print("解密数量:%d 文件数量:%d"%(entry_count,entry_file))



if __name__ == '__main__':
    print('file_entry') 


    
    