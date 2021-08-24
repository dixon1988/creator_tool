#!/usr/bin/env python
#coding:utf8
import os,sys,codecs,re,linecache,json,shutil,time,datetime,ctypes,platform

platform_name=platform.platform()
IsWds=platform_name.find("Windows")==0
IsIos = not( IsWds )

import tool
import start_path
import file_analy_delete
import file_entry
import file_analy
import etc2

# 更新地址拼接优化为 url + skinx + version
dir_tail_remote_asset = '-remote-asset'
import_md5_json = 'import_md5.json'
file_md5_json = 'file_md5.json'

_ccc_exe = ''
_ccc_ver = ''
_ccc_proj = ''
_ccc_buildPath = ''
_ccc_jsb_type = ''

_remote_assets = ''

_update_skin_num = ''
_version = ''
_inputid = ''
_ver_res = ''

_self_out_path = ''
_is_debug = '0'

_import_zip = '0'
_pkg_res_type=''
_import_catch = '1'
_is_short = '0'


#搜索路径-文件
def searchFilePath( analy_content, arg_search, arg_path_file ):
    #处理路径
    for maindir, subdir, file_name_list in os.walk(arg_search):
        for filename in file_name_list:
    
            #完整路径
            apath = os.path.join(maindir, filename) 
            apath = tool.path_replace(apath)

            #后缀
            # ext = os.path.splitext(apath)[1]

            #文件名
            file_key = os.path.splitext(filename)[0]
            new_key = file_key

            arr_path=apath.split("/")

            temp_key = arr_path[len(arr_path)-2]
            new_tpkey = temp_key

            if( file_key.find('.')!=-1 ):
                new_key=file_key.split('.')[0]

            if( new_tpkey.find('.')!=-1 ):
                new_tpkey=new_tpkey.split('.')[0]

            file_json = ""
            relativePath = ""
            bFind=False

            if new_key in analy_content:
                file_json = analy_content[new_key]
                relativePath = file_json["relativePath"]
                relativePath = tool.path_replace(relativePath)
                bFind=True

            if bFind==False and new_tpkey in analy_content:
                temp_json = analy_content[new_tpkey]
                relativePath = temp_json["relativePath"]
                relativePath = tool.path_replace(relativePath)
                bFind=True
            
            if bFind==False:
                continue

            # 匹配文件与路径
            if( relativePath.find(arg_path_file)!=-1 ):
                return apath
    return 0

# 简体大厅资源
def start_hall_res(is_build):
    return start_logic(is_build)
    
# 执行热更新
def start_logic(is_build):
    
    jsb_type = _ccc_jsb_type
    version = _version
    ver_res = _ver_res
    inputid = _inputid  # input("是否备份(link:link库、x.x.xxxx:使用x.x.xxxx版本库)：")

    tool.out_green('jsb_type:%s'%(jsb_type))
    tool.out_green("version:%s"%(version))
    tool.out_green("_update_skin_num:%s"%(_update_skin_num))
    tool.out_green("ver_res:%s"%(ver_res))
    tool.out_green("inputid:%s"%(inputid))
    
    # input("请输入版本类型:(0:code 1:GameAll 2:code&&GameAll 其他游戏:GameID)：")
    if( inputid=='0' ): 
        tool.out_green("inputid:0 => 生成大厅版本")
    if( inputid=='1'):
        tool.out_green("inputid:1 => 生成所有游戏版本")
    if( inputid=='2'):
        tool.out_green("inputid:2 => 生成大厅版本 和 所有游戏版本")
    if( inputid!='0' and inputid!='1' and inputid!='2' ):
        tool.out_green("inputid:%s => 生成单个游戏版本"%(inputid))

    ccc_proj_name = _ccc_proj.split('/')[-1]
    outroot_path = _ccc_proj + '/' + _ccc_buildPath
    build_path = outroot_path + '/' + jsb_type
    bake_path = build_path + "_" + version

    print('bake_path:'+bake_path)
    print('build_path:'+build_path)

    build_uuid_json = _ccc_proj + "/library/" + start_path.gen_uuid_json


    build_file_md5 = build_path + "/" + file_md5_json

    # 历史版本库校验 版本库字符串带两个点
    if( ver_res.count('.')==2 ):
        hirstory_path = build_path + "_" + ver_res
        print("历史版本库校验:%s"%(hirstory_path))

        build_uuid_json = hirstory_path + "/" + start_path.gen_uuid_json

        if not os.path.exists(hirstory_path):
            tool.out_red(hirstory_path+":历史版本库不存在,请检查版本库")
            return hirstory_path+":历史版本库不存在,请检查版本库"
        
        tool.out_green("%s:版本库存在，生成版本:%s=>%s"%(hirstory_path,hirstory_path,version))
        bake_path = hirstory_path

    tool.out_green("构建路径:%s"%(build_path))
    tool.out_green("备份路径:%s"%(bake_path))
    outfile_path = _self_out_path + '/' + ccc_proj_name
    
    # 使用历史版本
    if( ver_res!='link' ):
        print("版本库校验:%s"%(bake_path))
        if not os.path.exists(bake_path):
            tool.out_red("版本库不存在:" + bake_path)
            ver_res='link'
        else:
            tool.out_green("版本库存在:" + bake_path+",使用版本库:" + bake_path)

    # 使用当前版本
    if( ver_res=='link' ):
        if os.path.exists(bake_path):
            tool.out_green("清理备份:%s"%(bake_path))
            tool.system_rmtree(bake_path)

        shutil.copy(build_uuid_json, build_path)

        tool.out_green("备份版本：%s => %s"%(build_path, bake_path))
        os.rename(build_path, bake_path)
        
    # 生成大厅版本
    if( inputid=='0' or inputid=='2'):
        tool.out_green("生成大厅版本...")

        gameId = 0
        search_path = start_path.get_search_path(gameId)

        #清理目录
        if os.path.exists(build_path):
            tool.out_green( "清理目录:" + build_path )
            tool.system_rmtree(build_path)

        # 拷贝执行目录
        tool.out_green("拷贝src:%s => %s"%(bake_path, build_path))
        # shutil.copytree(bake_path, build_path)
        tool.system_copytree(bake_path, build_path)

        # 当前资源目录
        start_path.resetResRoot(build_path)
        tm_raw_path = build_path + start_path.root_res_raw

        # 获取分析文件
        analy_content = tool.read_file_json(build_uuid_json)

        # 整理资源，仅保留指定资源
        short_list = tool.get_game_list_2020( _ccc_proj + start_path.root_game_path )

        # 移除其他所有模块资源
        if _is_short=='1':
            res_del_list=[]
            for wkindID in short_list:
                bulid_res_game = "resources/Game/" + str( wkindID ) + "/"
                build_tex_game = "texture/Game/" + str( wkindID ) + "/"
                res_del_list.append(bulid_res_game)
                res_del_list.append(build_tex_game)
                tool.out_green("del:res=%s,tex:%s"%(bulid_res_game,build_tex_game))

            if len(res_del_list)>0:   
                tool.out_green("执行删除")
                file_analy_delete.start(build_path, res_del_list, )

        # 启用资源加密
        if _pkg_res_type=='entry':
            tool.out_cmd("加密资源=" + tm_raw_path )
            file_entry.start( tm_raw_path, '1' )
        
        # 启用 etc2-gzip pkm 转换
        if _pkg_res_type=='etc2_py' and IsWds:
            tool.out_cmd("etc2-gzip=" + tm_raw_path)
            etc2.do_etc2_py_logic( build_path, outfile_path, build_file_md5 )
        
        # import-zip支持 执行压缩，缓存文件 md5
        if _import_zip=='1':
            tool.out_green("压缩 import 目录")
            tool.zip_import_md5_for_path(build_path, True, import_md5_json)
        
        # 更新地址 拼接
        # http://xxx.com/hotupdate/skinX/1.1.10/gameId_0/
        remote_game_assets = _remote_assets + _update_skin_num + "/" + version + "/" + search_path +"/"
        
        # node.js 生成版本库
        node_js_param = 'node version_generator.js -v %s -u %s -s %s -d %s'%(version, remote_game_assets, build_path, build_path)
        tool.out_green("生成版本:=>" + node_js_param)
        os.system(node_js_param)
        
        # import-zip支持 替换缓存 zip-md5
        if _import_zip=='1':
            tool.out_green("替换 import_zip_md5")
            tool.cache_md5_replace( start_path.generator_project, build_path, import_md5_json )

        # project_mainfest路径
        build_project_manifest = build_path + "/" + start_path.generator_project
        build_version_manifest = build_path + "/" + start_path.generator_version
        
        packageUrl = _remote_assets + _update_skin_num + '/' + version + '/' + start_path.get_search_path(0) + '/'
        remoteManifestUrl = packageUrl + start_path.get_remote_project_manifest(0)
        remoteVersionUrl = packageUrl + start_path.get_remote_version_manifest(0)

        # 更新 project.manifest url
        project_json = tool.read_file_json(build_project_manifest)
        project_json['packageUrl'] = packageUrl
        project_json['remoteManifestUrl'] = remoteManifestUrl
        project_json['remoteVersionUrl'] = remoteVersionUrl
        project_json['gameId'] = gameId
        tool.write_file_json( build_project_manifest, project_json, _is_debug=='1' )

        # 更新 version.manifest url
        version_json = tool.read_file_json(build_version_manifest)
        version_json['packageUrl'] = packageUrl
        version_json['remoteManifestUrl'] = remoteManifestUrl
        version_json['remoteVersionUrl'] = remoteVersionUrl
        version_json['gameId'] = gameId
        tool.write_file_json( build_version_manifest, version_json, _is_debug=='1' )

        # 搜索路径 工程文件
        raw_asset_project = start_path.get_res_manifest_full_path(gameId)
        raw_asset_version = start_path.get_res_version_full_path(gameId)
        
        # 搜索真实文件
        raw_project_manifest_file = searchFilePath(analy_content, build_path + "/" + start_path.root_res_raw, raw_asset_project)
        raw_version_manifest_file = searchFilePath(analy_content, build_path + "/" + start_path.root_res_raw, raw_asset_version)
        
        if raw_project_manifest_file==0:
            tool.out_error('未找到' + raw_asset_project + '映射文件')
            sys.exit(0)

        # 更新路径
        tool.out_green("更新版本库: %s => %s"%(build_project_manifest, raw_project_manifest_file))
        tool.out_green("更新版本库: %s => %s"%(build_version_manifest, raw_version_manifest_file))
        shutil.copy(build_project_manifest, raw_project_manifest_file)
        shutil.copy(build_version_manifest, raw_version_manifest_file)

        # 远程版本整理 
        # skinx + version
        path_dst = outfile_path + "/%s/%s"%(_update_skin_num, version)
        remote_path = path_dst
        remote_search_path = path_dst + "/" + search_path

        # 清理远程版本
        tool.out_green("清理版本:" + remote_search_path )
        if os.path.exists(remote_search_path):tool.system_rmtree(remote_search_path)
        tool.mkdir(remote_search_path)

        # 生成远程版本
        tp_res_path = build_path + start_path.root_res
        tp_src_path = build_path + start_path.root_src
        tp_dst_res_path = remote_search_path + start_path.root_res
        tp_dst_src_path = remote_search_path + start_path.root_src

        tool.out_green("生成远程:%s => src:%s"%(tp_res_path, tp_dst_res_path))
        tool.out_green("生成远程:%s => src:%s"%(tp_src_path, tp_dst_src_path))
        shutil.copytree(tp_res_path, tp_dst_res_path)
        shutil.copytree(tp_src_path, tp_dst_src_path)

        # 远程版本号
        remote_dir = remote_search_path + '/' + start_path.get_version_path(gameId)
        tool.mkdir(remote_dir)
        remote_maifest_path = remote_search_path + '/' + start_path.get_remote_project_manifest(gameId)
        remote_version_path = remote_search_path + '/' + start_path.get_remote_version_manifest(gameId)
        shutil.copy(build_project_manifest, remote_maifest_path )
        shutil.copy(build_version_manifest, remote_version_path )

        # 更新assets版本库
        shutil.copy(build_project_manifest, raw_project_manifest_file )
        shutil.copy(build_version_manifest, raw_version_manifest_file )
    
        # 开启 import-zip 的情况下打包，恢复import目录 
        if is_build and _import_zip=='1':
            tool.out_green('恢复打包import')
            tool.zip_import_for_restore(build_path)
        tool.out_blue('简体大厅处理完成')

    # 生成游戏版本
    if( inputid!='0' ):
        tool.out_green("生成游戏版本...")

        # 当前资源目录
        start_path.resetResRoot(build_path)
        tm_raw_path = build_path + start_path.root_res
        tp_src_path = build_path + start_path.root_src

        # 合并删除路径，统一删除
        short_list = tool.get_game_list_2020( _ccc_proj + start_path.root_game_path )
        
        # 生成游戏版本
        for kindid in short_list:
            tempKindid = kindid
            if( inputid!='1' and inputid!='2' ):
                tempKindid=inputid
            
            # 清理目录
            tool.out_green("清理目录:\n%s,\n%s"%(tm_raw_path, tp_src_path))
            if os.path.exists(tm_raw_path):tool.system_rmtree(tm_raw_path)
            if os.path.exists(tp_src_path):tool.system_rmtree(tp_src_path)
            tool.mkdir(tm_raw_path)
            tool.mkdir(tp_src_path)

            tp_array = tempKindid.split('_')
            try:
                catch_num = int(tp_array[0])
                tool.out_green('catch_num:' + str(catch_num))
            except:
                tool.out_error('游戏目录格式错误，请检查格式：11_xx')
                sys.exit(1)

            gameId = int(tp_array[0])

            # 游戏资源路径
            texture="texture/Game/%s/"%(tempKindid)
            resources="resources/Game/%s/"%(tempKindid)

            # 分析并拷贝游戏资源
            tool.out_green("分析资源:%s => %s"%(bake_path, build_path))
            file_analy.start(bake_path, build_path, texture, resources)

            # 启用资源加密
            if _pkg_res_type=='entry':
                tool.out_cmd("加密资源=" + tm_raw_path )
                file_entry.start( tm_raw_path, '1' )
            
            # 启用 etc2-gzip pkm 转换
            if _pkg_res_type=='etc2_py' and IsWds:
                tool.out_cmd("etc2-gzip=" + tm_raw_path)
                etc2.do_etc2_py_logic( build_path, outfile_path, build_file_md5 )

            packageUrl = _remote_assets + _update_skin_num + "/" + version + "/" + start_path.get_search_path(tempKindid) + "/"

            node_js_param = 'node version_generator.js -v %s -u %s -s %s -d %s'%(version, packageUrl, build_path, build_path)
            tool.out_green("生成版本:" + node_js_param)
            os.system(node_js_param)
            
            build_project_manifest = build_path + "/" + start_path.generator_project
            build_version_manifest = build_path + "/" + start_path.generator_version
            
            # set-search-path
            project_json = tool.read_file_json(build_project_manifest)
            project_json['packageUrl'] = packageUrl
            project_json['remoteManifestUrl'] = packageUrl + start_path.get_remote_project_manifest(tempKindid)
            project_json['remoteVersionUrl'] = packageUrl + start_path.get_remote_version_manifest(tempKindid)
            project_json['gameId'] = gameId
            tool.write_file_json(build_project_manifest, project_json, _is_debug=='1')

            # set-search-path
            project_json = tool.read_file_json(build_version_manifest)
            project_json['packageUrl'] = packageUrl
            project_json['remoteManifestUrl'] = packageUrl + start_path.get_remote_project_manifest(tempKindid)
            project_json['remoteVersionUrl'] = packageUrl + start_path.get_remote_version_manifest(tempKindid)
            project_json['gameId'] = gameId
            tool.write_file_json(build_version_manifest, project_json, _is_debug=='1')

            if tempKindid=='':
                tool.out_red('error:tempKindid=')
                sys.exit(1)

            # 远程版本整理 
            # skinx + version
            search_path = start_path.get_search_path(gameId)
            path_dst = outfile_path + "/%s/%s"%(_update_skin_num, version)
            remote_search = path_dst + "/" + search_path

            # 生成远程版本库
            tool.out_green("清理版本:" + remote_search )
            if os.path.exists(remote_search):tool.system_rmtree(remote_search)
            tool.out_green("生成版本:%s=>%s"%(build_path, remote_search))
            tool.mkdir(remote_search)

            tp_res_path = build_path + start_path.root_res
            tp_src_path = build_path + start_path.root_src
            tp_dst_res_path = remote_search + start_path.root_res
            tp_dst_src_path = remote_search + start_path.root_src

            # 版本目录
            tool.out_green("生成远程:%s => src:%s"%(tp_res_path, tp_dst_res_path))
            tool.out_green("生成远程:%s => src:%s"%(tp_src_path, tp_dst_src_path))
            shutil.copytree(tp_res_path, tp_dst_res_path)
            shutil.copytree(tp_src_path, tp_dst_src_path)

            # 拷贝远程版本号
            remote_dir = remote_search + '/' + start_path.get_version_path(gameId)
            tool.mkdir(remote_dir)
            remote_maifest_path = remote_search + '/' + start_path.get_remote_project_manifest(gameId)
            remote_version_path = remote_search + '/' + start_path.get_remote_version_manifest(gameId)
            shutil.copy(build_project_manifest, remote_maifest_path)
            shutil.copy(build_version_manifest, remote_version_path)

            # 只生成单个游戏资源版本
            if( inputid!='1' and inputid!='2' ):
                break
    
    # 远程版本-备份mtime-json
    if is_build==False:
        shutil.copy(build_path + '/' + start_path.gen_uuid_json, path_dst)

        # 备份MD5json
        if _import_zip=='1':
            shutil.copy(build_path + '/' + import_md5_json, path_dst)
  
    tool.out_yellow("版本资源完成")
    
    return True
# ========================================python main
if __name__ == '__main__':
    print('import version_entry_start.py')
    