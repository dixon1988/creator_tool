#!/usr/bin/env python
#coding:utf8
import os,sys,codecs,re,linecache
import platform
import tool
import start_path
platform_name=platform.platform()
IsWds=platform_name.find("Windows")==0
IsIos = not( IsWds )

env = os.environ

def do_base_serverType(root_path, serverType):
    error = True
    base_full_path = root_path + '/assets/' + start_path.channel_config
    if os.path.exists(base_full_path):
        base_json = tool.read_file_json(base_full_path)
        base_json['serverType']=serverType;
        tool.write_file_json_indent4(base_full_path, base_json)

        print( "write:" + start_path.channel_config + ", serverType:" + str(serverType))
    else:
        error = 'not found ' + root_path
        tool.out_error(error)
    return error

if __name__ == '__main__':
    print('assets_script')