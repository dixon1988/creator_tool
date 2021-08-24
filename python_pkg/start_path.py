#!/usr/bin/env python
#coding:utf8
# 项目配置相关

# 工程变量
import os

native_log_path = "C:/Users/Administrator/.CocosCreator/logs/native.log"
generator_project = 'project.manifest'
generator_version = 'version.manifest'
gen_uuid_json = 'uuid-to-mtime.json'

# res路径定义 
root_res0 = '/res'
root_res1 = '/assets'
root_res = root_res0

root_src = '/src'

root_res_raw0 = '/res/raw-assets'
root_res_raw1 = '/assets/resources/native'
root_res_raw = root_res_raw0

# import路径
root_import0 = 'res/import/'
root_import1 = 'assets/resources/import'
root_import = root_import0
root_import_bake = 'bake_import'

version_path = "version_{gameId}"
search_path = "search_{gameId}"

project_manifest = 'project.manifest'
version_manifest = 'version.manifest'

channel_config = "resources/LaunchConfig/baseApp.json"

pkg_type_ios = 'ios'
pkg_type_android = 'android'
pkg_type_web = 'web'
pkg_type_hotUpdate = 'hotUpdate'
pkg_type_server = 'server'

# 子游戏根目录
root_game_path = "/assets/resources/Game"

# 热更新路径，会增加搜索路径
def get_version_path(gameId=0):
    return version_path.replace("{gameId}", str(gameId));

def get_search_path(gameId=0):
    return search_path.replace("{gameId}", str(gameId));

# 获取res缓存路径
def get_resources_version_path(gameId=0):
    return get_version_path(gameId) + '/'

# 获取远程版本文件
def get_remote_project_manifest(gameId):
    return get_version_path(gameId) + '/' + project_manifest

def get_remote_version_manifest(gameId):
    return get_version_path(gameId) + '/' + version_manifest

# 获取 project.manifest 在 res 下的完整路径
def get_res_manifest_full_path(gameId):
    return get_resources_version_path(gameId) + project_manifest

# 获取 versiong.manifest 在 res 下的完整路径
def get_res_version_full_path(gameId):
    return get_resources_version_path(gameId) + version_manifest

# 获取主渠道
def getMainChannelId(channel_id):
    c_id = str(channel_id)
    return c_id[0:6]

# 重置资源路径
def resetResRoot(build_path):
    global root_res_raw
    global root_res
    global root_import

    if not os.path.exists( build_path + root_res_raw0 ):
        root_res_raw = root_res_raw1
        root_res = root_res1
        root_import = root_import1