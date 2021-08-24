#!/usr/bin/env python
#coding:utf8
import os
import sys
import platform
import tkinter as tk
from tkinter import * 
import configparser
import time
import threading
import json
import shutil
import codecs
import subprocess
import hashlib
import platform
import io

# import path
fatherdir = os.path.dirname(os.path.abspath(__file__))
fatherdir = os.path.abspath(os.path.join(fatherdir, ".."))
sys.path.append(fatherdir+'\\python_service')

platform_name=platform.platform()
IsWds=platform_name.find("Windows")==0
IsMacOS=not IsWds

if IsMacOS:
    from biplist import *
from stat import *

# 自定义脚本
import tool
import assets_script
import batch_auto_apk
import version_entry_start
import start_path
import etc2
import oss_server

self_path = os.path.split(os.path.realpath(__file__))[0]
self_path = tool.path_replace(self_path)
os.chdir(self_path)
os.system('cd '+self_path)

self_out_path = os.path.abspath(os.path.join(self_path, ".."))
self_out_path = tool.path_replace(self_out_path)

env = os.environ
env['_self_path'] = self_path
env['_self_out_path'] = self_out_path

# 全局环境变量
g_creator_root  = ''        # ccc_路径
g_creator_ver   = ''        # ccc_版本
g_project_root  = ''        # 工程路径
g_remote_assets = ''        # 热更路径
g_project_title = ''        # project_title
g_build_path = ''        # build路径
g_batch_path = 'build_batch' # 批处理工程路径
g_platform_name = ''        # 平台名字：ios、android、web、hotUpdate
g_file_name = ''        # 输出文件名

g_channel_id = ''       # 打包渠道
g_config_id = 0         # 打包渠道
g_version = ''          # 打包版本
g_app_name = ''         # app名字
g_package_id = ''       # pkg_id
g_is_debug = 0          # debug
g_is_md5cache = 0       # md5cache
g_is_short = 0          # 简体大厅
g_pkg_res_type=''       # 资源处理方式
g_is_import_zip = 0     # import-zip
g_clean_jsb = 0
g_clean_library = 0

# android相关
g_keystore_name = ''
g_keystore_alias = ''
g_keystore_password = ''
g_apiLevel = ''
g_android_bak = ''

g_armeabi_v7a = 1
g_arm64_v8a = 0
g_x86 = 0

# ios
g_ios_arm64 = ''
g_ios_pkg_appstore = ''
g_ios_pkg_adhoc = ''
g_ios_pkg_enterprise = ''

g_signed_ipa_form_build = ''
g_signed_ipa_form_archive = ''

g_adhoc_teamid = ''
g_enterprise_teamid = ''
g_appstore_teamid = ''

g_dev_teamid = ''      # 开发者id
g_profiles_name = ''    # 发布证书
g_profiles_dev = ''    # 开发证书
g_profiles_enterprise = '' #证书名-enterprise
g_profiles_appstore = '' #证书名-appstore
g_profiles_adhoc = '' #证书名-adhoc

g_signingStyle_Automatic = '' #证书使用
g_signingStyle_manual = '' #证书使用

# web
g_is_copyWebBakeup = 1

# update
g_update_use_res_link = ''
g_update_use_res_old_ver = ''
g_update_use_res_old_str = ''
g_update_hot_version = ''
g_update_skin_num = ''
g_update_oss_upload = 0

g_update_out_res_hall = ''
g_update_out_res_all = ''
g_update_out_res_game_id = ''
g_update_out_res_id_str = ''

# code相关
g_server_name = ''      # 服务类型 publiu、test、local

# 文件输出路径暂存
g_out_file_path=''
g_out_path_root=''
g_ccc_build_param=''

# 工具配置
conf_file=None
conf=None
if IsMacOS:
    conf_file = self_path + "/conf/start_pkg_ios.conf"
    conf = configparser.ConfigParser()
else:
    conf_file = self_path + "/conf/start_pkg.conf"
    conf = configparser.ConfigParser()

# 输出配置
g_jsb_type = 'jsb-link'
g_web_mobile = 'web-mobile'
g_uuid_json = 'uuid-to-mtime.json'

# 获取批处理配置文件
def _get_batch_csv():
    if tools_is_android():
        if g_server_name=='public':
            return 'channel.csv'
        if g_server_name=='test':
            return 'channel_cs.csv'
    
    if tools_is_ios():
        if g_server_name=='public':
            return 'channel_' + g_dev_teamid + '.csv'
        if g_server_name=='test':
            return 'channel_cs.csv'

    if tools_is_web():
        if g_server_name=='public':
            return 'channel.csv'
        if g_server_name=='test':
            return 'channel_cs.csv'
        
    return 'channel.csv'

# 检查配置参数
def check_pack_args():
    #判断渠道号
    if g_channel_id < 100000 or g_channel_id > 999999:
        return tool.out_error('渠道包必须是6位数字')

    #判断应用名
    if len(g_app_name) < 1:
        return tool.out_error('没有填写应用名')

    #判断包名
    if len(g_package_id) < 1:
        return tool.out_error('没有填写包名')

    return True

# 获取 creator 启动头
def get_creator_start_cmd():
    ccc_exe = g_creator_root + '/CocosCreator.exe --nologin'
    if IsMacOS: 
        ccc_exe = g_creator_root + '/Contents/MacOS/CocosCreator --nologin'
    ccc_exe = tool.path_replace(ccc_exe)
    return ccc_exe

# 获得目录下的指定类型文件
def get_applications_app( srcPath, path_name ):
    for maindir, subdir, file_name_list in os.walk(srcPath):
        tmp_ary = maindir.split('/')
        tmp_path = tmp_ary[-1]
        if tmp_path.find(path_name)!=-1:
            return maindir
    return 0

# 工程目录
def get_project_name():
    proj_name=''
    rp_array = g_project_root.split('/')
    proj_name = rp_array[-1]
    return proj_name

# 工程目录-library
def get_build_root_library():
    root_library = g_project_root+'/library'
    return root_library

# 工程目录-uuid-to-mtime.json
def get_library_uuid_json():
    root_uuid_json = g_project_root+'/library/'+g_uuid_json
    return root_uuid_json

# 工程目录-temp
def get_build_root_temp():
    root_library = g_project_root+'/temp'
    return root_library

# 构建目录-根路径
def get_build_root_path():
    build_root_path = g_project_root + '/' + g_build_path
    return build_root_path

# 构建目录-平台类型-根路径
def get_build_platform_path(platform_name):
    build_platform_root_path = get_build_root_path()
    return build_platform_root_path+'/'+platform_name

def get_platform_root_uuid_json(platform_name):
    root_platform_uuid_json = get_build_platform_path(platform_name) + '/' + g_uuid_json
    return root_platform_uuid_json

def get_batch_path():
    _batch_path = g_project_root + '/' + g_batch_path
    return _batch_path

def get_batch_conf_path():
    batch_conf_path = ''
    
    if tools_is_ios():
        return self_out_path+'/batch_ios_conf'
    if tools_is_web():
        return self_out_path+'/batch_web_conf'
    if tools_is_android():
        return self_out_path+'/batch_android_conf'
    
    if IsMacOS and tools_is_hotUpdate():
        return self_out_path+'/batch_ios_conf'
    if IsWds and tools_is_hotUpdate():
        return self_out_path+'/batch_android_conf'
    return batch_conf_path

def get_batch_conf_csv_path():
    csv_path = get_batch_conf_path() + '/' + _get_batch_csv()
    return csv_path

# 获取工程输出目录
def get_project_out_root():
    proj_out_root = self_out_path + '/' + get_project_name()
    return proj_out_root

# list str 字符串查找
def find_list_str_num(str_list, re_str):
    num = 0
    for temp_str in str_list:
        if(temp_str.find(re_str) != -1):
            return num
        num += 1
    return -1

# 文件行数替换，直接替换指定行数
def build_txt_auto_replace(*replace_arg):

    root_web_mobile_path = get_build_platform_path(g_web_mobile)

    web_mobile_index_html = root_web_mobile_path +'/index.html'
    web_mobile_index_html_bakeup = root_web_mobile_path +'/index.html.bakeup'

    # 获得文件内容
    root_build_fp = codecs.open(web_mobile_index_html, 'rb+', 'utf-8')
    root_build_list = root_build_fp.readlines()
    root_build_fp.close()

    root_src_fp = codecs.open(web_mobile_index_html_bakeup, 'rb+', 'utf-8')
    root_src_list = root_src_fp.readlines()
    root_src_fp.close()

    # 循环替换
    replace_count = 0
    for temp_arg in replace_arg:
        num0 = find_list_str_num(root_build_list, temp_arg)
        num1 = find_list_str_num(root_src_list, temp_arg)

        # 查找成功
        if(num0 != -1 & num1 != -1):
            root_src_list[num1] = root_build_list[num0]
            replace_count += 1

    # 重新写入
    root_new_write = codecs.open(web_mobile_index_html, 'w+', 'utf-8')
    root_new_write.writelines(root_src_list)
    root_new_write.close()
    print("替换成功次数:%s" % (replace_count))

#获取渠道信息
def load_channel_list(csv_path):
    channel_list = list()

    fp = codecs.open(csv_path,'rb+','utf-8')
    read_num = 0
    while True:
        lines = fp.readline()
        if not lines:
            break

        lines = lines.replace(",\r\n","")
        channelInfo = lines.split(',')
        
        read_num += 1
        if read_num == 1:
            continue

        print(channelInfo)
        channel_list.append(channelInfo)
        
    fp.close()
    return channel_list

# 获取csv对应行信息
def get_channel_list(csv_cont,key,index):
    for tpinfo in csv_cont:
        if len(tpinfo)>index:
            if tpinfo[index]==key:
                return tpinfo
    return 0
def get_info_key_index(csv_info,key):
    index=0
    for tpinfo in csv_info:
        if tpinfo==key:
            return index
        index += 1
    return -1

def get_exportOption_list_name():
    if g_ios_pkg_adhoc==1:
        return 'adhoc.plist'
    if g_ios_pkg_appstore==1:
        return 'appstore.plist'
    if g_ios_pkg_enterprise==1:
        return 'enterprise.plist'
    return ''

# 替换资源
def replase_channel_skip(src_file, mtime_content):
    # 查找替换路径
    for key in mtime_content:
        temp_jsondata = mtime_content[key]
        relativePath = temp_jsondata['relativePath']
        relativePath = tool.path_replace(relativePath)
        #查找匹配
        if relativePath == src_file:
            return key
    return 0

# 打包
def do_start_pkg():
    do_pkg_platform() 
    
# 刷新渠道build
def do_update_channelid_version(buildTime):
    # 刷新build目录
    if os.path.exists(g_project_root):
        update_project_channelid_and_version(g_project_root, g_build_path, buildTime)

    if os.path.exists(g_project_root):
        update_project_channelid_and_version(g_project_root, g_batch_path, buildTime)

# 刷新assets
def do_update_channelid():
    # 刷新工程目录
    update_project_channelid_and_version(g_project_root, "", 0)
    
# 打包逻辑 0:构建+打包 1:只构建
def do_pkg_platform(pkg_type=0):
    global g_out_file_path
    global g_out_path_root

    _start_time = time.time()
    
    # 构建项目-web构建就是打包
    ccc_build_platform(g_project_root, 0, g_is_short)

    # 耗时输出
    time_ended = time.time()
    time_logic = time_ended - _start_time 
    tool.out_green('构建完成-----耗时:'+ str(time_logic) )

    # 只构建不编译-退出
    if pkg_type==1:return '构建完成-----耗时:'+ str(time_logic)

    # 打包项目
    ret = ccc_complie_platform(g_project_root)

    # 耗时输出
    _ended_time = time.time()
    _doing_time = _ended_time - _start_time
    print('耗时:' + str(_doing_time))

    # 执行完成打开目录
    print('===================================执行完成')
    return ret

# 批量打包安卓 先调用常规android打包，然后copy出的包，来作批处理
def do_start_batch_android():
    batch_conf_path = get_batch_conf_path()
    apk_list = tool.get_dir_file(batch_conf_path+'/apk', '.apk')
    mtime_list = tool.get_dir_file(batch_conf_path+'/apk', '.json')
    if len(apk_list)!=1 or len(mtime_list)!=1:
        tool.out_error('apk目录异常，请检查目录，仅允许存在一个 apk 与 mtime.json 文件')
        return

    batch_server = 'zs'
    if g_server_name=='test':batch_server='cs'
    dir_time = time.strftime('%m%d_%H%M',time.localtime(time.time()))
    
    batch_auto_apk.batch_server = batch_server
    outpath = apk_list[0].split('/')[-1].replace('.','_')

    batch_auto_apk.g_batch_conf_path = batch_conf_path
    batch_auto_apk.g_project_root_name = get_project_name()
    batch_auto_apk.g_batch_conf_apk = apk_list[0]
    batch_auto_apk.g_apk_mtime_json = mtime_list[0]
    batch_auto_apk.g_apk_path = apk_list[0]

    batch_auto_apk.g_batch_out_root = self_out_path + '/' + outpath + '/' + batch_server + '_' + dir_time
    batch_auto_apk.g_channel_csv = batch_conf_path + '/channel.csv'
    batch_auto_apk.g_channel_cs_csv = batch_conf_path + '/channel_cs.csv'
    batch_auto_apk.g_channel_info = batch_conf_path + '/channel_info.csv'

    batch_auto_apk.g_keystore_name = batch_conf_path + '/' + g_keystore_name
    batch_auto_apk.g_keystore_alias = g_keystore_alias
    batch_auto_apk.g_keystore_password = g_keystore_password

    batch_auto_apk.start()

# 开游戏配置文件
def do_open_gameConfig():
    gameConfig_path = self_path + '/conf'
    tool.open_finder(gameConfig_path)

# 批量打包安卓 先调用常规android打包，然后copy出的包，来作批处理
def do_start_batch_web_mobile():
    print('do_start_batch_web_mobile:')

# xocde archive
def xcode_ios_archive( tp_pk_id, xcode_proj, target_name, version, archive_path ):
    # archive
    # xcodebuild archive -project xxx.xcodeproj -sdk iphoneos -scheme scheme_name -configuration Release -archivePath archive_path

    # 清理archive路径
    tool.rmtree(0, archive_path)

    # cleanup
    _scheme_target = target_name + '-mobile'
    _xcode_clean_param = 'xcodebuild clean' + ' -project ' + xcode_proj + ' -configuration ' + 'Release' + ' -alltargets'
    print(_xcode_clean_param)
    os.system(_xcode_clean_param)

    # 证书名
    showBuildSettings=''
    profiles_name=' DEVELOPMENT_TEAM='+g_dev_teamid
    showBuildSettings+=profiles_name

    enable_automatic = ' CODE_SIGN_STYLE=Automatic'
    showBuildSettings+=enable_automatic

    product_identifier =' PRODUCT_BUNDLE_IDENTIFIER=' + tp_pk_id
    showBuildSettings += product_identifier

    # 编译archive
    _scheme_target = target_name + '-mobile'
    _xcode_archve_param = 'xcodebuild' + ' archive' + ' -project ' + xcode_proj + ' -sdk iphoneos' + ' -scheme ' + _scheme_target + ' -configuration ' + 'Release'  + ' -archivePath ' + archive_path + ' -allowProvisioningUpdates ' + showBuildSettings
    print(_xcode_archve_param)
    os.system(_xcode_archve_param)

# xcode export
def xcode_ios_export(tp_pk_id, archive_path, export_path):

    # 修改证书名
    _exportOptionsPlist = self_out_path + '/exportOption/' + get_exportOption_list_name()

    profiles_desc = g_profiles_name

    option_cont = readPlist(_exportOptionsPlist)
    option_cont['provisioningProfiles']={}
    option_cont['provisioningProfiles']={tp_pk_id:profiles_desc}
    option_cont['signingStyle']='automatic'
    if g_signingStyle_manual==1:
        option_cont['signingStyle']='manual'

    option_cont['teamID']=g_dev_teamid
    
    writePlist(option_cont, _exportOptionsPlist, False)

    _xcode_export_param = 'xcodebuild' + ' -exportArchive' + ' -archivePath ' + archive_path + ' -exportOptionsPlist ' + _exportOptionsPlist + ' -exportPath ' + export_path + ' -allowProvisioningUpdates'
    print(_xcode_export_param)
    os.system(_xcode_export_param)

# ios批量打包1: 批量执行  archive -> export ipa
def do_start_batch_ios():
    _start_time = time.time()

    # 平台校验
    if tools_is_ios() and IsMacOS==False: 
        return "打包ios 请在mac下执行！"

    proj_root = g_project_root

    # 1 ccc-build
    # ccc_build_platform(proj_root, 1)

    batch_path = get_batch_path()
    proj_root = g_project_root + '/' + g_build_path
    batch_version = g_version

    # 拷贝构建内容 到 批量路径下
    tool.rmtree(0, batch_path)
    tool.mkdir(batch_path)
    cp_param = 'cp -r ' + proj_root + '/jsb-link' + ' ' + batch_path + '/jsb-link'
    tool.out_cmd(cp_param)
    os.system(cp_param)

    _batch_conf_path = get_batch_conf_path()
    _csv_path = _batch_conf_path+'/'+_get_batch_csv()
    _batch_skin_path = _batch_conf_path + '/appskin'
    _channel_list = load_channel_list(_csv_path)

    _batch_path_proj_ios_mac = batch_path + '/jsb-link/frameworks/runtime-src/proj.ios_mac'
    _batch_reicon_path = _batch_path_proj_ios_mac + '/ios/Images.xcassets/AppIcon.appiconset'
    _batch_relaunchimage_path = _batch_path_proj_ios_mac + '/ios/Images.xcassets/LaunchImage.launchimage'

    _batch_res = batch_path + '/jsb-link/res'
    _batch_mtime_json = batch_path + '/jsb-link/uuid-to-mtime.json'
    _path_array = batch_path.split('/')

    _ccc_proj_name = _path_array[-2]
    _xcode_proj_name = g_project_title
    _xcode_build_proj = _batch_path_proj_ios_mac + '/' + _xcode_proj_name + '.xcodeproj'

    dir_time = time.strftime('%m%d_%H%M',time.localtime(time.time()))
    _batch_export_path = ''

    if g_server_name=='public':
        _batch_export_path = self_out_path + '/' + _ccc_proj_name + '/zs_' + dir_time + '_' + batch_version
    if g_server_name=='test':
        _batch_export_path = self_out_path + '/' + _ccc_proj_name + '/cs_' + dir_time + '_' + batch_version
    if g_server_name=='local':
        _batch_export_path = self_out_path + '/' + _ccc_proj_name + '/bd_' + dir_time + '_' + batch_version
    
    _batch_ret_failure = list() # 失败
    _batch_ret_succeed = list() # 成功
    _batch_ret_skip = list()  # 忽略
    _json_mtime_content = tool.read_file_json(_batch_mtime_json)

    info_plist = batch_path + '/' + g_jsb_type + '/frameworks/runtime-src/proj.ios_mac/ios/info.plist'
    # print(_channel_list)

    for tpinfo in _channel_list:
        tp_channel_id = tpinfo[1]
        tp_is_pkg = tpinfo[0]
        tp_file_name = tpinfo[4]
        tp_pk_id = tpinfo[3]

        if tp_is_pkg=='0':
            _batch_ret_skip.append(tp_channel_id)
            continue

        # 换肤
        replace_ios_project_skin(tpinfo, _batch_res, info_plist, _json_mtime_content, batch_version, _batch_reicon_path, _batch_relaunchimage_path)
        
        _out_result_path = self_out_path + '/' + _xcode_proj_name
        _archive_name = 'batch_' + batch_version + '.xcarchive'
        _ios_archive_full = _out_result_path + '/archive/'+ _archive_name

        # archive
        xcode_ios_archive(tp_pk_id, _xcode_build_proj, _xcode_proj_name, batch_version, _ios_archive_full)
        
        # export_path
        dir_time = time.strftime('%m%d_%H%M',time.localtime(time.time()))
        _exportPath = _out_result_path + '/ipa_' + dir_time + '_' + batch_version

        # export
        xcode_ios_export(tp_pk_id, _ios_archive_full, _exportPath)

        # 出包成功 移动到指定目录
        if os.path.exists(_exportPath):
            tool.mkdir(_batch_export_path)
            _src_ipa_name = _exportPath + '/' + _xcode_proj_name + '-mobile.ipa'
            _dst_ipa_name = _batch_export_path + '/' + tp_file_name + '.ipa'

            if os.path.exists(_dst_ipa_name):
                i = 0
                while os.path.exists(_dst_ipa_name):
                    i += 1
                    _dst_ipa_name = _batch_export_path + '/' + tp_file_name + str(i) + '.ipa' 

            os.rename(_src_ipa_name, _dst_ipa_name)
            _batch_ret_succeed.append(tp_channel_id)

            # 清理ipa生成路径
            tool.rmtree(0, _exportPath)
        else:
            _batch_ret_failure.append(tp_channel_id)

    # 备份 mtime.json _batch_mtime_json
    shutil.copyfile(_batch_mtime_json, _batch_export_path+'/uuid-to-mtime.json')

    # 备份csv
    shutil.copyfile( get_batch_conf_csv_path(), _batch_export_path + '/' + _get_batch_csv() )

    _ended_time = time.time()
    _doing_time = _ended_time - _start_time
    print('耗时:' + str(_doing_time))

    # 成功渠道
    print('成功:',len(_batch_ret_succeed))
    for tp in _batch_ret_succeed:     
        print('', tp)

    print('失败:',len(_batch_ret_failure))
    for tp in _batch_ret_failure:     
        print('', tp)

    print('忽略:',len(_batch_ret_skip))
    for tp in _batch_ret_skip:     
        print('', tp)

    # 执行完成打开目录
    print('===================================执行完成')
    return True

# 获取构建参数返回值
def tools_get_ccc_param_bool(var):
    if var==1:return'true'
    return 'false'

def tools_is_ios():
    return g_platform_name == start_path.pkg_type_ios
def tools_is_android():
    return g_platform_name == start_path.pkg_type_android
def tools_is_web():
    return g_platform_name == start_path.pkg_type_web
def tools_is_hotUpdate():
    return g_platform_name == start_path.pkg_type_hotUpdate

def tools_get_ccc_platform():
    if tools_is_ios():return 'ios'
    if tools_is_android():return 'android'
    if tools_is_web():return 'web-mobile'
    if tools_is_hotUpdate():return 'android'
    return 'null'

# 获取ui参数
def tools_get_ccc_android_abi():
    temp_abi = 'appABIs=['
    abiCount = 0
    if g_armeabi_v7a==1:
        temp_abi += "'armeabi-v7a'"
        abiCount += 1

    if g_arm64_v8a==1:
        if abiCount!=0:
            temp_abi+=','
        temp_abi += "'arm64-v8a'"
        abiCount+= 1

    if g_x86==1:
        if abiCount!=0:
            temp_abi+=','
        temp_abi += "'x86'"
    temp_abi+='];'
    return temp_abi

# build_hall_res
def ccc_build_hall_res(jsb_path, ver_res, inputid, is_build, channelId, version):
    print('===================================构建简体大厅')
    
    build_path = jsb_path.split('/')[-2]
    
    version_entry_start._self_out_path = self_out_path
    version_entry_start._ccc_exe = g_creator_root
    version_entry_start._ccc_ver = g_creator_ver
    version_entry_start._ccc_proj = g_project_root
    version_entry_start._ccc_buildPath = build_path
    version_entry_start._ccc_jsb_type = g_jsb_type
    
    version_entry_start._channel_id = channelId
    version_entry_start._version = version
    
    version_entry_start._is_short = str(g_is_short)
    version_entry_start._remote_assets = g_remote_assets
    version_entry_start._import_zip = str(g_is_import_zip)
    version_entry_start._update_skin_num = g_update_skin_num

    version_entry_start._pkg_res_type = g_pkg_res_type
    version_entry_start._ver_res = ver_res
    version_entry_start._inputid = inputid
    version_entry_start._is_debug = str(g_is_debug)

    return version_entry_start.start_hall_res(is_build)

# ccc build
def ccc_build_platform( proj_root, is_batch, is_short ):
    global g_out_file_path
    global g_out_path_root
    global g_ccc_build_param
    
    # 构建路径
    tp_build_name = g_build_path
    tp_build_path = proj_root + '/' + tp_build_name

    tp_jsb_path = tp_build_path + '/' + g_jsb_type
    tp_library = proj_root + '/library'
    tp_temp = proj_root + '/temp'

    tp_mtime_json = tp_library + '/uuid-to-mtime.json'
    tp_jsb_path_mtime = tp_jsb_path + '/uuid-to-mtime.json'

    if len(tp_build_path)==0:
        return '构建路径不能为空'

    # 若重新构建 清理 lib + temp
    if g_clean_library==1:
        print('tool.rmtree:', tp_library)
        tool.rmtree(0, tp_library)

        print('tool.rmtree:', tp_temp)
        tool.rmtree(0, tp_temp)

    # build-param
    tp_builded_short = 0
    ccc_exe = get_creator_start_cmd()
    _app_debug = tools_get_ccc_param_bool(g_is_debug)
    _app_md5cache = tools_get_ccc_param_bool(g_is_md5cache)
    tp_platform = tools_get_ccc_platform()

    _ccc_param_path = ' --path ' + proj_root
    _ccc_param_debug = 'debug='+ _app_debug + ';'
    _ccc_param_buildpath = 'buildPath=' + tp_build_name + ';'
    _ccc_param_md5Cache = 'md5Cache=' + _app_md5cache + ';'
    _ccc_param_apiLevel = 'apiLevel=' + g_apiLevel + ';'
    _ccc_param_title = 'title=' + g_project_title + ';'
    _ccc_param_platform = 'platform=' + tp_platform + ';'
    _ccc_param_packageName = 'packageName=' + g_package_id + ';'
    
    # 刷新渠道号与版本号
    if g_creator_ver.find('1.10')!=0:
        do_update_channelid_version(0)

    g_ccc_build_param = ccc_exe

    # android 构建参数
    if tools_is_android() or (tools_is_hotUpdate() and IsWds):
        _ccc_param_appABIS = tools_get_ccc_android_abi()
        _ccc_param_platform = 'platform=android;'
        g_ccc_build_param = ccc_exe + _ccc_param_path + ' --build "' + _ccc_param_buildpath + _ccc_param_platform + _ccc_param_md5Cache + _ccc_param_debug + _ccc_param_apiLevel + _ccc_param_packageName + _ccc_param_appABIS + _ccc_param_title + '"'

    # ios 构建参数
    if tools_is_ios() or (tools_is_hotUpdate() and IsMacOS):
        _ccc_param_platform = 'platform=ios;'
        g_ccc_build_param = ccc_exe + _ccc_param_path + ' --build "' + _ccc_param_buildpath + _ccc_param_platform + _ccc_param_md5Cache + _ccc_param_packageName + _ccc_param_debug + _ccc_param_title +'"'

    # web-mobile 构建参数
    if tools_is_web():
        _isNative = ( tools_is_ios() or tools_is_android())
        # 拼接构建参数
        g_ccc_build_param = ccc_exe + _ccc_param_path + ' --build "' + _ccc_param_buildpath + _ccc_param_platform + _ccc_param_md5Cache + _ccc_param_debug + '"'

    # 构建项目-g_platform_name
    print('===================================构建项目')
    print(g_ccc_build_param)
    os.system(g_ccc_build_param)

    # 引擎构建后相关处理，未重命名处理
    if tools_is_ios():
        proj_ios_mac = proj_root + '/' + g_build_path + '/' + g_jsb_type + '/frameworks/runtime-src/proj.ios_mac/'
        domains_path = tool.get_dir_file(proj_ios_mac, '.entitlements')
        if len(domains_path)>0:
            domains_file = domains_path[0]
            rename_domains_file = proj_ios_mac + '/' + g_project_title + '-mobile.entitlements'
            os.rename(domains_file, rename_domains_file)
    
    # 恢复 gamesocket.js 文件
    if tools_is_web():
        build_web_mobile_bake = proj_root + '/build-templates/web-bakeup'
        build_web_mobile_root = proj_root + '/' + g_build_path + '/web-mobile'
            
        # 执行 web-mobile 发布修改
        if g_is_copyWebBakeup==1:
            print('copy:%s => %s'%(build_web_mobile_bake, build_web_mobile_root))
            tool.copydir(build_web_mobile_bake,build_web_mobile_root)
        g_out_file_path = proj_root + '/build/web-mobile'

    # 备份json-mtime
    print('copy:%s=>%s'%(tp_mtime_json, tp_jsb_path_mtime))
    shutil.copy(tp_mtime_json, tp_jsb_path_mtime )

    # 原生才有简体一说
    if tools_is_ios() or tools_is_android() or tools_is_hotUpdate():
        # 执行简体逻辑
        if is_short==1:
            ccc_build_hall_res(tp_jsb_path, 'link', '0', True, g_channel_id, g_version)
            tp_builded_short=1

        # 是否批量
        tp_build_batch_name = g_build_path
        tp_batch_build_path = proj_root + '/' + tp_build_batch_name
        tp_batch_jsb_link = tp_batch_build_path + '/jsb-link'

        # 拷贝批量
        if is_batch==1:
            tool.rmtree(0, tp_batch_jsb_link)
            shutil.copytree(tp_jsb_path, tp_batch_jsb_link, symlinks=False, ignore=None)

        # 执行简体逻辑-未执行简体逻辑
        if is_short==1 and tp_builded_short==0:
            ccc_build_hall_res(tp_batch_jsb_link, 'link', '0', True, g_channel_id, g_version)
            
    return True

# ccc complie
def ccc_complie_platform(proj_root):
    global g_out_file_path
    global g_out_path_root
    global g_ccc_build_param
    
    tp_build_path = proj_root + '/' + g_build_path
    tp_jsb_path = tp_build_path + '/' + g_jsb_type
    
    # 编译ipa
    if tools_is_ios():
        # xcode archive
        project_name = proj_root.split('/')[-1]

        tp_pk_id = g_package_id
        xcode_proj = tp_jsb_path + '/frameworks/runtime-src/proj.ios_mac/' + g_project_title + '.xcodeproj'
        version = g_version

        out_root = self_out_path + '/' + project_name
        archive_path = out_root + '/archive.xcarchive'
        xcode_ios_archive(tp_pk_id, xcode_proj, g_project_title, version, archive_path)
        
        # 刷新渠道
        update_project_channelid_and_version(proj_root, g_build_path, 1)

        # xcode export
        dir_time = time.strftime('%m%d_%H%M',time.localtime(time.time()))
        export_path = out_root + '/ipa_' + dir_time + '_' + version
        xcode_ios_export(tp_pk_id, archive_path, export_path)

        # 获取导出的ipa调整
        export_list = tool.get_dir_file(export_path, '.ipa')
        
        if len(export_list)==0:
            return "打包失败，请检查日志"
        else:
            ipa_file =  export_list[0]
            root_path = os.path.abspath(os.path.join(ipa_file, ".."))
            file_name = root_path + '/' + g_file_name + '.ipa'
            os.rename( ipa_file, file_name )

        # 输出文件
        g_out_file_path = export_path
        
        return True
    
    # 编译生成apk
    if tools_is_android():
        # 是否有java code需要覆盖
        if g_android_bak!='':
            print('===================================拷贝Java code')
            pj_android_bak_src = proj_root + '/' + g_android_bak
            pj_android_bak_dst = tp_jsb_path + '/frameworks/runtime-src'
            tool.copydir(pj_android_bak_src, pj_android_bak_dst)
        
        # 编译apk
        print('===================================编译生成APK')
        ccc_build_param = g_ccc_build_param.replace('--build','--compile')
        
        # 删除已有包，避免出错
        tool.rmtree(0,  tp_jsb_path + '/publish')
        tool.rmtree(0,  tp_jsb_path + '/simulator')
        
        # 编译
        print(ccc_build_param)

        # 开启日志监控
        

        # 执行命令
        os.system(ccc_build_param)

        # 关闭日志监控

        # 拷贝生成的apk到指定目录
        _creator_compile_apk_release = tp_jsb_path + '/publish/android'
        _creator_compile_apk_debug = tp_jsb_path + '/simulator/android'

        _apk_list = []
        _apk_d_name = '.apk'
        if g_is_debug==1:
            _apk_d_name='-debug-signed.apk'
            _apk_list = tool.get_dir_file(_creator_compile_apk_debug, '.apk')
        else:
            _apk_d_name='.apk'
            _apk_list = tool.get_dir_file(_creator_compile_apk_release, '.apk')

        dir_time = time.strftime('%m%d_%H%M',time.localtime(time.time()))
        _out_result_path = self_out_path + '/' + get_project_name() + '/apk_'+ dir_time + '_' + g_version
        tool.mkdir(_out_result_path)

        # 输出 apk 包
        apk_count=0
        for apk_file in _apk_list:
            out_apk_path = _out_result_path + '/' + g_file_name + _apk_d_name
            if apk_count>0:
                out_apk_path = _out_result_path + '/' + g_file_name + str(apk_count) + _apk_d_name
            apk_count += 1
            print('outfile: %s => %s'%(apk_file, out_apk_path))
            shutil.copy(apk_file, out_apk_path)
            
            # 输出 apk 包匹配的 uuid-json文件
            uuid_to_mtime = tp_jsb_path + '/' + g_uuid_json
            uuid_to_mtimebk = _out_result_path + '/' + g_file_name + '_' + g_uuid_json

            print('outfile: %s => %s'%(uuid_to_mtime, uuid_to_mtimebk))
            shutil.copy(uuid_to_mtime, uuid_to_mtimebk)
        
        # 编译失败提示
        if apk_count==0:
            shutil.rmtree(_out_result_path)
            tool.out_error(' Compile native project failure!!!!! pls check native.log')
        else:
            g_out_file_path = _out_result_path
    
    return True
            
# ios批量打包1: 生成archive 重签名->export ipa 
def do_start_batch_archive_ios():

    start_time = time.time()

    # 平台校验
    if tools_is_ios() and IsMacOS==False: 
        return "打包ios 请在mac下执行！"

    proj_root = g_project_root

    # 1 ccc-build
    ccc_build_platform(proj_root, 1, g_is_short)

    # 2 xcode archive
    project_name = proj_root.split('/')[-1]

    tp_pk_id = g_package_id
    xcode_proj = proj_root + '/'+g_batch_path+'/' + g_jsb_type + '/frameworks/runtime-src/proj.ios_mac/' + g_project_title + '.xcodeproj'
    version = g_version

    out_root = self_out_path + '/' + project_name
    archive_path = out_root + '/archive.xcarchive'
    xcode_ios_archive(tp_pk_id, xcode_proj, g_project_title, version, archive_path)

    # 3 xocde export
    dir_time = time.strftime('%m%d_%H%M',time.localtime(time.time()))
    export_path = out_root + '/ipa_' + dir_time + '_' + version
    xcode_ios_export(tp_pk_id, archive_path, export_path)

    # 是否成功导出
    export_list = tool.get_dir_file(export_path, '.ipa')

    # 拷贝ipa至批量签名路径
    if len(export_list)==0:
        return 'export-failure,请检查日志。'

    # 清理批量路径
    apia_path = get_batch_conf_path() + '/aipa'
    tool.rmtree(0, apia_path)
    tool.mkdir(apia_path)

    src_batch_ipa = export_list[0]
    ipa_name = src_batch_ipa.split('/')[-1]

    dst_batch_ipa = apia_path + '/' + ipa_name
    src_mtime = proj_root + '/' + g_batch_path + '/' + g_jsb_type +'/uuid-to-mtime.json'
    dst_mtime = apia_path + '/uuid-to-mtime.json'

    # 拷贝=>ipa
    print('copyfile %s => %s'%(src_mtime, dst_mtime))
    shutil.copyfile(src_mtime, dst_mtime)

    print('copyfile %s => %s'%(src_batch_ipa, dst_batch_ipa))
    shutil.copyfile(src_batch_ipa, dst_batch_ipa)

    # 批量重签
    do_start_signed_ipa_form_ipa('2')

    ended_time = time.time()
    doing_time = ended_time - start_time
    print('耗时:' + str(doing_time))

    # # 执行完成打开目录
    # print('===================================执行完成')
    return True

# 重新签名
def xcode_resign_ipa( ipa_path, export_path, unzip, resign ):
    signed_conf_path = get_batch_conf_path()
    signed_conf_aipa = signed_conf_path + '/aipa'
    sigend_tmp_path = signed_conf_aipa + '/tmp'
    signed_ipa_path = ipa_path
    dev_team_id = g_dev_teamid

    entitlements_path = sigend_tmp_path + '/entitlements.plist' 
    signed_mobileprovision_root = signed_conf_path + '/' + dev_team_id

    mobile_provision = '.mobileprovision'
    signed_mobileprovision_all = signed_mobileprovision_root + '/' + g_dev_teamid + mobile_provision

    if unzip==1:
        tool.rmtree(0,sigend_tmp_path)
        tool.mkdir(sigend_tmp_path)

        # 通过mobileprovision文件生成：首先生成一个完整的plist文件 entitlements.plist
        signed_embedded_plist = sigend_tmp_path + '/' + 'embedded.plist'
        embedded_plist_param = 'security cms -D -i ' + signed_mobileprovision_all + ' > ' + signed_embedded_plist
        print(embedded_plist_param)
        os.system(embedded_plist_param)

        entitlements_plist_param = '/usr/libexec/PlistBuddy -x -c "Print:Entitlements" ' + signed_embedded_plist + ' > ' + entitlements_path
        print(entitlements_plist_param)
        os.system(entitlements_plist_param)

        # 1.解压ipa包 unzip xxx.ipa
        unzip_ipa_param = 'unzip ' + signed_ipa_path + ' -d ' + sigend_tmp_path
        print(unzip_ipa_param)
        os.system(unzip_ipa_param)

    if resign==1:
        
        signed_tmp_Payload = sigend_tmp_path+'/Payload'
        app_list = tool.get_dir_path(signed_tmp_Payload,'.app')
        signed_tmp_Payload_app = signed_tmp_Payload + '/' + app_list[0]
        Payload_app = 'Payload/' + app_list[0]

        # src = app_list[0] 
        # app_md5_name = hashlib.md5(src.encode(encoding='UTF-8')).hexdigest()
        # signed_new_Payload_app = signed_tmp_Payload + '/' + app_md5_name + '.app'
        # os.rename(signed_tmp_Payload_app, signed_new_Payload_app)
        # signed_tmp_Payload_app = signed_new_Payload_app
        # Payload_app = 'Payload/' + app_md5_name + '.app'

        # 2.删除签名文件 'rm -rf Payload/xxx.app/_CodeSignature/'
        unzip_ipa_param = 'rm -rf ' + signed_tmp_Payload_app + '/_CodeSignature/CodeResources'
        print(unzip_ipa_param)
        if os.path.exists(signed_tmp_Payload_app + '/_CodeSignature/CodeResources'):
            os.system(unzip_ipa_param)

        # 3.替换配置文件 cp embedded.mobileprovision Payload/xxx.app/
        print('copyfile %s => %s'%(signed_mobileprovision_all,signed_tmp_Payload_app+'/embedded.mobileprovision'))
        shutil.copyfile(signed_mobileprovision_all, signed_tmp_Payload_app+'/embedded.mobileprovision')

        # resign_ipa_full = signed_conf_aipa + '/' + 'resigned-'+ipa_name+'.ipa'
        cd_parma = 'cd ' + sigend_tmp_path
        print(cd_parma)
        os.system(cd_parma)
        os.chdir(sigend_tmp_path)

        # 4.签名 codesign -f -s "你的证书的名称" --entitlements entitlements.plist Payload/xxx.app
        codesign_param = 'codesign -f -s "' + g_profiles_dev + '" --entitlements entitlements.plist ' + Payload_app
        print(codesign_param)
        os.system(codesign_param)

        # 5.打包 zip -r resign_xxx.ipa Payload/
        ipa_full_name = signed_ipa_path.split('/')[-1]
        ipa_name = ipa_full_name.split('.ipa')[0]

        # resign_ipa_full = sigend_tmp_path + '/' + 'resigned-'+ipa_name+'.ipa'
        resign_ipa_full = ipa_name + '.ipa'
        zip_ipa_param = 'zip -r ' + resign_ipa_full + ' ' + 'Payload'
        print(zip_ipa_param)
        os.system(zip_ipa_param)

        tool.mkdir(export_path)

        src_ipa_path = sigend_tmp_path + '/' + resign_ipa_full
        dst_ipa_path = export_path + '/' +resign_ipa_full

        print('movefile %s => %s'%(src_ipa_path, dst_ipa_path))
        os.rename(src_ipa_path, dst_ipa_path)
        return dst_ipa_path
    return "null"

# ipa重新签名 
def do_start_signed_ipa_form_ipa(sign_num):

    _start_time = time.time()

    signed_conf_path = get_batch_conf_path()
    signed_conf_aipa = signed_conf_path + '/aipa'
    sigend_tmp_path = signed_conf_aipa + '/tmp'
    tool.rmtree(0,sigend_tmp_path)
    tool.mkdir(sigend_tmp_path)

    signed_ipa_list = tool.get_dir_file(signed_conf_aipa, '.ipa')
    signed_ipa_path = ''
    ipa_count = len(signed_ipa_list)

    ipa_mtime_path = ''
    mtime_json_list = tool.get_dir_file(signed_conf_aipa, '.json')

    dir_time = time.strftime('%m%d_%H%M',time.localtime(time.time()))
    _batch_export_path = self_out_path + '/resigned/' + dir_time + '_' + g_version

    if len(mtime_json_list)>0:
        ipa_mtime_path = mtime_json_list[0]

    # 环境检测
    if ipa_count==0: 
        return '未找到重签ipa，请检查路径配置:'+signed_conf_aipa
        

    # # ipa批量重签
    if sign_num=='1':
        if ipa_count<=0:
            return 'ipa重签，必须存在一个以上ipa包，请检查路径'+signed_conf_aipa

        for i in range(0, ipa_count):
            signed_ipa_path = signed_ipa_list[i]
            xcode_resign_ipa( signed_ipa_path, _batch_export_path, 1, 1 )

    # mtime_json 替换皮肤重签
    if sign_num=='2':
        if ipa_count!=1:
            return '批量ipa重签，只能存在一个ipa包，请检查路径'+signed_conf_aipa

        if len(ipa_mtime_path)==0 and os.path.exists(ipa_mtime_path)==False:
            return '请检查 mtime.json 文件，是否存在！'

        signed_ipa_path = signed_ipa_list[0]

        # 1.解压ipa
        xcode_resign_ipa( signed_ipa_path, _batch_export_path, 1, 0 )

        # 结果统计
        _batch_ret_failure = list()
        _batch_ret_succeed = list()
        _batch_ret_skip = list()

        # archive and build 路径
        unzip_tmp = get_batch_conf_path() + '/aipa/tmp'
        unzip_Payload = unzip_tmp + '/Payload'
        unzip_app_list = tool.get_dir_path(unzip_Payload, '.app')
        unzip_app_path = unzip_Payload + '/' + unzip_app_list[0]

        _assets_car_path = signed_conf_path + '/' + 'Assets.xcassets'

        _batch_write_channel = 'resources/common/channel.dat'
        _json_mtime_content = tool.read_file_json(ipa_mtime_path)

        _res_path = unzip_app_path + '/res'
        _batch_reicon_path = unzip_app_path
        _batch_relaunchimage_path = unzip_app_path

        _batch_conf_path = get_batch_conf_path()
        _csv_path = _batch_conf_path+'/'+_get_batch_csv()
        skin_path = _batch_conf_path + '/appskin'
        _channel_list = load_channel_list(_csv_path)

        info_plist = unzip_app_path + '/info.plist'

        # print(_channel_list)
        for tpinfo in _channel_list:

            # 替换信息
            tp_count = len(tpinfo)
            if tp_count<5:
                continue
            tp_is_pk = tpinfo[0]
            tp_channel_id = tpinfo[1]
            tp_file_name = tpinfo[4]

            tp_mainchn_id = tp_channel_id[0:3]

            # 忽略打包
            if tp_is_pk=='0':
                _batch_ret_skip.append(tp_channel_id)
                continue
            
            # 换肤
            replace_ios_project_skin(tpinfo, _res_path, info_plist, _json_mtime_content, '', _batch_reicon_path, _batch_relaunchimage_path)

            # build Assets.car
            # xcrun actool $DIR/Assets.xcassets --compile $DIR/build --platform iphoneos --minimum-deployment-target 8.0 --app-icon AppIcon --output-partial-info-plist $DIR/build/partial.plist
            tp_channel_icon = skin_path + '/' + tp_channel_id+'/icon'
            if os.path.exists(tp_channel_icon)==False:
                tp_channel_icon = skin_path + '/' + tp_mainchn_id+'/icon'
            tool.copydir(tp_channel_icon, _assets_car_path+'/AppIcon.appiconset')

            build_Assets_path = signed_conf_path + '/build'
            tool.rmtree(0, build_Assets_path)
            tool.mkdir(build_Assets_path)

            build_Assets_plist = signed_conf_path + '/build/partial.plist'
            build_Assets_car_param = 'xcrun actool ' + _assets_car_path + ' --compile ' + build_Assets_path + ' --platform iphoneos --minimum-deployment-target 8.0 --app-icon AppIcon --output-partial-info-plist ' + build_Assets_plist
            print(build_Assets_car_param)
            os.system(build_Assets_car_param)
            os.remove(build_Assets_plist)
            tool.copydir(build_Assets_path, _batch_reicon_path)

            # 重新签名
            src_ipa_path = xcode_resign_ipa( signed_ipa_path, _batch_export_path, 0, 1 )

            # 出包成功 移动到指定目录
            if os.path.exists(src_ipa_path):
                tool.mkdir(_batch_export_path)

                dst_ipa_path = _batch_export_path + '/' + tp_file_name + '.ipa'

                if os.path.exists(dst_ipa_path):
                    i = 0
                    while os.path.exists(dst_ipa_path):
                        i += 1
                        dst_ipa_path = _batch_export_path + '/' + tp_file_name + str(i) + '.ipa'

                print('movefile %s => %s'%(src_ipa_path,dst_ipa_path))
                os.rename(src_ipa_path, dst_ipa_path)
                _batch_ret_succeed.append(tp_channel_id)
            else:
                _batch_ret_failure.append(tp_channel_id)
        
        # 备份文件
        shutil.copyfile( ipa_mtime_path,  _batch_export_path+'/uuid-to-mtime.json')
        shutil.copyfile( get_batch_conf_csv_path(), _batch_export_path+'/'+_get_batch_csv() )

        _ended_time = time.time()
        _doing_time = _ended_time - _start_time
        print('耗时:' + str(_doing_time))
        
        print('=======================================================')
        print('忽略:',len(_batch_ret_skip))
        for tp in _batch_ret_skip:     
            print('', tp)
        print('-------------------------------------------------------')
        print('失败:',len(_batch_ret_failure))
        for tp in _batch_ret_failure:     
            print('', tp)
        print('-------------------------------------------------------')
        # 成功渠道
        print('成功:',len(_batch_ret_succeed))
        for tp in _batch_ret_succeed:     
            print('', tp)
        print('=======================================================')

    print('处理完成')
    return True

# 环境检查
def do_check_batch_environ_param():
    print('do_check_batch_logic')

    _ccc_proj_root = g_project_root

    # 构建路径
    _batch_build_path = _ccc_proj_root + '/' + g_build_path
    _batch_conf_path = get_batch_conf_path()
    _batch_logic_path = get_batch_path()

    if tools_is_ios():
        # ios批处理，不允许批处理路径与构建路径一样
        if _batch_logic_path==_batch_build_path:
            return 'ios批处理:批处理路径不能与构建路径一样！'

        if os.path.exists(_batch_build_path)==False:
            return 'ios批处理:工程路径异常，请检查！'

        if os.path.exists(_batch_conf_path)==False:
            return 'ios批处理:配置路径异常，请检查！'

        # csv
        _batch_csv_path = _batch_conf_path+'/'+_get_batch_csv()
        if os.path.exists(_batch_csv_path)==False:
            return 'ios批处理:配置文件文件不存在，请检查！'

        # csv 格式检查
        tp_channel_list = load_channel_list(_batch_csv_path)
        if len(tp_channel_list)==0:
            return '未读取到渠道配置，请检查csv文件列表！'

        tp_index = 0
        for tpinfo in tp_channel_list:
            tplen = len(tpinfo)
            
            if tplen<5:
                continue
            
            # 渠道号校验 暂时只校验长度 六位
            tp_channel_id = tpinfo[1]
            if len(tp_channel_id)!=6:
                return 'csv 渠道号必须为6位数值 索引:' + str(tp_index) + ' 错误数据:' + tp_channel_id
            tp_index+=1

        # csv 路径校验
        _info_csv = _batch_conf_path+'/'+ 'channel_info.csv'
        if os.path.exists(_info_csv)==False:
            return '请检查信息文件'

        # 请检查导出配置文件
        _export_option_plist = self_out_path+'/exportOption/' + get_exportOption_list_name()
        if os.path.exists(_export_option_plist)==False:
            return 'ios批处理:导出文件plist异常，请检查'+ get_exportOption_list_name() +'文件！'

    if tools_is_android():
        # keystore 校验
        _keystore = g_keystore_name
        _batch_keystore_path = _batch_conf_path+'/'+ _keystore
        if os.path.exists(_batch_keystore_path)==False:
            return _keystore+'文件不存在,请检查。'
        
        # csv 路径校验
        _info_csv = _batch_conf_path+'/'+ _get_batch_csv()
        if os.path.exists(_info_csv)==False:
            return '请检查信息文件'

        # csv
        _batch_csv_path = _batch_conf_path+'/'+_get_batch_csv()
        if os.path.exists(_batch_csv_path)==False:
            return 'ios批处理:配置文件文件不存在，请检查！'

        # csv 格式检查
        tp_channel_list = load_channel_list(_batch_csv_path)
        if len(tp_channel_list)==0:
            return '未读取到渠道配置，请检查csv文件列表！'
        
        tp_index=0
        for tpinfo in tp_channel_list:
            tplen = len(tpinfo)
            if tplen<2:
                continue
            
            # 长度校验
            if tplen<5:
                return 'csv信息分割错误 索引:' + str(tp_index) + ' 格式错误，请校验数据格式！'
            
            # 渠道号校验 暂时只校验长度 六位
            if len(tpinfo[1])!=6:
                return 'csv信息分割错误 索引:' + str(tp_index) + ' 格式错误，请校验数据格式！'
            tp_index+=1
    
    if tools_is_web():
        print('check:_is_pf_web_mobile')

    return True

# 构建大厅版本
def do_hall_res_script():
    jsb_path = get_build_platform_path(g_jsb_type)
    ccc_build_hall_res( jsb_path, 'link', '0', True, g_channel_id, g_version )
    print('大厅版本执行完成')
    return '简体大厅资源-完成！'

def replace_build_channel(channel_id, app_name, res_path, mtime_connect):
    
    res_raw_assets = res_path + '/' + 'raw-assets'
    res_import = res_path + '/' + 'import'

    # 替换渠道号
    channel_json_path = start_path.channel_config;
    tp_key = replase_channel_skip(channel_json_path, mtime_connect)

    if tp_key!=0:
        ext = os.path.splitext(channel_json_path)[1]
        dst_file_raw = res_raw_assets + '/' + tp_key[0:2] + '/' + tp_key + ext
        dst_file_ip = res_import + '/' + tp_key[0:2] + '/' + tp_key + ext
        dst_ret = 0
        
        # 编辑渠道号文件
        if os.path.exists(dst_file_raw):
            dst_ret = dst_file_raw
        if os.path.exists(dst_file_ip) and dst_ret==0:
            dst_ret = dst_file_ip

        if dst_ret!=0:
            json_content = tool.read_file_json(dst_ret)
            print('0-----:',json_content)
            json_content['channel_id'] = str(channel_id)
            json_content['appName'] = app_name
            print('1-----:',json_content)
            tool.write_file_content(dst_ret, json.dumps(json_content))

# 替换ios打包皮肤
def replace_ios_project_skin(tpinfo, res_path, info_plist, mtime_connect, version, icon_path, launch_path ):
    # 替换信息
    tp_count = len(tpinfo)
    if tp_count<5:
        return 0
    tp_channel_id = tpinfo[1]
    tp_app_name = tpinfo[2]
    tp_pk_id = tpinfo[3]

    # 是否有扩展处理
    tp_have_ex = tp_count>5
    tp_mainchn_id = tp_channel_id[0:3]

    batch_conf_path = get_batch_conf_path()

    res_raw_assets = res_path + '/' + 'raw-assets'
    res_import = res_path + '/' + 'import'
    skin_path = batch_conf_path + '/appskin'

    # 替换渠道号
    replace_build_channel(tp_channel_id, tp_app_name, res_path, mtime_connect)

    # 替换渠道皮肤
    print('获得渠道皮肤')
    tp_channel_skip = skin_path + '/' + tp_channel_id + '/skin'
    if os.path.exists(tp_channel_skip)==False:
        tp_channel_skip = skin_path+'/'+tp_mainchn_id + '/skin'
    _skip_list = tool.get_dir_all_file(tp_channel_skip)

    # 替换皮肤
    for tp_skip in _skip_list:
        tp_src_res = tp_skip.replace(tp_channel_skip+'/','')
        tp_key = replase_channel_skip(tp_src_res, mtime_connect)
        tp_ret = 0
        if tp_key!=0:
            ext = os.path.splitext(tp_skip)[1]
            dst_file_raw = res_raw_assets + '/' + tp_key[0:2] + '/' + tp_key + ext
            dst_file_ip = res_import + '/' + tp_key[0:2] + '/' + tp_key + ext

            # 查找替换路径
            if os.path.exists(dst_file_raw):
                print('copy:%s=>%s'%(tp_skip, dst_file_raw))
                shutil.copy(tp_skip, dst_file_raw)
                tp_ret = 1
            
            if os.path.exists(dst_file_ip) and tp_ret==0:
                print('copy:%s=>%s'%(tp_skip, dst_file_ip))
                shutil.copy(tp_skip, dst_file_ip)
                tp_ret = 1
            
            if tp_ret==0:
                print('无法查找路径:' + tp_skip + ' 请检查配置')

    # 替换应用id
    # 修改 Plist
    # defaults write ${ipaPath}/Payload/${schemeName}.app/info.plist "CFBundleName" $appName
    # defaults write ${ipaPath}/Payload/${schemeName}.app/info.plist "CFBundleDisplayName" $appDisplayName
    print('readPlist:'+info_plist)
    if info_plist and len(info_plist)>0:
        info_cont = readPlist(info_plist)
        
        # 替换 pk_id
        info_cont['CFBundleIdentifier'] = tp_pk_id
        
        # 替换游戏名字
        info_cont['CFBundleDisplayName'] = tp_app_name

        # 打包版本号
        if len(version)>0:
            info_cont['CFBundleShortVersionString'] = version
        
        # 替换version
        time_version = int(time.time())
        info_cont['CFBundleVersion'] = str(time_version)

        # 扩展处理-微信登陆
        if tp_have_ex:
            have_weixin = get_info_key_index(tpinfo,'weixin')
            have_jiuliao = get_info_key_index(tpinfo,'jiuliao')
            have_openinstall = get_info_key_index(tpinfo,'openinstall')

            # 扩展处理-微信登陆
            if have_weixin!=-1:
                # 获取微信信息
                ex_list = batch_conf_path + '/channel_info.csv'
                ex_info = load_channel_list(ex_list)
                ex_cont = get_channel_list(ex_info, tp_channel_id, 0)
                if ex_cont==0:
                    ex_cont = get_channel_list(ex_info, tp_channel_id[0:3]+'000', 0)
                weixin_index = get_info_key_index(ex_cont,'weixin')
                ex_tp_wxappid = ex_cont[weixin_index+1]
                ex_tp_wxsecret = ex_cont[weixin_index+2]
                ex_tp_universalLink = ex_cont[weixin_index+3]
                
                if not 'CFBundleURLTypes' in info_cont:
                    info_cont['CFBundleURLTypes']=[]
                # 查找微信信息修改
                urlTypes = info_cont['CFBundleURLTypes']
                isFind = False
                for dic in urlTypes:
                    if dic['CFBundleURLName']=='weixin':
                        wx_ary = dic['CFBundleURLSchemes']
                        wx_ary.clear()
                        wx_ary.append(ex_tp_wxappid)
                        wx_ary.append(ex_tp_wxsecret)
                        wx_ary.append(ex_tp_universalLink)
                        isFind=True
                        break
            
                # 校验修改
                if isFind==False:
                    dic = {'CFBundleURLName':'weixin','CFBundleURLSchemes':[ex_tp_wxappid,ex_tp_wxsecret,ex_tp_universalLink]}
                    info_cont['CFBundleURLTypes'].append(dic)

                # 修改代码中定义的微信相关信息，以及打开编译微信代码，注意请勿修改代码路径
                # OCDefine_h_path = _batch_path_proj_ios_mac+'/ios/native/OCDefine.h'
                # assets_script.do_ios_oc_code(OCDefine_h_path, 'contain_replace_lines', '//#define USING_WX', '#define USING_WX\n') # 打开编译微信代码开关

                # 写入配置
                writePlist(info_cont, info_plist, False)

            # 无微信登陆-删除且不编译微信key
            else:
                if 'CFBundleURLTypes' in info_cont:
                    urlTypes = info_cont['CFBundleURLTypes']
                    isFind = False
                    del_index = 0
                    for dic in urlTypes:
                        if dic['CFBundleURLName']=='weixin':
                            isFind=True
                            urlTypes.pop(del_index)
                            break
                        del_index+=1

                    # 写入配置
                    writePlist(info_cont, info_plist, False)

                    # 注释微信登录编译
                    # OCDefine_h_path = _batch_path_proj_ios_mac+'/ios/native/OCDefine.h'
                    # assets_script.do_ios_oc_code(OCDefine_h_path, 'contain_replace_lines', '#define USING_WX', '//#define USING_WX\n') 
                
                # 扩展处理-久聊支付
                if have_jiuliao!=-1:
                    print('jiuliao_index')

                # 扩展处理 openinstall
                ex_name = 'openinstall'
                if have_openinstall!=-1:
                    # openinstall
                    ex_list = batch_conf_path + '/channel_info.csv'
                    ex_info = load_channel_list(ex_list)
                    ex_cont = get_channel_list(ex_info, tp_channel_id, 0)
                    if ex_cont==0:
                        tp_main_channel_id = tp_channel_id[0:3] + '000'
                        ex_cont = get_channel_list(ex_info, tp_main_channel_id, 0)

                    tp_index = get_info_key_index(ex_cont,ex_name)
                    ex_appid = ex_cont[tp_index+1]
                    
                    # export url_type
                    urlTypes = info_cont['CFBundleURLTypes']
                    isFind = False
                    for dic in urlTypes:
                        if dic['CFBundleURLName']==ex_name:
                            dic['CFBundleURLSchemes'][0]=ex_appid
                            isFind=True
                            break
                
                    # 校验修改
                    if isFind==False:
                        dic = {'CFBundleURLName':ex_name,'CFBundleURLSchemes':[ex_appid]}
                        info_cont['CFBundleURLTypes'].append(dic)

                    info_cont['com.openinstall.APP_KEY']=ex_appid

                    # 启用openinstall
                    # OCDefine_h_path = _batch_path_proj_ios_mac+'/ios/native/OCDefine.h'
                    # assets_script.do_ios_oc_code(OCDefine_h_path, 'contain_replace_lines', '//#define USING_OPENINSTALL', '#define USING_OPENINSTALL\n') # 打开编译微信代码开关

                    # 写入配置
                    writePlist(info_cont, info_plist, False)

                # 无openinstall
                else:
                    if 'CFBundleURLTypes' in info_cont:
                        urlTypes = info_cont['CFBundleURLTypes']
                        isFind = False
                        del_index = 0
                        for dic in urlTypes:
                            if dic['CFBundleURLName']==ex_name:
                                isFind=True
                                urlTypes.pop(del_index)
                                break
                            del_index+=1                

                        # 写入配置
                        writePlist(info_cont, info_plist, False)

                        # 禁用openinstall
                        # OCDefine_h_path = _batch_path_proj_ios_mac+'/ios/native/OCDefine.h'
                        # assets_script.do_ios_oc_code(OCDefine_h_path, 'contain_replace_lines', '#define USING_OPENINSTALL', '//#define USING_OPENINSTALL\n') 

        # 没有扩展-屏蔽微信
        else:
            #移除微信key
            if 'CFBundleURLTypes' in info_cont:

                # 清理扩展
                info_cont['CFBundleURLTypes']=[]             

                # 写入配置
                writePlist(info_cont, info_plist, False)

                # 禁用微信 禁用openinstall
                # OCDefine_h_path = _batch_path_proj_ios_mac+'/ios/native/OCDefine.h'
                # assets_script.do_ios_oc_code(OCDefine_h_path, 'contain_replace_lines', '#define USING_OPENINSTALL', '//#define USING_OPENINSTALL\n') 
                # assets_script.do_ios_oc_code(OCDefine_h_path, 'contain_replace_lines', '#define USING_WX', '//#define USING_WX\n') # 打开编译微信代码开关

    # 替换icon 
    if icon_path and len(icon_path)>0:
        tp_channel_icon = skin_path + '/' + tp_channel_id+'/icon'
        if os.path.exists(tp_channel_icon)==False:
            tp_channel_icon = skin_path + '/' + tp_mainchn_id+'/icon'
    
        tool.copydir(tp_channel_icon, icon_path)

    # 替换启动图
    if launch_path and len(launch_path)>0:
        tp_channel_launch = skin_path + '/' + tp_channel_id+'/launch'
        if os.path.exists(tp_channel_launch)==False:
            tp_channel_launch = skin_path + '/' + tp_mainchn_id+'/launch'
        tool.copydir(tp_channel_launch, launch_path)

def update_project_channelid_and_version(proj_path, build_path, buildTime):
    print('def:update_project_channelid_and_version: '+ proj_path + ' build_path:' + build_path)

    # 更新路径与数据
    mtime_json = 'uuid-to-mtime.json'
    logic_proj = proj_path + '/' + build_path + '/' + g_jsb_type
    if not os.path.exists(logic_proj):
        return;
    mtime_path = logic_proj + '/' + mtime_json

    _res_path = logic_proj + '/res'
    _res_import = _res_path + '/import'
    _res_raw_assets = _res_path + '/raw-assets'

    tp_channel_id = g_channel_id
    tp_main_channelId = start_path.getMainChannelId(tp_channel_id)
    tp_app_name = g_app_name

    project_manifest = start_path.get_res_manifest_full_path(0)
    version_manifest = start_path.get_res_version_full_path(0)
    channel_file = start_path.channel_config

    # 更新assets目录
    assets_path = proj_path + '/assets'
    if os.path.exists(assets_path):
        # 更新assets渠道号
        channel_json = proj_path + '/assets/' + channel_file

        # 获取微信信息
        batch_conf_path = get_batch_conf_path()
        if batch_conf_path==None: 
            tool.out_error('batch_conf_path not found')
            return
        ex_list = batch_conf_path + '/channel_info.csv'
        ex_info = load_channel_list(ex_list)
        ex_cont = get_channel_list(ex_info, tp_channel_id, 0)
        
        # 微信信息
        weixin_index = ''
        ex_tp_wxappid = ''
        ex_tp_wxsecret = ''
        ex_tp_universalLink = ''
        
        if ex_cont==0:ex_cont=get_channel_list(ex_info, tp_main_channelId, 0)
        if ex_cont==0:ex_cont=get_channel_list(ex_info, '0', 0)
        if ex_cont!=0:
            weixin_index = get_info_key_index(ex_cont,'weixin')
            if weixin_index!=-1:
                ex_tp_wxappid = ex_cont[weixin_index+1]
                ex_tp_wxsecret = ex_cont[weixin_index+2]
                ex_tp_universalLink = ex_cont[weixin_index+3]
            
        if os.path.exists(channel_json):
            json_content = tool.read_file_json(channel_json)
            print('assets0------:',json_content)
            # channel_content = json_content['json']
            json_content['channel_id'] = str(tp_channel_id)
            json_content['appName'] = tp_app_name
            json_content['wxappid'] = ex_tp_wxappid
            json_content['wxappsecret'] = ex_tp_wxsecret
            json_content['universalLink'] = ex_tp_universalLink
            print('assets1------:',json_content)
            tool.write_file_json_indent4(channel_json, json_content)

        # 更新版本号
        pm_path = proj_path + '/assets/' + project_manifest
        vm_path = proj_path + '/assets/' + version_manifest

        if os.path.exists(vm_path):
            # 更新version
            vm_content = tool.read_file_json(vm_path)
            print('version0:',vm_content)
            
            vm_content['version'] = g_version 
            print('version1:',vm_content)
            tool.write_file_json(vm_path, vm_content)

            # 更新project
            pm_content = tool.read_file_json(pm_path)
            pm_content['version'] = vm_content['version']
            
            tool.write_file_json(pm_path, pm_content)

    # 编译前
    if buildTime==0:return;
    
    # 构建后的project修改
    if not os.path.exists(logic_proj):
        tool.out_red('warning:'+'not found path:'+logic_proj)
        return

    if not os.path.exists(mtime_path):
        tool.out_red('warning:'+'not found file:'+mtime_path)
        return
    
    _json_mtime_content = tool.read_file_json(mtime_path)
    
    # 更新版本 - version.manifest 
    tp_key = replase_channel_skip(version_manifest, _json_mtime_content)
    if tp_key!=0:
        ext = os.path.splitext(version_manifest)[1]
        dst_file_raw = _res_raw_assets + '/' + tp_key[0:2] + '/' + tp_key + ext
        dst_file_ip = _res_import + '/' + tp_key[0:2] + '/' + tp_key + ext
        dst_ret = 0
        
        if os.path.exists(dst_file_raw):
            dst_ret = dst_file_raw
        if os.path.exists(dst_file_ip) and dst_ret==0:
            dst_ret = dst_file_ip

        if dst_ret!=0:
            vm_content = tool.read_file_json(dst_ret)
            print('version0:',vm_content)
            
            vm_content['version'] = g_version
            print('version1:',vm_content)
            
            tool.write_file_json(dst_ret, vm_content)

    # 更新版本 - project.manifest 暂不更新 url{version}，url{version}
    tp_key = replase_channel_skip(project_manifest, _json_mtime_content)
    if tp_key!=0:
        ext = os.path.splitext(project_manifest)[1]
        dst_file_raw = _res_raw_assets + '/' + tp_key[0:2] + '/' + tp_key + ext
        dst_file_ip = _res_import + '/' + tp_key[0:2] + '/' + tp_key + ext
        dst_ret = 0
        
        if os.path.exists(dst_file_raw):dst_ret=dst_file_raw
        if os.path.exists(dst_file_ip) and dst_ret==0:dst_ret=dst_file_ip

        # 更新project.manifest
        if dst_ret!=0:
            vm_content = tool.read_file_json(dst_ret)
            vm_content['version'] = g_version
            
            tool.write_file_json(dst_ret, vm_content)
            
    # ios-换肤
    if tools_is_ios():
        # 更新icon 与 启动图
        proj_ios_mac = logic_proj + '/frameworks/runtime-src/proj.ios_mac'
        images_xcassets_root = proj_ios_mac + '/Images.xcassets'
        appIcon_appiconset = images_xcassets_root + '/AppIcon.appiconset' 
        launchImage_launchimage = images_xcassets_root + '/LaunchImage.launchimage'
        info_plist = proj_ios_mac + '/ios/Info.plist'
        
        # 替换-skin
        csv_path = get_batch_conf_path() + '/' + _get_batch_csv()
        channel_list = load_channel_list(csv_path)
        channel_info = get_channel_list(channel_list, tp_channel_id, 1)
        replace_ios_project_skin(channel_info, _res_path, info_plist, _json_mtime_content, g_version, appIcon_appiconset, launchImage_launchimage)
    
        # 替换通用连接域
        entitle_path = tool.get_dir_file(proj_ios_mac,'.entitlements')
        if len(entitle_path)>0:
            # applinks
            batch_conf_path = get_batch_conf_path()
            ulink_path = batch_conf_path + '/universalLink.csv'
            ulink_info = load_channel_list(ulink_path)
            ulink_cont = get_channel_list(ulink_info, tp_channel_id, 0)
            if ulink_cont==0:ulink_cont=get_channel_list(ulink_info, tp_channel_id[0:3]+'000', 0)
            if ulink_cont==0:ulink_cont=get_channel_list(ulink_info, '0', 0)
            ulinks_idx = get_info_key_index(ulink_cont,'applinks')
            ex_tp_domains = ulink_cont[ulinks_idx+1]

            domains_plist_path = entitle_path[0]
            domains_cont= readPlist(domains_plist_path)
            domains_key = 'com.apple.developer.associated-domains'

            if not domains_key in domains_cont:domains_cont[domains_key]=[]
            dp_array = domains_cont[domains_key]

            if len(dp_array)==0:
                dp_array.append(ex_tp_domains)
            else:
                dp_array[0]=ex_tp_domains
            writePlist(domains_cont, domains_plist_path, False)

    # andoid-换肤
    if tools_is_android():
        replace_build_channel(tp_channel_id, g_app_name, _res_path, _json_mtime_content)

# 打开批处理模板
def do_open_batch_skin_templates():
    _batch_conf_path = get_batch_conf_path()
    _batch_skin_path = _batch_conf_path + '/appskin'
    _batch_skin_help = _batch_skin_path+'/template_help.txt'
    
    if os.path.exists(_batch_skin_path):
        tool.open_finder(_batch_skin_path)

    if os.path.exists(_batch_skin_help):
        tool.open_finder(_batch_skin_help)

# 打开配置版本
def do_open_batch_csv():
    _batch_conf_path = get_batch_conf_path()
    _csv_path = _batch_conf_path+'/'+_get_batch_csv()

    if os.path.exists(_csv_path)==False:
        tool.out_error( '配置路径异常，请检查:' + _csv_path )
        return
    tool.open_finder(_csv_path)

# install-res+bugliy
def do_event_install_entry_engine(ccc_ver):

    _ccc_root = g_creator_root
    install_file_path = self_out_path + '/install_native_' + ccc_ver +'/resources'

    # 拷贝并 逆向备份原始文件
    if IsWds:
        tool.copydir(install_file_path, _ccc_root+'/resources', True, True)
    else:
        tool.copydir(install_file_path, _ccc_root+'/Contents/resources', True, True)
    tool.out_blue('安装完成')

# 启动creator
def do_start_creator_app():
    ccc_exe = get_creator_start_cmd()
    subprocess.call(ccc_exe, shell=True)

# 构建热更资源
def do_build_hotUpdate():
    
    global g_out_file_path
    global g_out_path_root
    
    # 输出资源类型
    inputid='0'
    if g_update_out_res_hall==1:inputid='0'
    if g_update_out_res_all==1:inputid='2'
    if g_update_out_res_game_id==1:inputid=g_update_out_res_id_str

    # use-res-link-ver
    ver_res = 'link'
    
    # use-old-ver
    if g_update_use_res_old_ver==1:ver_res = g_update_use_res_old_str

    jsb_path = get_build_platform_path(g_jsb_type)
    
    # 构建
    ccc_build_platform(g_project_root, 0, 0)
    
    # 热更处理
    ret = ccc_build_hall_res( jsb_path, ver_res, inputid, False, g_channel_id, g_update_hot_version)
    g_out_file_path = self_out_path + '/' + get_project_name() + '/' + g_update_skin_num + '/' + g_update_hot_version
    g_out_path_root = g_update_skin_num + '/' + g_update_hot_version
    
    # 热更自动上传是否开启
    if g_update_oss_upload==1 and tools_is_hotUpdate():
        oss_server.startUpload(g_out_file_path, g_out_path_root)
    return ret

# CODE EDIT=================================================================================
_write_assets_time=0
_write_delay_time=1.0

# 正式服
def _set_server_public():
    tool.out_green( '修改连接 - 正式服:' )
    ret = assets_script.do_base_serverType(g_project_root, 0)
    return ret
    
# 测试服
def _set_server_test():
    tool.out_green( '修改连接 - 测试服:' )
    ret = assets_script.do_base_serverType(g_project_root, 1)
    return ret

# 内测服
def _set_server_local():
    tool.out_green( '修改连接 - 内测服:' )
    ret = assets_script.do_base_serverType(g_project_root, 2)
    return ret

