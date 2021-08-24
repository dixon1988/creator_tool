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
import io
import start_config
import copyGame

# import path
fatherdir = os.path.dirname(os.path.abspath(__file__))
fatherdir = os.path.abspath(os.path.join(fatherdir, ".."))
sys.path.append(fatherdir+'/python_service')

# 平台持续类型
platform_name=platform.platform()
IsIos=platform_name.find("Darwin")==0
IsWds=platform_name.find("Windows")==0

if IsIos:
    from biplist import *
from stat import *

# 自定义脚本
import tool
import start_pkg
import pkg_client
import pkg_cmd
import pkg_buf

this = sys.modules[__name__]
self_path = os.path.split(os.path.realpath(__file__))[0]
self_path = tool.path_replace(self_path)

os.chdir(self_path)

self_out_path = os.path.abspath(os.path.join(self_path, ".."))
self_out_path = tool.path_replace(self_out_path)

print(":-------------------------------------------:")
print("platform:%s"%(platform_name))
print(":-------------------------------------------:")

print('self_path = '+self_path)
print('self_out_path = ' + self_out_path)

# 窗口设置
tk_root = tk.Tk()

win_w=680
win_h=730
if IsIos:
    win_w=700
sw = tk_root.winfo_screenwidth()
sh = tk_root.winfo_screenheight()

win_geometry = str(win_w) + 'x' + str(win_h) + '+'+ str(int((sw-win_w)/2)) + '+' + str(int((sh-win_h)/2))

tk_root.title('CocosCreator-v2.4.5--请保证原工程目录编译正常通过！')
tk_root.geometry(win_geometry)

def_font=('宋体', 10)
if IsIos:def_font=('宋体', 12)

# 启用禁用
s_state_normal = 'normal'
s_state_disabled = 'disabled'

g_creator_root = tk.StringVar()     # CocosCreator.exe 所在目录
g_creator_ver = tk.StringVar()      # ver
g_project_root = tk.StringVar()     # 工程目录
g_remote_assets = tk.StringVar()    # 热更远程地址

g_project_title = tk.StringVar()    # 工程标题 ios：[target]-mobile
g_build_path = tk.StringVar()       # 构建路径

g_channel_id = tk.IntVar()          # 渠道号: 102011
g_config_id = tk.StringVar()        # 配置编号：102
g_version = tk.StringVar()          # 版本号: 1.1.1
g_app_name = tk.StringVar()         # 应用名: 火特娱乐991
g_package_id = tk.StringVar()       # 包名: org.HTQP.game

g_is_res_normal = tk.IntVar()       # 资源默认
g_is_encrypted = tk.IntVar()        # 资源加密
g_is_etc2_ccc = tk.IntVar()         # ccc-etc2压缩
g_is_etc2_py = tk.IntVar()          # 资源etc2-gzi

g_is_debug = tk.IntVar()            # 是否debug
g_is_md5cache = tk.IntVar()         # md5cache
g_is_short = tk.IntVar()            # 简体包
g_is_import_zip = tk.IntVar()       # 是否自动压缩 import-zip

# 平台类型
g_is_idx = tk.IntVar()
g_is_android    = tk.IntVar()       # android
g_is_ios        = tk.IntVar()       # ios
g_is_web_mobile = tk.IntVar()       # web_mobile
g_is_hot_update = tk.IntVar()       # 构建热更新
g_is_server     = tk.IntVar()       # 打包服务
g_is_copyGame   = tk.IntVar()       # 打包服务
g_is_other     = tk.IntVar()       # 其他

s_name_android = 'android'
s_name_ios = 'ios'
s_name_web = 'webMobile'
s_name_update = 'update'
s_name_server = 'server'
s_name_copyGame = 'copyGame'
s_name_other = 'other'

s_type_name = []
s_type_name.append(s_name_android)
s_type_name.append(s_name_ios)
s_type_name.append(s_name_web)
s_type_name.append(s_name_update)
# s_type_name.append(s_name_server)
s_type_name.append(s_name_copyGame)
s_type_name.append(s_name_other)

s_type_platform = []
s_type_platform.append(g_is_android)
s_type_platform.append(g_is_ios)
s_type_platform.append(g_is_web_mobile)
s_type_platform.append(g_is_hot_update)
# s_type_platform.append(g_is_server)
s_type_platform.append(g_is_copyGame)
s_type_platform.append(g_is_other)

g_is_copyWebBakeup = tk.IntVar()    # copy web_bakeup

g_file_name = tk.StringVar()        # 指定输出文件名
g_clean_jsb = tk.IntVar()           # 清理link
g_clean_library = tk.IntVar()       # 清理libiary

# android
g_armeabi_v7a = tk.IntVar()
g_arm64_v8a = tk.IntVar()
g_x86 = tk.IntVar()

g_keystore_name = tk.StringVar()
g_keystore_password = tk.StringVar()
g_keystore_alias = tk.StringVar()
g_apiLevel = tk.StringVar()
g_android_bak = tk.StringVar()

# 热更资源
g_update_use_res_link = tk.IntVar()         # 使用link版本
g_update_use_res_old_ver = tk.IntVar()      # 使用其他版本
g_update_use_res_old_str = tk.StringVar()   # 历史版本str
g_update_hot_version = tk.StringVar()       # 生成热更版本
g_update_skin_num = tk.StringVar()     # 皮肤号
g_update_oss_upload = tk.IntVar() # update-oss-upload

g_update_out_res_hall = tk.IntVar()         # 输出大厅版本
g_update_out_res_all = tk.IntVar()          # 输出所有版本
g_update_out_res_game_id = tk.IntVar()      # 输出所有版本
g_update_out_res_id_str = tk.StringVar()    # 输出指定id

# 代码编辑修改
g_server_public = tk.IntVar()       # 正式服
g_server_test = tk.IntVar()         # 测试服
g_server_local = tk.IntVar()        # 内网

# 批处理设置
g_batch_path = tk.StringVar()
g_batch_path.set('build_batch')
g_batch_timeVer=tk.StringVar()

# ios
g_ios_arm64 = tk.IntVar()
g_ios_pkg_appstore = tk.IntVar()
g_ios_pkg_adhoc = tk.IntVar()
g_ios_pkg_enterprise = tk.IntVar()

g_signed_ipa_form_build = tk.IntVar()
g_signed_ipa_form_archive = tk.IntVar()

g_adhoc_teamid = tk.StringVar()
g_enterprise_teamid = tk.StringVar()
g_appstore_teamid = tk.StringVar()

g_dev_teamid = tk.StringVar()      # 开发者id
g_profiles_name = tk.StringVar()    # 发布证书
g_profiles_dev = tk.StringVar()    # 开发证书
g_profiles_enterprise = tk.StringVar() #证书名-enterprise
g_profiles_appstore = tk.StringVar() #证书名-appstore
g_profiles_adhoc = tk.StringVar() #证书名-adhoc

g_signingStyle_Automatic = tk.StringVar() #证书使用
g_signingStyle_manual = tk.StringVar() #证书使用

# server
g_server_win_ip = tk.StringVar()
g_server_mac_ip = tk.StringVar()
g_server_port = tk.StringVar()
g_server_accounts = tk.StringVar()
g_server_password = tk.StringVar()

g_task_add = tk.IntVar()
g_task_first = tk.IntVar()

g_is_svn_update = tk.IntVar()
g_is_ftp_up = tk.IntVar()
g_is_oss_up = tk.IntVar()
g_is_share_up = tk.IntVar()
g_sever_batch = tk.IntVar()


# copyGame-replace-script-value
g_run_root = tk.StringVar();g_run_root.set('例如：xxx/asset/resources/Game/123_LHD')
g_old_script = tk.StringVar()
g_new_script = tk.StringVar()
g_path_library = tk.StringVar()
g_new_name = tk.StringVar()
g_script_head = tk.StringVar() 

# frame分组
s_frame_item = {
    'project':[],
    s_type_name[0]:[],
    s_type_name[1]:[],
    s_type_name[2]:[],
    s_type_name[3]:[],
    s_type_name[4]:[],
    s_type_name[5]:[],
    'all':[],
    'item_btn':[],
    'server_operate':[]
}

f_check_w=18
f_normal=0      # 默认frame
f_new=1         # 新建frame
f_renew=2       # 不跳行 新建frame
f_listItem_w = 10

f_frame_h = 30
f_frame_padx = 30
f_check_padx = 40

entry_relief='solid'
if IsIos: entry_relief='groove'

# anchor当可用空间大于组件所需求的大小时，该选项决定组件被放置在容器的何处。
# 该选项支持 N（北，代表上）、E（东，代表右）、S（南，代表下）、W（西，代表左）、NW（西北，代表左上）、
# NE（东北，代表右上）、SW（西南，代表左下）、SE（东南，代表右下）、CENTER（中，默认值）这些值。
# expand该 bool 值指定当父容器增大时才是否拉伸组件。
# fill	设置组件是否沿水平或垂直方向填充。该选项支持 NONE、X、Y、BOTH 四个值，其中 NONE 表示不填充，BOTH 表示沿着两个方向填充。
# ipadx	指定组件在 x 方向（水平）上的内部留白（padding）。
# ipady	指定组件在 y 方向（水平）上的内部留白（padding）。
# padx	指定组件在 x 方向（水平）上与其他组件的间距。
# pady	指定组件在 y 方向（水平）上与其他组件的间距。
# side  设置组件的添加位置，可以设置为 TOP、BOTTOM、LEFT 或 RIGHT 这四个值的其中之一。
def ui_getFrameWidth( w_scale ):
    tk_item = list()
    tp_w = int(win_w*w_scale)
    tk_item.append(tp_w)
    tk_item.append(win_w-tp_w)
    return tk_item

def ui_getFrameList(propagate=False, root=tk_root, w=win_w, h=f_frame_h):
    tk_item = list()
    frame = ui_getFrame(propagate, root, w, h)
    tk_item.append(frame)
    return tk_item

def ui_getSubFrame(propagate=False, root=tk_root, w=win_w, h=f_frame_h):
    tp_frame = tk.Frame(root, width=w, height=h)
    tp_frame.propagate(propagate)
    tp_frame.pack(side=LEFT)
    return tp_frame

def ui_getFrame(propagate=False, root=tk_root, w=win_w, h=f_frame_h):
    tp_frame = tk.Frame(root, width=w, height=h)
    tp_frame.propagate(propagate)
    tp_frame.pack(side=TOP)
    return tp_frame

# 分割线=
def ui_getFrameLine(h=f_frame_h, title='', bframeLine=True):
    tp_parent = ui_getFrameList(False, tk_root, win_w, h)
    if bframeLine:
        txt_line = '========================================================================='
        txt_title = txt_line + title + txt_line
        tk_lab=tk.Label( tp_parent[0], text=txt_title, font=def_font)
        tk_lab.pack()
        tp_parent.append(tk_lab)
    return tp_parent

# 分割线-
def ui_getFrameLine2(h=f_frame_h, title='', bframeLine=True):
    tp_parent = ui_getFrameList(False, tk_root, win_w, h)
    if bframeLine:
        txt_line = '--------------------------------------------------------------------------'
        txt_title = txt_line + title + txt_line
        tk_lab=tk.Label( tp_parent[0], text=txt_title, font=def_font)
        tk_lab.pack()
        tp_parent.append(tk_lab)
    return tp_parent

def ui_setFrameLine(frame_list, title=''):
    if frame_list==None: return
    txt_line = '===================================================================='
    txt_title = txt_line + title + txt_line
    frame_list[1].config(text=txt_title)

def ui_setFrameLine2(frame_list, title=''):
    if frame_list==None: return
    txt_line = '--------------------------------------------------------------------------'
    txt_title = txt_line + title + txt_line
    frame_list[1].config(text=txt_title)

# 更新类型
def ui_listbox_newf(list_array, list_name=None, ckb_cmd=None, i_frame=f_new, i_root=tk_root, item_side=LEFT, i_w=win_w):
    tk_item = list()

    #p0 frame
    if i_frame==f_new:
        frame = ui_getFrame(False, i_root, i_w, f_frame_h)
    elif i_frame==f_renew:
        frame = ui_getSubFrame(False, i_root[0], i_w, f_frame_h)
    else:
        frame = i_root[0]
    tk_item.append(frame)

    #p1 预留参数
    if list_name!=None:
        tk_lab = tk.Label( frame, text=list_name, font=def_font )
        tk_lab.pack(side=item_side)
        tk_item.append(tk_lab)
    else:
        tk_item.append(0)

    obj_item = tk.Listbox(frame, justify='left', width=f_listItem_w, height=50, command=ckb_cmd)
    for item in list_array:obj_item.insert(END, item)
    tk_item.append(obj_item)
    obj_item.pack(side=item_side)
    return tk_item

# 创建组件 frame + 0 + checkbutton
def ui_checkbutton_item(label, ckb_var=None, ckb_cmd=None, ckb_w=f_check_w, i_frame=f_new, i_root=tk_root, item_side=LEFT, i_w=win_w ):
    tk_item = list()

    #p0 frame
    if i_frame==f_new:
        frame = ui_getFrame(False, i_root, i_w, f_frame_h)
    elif i_frame==f_renew:
        frame = ui_getSubFrame(False, i_root[0], i_w, f_frame_h)
    else:
        frame = i_root[0]
    tk_item.append(frame)

    #p1 预留参数
    if ckb_var==None:
        tk_lab = tk.Label( frame, text=label, font=def_font )
        tk_lab.pack(side=item_side)
        tk_item.append(tk_lab)
    else:
        tk_item.append(0)

    #p2 组件
    if ckb_var!=None:
        obj_item = tk.Checkbutton(frame, text=label, anchor='w', justify='left', width=ckb_w, font=def_font, command=ckb_cmd, onvalue=1, offvalue=0, variable=ckb_var )
        obj_item.pack(side=item_side)
        tk_item.append(obj_item)
    else:
        tk_item.append(0)
    return tk_item

def ui_checkbutton_newf(label, ckb_var=None, ckb_cmd=None, ckb_w=f_check_w, i_frame=f_new, i_root=tk_root, item_side=LEFT, i_w=win_w ):
    return ui_checkbutton_item(label, ckb_var, ckb_cmd, ckb_w, i_frame, i_root, item_side, i_w)

# 创建组件 frame + 0 + button
def ui_button_item(label, btn_w, btn_cmd, i_frame, i_root=tk_root, item_side=LEFT, i_w=win_w):
    tk_item = list()

    #p0 frame
    if i_frame==f_new:
        frame = ui_getFrame(False, i_root, i_w, f_frame_h)
    elif i_frame==f_renew:
        frame = ui_getSubFrame(False, i_root[0], i_w, f_frame_h)
    else:
        frame = i_root[0]
    tk_item.append(frame)

    #p1 param
    tk_item.append(0)

    #p2 obj_item
    obj_item = tk.Button(frame, text=label, font=def_font, width=btn_w, command=btn_cmd)
    obj_item.pack(side=item_side)
    tk_item.append(obj_item)

    return tk_item
def ui_button_newf(label, btn_w, btn_cmd, i_frame=f_new, i_root=tk_root, item_side=LEFT, i_w=win_w):
    return ui_button_item(label, btn_w, btn_cmd, i_frame, i_root, item_side, i_w)

# 创建组件 frame + 0 + button
def ui_entry_item(label, lab_w, entry_w, entry_var, i_frame, i_root=tk_root, item_side=LEFT, i_w=win_w ):
    tk_item = list()

    #p0 frame
    if i_frame==f_new:
        frame = ui_getFrame(False, i_root, i_w, f_frame_h)
    elif i_frame==f_renew:
        frame = ui_getSubFrame(False, i_root[0], i_w, f_frame_h)
    else:
        frame = i_root[0]
    tk_item.append(frame)

    #p1 label
    tk_lab = tk.Label(frame, text=label, font=def_font, width=lab_w, justify="right", anchor='ne')
    tk_lab.pack(side=item_side)
    tk_item.append(tk_lab)

    #p2 组件
    if entry_var!=None:
        obj_item = tk.Entry(frame,font=def_font,width=entry_w,relief=entry_relief,textvariable=entry_var)
        obj_item.pack(side=item_side)
        tk_item.append(obj_item)
    else:
        tk_item.append(0)

    return tk_item
def ui_entry_newf(label, lab_w, entry_w, entry_var, i_frame=f_new, i_root=tk_root, item_side=LEFT, i_w=win_w ):
    return ui_entry_item(label, lab_w, entry_w, entry_var, i_frame, i_root, item_side, i_w)

# 创建组件 frame + label + checkbutton + entry
def ui_checkbutton_entry_item(label, ckb_var=None, ckb_cmd=None, entry_w=0, entry_var=None, ckb_w=f_check_w, i_frame=f_normal, i_root=tk_root, item_side=LEFT, i_w=win_w ):
    tk_item = list()

    #p0 frame
    if i_frame==f_new:
        frame = ui_getFrame(False, i_root, i_w, f_frame_h)
    elif i_frame==f_renew:
        frame = ui_getSubFrame(False, i_root[0], i_w, f_frame_h)
    else:
        frame = i_root[0]
    tk_item.append(frame)

    #p1 预留参数
    if ckb_var==None:
        tk_lab = tk.Label( frame, text=label, font=def_font )
        tk_lab.pack(side='left')
        tk_item.append(tk_lab)
    else:
        tk_item.append(0)

    #p2 组件
    if ckb_var!=None:
        obj_item = tk.Checkbutton(frame, text=label, anchor='w', justify='left', width=ckb_w, font=def_font, command=ckb_cmd, onvalue=1, offvalue=0, variable=ckb_var )
        obj_item.pack( side='left')
        tk_item.append(obj_item)
    else:
        tk_item.append(0)

    #P4 entry组件
    if entry_var!=None:
        obj_item = tk.Entry(frame,font=def_font,width=entry_w,relief=entry_relief,textvariable=entry_var)
        obj_item.pack(side='left')
        tk_item.append(obj_item)

    return tk_item

# 设置环境变量
def do_btn_setpkg_environ():
    start_pkg.g_creator_root = g_creator_root.get()
    start_pkg.g_creator_ver = g_creator_ver.get()
    start_pkg.g_project_root = g_project_root.get()
    start_pkg.g_remote_assets = g_remote_assets.get()
    start_pkg.g_project_title = g_project_title.get()
    start_pkg.g_build_path = g_build_path.get()

    if g_is_ios.get()==1:start_pkg.g_platform_name = 'ios'
    if g_is_android.get()==1:start_pkg.g_platform_name = 'android'
    if g_is_web_mobile.get()==1:start_pkg.g_platform_name = 'web'
    if g_is_hot_update.get()==1:start_pkg.g_platform_name = 'hotUpdate'

    start_pkg.g_batch_path = g_batch_path.get()
    start_pkg.g_file_name = g_file_name.get()

    start_pkg.g_channel_id = str(g_channel_id.get())
    start_pkg.g_version = g_version.get()
    start_pkg.g_app_name = g_app_name.get()
    start_pkg.g_package_id = g_package_id.get()
    start_pkg.g_is_debug = g_is_debug.get()
    start_pkg.g_is_md5cache = g_is_md5cache.get()
    start_pkg.g_is_short = g_is_short.get()
    start_pkg.g_is_import_zip = g_is_import_zip.get()

    start_pkg.g_pkg_res_type = 'normal'
    if g_is_res_normal.get()==1:start_pkg.g_pkg_res_type = 'normal'
    if g_is_encrypted.get()==1:start_pkg.g_pkg_res_type = 'encry'
    if g_is_etc2_ccc.get()==1:start_pkg.g_pkg_res_type = 'etc2_ccc'
    if g_is_etc2_py.get()==1:start_pkg.g_pkg_res_type = 'etc2_py'

    start_pkg.g_clean_jsb = g_clean_jsb.get()
    start_pkg.g_clean_library = g_clean_library.get()

    # android相关
    start_pkg.g_keystore_name = g_keystore_name.get()
    start_pkg.g_keystore_alias = g_keystore_alias.get()
    start_pkg.g_keystore_password = g_keystore_password.get()
    start_pkg.g_apiLevel = g_apiLevel.get()
    start_pkg.g_android_bak = g_android_bak.get()

    start_pkg.g_armeabi_v7a = g_armeabi_v7a.get()
    start_pkg.g_arm64_v8a = g_arm64_v8a.get()
    start_pkg.g_x86 = g_x86.get()

    # ios
    start_pkg.g_ios_arm64 = g_ios_arm64.get()
    start_pkg.g_ios_pkg_appstore = g_ios_pkg_appstore.get()
    start_pkg.g_ios_pkg_adhoc = g_ios_pkg_adhoc.get()
    start_pkg.g_ios_pkg_enterprise = g_ios_pkg_enterprise.get()

    start_pkg.g_signed_ipa_form_build = g_signed_ipa_form_build.get()
    start_pkg.g_signed_ipa_form_archive = g_signed_ipa_form_archive.get()

    start_pkg.g_adhoc_teamid = g_adhoc_teamid.get()
    start_pkg.g_enterprise_teamid = g_enterprise_teamid.get()
    start_pkg.g_appstore_teamid = g_appstore_teamid.get()

    start_pkg.g_dev_teamid = g_dev_teamid.get()
    start_pkg.g_profiles_name = g_profiles_name.get()
    start_pkg.g_profiles_dev = g_profiles_dev.get()
    start_pkg.g_profiles_enterprise = g_profiles_enterprise.get()
    start_pkg.g_profiles_appstore = g_profiles_appstore.get()
    start_pkg.g_profiles_adhoc = g_profiles_adhoc.get()

    start_pkg.g_signingStyle_Automatic = g_signingStyle_Automatic.get()
    start_pkg.g_signingStyle_manual = g_signingStyle_manual.get()

    # update
    start_pkg.g_update_use_res_link = g_update_use_res_link.get()
    start_pkg.g_update_use_res_old_ver = g_update_use_res_old_ver.get()
    start_pkg.g_update_use_res_old_str = g_update_use_res_old_str.get()
    start_pkg.g_update_hot_version = g_update_hot_version.get()
    start_pkg.g_update_skin_num = g_update_skin_num.get()
    start_pkg.g_update_oss_upload = g_update_oss_upload.get()

    start_pkg.g_update_out_res_hall = g_update_out_res_hall.get()
    start_pkg.g_update_out_res_all = g_update_out_res_all.get()
    start_pkg.g_update_out_res_game_id = g_update_out_res_game_id.get()
    start_pkg.g_update_out_res_id_str = g_update_out_res_id_str.get()

    # web
    start_pkg.g_is_copyWebBakeup = g_is_copyWebBakeup.get()

    # code相关
    start_pkg.g_server_name = 'public'
    if g_server_test.get()==1:start_pkg.g_server_name='test'
    if g_server_local.get()==1:start_pkg.g_server_name='local'

# 获取打包数据
def get_cmd_build_data_buf():
    pkg_buf.g_server_accounts = g_server_accounts.get()
    pkg_buf.g_server_password = g_server_password.get()

    pkg_buf.g_config_id = g_config_id.get()

    pkg_buf.g_task_add = g_task_add.get()
    pkg_buf.g_task_first = g_task_first.get()

    pkg_buf.g_is_svn_update = g_is_svn_update.get()
    pkg_buf.g_is_ftp_up = g_is_ftp_up.get()
    pkg_buf.g_is_oss_up = g_is_oss_up.get()
    pkg_buf.g_is_share_up = g_is_share_up.get()
    pkg_buf.g_sever_batch = g_sever_batch.get()
    pkg_buf.g_hot_type = 'hall'

    if g_server_public.get()==1:pkg_buf.g_server_name = 'public'
    if g_server_test.get()==1:pkg_buf.g_server_name = 'test'
    if g_server_local.get()==1:pkg_buf.g_server_name = 'local'

    return pkg_buf.getBufData(pkg_buf)

# 设置时间版本
def do_btn_set_time_ver():
    time_ver = tool.get_timestamp()
    g_batch_timeVer.set(time_ver)

# 设置按钮状态
def do_btn_set_state(state):
    for item in s_frame_item['item_btn']:
        item[2]['state'] = state

    if state==s_state_normal:
        do_set_platform(g_is_idx.get())

    # 保存配置
    if state==s_state_disabled:
        on_close_opt(0)

# 打包
def do_start_pkg():
    do_btn_setpkg_environ()
    pkg_ret = start_pkg.do_pkg_platform()
    if pkg_ret!=False and pkg_ret!=True:
        tool.msgbox(pkg_ret)
    do_btn_set_state(s_state_normal)

# 批量打包
def do_start_batch_web_mobile():
    tool.msgbox('暂未实现')
    do_btn_set_state(s_state_normal)

# 保存工具配置
def do_btn_save_opt():
    on_close_opt(0)
    tool.msgbox('保存成功')

# 刷新渠道build
def do_update_channelid_version0():
    do_btn_setpkg_environ()

    start_pkg.do_update_channelid_version(0)

    do_btn_set_state(s_state_normal)
    print('刷新完成')

# 刷新assets
def do_update_channelid_version1():
    do_btn_setpkg_environ()

    # 刷新工程目录
    start_pkg.do_update_channelid()

    do_btn_set_state(s_state_normal)
    print('刷新完成')

# 构建工程
def do_build_project():
    do_btn_setpkg_environ()

    # 只构建工程
    pkg_ret = start_pkg.do_pkg_platform(1)
    if pkg_ret!=False and pkg_ret!=True:
        tool.msgbox(pkg_ret)
    do_btn_set_state(s_state_normal)

# 简体大厅资源
def do_hall_res_script():
    do_btn_setpkg_environ()

    # 只构建工程
    pkg_ret = start_pkg.do_hall_res_script()
    if pkg_ret!=False and pkg_ret!=True:
        tool.msgbox(pkg_ret)
    do_btn_set_state(s_state_normal)

# 构建大厅版本
def do_btn_build_hall_res_version():
    print('do_btn_build_hall_res_version')
    # 创建
    t = threading.Thread(target=do_hall_res_script, args=[])
    # 守护 !!!
    t.setDaemon(True)
    # 启动
    t.start()
    # 禁用按钮
    do_btn_set_state(s_state_disabled)

# 更新渠道号与版本号
def do_btn_update_channelid_version0():
    print('do_btn_update_channelid_version0')
    # 创建
    t = threading.Thread(target=do_update_channelid_version0, args=[])
    # 守护 !!!
    t.setDaemon(True)
    # 启动
    t.start()
    # 禁用按钮
    do_btn_set_state(s_state_disabled)

# 更新渠道号与版本号
def do_btn_update_channelid_version1():
    # 创建
    t = threading.Thread(target=do_update_channelid_version1, args=[])
    # 守护 !!!
    t.setDaemon(True)
    # 启动
    t.start()
    # 禁用按钮
    do_btn_set_state(s_state_disabled)
    
# 构建项目
def do_btn_build_project():
    # 创建
    t = threading.Thread(target=do_build_project, args=[])
    # 守护 !!!
    t.setDaemon(True)
    # 启动
    t.start()
    # 禁用按钮
    do_btn_set_state(s_state_disabled)

# 打开批处理模板
def do_open_batch_skin_templates():

    do_btn_setpkg_environ()

    _batch_conf_path = start_pkg.get_batch_conf_path()
    _batch_skin_path = _batch_conf_path + '/appskin'
    _batch_skin_help = _batch_skin_path + '/template_help.txt'

    if os.path.exists(_batch_skin_path):
        tool.open_finder(_batch_skin_path)

    if os.path.exists(_batch_skin_help):
        tool.open_finder(_batch_skin_help)

# 打开配置版本
def do_open_batch_csv():
    _batch_conf_path = start_pkg.get_batch_conf_path()
    _csv_path = _batch_conf_path + '/' + start_pkg._get_batch_csv()

    if os.path.exists(_csv_path)==False:
        tool.msgbox( '配置路径异常，请检查:' + _csv_path )
        return
    tool.open_finder(_csv_path)

# 恢复事件按钮
def do_event_reset_btn_state():
    # 恢复按钮
    do_btn_set_state(s_state_normal)

# 替换匹配脚本
def do_event_replace_script():
    run_root = g_run_root.get()
    old_script = g_old_script.get()
    new_script = g_new_script.get()
    path_lib = g_path_library.get()
    on_close_opt(0)
    copyGame.replace_script(run_root, old_script, new_script, path_lib)

# 生成匹配关系
def do_event_search_script():
    run_root = g_run_root.get()
    old_script = g_old_script.get()
    new_script = g_new_script.get()
    path_lib = g_path_library.get()
    on_close_opt(0)
    copyGame.search_script(run_root, old_script, new_script, path_lib)

# 生成新游戏
def do_event_create_path():
    run_root = g_run_root.get()
    old_script = g_old_script.get()
    new_name = g_new_name.get()
    path_lib = g_path_library.get()
    new_head = g_script_head.get()
    on_close_opt(0)
    copyGame.create_new_path(run_root, old_script, new_name, new_head, path_lib)

# 校验环境变量
def do_check_batch_logic():
    #初始化环境变量
    do_btn_setpkg_environ()

    # 检查环境
    check_ret = start_pkg.do_check_batch_environ_param()

    if check_ret!=True:
        tool.msgbox(check_ret)
    else:
        tool.msgbox('校验通过！')
    return True

# 开游戏配置文件
def do_open_gameConfig():
    gameConfig_path = self_path + '/conf'
    tool.open_finder(gameConfig_path)
    do_btn_set_state(s_state_normal)

# 批量打包
def do_start_batch_android():
    do_btn_setpkg_environ()
    start_pkg.do_start_batch_android()
    do_btn_set_state(s_state_normal)

# ios批量archive 重签名->export ipa 
def do_start_batch_archive_ios():
    do_btn_setpkg_environ()
    check_ret = start_pkg.do_start_batch_archive_ios()
    if check_ret!=True: tool.msgbox(check_ret)
    do_btn_set_state(s_state_normal)

# ipa批量重签
def do_start_signed_ipa_form_ipa(arg):
    do_btn_setpkg_environ()
    check_ret = start_pkg.do_start_signed_ipa_form_ipa(arg)
    if check_ret!=True: tool.msgbox(check_ret)
    do_btn_set_state(s_state_normal)

# 批量编译 pk-ipa
def do_start_batch_ios():

    #初始化环境变量
    do_btn_setpkg_environ()

    # 检查环境
    check_ret = start_pkg.do_start_batch_ios()
    if check_ret!=True: tool.msgbox(check_ret)
    do_btn_set_state(s_state_normal)

#==================================================================================
# 平台打包
def do_event_package_platform():
    # 创建
    t = threading.Thread(target=do_start_pkg, args=[])
    # 守护 !!!
    t.setDaemon(True) 
    # 启动
    t.start()
    # 禁用按钮
    do_btn_set_state(s_state_disabled)

# 批处理IOS
def do_event_package_batch_ios():

    # build-批量处理
    if g_signed_ipa_form_build.get()==1:
        # 创建
        t = threading.Thread(target=do_start_batch_ios, args=[])
        # 守护 !!!
        t.setDaemon(True) 
        # 启动
        t.start()

    # archive-批量处理
    elif g_signed_ipa_form_archive.get()==1:
        # 创建
        t = threading.Thread(target=do_start_batch_archive_ios, args=[])
        # 守护 !!!
        t.setDaemon(True) 
        # 启动
        t.start()

    # ipa重签
    else:
        # 创建
        t = threading.Thread(target=do_start_signed_ipa_form_ipa, args=[])
        # 守护 !!!
        t.setDaemon(True) 
        # 启动
        t.start()

    # 禁用按钮
    do_btn_set_state(s_state_disabled)

# 重签ipa
def do_event_resigned_ipa1():
    # 创建
    t = threading.Thread(target=do_start_signed_ipa_form_ipa, args=['1'])
    # 守护 !!!
    t.setDaemon(True) 
    # 启动
    t.start()
    # 禁用按钮
    do_btn_set_state(s_state_disabled)

# 重签ipa
def do_event_resigned_ipa2():
    # 创建
    t = threading.Thread(target=do_start_signed_ipa_form_ipa, args=['2'])
    # 守护 !!!
    t.setDaemon(True) 
    # 启动
    t.start()
    # 禁用按钮
    do_btn_set_state(s_state_disabled)

# 批处理android
def do_event_package_batch_android():
    # 创建
    t = threading.Thread(target=do_start_batch_android, args=[])
    # 守护 !!!
    t.setDaemon(True) 
    # 启动
    t.start()

    # 禁用按钮
    do_btn_set_state(s_state_disabled)

# 批处理android
def do_event_open_gameConfig():
    # 创建
    t = threading.Thread(target=do_open_gameConfig, args=[])
    # 守护 !!!
    t.setDaemon(True) 
    # 启动
    t.start()

    # 禁用按钮
    do_btn_set_state(s_state_disabled)

# 批处理web
def do_event_package_batch_web_mobile():
    # 创建
    t = threading.Thread(target=do_start_batch_web_mobile, args=[])
    # 守护 !!!
    t.setDaemon(True) 
    # 启动
    t.start()

    # 禁用按钮
    do_btn_set_state(s_state_disabled)

# 输出根目录
def do_event_open_self():
    tool.open_finder(self_out_path)

# 打开配置目录
def do_event_open_batch_conf_path():
    do_btn_setpkg_environ()
    tool.open_finder(start_pkg.get_batch_conf_path())

# 项目输出目录
def do_event_open_out_root():
    do_btn_setpkg_environ()
    open_path = start_pkg.get_project_out_root()
    if os.path.exists(open_path)==False:
        tool.mkdir(open_path)
    tool.open_finder(open_path)

# 反编译pyc
def do_event_uncompyle_py_path():
    do_btn_setpkg_environ()
    succeed = tool.uncompyle_py_file(g_project_root.get())
    if succeed!=True:
        tool.msgbox(succeed)

# 批量合并文件 到 文件夹
def do_event_batch_movefile_to_finder():
    do_btn_setpkg_environ()
    succeed = tool.move_file_to_finder( g_project_root.get(), g_remote_assets.get() )
    if succeed!=True:
        tool.msgbox(succeed)

# 构建热更新
def do_build_hotUpdate():
    do_btn_setpkg_environ()
    ret = start_pkg.do_build_hotUpdate()
    if ret!=False and ret!=True:tool.msgbox(ret)
    do_btn_set_state(s_state_normal)

# 正式服
def _set_server_public():
    do_btn_setpkg_environ()
    ret = start_pkg._set_server_public()

    if ret!=True:
        tool.msgbox(ret)
        g_server_public.set(0)
    else:
        g_server_public.set(1)
        g_server_test.set(0)
        g_server_local.set(0)

# 测试服
def _set_server_test():
    do_btn_setpkg_environ()
    ret = start_pkg._set_server_test()

    if ret!=True:
        tool.msgbox(ret)
        g_server_test.set(0)
    else:
        g_server_public.set(0)
        g_server_test.set(1)
        g_server_local.set(0)

# 内测服
def _set_server_local():
    do_btn_setpkg_environ()
    ret = start_pkg._set_server_local()

    if ret!=True:
        tool.msgbox(ret)
        g_server_local.set(0)
    else:
        g_server_public.set(0)
        g_server_test.set(0)
        g_server_local.set(1)

# creator root
def do_cmd_set_config_id(event):    
    # if event!='1' and event.keysym=='Control_L':return
    if event!='1':
        t=threading.Thread(target=do_cmd_set_config_id, args=['1'])
        t.setDaemon(True)
        t.start()
        return

    conf_id = g_config_id.get()
    if start_config.has_conf_obj(conf_id):
        start_config.on_read_config_by_ui(this, conf_id)
    
# install-res+bugliy
def do_event_install_entry_engine_version():
    do_event_install_entry_engine(tool.var_string(g_creator_ver))

# install-res+bugliy
def do_event_install_entry_engine(ccc_ver):

    _ccc_root = tool.var_string(g_creator_root)
    install_file_path = self_out_path + '/install_native_' + ccc_ver +'/resources'

    # 拷贝并 逆向备份原始文件
    if IsWds:
        tool.copydir(install_file_path, _ccc_root+'/resources', True, True)
    else:
        tool.copydir(install_file_path, _ccc_root+'/Contents/resources', True, True)
    tool.msgbox('安装完成')

# 启动creator
def do_start_creator_app():
    do_btn_setpkg_environ()
    _ccc_exe = start_pkg.get_creator_start_cmd()
    subprocess.call(_ccc_exe, shell=True)

# CreatorRoot
def do_event_start_creator():
    # 创建
    t = threading.Thread(target=do_start_creator_app, args=[])
    # 守护 !!!
    t.setDaemon(True)
    # 启动
    t.start()

# 构建热更资源
def do_event_build_hotUpdate():
    # 创建
    t = threading.Thread(target=do_build_hotUpdate, args=[])
    # 守护 !!!
    t.setDaemon(True)
    # 启动
    t.start()
    do_btn_set_state(s_state_disabled)

def do_event_build_open_hot_list():
    do_btn_setpkg_environ()
    do_open_path( start_pkg.get_build_root_path(),  0, 1)

# CreatorRoot
def do_event_open_creator_root():
    do_open_path( g_creator_root.get(),  0, 1)

# ProjectRoot
def do_event_open_project_root():
    do_open_path( g_project_root.get(), 0, 1)

def do_open_native_log():
    file_path = tool.get_tool_conf("creator_log_path")
    do_open_path( file_path, 0, 1)

# ProjectRoot-build
def do_event_open_project_build():
    do_btn_setpkg_environ()
    do_open_path( start_pkg.get_build_root_path(), 0, 1)

# 打开bake目录
def do_event_open_android_bak_root():
    _pj_android_bak_src = g_project_root.get() + '/' + g_android_bak.get()
    do_open_path(_pj_android_bak_src, 0, 1)

# 打开web_bakeup
def do_event_open_web_bakeup():
    _pj_android_bak_src = g_project_root.get() + '/build-templates/web-bakeup'
    do_open_path(_pj_android_bak_src, 0, 1)

# 打开路径
def do_open_path(path, can_creator=0, tips=0):
    # 是否创建
    if os.path.exists(path)==False:
        if can_creator==1:
            tool.mkdir(path)
        if can_creator==0 and tips==1:
            tool.msgbox('没有此路径，请检查路径！')
    else:
        tool.open_finder(path)

# 显示分组功能 _ios
def _enable_platform_frame( frame_aray, state, idx=-1 ):
    if state==s_state_disabled:
        for item in frame_aray:
            item[0].pack_forget()
    else:
        for item in frame_aray:
            item[0].pack()
#==================================================================================
# 设置批处理平台
def do_set_platform(idx):
    name = s_type_name[idx]
    _enable_platform_frame(s_frame_item['all'], s_state_disabled)
    ui_setFrameLine2(s_title_platform, name )
    _enable_platform_frame(s_frame_item[name], s_state_normal)

    # 打包ios
    if g_is_ios.get()==1 or g_is_android.get()==1 or g_is_web_mobile.get()==1:
        _enable_platform_frame(s_frame_item['project'], s_state_normal)

def _setPlatformType(idx):
    g_is_idx.set(idx)
    g_is_ios.set(0)
    g_is_android.set(0)
    g_is_web_mobile.set(0)
    g_is_hot_update.set(0)
    g_is_server.set(0)
    g_is_copyGame.set(0)
    g_is_other.set(0)

    s_type_platform[idx].set(1)
    do_set_platform(idx)


# android abi select one at least
def _setAndroid_abi(abi_type):
    tp_select_count = 0
    if g_armeabi_v7a.get()==1:
        tp_select_count+=1

    if g_arm64_v8a.get()==1:
        tp_select_count+=1

    if g_x86.get()==1:
        tp_select_count+=1

    if tp_select_count==0 and abi_type==0:
        g_armeabi_v7a.set(1)

    if tp_select_count==0 and abi_type==1:
        g_arm64_v8a.set(1)

    if tp_select_count==0 and abi_type==2:
        g_x86.set(1)

def _set_res_entry():
    if g_is_encrypted.get()==1:
        g_is_etc2_ccc.set(0)
        g_is_etc2_py.set(0)
        g_is_res_normal.set(0)

def _set_res_etc2_gzip():
    if g_is_etc2_py.get()==1:
        g_is_etc2_ccc.set(0)
        g_is_encrypted.set(0)
        g_is_res_normal.set(0)

def _set_res_etc2():
    if g_is_etc2_ccc.get()==1:
        g_is_etc2_py.set(0)
        g_is_encrypted.set(0)
        g_is_res_normal.set(0)

def _set_res_normal():
    g_is_res_normal.set(1)
    g_is_etc2_ccc.set(0)
    g_is_etc2_py.set(0)
    g_is_encrypted.set(0)

# set android abi type
def _setAndroid_v7a():
    _setAndroid_abi(0)

# set android abi type
def _setAndroid_v8a():
    _setAndroid_abi(1)

# set android abi type
def _setAndroid_x86():
    _setAndroid_abi(2)

# archive
def _set_ios_architectures():
    g_ios_arm64.set(1)

def _set_signed_ipa_form_build():
    g_signed_ipa_form_build.set(1)
    g_signed_ipa_form_archive.set(0)
    print('_set_signed_ipa_form_build')

def _set_signed_ipa_form_archive():
    g_signed_ipa_form_build.set(0)
    g_signed_ipa_form_archive.set(1)
    print('_set_signed_ipa_form_archive')

# appstore
def _set_ios_pkg_appstore():
    g_ios_pkg_appstore.set(1)
    g_ios_pkg_adhoc.set(0)
    g_ios_pkg_enterprise.set(0)

    g_profiles_name.set(g_profiles_appstore.get())
    g_dev_teamid.set(g_appstore_teamid.get())

# adhoc
def _set_ios_pkg_adhoc():
    g_ios_pkg_appstore.set(0)
    g_ios_pkg_adhoc.set(1)
    g_ios_pkg_enterprise.set(0)
    g_profiles_name.set(g_profiles_adhoc.get())
    g_dev_teamid.set(g_adhoc_teamid.get())

# 企业打包
def _set_ios_pkg_enterprise():
    g_ios_pkg_appstore.set(0)
    g_ios_pkg_adhoc.set(0)
    g_ios_pkg_enterprise.set(1)
    g_profiles_name.set(g_profiles_enterprise.get())
    g_dev_teamid.set(g_enterprise_teamid.get())

# 设置
def _set_signingStyle_Automatic():
    g_signingStyle_Automatic.set(1)
    g_signingStyle_manual.set(0)

def _set_signingStyle_manual():  
    g_signingStyle_Automatic.set(0)
    g_signingStyle_manual.set(1)

# server-event =================================================================================
def do_server_info(event):
    win_ip = g_server_win_ip.get()
    mac_ip = g_server_mac_ip.get()
    port = g_server_port.get()
    accounts = g_server_accounts.get()
    password = g_server_password.get()

    et_dict = json.loads(event)
    if et_dict['cmd']==pkg_cmd.CMD_PK_IPA:
        pkg_client.set_client_info( mac_ip, port, accounts, password, s_server_label[2], event )
    else:
        pkg_client.set_client_info( win_ip, port, accounts, password, s_server_label[2], event )

# 事件发送
def do_async_server_check(event=None):
    if event==None:t=threading.Thread(target=do_async_server_check,args=['1']);t.setDaemon(True);t.start();return
    do_server_info(event)

# 查询任务
def do_async_server_task_check(event=None):
    # print('do_async_server_task_check')
    if event==None:t=threading.Thread(target=do_async_server_task_check,args=['1']);t.setDaemon(True);t.start();return

    # 打包资料
    data_buf = get_cmd_build_data_buf()
    cmd_buf = pkg_cmd.get_cmd_buf(pkg_cmd.CMD_CHECK, data_buf)

    # check链接
    do_async_server_check(cmd_buf)
        
# cmd_pk_apk
def do_async_server_pk_apk(event=None):
    # print('do_async_server_pk_apk')
    if event==None:t=threading.Thread(target=do_async_server_pk_apk,args=['1']);t.setDaemon(True);t.start();return

    # 打包资料
    data_buf = get_cmd_build_data_buf()
    cmd_buf = pkg_cmd.get_cmd_buf(pkg_cmd.CMD_PK_APK, data_buf)

    # check链接
    do_async_server_check(cmd_buf)

# cmd_pk_ios
def do_async_server_pk_ipa(event=None):
    # print('do_async_server_pk_ios')
    if event==None:t=threading.Thread(target=do_async_server_pk_ipa,args=['1']);t.setDaemon(True);t.start();return

    # 打包资料
    data_buf = get_cmd_build_data_buf()
    cmd_buf = pkg_cmd.get_cmd_buf(pkg_cmd.CMD_PK_IPA, data_buf)

    # check链接
    do_async_server_check(cmd_buf)

# cmd_pk_web
def do_async_server_pk_web(event=None):
    print('do_async_server_pk_web')
    if event==None:t=threading.Thread(target=do_async_server_pk_web,args=['1']);t.setDaemon(True);t.start();return

    # 打包资料
    data_buf = get_cmd_build_data_buf()
    cmd_buf = pkg_cmd.get_cmd_buf(pkg_cmd.CMD_PK_WEB, data_buf)

    # check链接
    do_async_server_check(cmd_buf)
    
# cmd_pk_hotUpdate
def do_async_server_pk_hotUpdate(event=None):
    print('do_async_server_pk_hotUpdate')
    if event==None:t=threading.Thread(target=do_async_server_pk_hotUpdate,args=['1']);t.setDaemon(True);t.start();return

    # 打包资料
    data_buf = get_cmd_build_data_buf()
    data_buf['hot_type']='all'
    cmd_buf = pkg_cmd.get_cmd_buf(pkg_cmd.CMD_PK_HOTUPDATE, data_buf)

    # check链接
    do_async_server_check(cmd_buf)
    
# cmd_pk_hotUpdate
def do_async_server_pk_hotHall(event=None):
    print('do_async_server_pk_hotUpdate')
    if event==None:t=threading.Thread(target=do_async_server_pk_hotHall,args=['1']);t.setDaemon(True);t.start();return

    # 打包资料
    data_buf = get_cmd_build_data_buf()
    cmd_buf = pkg_cmd.get_cmd_buf(pkg_cmd.CMD_PK_HOTUPDATE, data_buf)

    # check链接
    do_async_server_check(cmd_buf)

# cmd_del_task
def do_async_server_del_task(event=None):
    print('do_async_server_del_task')
    if event==None:t=threading.Thread(target=do_async_server_del_task,args=['1']);t.setDaemon(True);t.start();return

    # 打包资料
    data_buf = get_cmd_build_data_buf()
    cmd_buf = pkg_cmd.get_cmd_buf(pkg_cmd.CMD_DEL, data_buf)

    # check链接
    do_async_server_check(cmd_buf)

# 任务方式
def _g_task_add():g_task_add.set(1);g_task_first.set(0)
def _g_task_first():g_task_add.set(0);g_task_first.set(1)
    
#=================================================================================
# 热更参数设置
# 使用资源参数设置
def _setUpdateUseResLink():
    g_update_use_res_link.set(1)
    g_update_use_res_old_ver.set(0)

def _setUpdateUseResOldVer():
    g_update_use_res_link.set(0)
    g_update_use_res_old_ver.set(1)

def _setUpdateOutResHall():
    g_update_out_res_hall.set(1)
    g_update_out_res_all.set(0)
    g_update_out_res_game_id.set(0)

def _setUpdateOutResAll():
    g_update_out_res_hall.set(0)
    g_update_out_res_all.set(1)
    g_update_out_res_game_id.set(0)

def _setUpdateOutResID():
    g_update_out_res_hall.set(0)
    g_update_out_res_all.set(0)
    g_update_out_res_game_id.set(1)

# CODE EDIT=================================================================================
# ui 数值定义
def_entry_w_newf = 12
def_entry_w_item = 13
def uiFrameWidth0(len):
    return ui_getFrameWidth(len/100)[0]
def uiFrameWidth1(len):
    return ui_getFrameWidth(len/100)[1]

tp_parent = ui_getFrameList()
tp_item = ui_entry_newf('creatorRoot:', def_entry_w_newf, 100, g_creator_root, f_renew, tp_parent, LEFT, uiFrameWidth0(50))
tp_item = ui_button_newf('启动creator', 10, do_event_start_creator, f_renew, tp_parent, RIGHT, uiFrameWidth1(50))
tp_item = ui_button_item('打开目录', 10, do_event_open_creator_root, f_normal, tp_item, RIGHT)
tp_item = ui_button_item('引擎定制', 10, do_event_install_entry_engine_version, f_normal, tp_item, RIGHT)
tp_item = ui_entry_item('-v:', 4, 6, g_creator_ver, f_normal, tp_item, LEFT)

tp_parent = ui_getFrameList()
tp_item = ui_entry_newf('projectRoot:', def_entry_w_newf, 50, g_project_root, f_renew, tp_parent, LEFT, uiFrameWidth0(64))
tp_item = ui_button_item('native.log', 10, do_open_native_log, f_renew, tp_parent, RIGHT, uiFrameWidth1(64))
tp_item = ui_button_item('打开build', 10, do_event_open_project_build, f_normal, tp_item, RIGHT)
tp_item = ui_button_item('打开目录', 10, do_event_open_project_root, f_normal, tp_item, RIGHT)

tp_parent = ui_getFrameList()
tp_item = ui_entry_newf('热更地址:', def_entry_w_newf, 60, g_remote_assets, f_renew, tp_parent, LEFT, uiFrameWidth0(64))
tp_item = ui_button_newf('保存配置', 10, do_btn_save_opt, f_renew, tp_parent, RIGHT, uiFrameWidth1(64))
tp_item = ui_button_item('时间版本', 10, do_btn_set_time_ver, f_normal, tp_item, RIGHT)

tp_item = ui_entry_newf('Proj_Title:', def_entry_w_newf, 15, g_project_title, f_new)
tp_item = ui_entry_item('构建路径:', def_entry_w_item, 15, g_build_path, f_normal, tp_item)
tp_item = ui_entry_item('输出文件:', def_entry_w_item, 15, g_file_name, f_normal, tp_item)

tp_item = ui_entry_newf('渠道号:', def_entry_w_newf, 15, g_channel_id)
tp_item = ui_entry_item('版本号:', def_entry_w_item, 15, g_version, f_normal, tp_item)
tp_item = ui_entry_item('时间版本:', def_entry_w_item, 15, g_batch_timeVer, f_normal, tp_item)

tp_item = ui_entry_newf('配置编号:', def_entry_w_newf, 15, g_config_id, f_new);tp_item[2].bind('<Key>', do_cmd_set_config_id)
tp_item = ui_entry_item('应用名:', def_entry_w_item, 15, g_app_name, f_normal, tp_item)
tp_item = ui_entry_item('包名:', def_entry_w_item, 15, g_package_id, f_normal, tp_item)

tp_five_w = f_check_w
tp_item = ui_checkbutton_newf('资源-加密', g_is_encrypted, _set_res_entry, tp_five_w, f_new );tp_item[0].config(padx=f_check_padx)
tp_item = ui_checkbutton_item('资源-etc2-gzip', g_is_etc2_py, _set_res_etc2_gzip, tp_five_w, f_normal, tp_item)
tp_item = ui_checkbutton_item('import-zip', g_is_import_zip, None, tp_five_w, f_normal, tp_item )
tp_item = ui_checkbutton_item('简体大厅包', g_is_short, None, tp_five_w, f_normal, tp_item)

tp_item = ui_checkbutton_newf('清理jsb-link', g_clean_jsb, None, tp_five_w, f_new);tp_item[0].config(padx=f_check_padx)
tp_item = ui_checkbutton_item('清理library', g_clean_library, None, tp_five_w, f_normal, tp_item)
tp_item = ui_checkbutton_item('debug', g_is_debug, None, tp_five_w, f_normal, tp_item )
tp_item = ui_checkbutton_item('md5cache', g_is_md5cache, None, tp_five_w, f_normal, tp_item )

# ui_getFrameLine2(f_frame_h, '服务配置')
tp_item = ui_checkbutton_newf('正式服', g_server_public, _set_server_public, tp_five_w, f_new );tp_item[0].config(padx=f_check_padx)
tp_item = ui_checkbutton_item('外测服', g_server_test, _set_server_test, tp_five_w, f_normal, tp_item )
tp_item = ui_checkbutton_item('内测服', g_server_local, _set_server_local, tp_five_w, f_normal, tp_item )

ui_getFrameLine(f_frame_h/2, '', False)
ui_getFrameLine(f_frame_h, 'platform')
tp_item_w = f_check_w-6
tp_item = ui_checkbutton_newf( s_type_name[0], g_is_android, lambda:_setPlatformType(0), tp_item_w, f_new ); tp_item[0].config(padx=f_frame_padx);s_frame_item['item_btn'].append(tp_item)
tp_item = ui_checkbutton_item( s_type_name[1], g_is_ios, lambda:_setPlatformType(1), tp_item_w, f_normal, tp_item);s_frame_item['item_btn'].append(tp_item)
tp_item = ui_checkbutton_item( s_type_name[2], g_is_web_mobile, lambda:_setPlatformType(2), tp_item_w, f_normal, tp_item);s_frame_item['item_btn'].append(tp_item)
tp_item = ui_checkbutton_item( s_type_name[3], g_is_hot_update, lambda:_setPlatformType(3), tp_item_w, f_normal, tp_item);s_frame_item['item_btn'].append(tp_item)
# tp_item = ui_checkbutton_item( s_type_name[4], g_is_server, lambda:_setPlatformType(4), tp_item_w, f_normal, tp_item);s_frame_item['item_btn'].append(tp_item)
tp_item = ui_checkbutton_item( s_type_name[4], g_is_copyGame, lambda:_setPlatformType(4), tp_item_w, f_normal, tp_item);s_frame_item['item_btn'].append(tp_item)

tp_item = ui_checkbutton_item( s_type_name[5], g_is_other, lambda:_setPlatformType(5), tp_item_w, f_normal, tp_item);s_frame_item['item_btn'].append(tp_item)
ui_getFrameLine(f_frame_h/2, '', False)

s_title_platform = None
s_title_platform = ui_getFrameLine2(f_frame_h, '.....')
# s_title_platform[0].config(bg='red')

# 华丽的分割线
# android==============================================================================================================================
tp_item = ui_checkbutton_newf('armeabi-v7a', g_armeabi_v7a, _setAndroid_v7a, f_check_w, f_new)
tp_item = ui_checkbutton_item('arm64-v8a', g_arm64_v8a, _setAndroid_v8a, f_check_w, f_normal, tp_item)
tp_item = ui_checkbutton_item('x86', g_x86, _setAndroid_x86, f_check_w, f_normal, tp_item)
tp_item[0].config(padx=f_frame_padx)
s_frame_item[s_name_android].append(tp_item)
s_frame_item['all'].append(tp_item)

tp_item = ui_entry_newf('apiLevel:', def_entry_w_newf, 15, g_apiLevel, f_new)
tp_item = ui_entry_item('android_templates:', 20, 20, g_android_bak, f_normal, tp_item)
tp_item = ui_button_item('打开bakeup', 10, do_event_open_android_bak_root, f_normal, tp_item)
tp_item[0].config(padx=f_frame_padx)
s_frame_item[s_name_android].append(tp_item)
s_frame_item['all'].append(tp_item)

tp_item = ui_entry_newf('ks_file:', def_entry_w_newf, 20, g_keystore_name, f_new)
tp_item = ui_entry_item('password:', def_entry_w_item, 12, g_keystore_password, f_normal, tp_item)
tp_item = ui_entry_item('alias:', def_entry_w_item, 12, g_keystore_alias, f_normal, tp_item)
tp_item[0].config(padx=f_frame_padx)
s_frame_item[s_name_android].append(tp_item)
s_frame_item['all'].append(tp_item)

tp_item = ui_getFrameLine(f_frame_h/2, '', False)
s_frame_item[s_name_android].append(tp_item)
s_frame_item['all'].append(tp_item)

tp_item = ui_button_newf('pk-apk', 12, do_event_package_platform, f_new, tk_root, RIGHT);s_frame_item['item_btn'].append(tp_item)
tp_item = ui_button_item('批量pk-apk', 12, do_event_package_batch_android, f_normal, tp_item, RIGHT);s_frame_item['item_btn'].append(tp_item)
# tp_item[0].config(bg='red')
s_frame_item[s_name_android].append(tp_item)
s_frame_item['all'].append(tp_item)
# android==============================================================================================================================

# ios==================================================================================================================================
tp_item = ui_entry_newf('TeamID:', 10, 15, g_dev_teamid);
tp_item = ui_entry_item('ios_dis:', 10, 15, g_profiles_name, f_normal, tp_item)
tp_item = ui_entry_item('ios_sign:', 10, 40, g_profiles_dev, f_normal, tp_item)
s_frame_item['ios'].append(tp_item)
s_frame_item['all'].append(tp_item)

tp_item = ui_checkbutton_newf('arm64', g_ios_arm64, _set_ios_architectures)
tp_item = ui_checkbutton_item('appstore', g_ios_pkg_appstore, _set_ios_pkg_appstore, f_check_w, f_normal, tp_item)
tp_item = ui_checkbutton_item('adhoc', g_ios_pkg_adhoc, _set_ios_pkg_adhoc, f_check_w, f_normal, tp_item)
tp_item = ui_checkbutton_item('enterprise', g_ios_pkg_enterprise, _set_ios_pkg_enterprise, f_check_w, f_normal, tp_item)
tp_item[0].config(padx=f_frame_padx)
s_frame_item['ios'].append(tp_item)
s_frame_item['all'].append(tp_item)

tp_item = ui_checkbutton_newf('batch_build', g_signed_ipa_form_build, _set_signed_ipa_form_build, f_check_w, f_new)
tp_item = ui_checkbutton_item('batch_archive', g_signed_ipa_form_archive, _set_signed_ipa_form_archive, f_check_w, f_normal, tp_item)
tp_item = ui_checkbutton_item('signing-Automatic', g_signingStyle_Automatic, _set_signingStyle_Automatic, f_check_w, f_normal, tp_item)
tp_item = ui_checkbutton_item('signing-manual', g_signingStyle_manual, _set_signingStyle_manual, f_check_w, f_normal, tp_item)
tp_item[0].config(padx=f_frame_padx)
s_frame_item['ios'].append(tp_item)
s_frame_item['all'].append(tp_item)

tp_item = ui_getFrameLine(f_frame_h/2, '', False)
s_frame_item['ios'].append(tp_item)
s_frame_item['all'].append(tp_item)

# 批量ipa重签：batch_ios_conf/aipa：[1.ipa、2.ipa、3.ipa]多个ipa依次重签
# 批量csv重签：使用dev.csv 根据配置的一个母包来重签签名，aipa此时只能存在一个ipa+mtime文件
tp_item = ui_button_newf('pk-ipa', 12, do_event_package_platform, f_new, tk_root, RIGHT);s_frame_item['item_btn'].append(tp_item)
tp_item = ui_button_item('批量pk-ipa', 12, do_event_package_batch_ios, f_normal, tp_item, RIGHT);s_frame_item['item_btn'].append(tp_item)
tp_item = ui_button_item('批量csv重签', 12, do_event_resigned_ipa2, f_normal, tp_item, RIGHT);s_frame_item['item_btn'].append(tp_item)
tp_item = ui_button_item('批量ipa重签', 12, do_event_resigned_ipa1, f_normal, tp_item, RIGHT);s_frame_item['item_btn'].append(tp_item)
# tp_item[0].config(bg='red')
s_frame_item['ios'].append(tp_item)
s_frame_item['all'].append(tp_item)
# ios==================================================================================================================================

# web_Mobile===========================================================================================================================
tp_item = ui_checkbutton_newf('copy-web-bakeup', g_is_copyWebBakeup, None, f_check_w, f_new, tk_root, LEFT);s_frame_item['item_btn'].append(tp_item)
tp_item[0].config(padx=f_frame_padx)
s_frame_item[s_name_web].append(tp_item)
s_frame_item['all'].append(tp_item)

tp_item = ui_checkbutton_newf('ui预留', None, None, f_check_w, f_new, tk_root, LEFT)
tp_item[0].config(padx=f_frame_padx)
s_frame_item[s_name_web].append(tp_item)
s_frame_item['all'].append(tp_item)

tp_item = ui_checkbutton_newf('ui预留', None, None, f_check_w, f_new, tk_root, LEFT)
tp_item[0].config(padx=f_frame_padx)
s_frame_item[s_name_web].append(tp_item)
s_frame_item['all'].append(tp_item)

tp_item = ui_getFrameLine(f_frame_h/2, '', False)
s_frame_item[s_name_web].append(tp_item)
s_frame_item['all'].append(tp_item)

tp_item = ui_button_newf('pk-web', 12, do_event_package_platform, f_new, tk_root, RIGHT);s_frame_item['item_btn'].append(tp_item)
tp_item = ui_button_item('批量pk-web', 12, do_event_package_batch_web_mobile, f_normal, tp_item, RIGHT);s_frame_item['item_btn'].append(tp_item)
tp_item = ui_button_item('打开bakeup', 12, do_event_open_web_bakeup, f_normal, tp_item, RIGHT)
# tp_item[0].config(bg='red')
s_frame_item[s_name_web].append(tp_item)
s_frame_item['all'].append(tp_item)
# web_Mobile==================================================================================================================================

# hotUpdate===================================================================================================================================
# tp_item = ui_listbox_newf([0,1,2,3,4,5], '更新类型', None, f_new)
tp_item = ui_checkbutton_newf('大厅更新', g_update_out_res_hall, _setUpdateOutResHall, 14, f_new )
tp_item = ui_checkbutton_item('所有更新', g_update_out_res_all, _setUpdateOutResAll, 14, f_normal, tp_item )
tp_item = ui_checkbutton_entry_item('指定游戏ID:', g_update_out_res_game_id, _setUpdateOutResID, 10, g_update_out_res_id_str, 10, f_normal, tp_item )

tp_item = ui_entry_item('皮肤号:', 12, 10, g_update_skin_num, f_normal, tp_item)
tp_item[0].config(padx=f_frame_padx)
s_frame_item[s_name_update].append(tp_item)
s_frame_item['all'].append(tp_item)

tp_item = ui_checkbutton_newf('使用构建版本', g_update_use_res_link, _setUpdateUseResLink, 14, f_new )
tp_item = ui_checkbutton_entry_item('使用版本库:', g_update_use_res_old_ver, _setUpdateUseResOldVer, 8, g_update_use_res_old_str, 10, f_normal, tp_item)
tp_item = ui_entry_item('生成版本:', def_entry_w_newf, 15, g_update_hot_version, f_normal, tp_item)
tp_item[0].config(padx=f_frame_padx)
s_frame_item[s_name_update].append(tp_item)
s_frame_item['all'].append(tp_item)

tp_item = ui_checkbutton_newf('oss-upload', g_update_oss_upload, None, f_check_w, f_new, tk_root, LEFT)
tp_item[0].config(padx=f_frame_padx)
s_frame_item[s_name_update].append(tp_item)
s_frame_item['all'].append(tp_item)

tp_item = ui_getFrameLine(f_frame_h/2, '', False)
s_frame_item[s_name_update].append(tp_item)
s_frame_item['all'].append(tp_item)

tp_item = ui_button_newf('构建热更', 12, do_event_build_hotUpdate, f_new, tk_root, RIGHT);s_frame_item['item_btn'].append(tp_item)
tp_item = ui_button_item('打开列表', 12, do_event_build_open_hot_list, f_normal, tp_item, RIGHT)
tp_item = ui_button_item('脚本目录', 12, do_event_open_self, f_normal, tp_item, RIGHT)
tp_item = ui_button_item('输出目录', 12, do_event_open_out_root, f_normal, tp_item, RIGHT)
# tp_item[0].config(bg='red')
s_frame_item[s_name_update].append(tp_item)
s_frame_item['all'].append(tp_item)

tp_item = ui_button_newf('重置按钮', 12, do_event_reset_btn_state, f_new, tk_root, RIGHT)
tp_item = ui_button_item('反编译pyc', 12, do_event_uncompyle_py_path, f_normal, tp_item, RIGHT)
s_frame_item[s_name_update].append(tp_item)
s_frame_item['all'].append(tp_item)
# hotUpdate============================================================================================================================

# # server===============================================================================================================================
# s_server_label = ui_getFrameList(True, tk_root)
# tk_lab=tk.Label( s_server_label[0], text='状态:', foreground='red', font=def_font)
# tk_lab.pack(side=LEFT)
# s_server_label.append(tk_lab)
# tk_lab=tk.Label( s_server_label[0], text='无', foreground='red', font=def_font)
# tk_lab.pack(side=LEFT)
# s_server_label.append(tk_lab)

# s_frame_item[s_name_server].append(s_server_label)
# s_frame_item['all'].append(s_server_label)

# tp_item = ui_entry_newf('win-server:', 12, 18, g_server_win_ip)
# tp_item = ui_entry_item('mac-server:', 15, 15, g_server_mac_ip, f_normal, tp_item)
# tp_item = ui_entry_item('port:', 8, 15, g_server_port, f_normal, tp_item)
# tp_item[0].config(padx=f_frame_padx)
# s_frame_item[s_name_server].append(tp_item)
# s_frame_item['all'].append(tp_item)

# tp_item = ui_entry_newf('账号:', 12, 18, g_server_accounts)
# tp_item = ui_entry_item('密码:', 15, 15, g_server_password, f_normal, tp_item)
# tp_item[0].config(padx=f_frame_padx)
# s_frame_item[s_name_server].append(tp_item)
# s_frame_item['all'].append(tp_item)

# tp_item[0].config(padx=f_frame_padx)
# s_frame_item[s_name_server].append(tp_item)
# s_frame_item['all'].append(tp_item)

# tp_item = ui_checkbutton_newf('添加任务', g_task_add, _g_task_add, f_check_w, f_new, tk_root, LEFT)
# tp_item = ui_checkbutton_item('优先任务', g_task_first, _g_task_first, f_check_w, f_normal, tp_item)
# tp_item = ui_checkbutton_item('编译后-批量csv', g_sever_batch, None, f_check_w, f_normal, tp_item)
# tp_item[0].config(padx=f_check_padx)
# s_frame_item[s_name_server].append(tp_item)
# s_frame_item['all'].append(tp_item)

# tp_item = ui_checkbutton_newf('更新svn', g_is_svn_update, None, f_check_w, f_new, tk_root, LEFT)
# tp_item = ui_checkbutton_item('上传oss', g_is_oss_up, None, f_check_w, f_normal, tp_item)
# tp_item = ui_checkbutton_item('上传ftp', g_is_ftp_up, None, f_check_w, f_normal, tp_item)
# tp_item = ui_checkbutton_item('上传共享', g_is_share_up, None, f_check_w, f_normal, tp_item)
# tp_item[0].config(padx=f_check_padx)
# s_frame_item[s_name_server].append(tp_item)
# s_frame_item['all'].append(tp_item)

# tp_item = ui_getFrameLine(f_frame_h/2, '', False)
# s_frame_item[s_name_server].append(tp_item)
# s_frame_item['all'].append(tp_item)

# tp_item = ui_button_newf('查询任务', 12, do_async_server_task_check, f_new, tk_root, RIGHT)
# tp_item = ui_button_item('清空任务', 12, do_async_server_del_task, f_normal, tp_item, RIGHT)
# s_frame_item[s_name_server].append(tp_item)
# s_frame_item['all'].append(tp_item)

# tp_item = ui_button_newf('pk-apk', 12, do_async_server_pk_apk, f_new, tk_root, RIGHT)
# tp_item = ui_button_item('pk-ipa', 12, do_async_server_pk_ipa, f_normal, tp_item, RIGHT)
# tp_item = ui_button_item('pk-web', 12, do_async_server_pk_web, f_normal, tp_item, RIGHT)
# tp_item = ui_button_item('pk-整包热更', 12, do_async_server_pk_hotUpdate, f_normal, tp_item, RIGHT)
# tp_item = ui_button_item('pk-大厅热更', 12, do_async_server_pk_hotHall, f_normal, tp_item, RIGHT)

# s_frame_item[s_name_server].append(tp_item)
# s_frame_item['all'].append(tp_item)
# # server===============================================================================================================================

# copyGame==============================================================================================================================
s_tp_frame_w = 95
s_tp_entrt_w = 100
tp_parent = ui_getFrameList()
s_frame_item[s_name_copyGame].append(tp_parent)
s_frame_item['all'].append(tp_parent)

tp_item = ui_entry_newf('游戏根路径:', def_entry_w_newf, s_tp_entrt_w, g_run_root, f_renew, tp_parent, LEFT, uiFrameWidth0(s_tp_frame_w))
s_frame_item[s_name_copyGame].append(tp_item)
s_frame_item['all'].append(tp_item)

tp_parent = ui_getFrameList()
s_frame_item[s_name_copyGame].append(tp_parent)
s_frame_item['all'].append(tp_parent)

tp_item = ui_entry_newf('旧脚本根路径:', def_entry_w_newf, s_tp_entrt_w, g_old_script, f_renew, tp_parent, LEFT, uiFrameWidth0(s_tp_frame_w))
s_frame_item[s_name_copyGame].append(tp_item)
s_frame_item['all'].append(tp_item)

tp_parent = ui_getFrameList()
s_frame_item[s_name_copyGame].append(tp_parent)
s_frame_item['all'].append(tp_parent)

tp_item = ui_entry_newf('新脚本根路径:', def_entry_w_newf, s_tp_entrt_w, g_new_script, f_renew, tp_parent, LEFT, uiFrameWidth0(s_tp_frame_w))
s_frame_item[s_name_copyGame].append(tp_item)
s_frame_item['all'].append(tp_item)

tp_parent = ui_getFrameList()
s_frame_item[s_name_copyGame].append(tp_parent)
s_frame_item['all'].append(tp_parent)

tp_item = ui_entry_newf('library:', def_entry_w_newf, s_tp_entrt_w, g_path_library, f_renew, tp_parent, LEFT, uiFrameWidth0(s_tp_frame_w))
s_frame_item[s_name_copyGame].append(tp_item)
s_frame_item['all'].append(tp_item)

tp_parent = ui_getFrameList()
s_frame_item[s_name_copyGame].append(tp_parent)
s_frame_item['all'].append(tp_parent)

tp_item = ui_entry_newf('导入根目录:', def_entry_w_newf, 15, g_new_name, f_renew, tp_parent, LEFT, uiFrameWidth0(s_tp_frame_w))
tp_item = ui_entry_item('新脚本前缀:', def_entry_w_newf+5, 15, g_script_head, f_normal, tp_item, LEFT, uiFrameWidth0(s_tp_frame_w))
s_frame_item[s_name_copyGame].append(tp_item)
s_frame_item['all'].append(tp_item)

tp_parent = ui_getFrameList()
s_frame_item[s_name_copyGame].append(tp_parent)
s_frame_item['all'].append(tp_parent)

tp_item = ui_button_newf('替换匹配脚本1', 15, do_event_replace_script, f_new, tk_root, RIGHT)
tp_item = ui_button_item('             ', 15, None, f_normal, tp_item, RIGHT)
tp_item = ui_button_item('生成匹配关系0', 15, do_event_search_script, f_normal, tp_item, RIGHT)
tp_item = ui_button_item('             ', 15, None, f_normal, tp_item, RIGHT)
tp_item = ui_button_item('导入新游戏目录', 15, do_event_create_path, f_normal, tp_item, RIGHT)
s_frame_item[s_name_copyGame].append(tp_item)
s_frame_item['all'].append(tp_item)
# copyGame==============================================================================================================================


# project==============================================================================================================================
tp_item = ui_button_newf('重置按钮', 12, do_event_reset_btn_state, f_new, tk_root, RIGHT)
tp_item = ui_button_item('批量配置csv', 12, do_open_batch_csv, f_normal, tp_item, RIGHT)
tp_item = ui_button_item('批量环境检查',12, do_check_batch_logic, f_normal, tp_item, RIGHT)
tp_item = ui_button_item('批量配置目录', 12, do_event_open_batch_conf_path, f_normal, tp_item, RIGHT)
tp_item = ui_button_item('脚本目录', 12, do_event_open_self, f_normal, tp_item, RIGHT)
tp_item = ui_button_item('输出目录', 12, do_event_open_out_root, f_normal, tp_item, RIGHT)
# tp_item[0].config(bg='red')
s_frame_item['project'].append(tp_item)
s_frame_item['all'].append(tp_item)

tp_item = ui_button_newf('构建项目', 12, do_btn_build_project, f_new, tk_root, RIGHT);s_frame_item['item_btn'].append(tp_item)
tp_item = ui_button_item('简体大厅资源', 12, do_btn_build_hall_res_version, f_normal, tp_item, RIGHT);s_frame_item['item_btn'].append(tp_item)
tp_item = ui_button_item('刷新build渠道', 12, do_btn_update_channelid_version0, f_normal, tp_item, RIGHT)
tp_item = ui_button_item('刷新assets渠道', 12, do_btn_update_channelid_version1, f_normal, tp_item, RIGHT)
tp_item = ui_button_item('简体配置', 12, do_event_open_gameConfig, f_normal, tp_item, RIGHT)
tp_item = ui_button_item('换肤帮助', 12, do_open_batch_skin_templates, f_normal, tp_item, RIGHT)
# tp_item[0].config(bg='red')
s_frame_item['project'].append(tp_item)
s_frame_item['all'].append(tp_item)
# project==============================================================================================================================

# other============================================================================================================================
tp_item = ui_checkbutton_newf('projectRoot = src_path', None, None, f_check_w, f_new, tk_root, TOP)
tp_item[0].config(padx=f_check_padx)
s_frame_item[s_name_other].append(tp_item)
s_frame_item['all'].append(tp_item)

tp_item = ui_checkbutton_newf('热更地址    = dst_path', None, None, f_check_w, f_new, tk_root, TOP)
tp_item[0].config(padx=f_check_padx)
s_frame_item[s_name_other].append(tp_item)
s_frame_item['all'].append(tp_item)

# tp_item = ui_checkbutton_newf('creatorRoot = src_root', None, None, f_check_w, f_new, tk_root, TOP)
# tp_item[0].config(padx=f_check_padx)
# s_frame_item[s_name_other].append(tp_item)
# s_frame_item['all'].append(tp_item)

tp_item = ui_button_newf('重置按钮', 12, do_event_reset_btn_state, f_new, tk_root, RIGHT)
tp_item = ui_button_item('反编译pyc', 12, do_event_uncompyle_py_path, f_normal, tp_item, RIGHT)
tp_item = ui_button_item('移动所有src文件->dst文件夹', 30, do_event_batch_movefile_to_finder, f_normal, tp_item, RIGHT)
s_frame_item[s_name_other].append(tp_item)
s_frame_item['all'].append(tp_item)
# other============================================================================================================================


def on_close_tool():
    on_close_opt(1)

# 保存配置
def on_close_opt(bClose):
    # 设置配置
    g_creator_root.set(tool.path_replace(g_creator_root.get()))
    g_project_root.set(tool.path_replace(g_project_root.get()))

    if g_ios_pkg_enterprise.get()==1:
        g_profiles_enterprise.set(g_profiles_name.get())
        g_enterprise_teamid.set(g_dev_teamid.get())

    if g_ios_pkg_adhoc.get()==1:
        g_profiles_adhoc.set(g_profiles_name.get())
        g_adhoc_teamid.set(g_dev_teamid.get())
        
    if g_ios_pkg_appstore.get()==1:
        g_profiles_appstore.set(g_profiles_name.get())
        g_appstore_teamid.set(g_dev_teamid.get())
    
    # 保存配置
    start_config.on_save_config_by_ui(this)

    if bClose==1:
        pkg_client.stop_client()
        tk_root.destroy()

# 配置读取
def on_load_opts():
    
    # 读取配置
    start_config.on_read_config_by_ui(this)

    # 根据目录 自动设置版本
    ccc_ver = tool.var_string(g_creator_root)

    # 更新配置
    if g_server_public.get()==1:
        _set_server_public()

    if g_server_test.get()==1:
        _set_server_test()

    if g_server_local.get()==1:
        _set_server_local()

    # 环境校验
    do_set_platform(g_is_idx.get())

    # 更新时间版本
    do_btn_set_time_ver()
    
on_load_opts()

# 主窗口循环显示
tk_root.protocol("WM_DELETE_WINDOW", on_close_tool)
tk_root.resizable(width=False, height=False)
tk_root.mainloop()






