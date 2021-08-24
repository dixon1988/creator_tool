#!/usr/bin/env python
#coding:utf8
import threading
from colorama import init, Fore, Back, Style
import os
import json
import codecs
import hashlib
import subprocess
import shutil
import time
import zipfile
import platform
import start_path
from tkinter import messagebox

platform_name=platform.platform()
IsWds=platform_name.find("Windows")==0
IsIos = not( IsWds )

def run_script(py_script):
    if IsIos:
       return os.system( 'python3 ' + py_script)
    else:
       return os.system(py_script)

init(autoreset=True)

def path_replace(path):
    return path.replace('\\','/')

def path_replace2(path):
    return path.replace('/','\\')

def var_string(var):
    return path_replace(str(var.get()))

self_path = os.path.split(os.path.realpath(__file__))[0]
self_path = path_replace(self_path)

g_conf_path = self_path + '/conf/tool.json'
g_server_conf_path = self_path + '/conf/server.json'

class color:
    #  前景色:红色  背景色:默认
    red = Fore.RED
 
    #  前景色:绿色  背景色:默认
    green = Fore.GREEN 
 
    #  前景色:黄色  背景色:默认
    yellow = Fore.YELLOW
 
    #  前景色:蓝色  背景色:默认
    blue = Fore.BLUE
 
    #  前景色:洋红色  背景色:默认
    magenta = Fore.MAGENTA
 
    #  前景色:青色  背景色:默认
    cyan = Fore.CYAN
 
    #  前景色:白色  背景色:默认
    white = Fore.WHITE

    #  前景色:黑色  背景色:默认
    black = Fore.BLACK

def out(s, c=color.white, reset=0):
    if reset!=0:
        print( c + s + Fore.RESET )
    else:
        print( c + s )

#  前景色:绿色  背景色:默认
def out_green(s, reset=0):
    if reset!=0:
        print( color.green + s + Fore.RESET )
    else:
        print( color.green + s )

#  前景色:红色  背景色:默认
def out_red(s, reset=0):
    if reset!=0:
        print( color.red + s + Fore.RESET )
    else:
        print( color.red + s )

#  错误-红色
def out_error(s, reset=0):
    if reset!=0:
        print( color.red + 'error: ' + s + Fore.RESET )
    else:
        print( color.red + 'error: ' + s )

#  警告-青色
def out_warning(s, reset=0):
    if reset!=0:
        print( color.cyan + 'warning: ' + s + Fore.RESET )
    else:
        print( color.cyan + 'warning: ' + s )
        
#  成功-绿色
def out_succeed(s, reset=0):
    if reset!=0:
        print( color.green + s + Fore.RESET )
    else:
        print( color.green + s )

#  完成-黄色
def out_done(s, reset=0):
    if reset!=0:
        print( color.yellow + s + Fore.RESET )
    else:
        print( color.yellow + s )

#  命令-蓝色
def out_cmd(s, reset=0):
    if reset!=0:
        print( color.blue + 'cmd:' + s + Fore.RESET )
    else:
        print( color.blue + 'cmd:' + s )

#  前景色:白色  背景色:默认
def out_white(s, reset=0):
    if reset!=0:
        print( color.white + s + Fore.RESET )
    else:
        print( color.white + s )

#  前景色:黑色  背景色:默认
def out_black(s, reset=0):
    if reset!=0:
        print( color.black + s + Fore.RESET )
    else:
        print( color.black + s )

#  前景色:青色  背景色:默认
def out_cyan(s, reset=0):
    if reset!=0:
        print( color.cyan + s + Fore.RESET )
    else:
        print( color.cyan + s )

#  前景色:青色  背景色:默认
def out_magenta(s, reset=0):
    if reset!=0:
        print( color.magenta + s + Fore.RESET )
    else:
        print( color.magenta + s )

#  前景色:蓝色  背景色:默认
def out_blue(s, reset=0):
    if reset!=0:
        print( color.blue + s + Fore.RESET )
    else:
        print( color.blue + s )

#  前景色:黄色  背景色:默认
def out_yellow(s, reset=0):
    if reset!=0:
        print( color.yellow + s + Fore.RESET )
    else:
        print( color.yellow + s )

# 设置记录
def set_tk_opt( conf, tk_key, tk_var ):
    if conf.has_section('opt')==False:
        conf.add_section("opt")
        
    conf.set('opt', tk_key, str(tk_var.get()))

# 获取记录
def get_tk_opt( conf, tk_key, tk_var ):
    if conf.has_option('opt', tk_key)==True:
        tk_var.set(conf.get('opt',tk_key))

# number判定
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False

# 获取json文件内容
def read_file_json(file_path):
    fp = codecs.open(file_path,'r+','utf-8')
    load_data=fp.read()
    fp.close()
    tp_connect = json.loads(load_data)
    return tp_connect

# 获取文件内容
def read_file_string(file_path):
    fp = codecs.open(file_path,'r+','utf-8')
    load_data=fp.read()
    fp.close()
    return load_data

# 获取文件内容
def read_file_lines(file_path):
    fp = codecs.open(file_path,'r+','utf-8')
    load_data=fp.readlines()
    fp.close()
    return load_data

# 保存内容
def save_file_string(file_path, buf):
    fp = codecs.open(file_path,'w+','utf-8')
    fp.write( buf )
    fp.flush()
    fp.close()

# 写入json文件 str_data
def write_file_content(file_path, str_data):
    save_file_string(file_path, str_data)
    
# 写入json文件 json_obj
def write_file_json(file_path, json_obj, isDebug=False):
    if isDebug==True:
        save_file_string(file_path, json.dumps(json_obj,indent=4))
    else: 
        save_file_string(file_path, json.dumps(json_obj))

# 写入json文件 json_obj
def write_file_json_indent4(file_path, json_obj):
    save_file_string(file_path, json.dumps(json_obj,indent=4))

# 计算内容md5
def hashlib_md5(buf):
    md5=hashlib.md5(buf.encode(encoding='UTF-8')).hexdigest()
    return md5

# 计算二进制文件md5
def hashlib_md5_file(file_path):
    fp = codecs.open(file_path, 'rb')
    md = hashlib.md5()
    md.update(fp.read())
    fp.close()
    md5 = md.hexdigest()
    return md5

# 获取工具配置
def get_tool_conf(key):
    tool_conf = read_file_json( g_conf_path )
    return tool_conf[key]

# 获得加密key
def get_entry_file_type():
    gameconf = read_file_json( g_conf_path )
    entry_file_type = gameconf['entry_file_type']
    file_array = []

    for file in entry_file_type:
        file_array.append(file)

    return file_array

# 获得加密忽略文件列表
def get_entry_ignore_list():
    gameconf = read_file_json( g_conf_path )
    igonre_file = gameconf['entry_ignore_file']
    igonre_array = []

    for file in igonre_file:
        igonre_array.append(file)

    return igonre_array

# 获得ftp文件信息
def get_server_info():
    gameconf = read_file_json( g_server_conf_path )
    server_info = gameconf['service']
    return server_info

# 获得ftp文件信息
def get_server_conf(key):
    gameconf = read_file_json( g_server_conf_path )
    server_info = gameconf[key]
    return server_info

# 获取游戏列表
def get_game_list_2020(game_root):
    # 获取排除游戏设置
    gameconf = read_file_json( g_conf_path )
    pkg_game = gameconf['game_pkg']
    
    # 子游戏目录
    list_dir = os.listdir(game_root)
    list_dir.sort()

    game_array = []
    
    # 获取所有子游戏
    for dir_name in list_dir:
        if get_file_ext(dir_name)==".meta":continue
        if not is_number(dir_name):continue

        # 排除打包游戏
        b_pkg_game = False
        for key in pkg_game:
            if dir_name==key:
                b_pkg_game=True
                break
        if not b_pkg_game:
            game_array.append(dir_name)
    return game_array

# 获取游戏列表
def get_game_list_1_10():
    game_array = []

    # 获取排除游戏设置
    gameconf = read_file_json( g_conf_path )
    game_list = gameconf['gamelist1_10']
    
    # 获取所有子游戏
    for dir_name in game_list:
        game_array.append(dir_name)
    return game_array

# 打开文件夹
def open_finder(fullpath):
    print('open_finder:'+fullpath)
    if IsIos:
        subprocess.call(["open", fullpath])
    else:
        os.startfile(fullpath)

#显示消息框
def msgbox(text):
    messagebox.showinfo(title='消息', message=text)
    return False

# 获得目录下的指定类型文件
def get_dir_file2( srcPath, file_array ):
    apk_list = []
    for maindir, subdir, file_name_list in os.walk(srcPath):
        for filename in file_name_list:
            #绝对路径
            apath = os.path.join(maindir, filename)
            apath = path_replace(apath)

            #后缀
            ext = os.path.splitext(apath)[1]

            # 查找类型
            for find_type in file_array:
                if ext==find_type:
                    apk_list.append(apath)
                    break
    return apk_list

# 
# def del_dir_file_exclude_type( srcPath, file_type ):

# 获得目录下的指定类型文件
def get_dir_file( srcPath, file_type ):
    apk_list = []
    for maindir, subdir, file_name_list in os.walk(srcPath):
        for filename in file_name_list:
            #绝对路径
            apath = os.path.join(maindir, filename)
            apath = path_replace(apath)

            #后缀
            ext = os.path.splitext(apath)[1]

            if ext==file_type:
                apk_list.append(apath)
    return apk_list

# 获得目录下的指定类型文件
def get_dir_path( srcPath, file_type ):
    path_list = []
    for maindir, subdir, file_name_list in os.walk(srcPath):
        for tp_dir in subdir:
            if tp_dir.find(file_type)!=-1:
                path_list.append(tp_dir)
    return path_list

# 获取下所有文件
def get_dir_all_file( dir_path ):
    apk_list = []
    for maindir, subdir, file_name_list in os.walk(dir_path):
        for filename in file_name_list:
            #绝对路径
            apath = os.path.join(maindir, filename)
            apath = path_replace(apath)

            if apath.find('.DS_Store')!=-1 or apath.find('.svn')!=-1:
                continue

            #后缀
            tp_file = apath.split('/')[-1]

            apk_list.append(apath)
            print(apath)
    return apk_list

# 删除目录
def system_rmtree(path): 
    if IsIos:
        shutil.rmtree(path)
    else:
        arg_path = "rd " + path_replace2(path) + " /s /q"
        out_blue(arg_path)
        os.system(arg_path)

# 拷贝命令
def system_copytree(bake_path, build_path): 
    if IsIos:
        shutil.copytree(bake_path, build_path)
    else:
        # xcopy %curPath%winpcap\win64\dll\win32\* %systemroot%\System32\ /s/e/y
        arg_path = "xcopy " + path_replace2(bake_path)  + "\*.* " + path_replace2(build_path) + "\ /e /y /q"
        out_blue(arg_path)
        os.system(arg_path)

# 删除目录
def rmtree(self, top):
    if os.path.exists(top)==False: 
        return

    for root, dirs, files in os.walk(top, topdown=False):
        for name in files:
            filename = os.path.join(root, name)
            filename = path_replace(filename)
            os.chmod(filename, os.st.S_IWUSR)
            os.remove(filename)
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(top)

# 创建目录
def mkdir(path):
    if not os.path.isdir(path):
        mkdir(os.path.split(path)[0])
    else:
        return
    os.makedirs(path)

# 拷贝目录
def copydir( srcPath, dstPath, bakeup_dstPath=False, printLog=False ):
    print("copystart:%s => %s"%(srcPath, dstPath))
    copy_count=0

    srcPath_bakeup = srcPath + '_bakeup'

    #处理路径
    for maindir, subdir, file_list in os.walk(srcPath):
        for filename in file_list:
            #绝对路径
            apath = os.path.join(maindir, filename)
            apath = path_replace(apath)
            
            if apath.find('.DS_Store')!=-1 or apath.find('.svn')!=-1:
                continue

            # 拷贝目录
            target_file = apath.replace(srcPath,dstPath)
            target_dir = os.path.abspath(os.path.dirname(target_file))
            target_dir = path_replace(target_dir)

            # 备份源文件
            if bakeup_dstPath:
                bakeup_src_file = apath.replace(srcPath,dstPath)
                bakeup_dst_file = apath.replace(srcPath,srcPath_bakeup)

                # 备份文件存在，且未备份时，执行备份
                if os.path.exists(bakeup_src_file) and not os.path.exists(bakeup_dst_file):
                    bakeup_target_dir = os.path.abspath(os.path.dirname(bakeup_dst_file))
                    bakeup_target_dir = path_replace(bakeup_target_dir)
                    mkdir(bakeup_target_dir)
                    if printLog:
                        print("copydir: %s => %s"%(bakeup_src_file, bakeup_dst_file))
                    shutil.copy(bakeup_src_file, bakeup_dst_file)

            # 目录校验
            mkdir(target_dir)

            # 执行拷贝
            if printLog:
                print("copydir: %s => %s"%(apath, target_file))
            shutil.copy(apath, target_file)
            copy_count+=1
    
    print("copydoned:%s => %s filecount:%d"%(srcPath,dstPath,copy_count))

def copydir4( srcPath, dstPath, src_root_path, dst_root_path):
    print("copystart:%s => %s"%(srcPath,dstPath))
    copy_count=0

    #处理路径
    for maindir, subdir, file_name_list in os.walk(srcPath):
        for filename in file_name_list:
            #完整路径
            apath = os.path.join(maindir, filename)
            apath = path_replace(apath)

            # 拷贝目录
            targetDir=apath.replace(src_root_path,dst_root_path)
            targetDir=os.path.abspath(os.path.dirname(targetDir))

            # 目录校验
            mkdir(targetDir)

            # 执行拷贝
            shutil.copy(apath, targetDir)

            copy_count+=1

    print("copydoned: filecount:%d"%(copy_count))

# 获得时间戳
def get_timestamp():
    time_ver = int(time.time())
    return str(time_ver)

# 版本转换
def get_ccc_ver(p1,p2,p3):
    return p1*100000 + p2*1000 + p3

# etc2支持版本 0:新 1:旧版本
def get_etc2_new(ccc_root):
    ver_flag = get_ccc_ver(2, 2, 0)
    
    # ccc 版本校验
    ver_path = ccc_root
    ver_start = ver_path.find('CocosCreator_') + 13
    ver_str = ver_path[ver_start:len(ver_path)]
    ver_array = ver_str.split('.')
    ver_int = get_ccc_ver( int(ver_array[0]), int(ver_array[1]), int(ver_array[2]) )
    
    # ccc 添加 json 自动转换
    if( ver_int>= ver_flag ):
        return '1'
    return '0'


# 获取文件后缀名
def get_file_ext(path): 
    return os.path.splitext(path)[1]

def get_file_name(path):
    filename = os.path.basename(path)
    return filename.split('.')[0]

def get_meta_json_ct_type(ct_name):
    gameconf = read_file_json( g_conf_path )
    json_ct_obj = gameconf['meta_json_content']
    
    if ct_name in json_ct_obj:
        return json_ct_obj[ct_name]
    
    out_error('ct_type ' + ct_name + ' is not found, pls check type')
    return False

def get_meta_json_ct_ignore_piexl():
    gameconf = read_file_json( g_conf_path )
    json_ct_obj = gameconf['meta_json_content']
    ignore_piexl = json_ct_obj['ignore_piexl']
    w = ignore_piexl[0]
    h = ignore_piexl[1]
    return int(w)*int(h)

# zip_import 恢复
def zip_import_for_restore(root_path):
    tp_bake_import = start_path.root_import_bake
    tp_import = root_path + '/' + start_path.root_import
    
    # 删除压缩zip目录
    if os.path.exists(tp_import): 
        shutil.rmtree(tp_import)
        
    # 从备份目录恢复
    bk_import = root_path + '/' + tp_bake_import
    if os.path.exists(bk_import):
        print('备份import目录：'+bk_import)
        shutil.copytree(bk_import, tp_import)

# zip_import 压缩
def zip_import_md5_for_path(root_path, del_path, import_json ):
    print("zip_start:" + root_path)
    zip_count=0

    tp_import = start_path.root_import
    tp_bake_import = start_path.root_import_bake

    import_path = root_path + '/' + tp_import
    if not os.path.exists(import_path): return
    
    # 备份import目录，以防后面再次使用到
    bk_import = root_path + '/' + tp_bake_import
    if os.path.exists(bk_import):shutil.rmtree(bk_import)
    print('备份import目录：' + bk_import)
    shutil.copytree(import_path, bk_import)
    
    #处理路径
    list_dir = os.listdir(import_path)
    list_dir.sort()
    list_zip_md5 = {}

    for dir_name in list_dir:
        tmp_key = tp_import + '/' + dir_name + '.zip'
        tmp_path = import_path + '/' + dir_name
        zip_path = tmp_path + '.zip'
        # print( zip_count, ':', tmp_path )
        
        # fzipinfo = fzip.getinfo()
        dir_files = os.listdir(tmp_path)
        dir_files.sort()
        if len(dir_files)==0:
            out_warning('===============zip_path filecount=0')
            continue
        
        # 生成zip + zip内容
        fzip = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
        str_buf = ''
        file_list = []
        
        for dir_file in dir_files:
            tmp_full = tmp_path + '/' + dir_file
            tmp_file = dir_name + '/' + dir_file
            fzip.write(tmp_full, arcname=tmp_file, compress_type=zipfile.ZIP_DEFLATED)
            
            str_buf = str_buf + read_file_string(tmp_full) +'\n'

            file_list.append(dir_file)
        fzip.close()

        # 生成zip内容md5
        md5 = hashlib_md5(str_buf)

        list_zip_md5[tmp_key] = md5

        # 删除已压缩目录
        if del_path:
            shutil.rmtree(tmp_path)
        zip_count +=1

    import_md5_path = root_path + '/' + import_json

    # 保存记录，等待使用
    write_file_json(import_md5_path, list_zip_md5)

    print("zip_ended:" , zip_count)

# 记录文件md5值
def file_md5_for_path(root_path, file_md5):
    raw_assets = root_path + '/res/raw-assets'
    filelist = get_dir_file2(raw_assets, ['.jpg', '.png'])
    
    key_root = 'res/raw-assets'
    
    json_md5_obj = {}
    for filepath in filelist:
        key = get_file_name(filepath)
        filekey = key_root + '/' + key[0:2] + '/' + key + '.pkm'
        json_md5_obj[filekey] = hashlib_md5_file(filepath) 
    
    file_md5_path = root_path + '/' + file_md5
    write_file_json(file_md5_path, json_md5_obj)
    
# cache_md5_replace
def cache_md5_replace(manifest, build_path, cache_filename):
    manifest_path = build_path + '/' + manifest
    cache_path = build_path + '/' + cache_filename

    cache_json = read_file_json(cache_path)
    manifest_json = read_file_json(manifest_path)

    assets = manifest_json['assets']

    allcount = 0
    rp_count = 0
    for cache_key in cache_json:
        allcount += 1
        if cache_key in assets:
            file_info = assets[cache_key]
            file_info['md5'] = cache_json[cache_key]
            rp_count +=1 

    if allcount==rp_count:
        out_green('cache_md5_replace succeed! allcount:' + str(allcount) + ' rp_count:' + str(rp_count))
    else:
        out_red('warnind:cache_md5_replace: allcount' + str(allcount) + ' rp_count:' + str(rp_count))

    write_file_json(manifest_path, manifest_json)

# 压缩文件
def zip_dir(dirname, zipfilename):
    filelist = []
    if os.path.isfile(dirname):
        filelist.append(dirname)
    else:
        for root, dirs, files in os.walk(dirname):
            for name in files:
                filelist.append(os.path.join(root, name))
                zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
    
    for tar in filelist:
        arcname = tar[len(dirname):]
        #print arcname
        zf.write(tar,arcname)
    zf.close()

# 解压文件
def unzip_file(zipfilename, unziptodir):
    if not os.path.exists(unziptodir):
        os.mkdir(unziptodir, 777)
    zfobj = zipfile.ZipFile(zipfilename)
    for name in zfobj.namelist():
        name = name.replace('\\','/')
        if name.endswith('/'):
            os.mkdir(os.path.join(unziptodir, name))
        else:
            ext_filename = os.path.join(unziptodir, name)
            ext_dir= os.path.dirname(ext_filename)
            if not os.path.exists(ext_dir):
                os.mkdir(ext_dir,777)
            outfile = open(ext_filename, 'wb')
            outfile.write(zfobj.read(name))
            outfile.close()
            
# 反编译pyc
def uncompyle_py_file(path):
    # uncompyle6 models.pyc > models.py
    file_list = get_dir_file(path, '.pyc')
    count=0
    for file in file_list:
        # file_pyc = get_file_name(file) + get_file_ext(file)
        # file_py = get_file_name(file) + get_file_ext(file)
        try:
            param_cmd = 'uncompyle6 ' + file + ' > ' + file.replace('.pyc','.py')
            out_cmd(param_cmd)
            os.system(param_cmd)
            count += 1
        except Exception as error:
            print(error)
            
    if count==len(file_list):
        out_green('反编译成功')
        return True
    return False

# 批量移动文件到文件夹
def move_file_to_finder(src_root, dst_root):
    mkdir(dst_root)
    src_path = path_replace(src_root)
    dst_path = path_replace(dst_root)
    file_list = get_dir_all_file(src_path)
    
    print("开始移动:", len(file_list))
    for file in file_list:
        file_ext = get_file_name(file) + get_file_ext(file)
        dst_save = dst_path + '/' + file_ext
        os.rename(file, dst_save)
    print("移动结束:")

    return "移动成功+%d"%(len(file_list))

# 多线程日志监控
def do_thread_log_catch(log_file):
    # 创建
    t = threading.Thread(target=do_log_catch, args=[log_file])
    # 守护 !!!
    t.setDaemon(True)
    # 启动
    t.start()

# def do_log_catch():