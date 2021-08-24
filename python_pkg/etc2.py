#!/usr/bin/env python
#coding:utf8 
import os
import hashlib
import shutil
import platform
import gzip
from PIL import Image

import tool
import start_path

platform_name=platform.platform()
IsWds=platform_name.find("Windows")==0
IsIos = not( IsWds )
env = os.environ

root_path = ''
root_out = ''
cache_dir = ''
cachePPM_dir = ''

etc2_failure = []

self_path = ''
self_out_path = ''
etcpack_cmd = 'etcpack '

def do_environ():
    global root_path
    global root_out
    global cache_dir
    global cachePPM_dir

    global self_path
    global self_out_path
    global etcpack_cmd
    
    self_path = env['_self_path']
    self_out_path = env['_self_out_path']

def path_replace(path):
    return path.replace('\\','/')

def CalcMD5(filepath):
    with open(filepath,'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        md5 = md5obj.hexdigest()
        return md5

def process(root):
    output = []
    ignore_piexl = tool.get_meta_json_ct_ignore_piexl()
    
    for parent, subdirs, files in os.walk(root):
        for name in files:
            if name.endswith('.png') or name.endswith('.jpg') or name.endswith('.pkm'):
                fp = os.path.join(parent,name)
                fp = path_replace(fp)

                if name.endswith('.png') or name.endswith('.jpg'):
                    img = Image.open(fp)
                    if img.size[0]*img.size[1] <= ignore_piexl:
                        tool.out_warning('ignore too small piexl file: ' + str(ignore_piexl) + ' piexl' + fp)
                        continue
                output.append(fp)
    print('etc2.process: filecount:', len(output))
    return output

# etc2+gzip
def convert_etc2_gzip(filepath):
    
    directory = os.path.dirname(filepath)
    md5 = CalcMD5(filepath)
    cacheFilePath = os.path.join(cache_dir,md5)
    cacheFilePath = path_replace(cacheFilePath)
    
    inCache = os.path.exists(cacheFilePath)
    pkmPath = os.path.join(directory,os.path.splitext(os.path.basename(filepath))[0]+".pkm")
    pkmPath = path_replace(pkmPath)
    
    ppmPath = os.path.join(directory,os.path.splitext(os.path.basename(filepath))[0]+".ppm")
    ppmPath = path_replace(ppmPath)
    
    targetPath = os.path.join(directory,os.path.basename(filepath))
    targetPath = path_replace(targetPath)
    
    if inCache:
        print("copy cached ", pkmPath)
        f_in = open(cacheFilePath, 'rb')
        f_out = gzip.open(cacheFilePath+'.gz', 'wb')
        f_out.writelines(f_in)
        f_out.close()
        f_in.close()
        #os.remove(cacheFilePath)
        shutil.move(cacheFilePath+'.gz',targetPath)
        
        #shutil.copy(cacheFilePath,targetPath)
    else:
        command = etcpack_cmd + filepath + ' ' + directory + ' -c etc2 -f RGBA8'
        print(command)
        os.system(command)
        #os.remove(ppmPath)
        shutil.copy(pkmPath,cacheFilePath)
        f_in = open(pkmPath, 'rb')
        f_out = gzip.open(pkmPath+'.gz', 'wb')
        f_out.writelines(f_in)
        f_out.close()
        f_in.close()
        os.remove(pkmPath)
        #os.remove(cacheFilePath)
        shutil.move(pkmPath+'.gz',targetPath)
        print("cache copyed ", targetPath)
        #os.remove(cache_dir)

# 创建目录
def mkdir(path):
    if not os.path.isdir(path):
        mkdir(os.path.split(path)[0])
    else:
        return
    os.makedirs(path)

# 此操作etc2仅支持 win系统
# ccc1.x etc2 + gzip
def start_etc2_gzip_to_png( root, outroot ):
    print('etc2.start:' + root + ' outroot:' + outroot)
    
    global root_path
    global cache_dir
    global cachePPM_dir
    
    root_path = root
    cache_dir = outroot+'/cache_etc2_gzip'
    cachePPM_dir = outroot+'/ppm_etc2_gzip'
    
    mkdir(cache_dir)
    mkdir(cachePPM_dir)
    
    files = process(root)

    for path in files:
        convert_etc2_gzip(path)

# 此操作etc2仅支持 win系统
# ccc1.x etc2
def start_etc2_to_png( root, outroot ):
    print('etc2.start:' + root + ' outroot:' + outroot)
    
    global root_path
    global cache_dir
    global cachePPM_dir
    
    root_path = root
    cache_dir = self_out_path + '/cache_etc2'
    cachePPM_dir = self_out_path + '/ppm_etc2'
    
    mkdir(cache_dir)
    mkdir(cachePPM_dir)
    
    files = process(root)

    for path in files:
        convert_etc2_gzip(path)

# ccc2.2.x 此操作etc2仅支持 win系统
def start_etc2_gzip_to_pkm( root_res, res_import, outroot, fp_file_md5 ):
    start_etc2_to_pkm(root_res, res_import, outroot, fp_file_md5, True)
            
# 此操作etc2仅支持 win系统
# ccc2.2.x
def start_etc2_to_pkm( root_res, res_import, outroot, fp_file_md5, res_gzip=False ):
    print('etc2.start_etc2_to_pkm:' + root_res + ' outroot:' + outroot)
    
    do_environ()
    
    global etc2_failure

    cache_dir = self_out_path + '/cache_etc2_pkm'
    if res_gzip: cache_dir = self_out_path + '/cache_etc2_gzip_pkm'
    mkdir(cache_dir)
    
    files = process(root_res)
    
    pkm_failure_count = 0
    pkm_count = 0
    for filepath in files:
        md5 = CalcMD5(filepath)
        cacheFilePath = os.path.join(cache_dir,md5)
        cacheFilePath = tool.path_replace(cacheFilePath)
        
        # inCache = os.path.exists(cacheFilePath)
        cacheFilePath = cacheFilePath+'.pkm'
        pkm_cache = os.path.exists(cacheFilePath)
        
        tp_file_name = os.path.basename(filepath)
        tp_path = os.path.splitext(tp_file_name)

        directory = os.path.dirname(filepath)
        pkmPath = os.path.join(directory, tp_path[0]+".pkm")
        pkmPath = tool.path_replace(pkmPath)
        
        file_ext = tool.get_file_ext(filepath)

        if pkm_cache:
            print("copy:", pkmPath)
            shutil.copy(cacheFilePath, pkmPath)
            pkm_count += 1
        else:
            # mac下暂未实现etc2转换
            if IsIos:
                etc2_failure.append(filepath)
                tool.out_warning('pkm failure:'+filepath)
                pkm_failure_count += 1
                continue

            rgb_name = 'RGBA8'
            if file_ext=='.jpg':rgb_name='RGB'
            
            if IsWds:
                command = 'etcpack ' + filepath + ' ' + directory + ' -c etc2 -f ' + rgb_name + ' -s fast'
                os.system(command)
            # else:
            #     command = 'EtcTool ' + filepath + ' ' + directory + ' -c etc2 -f ' + rgb_name + ' -s fast'
            #     os.system(command)

            # 压缩pkm
            f_in = open(pkmPath, 'rb')
            f_out = gzip.open(pkmPath+'.gz', 'wb')
            f_out.writelines(f_in)
            f_out.close()
            f_in.close()
            os.remove(pkmPath)
            shutil.move(pkmPath+'.gz', pkmPath)
            
            # 缓存pkm
            shutil.copy(pkmPath, cacheFilePath)
            pkm_count += 1
            
            print("cache:", pkmPath)

        # 修改 json 描述文件-对应图片类型
        file_name = tool.get_file_name(filepath)
        file_dir = file_name[0:2]
        json_path = res_import + '/' + file_dir + '/' + file_name +'.json'
        new_ext = tool.get_file_ext(pkmPath)

        if os.path.exists(json_path):
            json_obj = tool.read_file_json(json_path)
            content = json_obj[5]
            res_desc = content[0]
            ct_array = res_desc.split(',')
            ct_ret = tool.get_meta_json_ct_type(new_ext+file_ext)
            if ct_ret!=False:
                ct_array[0] = ct_ret
            content[0] = ','.join(ct_array)
            json_obj[5] = content
            tool.write_file_json(json_path, json_obj)

            print('json:', file_name + '.json', ',res_desc:', json_obj)

    # 清理源文件
    for filepath in files:
        os.remove(filepath)

    tool.out_done('pkm change done! change count:'+ str(pkm_count))
    # tool.out_green('write pkm md5 cache')
    if IsIos:tool.out_warning('pkm failure count:'+str(pkm_failure_count))

# etc2-conf
def get_meta_conf(conf_key):
    
    if conf_key=='etc2_conf':
        return 'platformSettings'
    
    elif conf_key=='ios':
        return 'ios'
    
    elif conf_key=='android':
        return 'android'
    
    elif conf_key=='web':
        return 'web'
    
    elif conf_key=='normal':
        return 'normal'
    return 'error'

# etc2 conf
def get_meta_etc2_pf_cont(file_ext):
    if file_ext=='.png':
        return {"formats": [{"name": "etc2","quality": "fast"}]}
    else:
        return {"formats": [{"name": "etc2_rgb","quality": "fast"}]}

# ccc2.2-later
# etc2：.meta 中添加 etc2 json 转换配置 支持win+mac
# 1.png to etc2 
# 2.jpg to etc2_rgb
# "platformSettings": {
#     "ios": {
#         "formats": [{
#             "name": "etc2_rgb",
#             "quality": "fast"
#             }]
#         }
#     },
#     "android": {
#         "formats": [{
#             "name": "etc2",
#             "quality": "fast"
#             }]
#         }

# 添加 etc2 json 转换配置
def start_add_meta_etc2_conf( root_assets, target_platform ):
    
    file_array = tool.get_dir_file2(root_assets, ['.png','.jpg'])
    
    etc2_set_key = get_meta_conf('etc2_conf')
    etc2_pf_key = get_meta_conf(target_platform)
    
    etc2_count = 0
    
    # 添加 etc2 配置
    for file in file_array:
          
        # 查找 meta 文件，添加 etc2 转换配置
        file_ext = tool.get_file_ext(file)
        file_meta = file + '.meta'
        if os.path.exists(file_meta):
            
            # 获取meta配置
            meta_json = tool.read_file_json(file_meta)
            meta_write = False
            
            # png=>etc2 jpg=>etc2_rgb
            if etc2_set_key in meta_json:
                if etc2_pf_key=='normal':
                    meta_json[etc2_set_key] = {}
                else:
                    etc2_json_cof = meta_json[etc2_set_key]
                    etc2_json_cof[etc2_pf_key] = get_meta_etc2_pf_cont(file_ext)
                meta_write = True
            if meta_write:
                tool.write_file_json(file_meta, meta_json)
                etc2_count += 1
    
    # 校验配置
    if etc2_count==len(file_array):
        tool.out_green('etc2 meta config add succeed !!! filecount = ' + str(etc2_count))
        
    print('start_add_meta_etc2_conf')

# 还原 meta 平台配置
def start_meta_normal(root_assets):
    start_add_meta_etc2_conf(root_assets, 'normal')

# ccc2.2 对 pkm 进行 gzip 压缩
def start_gzip_for_pkm( root_assets, outroot ):
    
    file_array = tool.get_dir_file2(root_assets, ['.pkm'])
    
    for pkmPath in file_array:
        f_in = open(pkmPath, 'rb')
        f_out = gzip.open(pkmPath+'.gz', 'wb')
        f_out.writelines(f_in)
        f_out.close()
        f_in.close()
        os.remove(pkmPath)
        shutil.move(pkmPath+'.gz', pkmPath)

# etc 脚本转换
def do_etc2_py_logic( pjroot_jsbpath, ccc_outroot, fp_file_md5 ):
    # 记录失败日志
    global etc2_failure
    etc2_failure = []

    # 执行替换
    tp_raw_assets = pjroot_jsbpath + '/' + start_path.root_res_raw
    tp_import_build = pjroot_jsbpath + '/' + start_path.root_import

    tool.out_green("etc2压缩资源："+ tp_raw_assets)
    start_etc2_gzip_to_pkm(tp_raw_assets, tp_import_build, ccc_outroot, fp_file_md5)

    # 输出日志
    if len(etc2_failure)>0:
        for filepath in etc2_failure:
            print('cache failure: ' + filepath)
        tool.out_warning('pkm cache failure:'+ str(len(etc2_failure)))

# test main
# if __name__ == '__main__':
    
#     print('etc2 start')
    
#     # start( root_path,  root_out )
    
#     print('etc2 done')
    
# files = process(root)
# print(files)
# for path in files:
#     convert(path)
