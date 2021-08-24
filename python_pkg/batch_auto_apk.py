#!/usr/bin/env python
#coding:utf8
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import os,sys,codecs,json,re,shutil
import hashlib
import time

import csv_info_script
import tool
import start_path

g_run_system = True

g_apkfile_path = ''
g_skin_path = ''

g_batch_conf_path = ''
g_project_root_name = ''
g_batch_conf_apk = ''
g_batch_out_root = ''

g_apk_path = ''
g_apk_mtime_json = ''

g_channel_csv = ''
g_channel_cs_csv = ''
g_channel_info = ''

g_keystore_name = ''
g_keystore_alias = ''
g_keystore_password = ''

g_pkg_last_filename = ''
g_pkg_last_index = ''
g_pkg_version = ''

#分析资源路径地址
def Get_uuid_for_file ( path_File ):
    listFile =  os.path.splitext( path_File )
    res_format = listFile[1]

    #读取uuid-to-mtime.json文件内容
    fp = codecs.open(g_apk_mtime_json, 'r+', 'utf-8')
    load_dict=fp.read()
    fp.close()
    analy_content = json.loads(load_dict)
    
    file_uuid = ''
    #循环解析json
    for key in analy_content:
        tempJsondata = analy_content[key]
        relativePath = tempJsondata['relativePath']
        relativePath = tool.path_replace(relativePath)

        if relativePath == path_File :
            file_uuid = key
            break

    if file_uuid == '' :
        print( 'analy invalid, file:', path_File )
        sys.exit(1)

    #uuid 前两位为文件夹名称
    path_dir = file_uuid[ 0:2 ]
    path_uuid = g_apkfile_path + '/assets/res/raw-assets/%s/%s%s'%( path_dir, file_uuid, res_format )
    if not os.path.exists( path_uuid ):
        path_uuid = g_apkfile_path + '/assets/res/import/%s/%s%s'%( path_dir, file_uuid, res_format )
    
    print("analy sucess ---  file path :", path_File )
    print("analy sucess ---  uuid path :", path_uuid )
    return path_uuid

#更改应用名
def change_apk_name(apk_name, channel_id, info_list):

    apkfile_res = g_apkfile_path + '/res'
    apkfile_xml = apkfile_res + '/values/strings.xml'
    fp = codecs.open( apkfile_xml, 'r+', 'utf-8')
    cache_file = list()

    read_num=0
    while True:
        lines = fp.readline()
        if not lines:
            break

        read_num += 1
        if lines == "":
            continue
        
        #第3行为包名所在行所以要加以处理，重新定义名字
        if lines.find('app_name') != -1:
            lines = "    <string name=\"app_name\">%s</string>\r\n"%(apk_name)
            
        cache_file.append(lines)
        #print(lines)

    fp.close()

    #重新写入新文件内容
    fw = codecs.open(apkfile_xml, 'w+', 'utf-8')
    fw.writelines(cache_file)
    fw.close()

    #重新写入渠道号和包名======================================================
    path_channel = Get_uuid_for_file( start_path.channel_config ) 
    fwjd = codecs.open(path_channel,'r+','utf-8')
    load_dict=fwjd.read()
    fwjd.close()

    str_channelId = str(channel_id)
    appName = str( apk_name )
 
    #修改字段
    channel_json = json.loads( load_dict )
    channel_json['channel_id'] = str_channelId
    channel_json['appName'] = appName

    weixin_info = csv_info_script.get_info_idx_info( info_list, channel_id, 'weixin')
    if len(weixin_info)>0:
        channel_json['wxappid'] = weixin_info[1]
        channel_json['wxappsecret'] = weixin_info[2]

    #写入文件
    json_ChannelData = json.dumps( channel_json )
    print('wirtestr:', json_ChannelData)
    wfp = codecs.open( path_channel, 'w+','utf-8' )
    wfp.writelines( json_ChannelData )
    wfp.close()

#制作打包资源
def make_package_res( channel_id ):

    str_channel_id = str(channel_id)
    mainChannel_id = str_channel_id[0:3]

	#拷贝文件夹资源
    Dst_Src = g_apkfile_path + '/assets'

    Res_Src = g_skin_path + '/' + str_channel_id
    skin_src = Res_Src + '/skin'

	# 判断有没单独渠道包资源
    if not os.path.exists(Res_Src):
        Res_Src = g_skin_path + '/' + mainChannel_id
        skin_src = Res_Src + '/skin'

    # 如果没有配置icon皮肤，则直接跳过并输出警告
    if not os.path.exists(Res_Src):
        print('====================================================================================================')
        print('warning: not found ' + str_channel_id + '-skin or ' + mainChannel_id + '-skin,skip icon and skin replace')
        print('====================================================================================================')
        return

    # 是否有换肤文件
    for maindir, subdir, file_name_list in os.walk(skin_src):
        for file_name in file_name_list:
            old_file = os.path.join( maindir, file_name )
            #获取对应的uuid路径
            tempPath = old_file.replace( Res_Src+'\\', '')
            path_uuid = Get_uuid_for_file( tempPath )
            #拷贝并且重命名
            shutil.copyfile(old_file, path_uuid)
            print('copy sucess -- file :', old_file )
 
	   
    #拷贝游戏icon
    app_icon_path = Res_Src + '/icon'
    apkfile_res = g_apkfile_path + '/res'

    #48*48
    src_icon_48 = app_icon_path + '/icon_48.png'
    dst_icon_mdpi = apkfile_res + '/mipmap-mdpi/game_icon.png'

    print('copyfile:%s => %s'%(src_icon_48,dst_icon_mdpi))
    shutil.copy(src_icon_48, dst_icon_mdpi )

	#72*72
    src_icon_72 = app_icon_path + '/icon_72.png'
    dst_icon_hdpi = apkfile_res + '/mipmap-hdpi/game_icon.png'

    print('copyfile:%s => %s'%(src_icon_72, dst_icon_hdpi))
    shutil.copy(src_icon_72, dst_icon_hdpi )
	
    #96*96
    src_icon_96 = app_icon_path + '/icon_96.png'
    dst_icon_xhdpi = apkfile_res + '/mipmap-xhdpi/game_icon.png'

    print('copyfile:%s => %s'%(src_icon_96, dst_icon_xhdpi))
    shutil.copy(src_icon_96, dst_icon_xhdpi )

    #144*144
    src_icon_144 = app_icon_path + '/icon_144.png'
    dst_icon_xxhdpi = apkfile_res + '/mipmap-xxhdpi/game_icon.png'

    print('copyfile:%s => %s'%(src_icon_144, dst_icon_xxhdpi))
    shutil.copy(src_icon_144, dst_icon_xxhdpi )

    #拷贝启动图
    src_splash = app_icon_path + '/splash.jpg'

    dst_splash_hdpi = apkfile_res + '/mipmap-mdpi/splash.jpg'
    print('copyfile:%s => %s'%(src_splash, dst_splash_hdpi))
    shutil.copy(src_splash, dst_splash_hdpi )

    dst_splash_mdpi = apkfile_res + '/mipmap-hdpi/splash.jpg'
    print('copyfile:%s => %s'%(src_splash, dst_splash_mdpi))
    shutil.copy(src_splash, dst_splash_mdpi )

    dst_splash_xhdpi = apkfile_res + '/mipmap-xhdpi/splash.jpg'
    print('copyfile:%s => %s'%(src_splash, dst_splash_xhdpi))
    shutil.copy(src_splash, dst_splash_xhdpi )

    dst_splash_xxhdpi = apkfile_res + '/mipmap-xxhdpi/splash.jpg'
    print('copyfile:%s => %s'%(src_splash, dst_splash_xxhdpi))
    shutil.copy(src_splash, dst_splash_xxhdpi )

#package_org 解压后 .\apkfile 文件中的包名
#package_name 新apk的包名
def modify_package( package_name, channel_id, info_list ):

    # # 扩展-jiuliao
    # jiuliao = csv_info_script.get_info_idx_info( info_list, channel_id, 'jiuliao')
    # len_jiuliao = len(jiuliao)

    # 扩展-openinstall
    openinstall = csv_info_script.get_info_idx_info( info_list, channel_id, 'openinstall')
    len_openinstall = len(openinstall)
    
    # 扩展-weixin
    weixin = csv_info_script.get_info_idx_info( info_list, channel_id, 'weixin')
    len_weixin = len(weixin)

    file_path = g_apkfile_path + '/AndroidManifest.xml'

    # #获取原包名
    tree = ET.parse(r'%s'%(file_path))
    root = tree.getroot()
    package_org = root.attrib["package"]
    
    if (package_org == package_name):
        print( 'not modify package name')
        return

    print( 'package_org:', package_org, 'package_name', package_name )
    path_smali = package_org.replace('.', '/')
    root_path = g_apkfile_path + '/smali/%s'%(path_smali)
    print('root_path:', root_path)

    #修改./apkfile/AndroidManifest.xml 包名
    with open(file_path, 'r') as f:
        file_content = f.read()
        new_file = file_content.replace(package_org, package_name)
        
        #替换打开解决相机崩溃加上的 apk包名属性
        old_fileprovider = ('%s.fileprovider'%( package_org ))
        new_fileprovider = ( '%s.fileprovider'%( package_name ) )
        new_file = new_file.replace(old_fileprovider, new_fileprovider)
        
    with open(file_path, 'w') as f:
        f.write(new_file)

    #修改 ./apkfile/AndroidManifest.xml 久聊支付相关信息
    fp_xml = codecs.open( file_path, 'r+', 'utf-8')
    xml_file = list()

    read_num=0
    while True:
        lines = fp_xml.readline()
        if not lines:
            break

        read_num += 1
        if lines == "":
            continue
        
        # 久聊扩展
        if len_jiuliao!=0:
            #替换数据
            if lines.find('baiduappid') != -1:
                lines = '        <meta-data android:name="baiduappid" android:value="%s"/>\r\n'%( jiuliao[1] )
            
            if lines.find('baiduappsecrety') != -1:
                lines = '        <meta-data android:name="baiduappsecrety" android:value="%s"/>\r\n'%( jiuliao[2] )

        # openinstall扩展
        if len_openinstall!=0:
            if lines.find('com.openinstall.APP_KEY') != -1:
                lines = '        <meta-data android:name="com.openinstall.APP_KEY" android:value="%s"/>\r\n'%( openinstall[1] )
            
            if lines.find('android:scheme=') != -1:
                lines = '                <data android:scheme="%s"/>\r\n'%( openinstall[1] )

        xml_file.append(lines)
       
    fp_xml.close()
    
    #重新写入新文件内容
    fw = codecs.open( file_path,'w+','utf-8')
    fw.writelines( xml_file )
    fw.close()

    #修改 ./apkfile/smali 文件下 包名
    list_dirs = os.walk(root_path)
    other_package = package_name.replace('.', '/').encode()
    other_package_org = package_org.replace('.', '/').encode()
    print( 'other_package:', other_package, 'other_package_org:', other_package_org)
   
    for root, dirs, files in list_dirs:
        
        for file_name in files:
  
            path = root + '/' + file_name
 
            modify_file = ''
            with open(path, 'rb') as f:
                file_s = f.read()
                modify_file = file_s.replace(other_package_org, other_package)
            
            with open(path, 'wb') as f:
                f.write(modify_file)

   
    #修改包名对应的文件夹名称
    oldList = package_org.split('.')
    newList = package_name.split('.')
    
    while len(oldList)  > 0 :
        strIndex = '/'
        path_src = g_apk_path + '/apkfile/smali/%s'%( strIndex.join( oldList ) )

        #弹出list最后一个元素
        old_last = oldList.pop()
        new_last = newList.pop()

        if (old_last == new_last):
            continue
            
        path_dst = path_src.replace( old_last, new_last )
        print( 'path_src:', path_src, 'path_dst:', path_dst)

        if os.path.exists(path_src)==False:
            continue
        os.rename(path_src, path_dst)

#修改apk的code值和版本号
def modify_Apkcode( ):
    global g_pkg_version

    #获取内置资源manifest文件的版本号
    file_version = start_path.getResVersionFullPath(0)
    uuid_version = Get_uuid_for_file( file_version )

    fwjd = codecs.open(uuid_version,'r+','utf-8')
    load_dict=fwjd.read()
    fwjd.close()
    
    version_json = json.loads( load_dict )
    str_version = version_json["version"]

    str_version_code = str(int(time.time()))
    print( 'version_code:', str_version_code)
    
    g_pkg_version = str_version

    #修改apktool.yml文件信息
    # newList = package_name.split('.')
    # strIndex = '\\'

    # file_config = '.\\apkfile\\smali\\%s\\BuildConfig.smali'%( strIndex.join( newList ) )
    # print("file config:" + file_config )

    file_apktool_yml = g_apkfile_path + '/apktool.yml'
    yml_fw = codecs.open(file_apktool_yml,'r+','utf-8')
    xml_file = list()

    read_num=0
    while True:
        lines = yml_fw.readline()
        if not lines:
            break

        read_num += 1
        if lines == "":
            continue
        
        #替换数据
        if lines.find('versionCode') != -1:
            lines = "  versionCode: '%s'\n"%( str_version_code )
        
        if lines.find('versionName') != -1:
            lines = "  versionName: '%s'\n"%( str_version )

        xml_file.append(lines)
    
    yml_fw.close()
    
    #重新写入新文件内容
    fw = codecs.open( file_apktool_yml,'w+','utf-8')
    fw.writelines( xml_file )
    fw.close()

#打包&签名
def package_signature(channel_info):

    #创建放apk的文件夹
    filename = channel_info[4]
    package_name = channel_info[3]

    listPath = package_name.split('.')
    folder = g_batch_out_root + '/' + g_pkg_version + '_' + '_'.join( listPath )

     #判断是否存在文件夹如果不存在则创建为文件夹
    if os.path.exists(folder)==False:
        os.makedirs(folder)

    str_apk_filename = filename
    num_count = filename.count('#')
    if num_count==1:
        tp_list = filename.split('#')
        str_apk_filename = tp_list[0] + str(g_pkg_last_index)

    if num_count==2:
        tp_list = filename.split('##')
        str_apk_filename = tp_list[0] + str(int(g_pkg_last_index/10)) + str(int(g_pkg_last_index%10))

    if num_count==3:
        tp_list = filename.split('###')
        str_apk_filename = tp_list[0] + str(int(g_pkg_last_index/100)) + str(int(g_pkg_last_index/10%10)) + str(int(g_pkg_last_index%10))

    # 目标包存放
    dst_apk_path = folder + '/' + str_apk_filename + '.apk'

	# 重新打包
    new_unsigned_apk_path = g_batch_out_root+'/unsigned.apk'

    apktool_param = "apktool b %s -o %s"%(g_apkfile_path, new_unsigned_apk_path)
    print('apktool:', apktool_param)
    os.system(apktool_param)

    #签名文件路径
    keystore = g_keystore_name
    password = g_keystore_password
    alias = g_keystore_alias

    #签名
    new_signed_apk_path = "jarsigner -verbose -digestalg SHA1 -sigalg MD5withRSA -keystore %s -storepass %s -keypass %s -signedjar %s %s %s"%(keystore, password, password, dst_apk_path, new_unsigned_apk_path, alias)
    print('signed:', new_signed_apk_path)
    os.system(new_signed_apk_path)
    os.remove(new_unsigned_apk_path)
    
    shutil.copy(g_apk_mtime_json, g_batch_out_root)
    
    print("打包完成:", dst_apk_path)

#根据渠道号打包
def create_package_bychannel(channel_info, info_list):
    print('渠道号: ', channel_info[1], '应用名：', channel_info[2], '包名：', channel_info[3], "输出文件名:", channel_info[4], "扩展：", channel_info[5] )

    channel_id = channel_info[1]
    apk_name = channel_info[2]
    package_name = channel_info[3]

    make_package_res(int(channel_id))

    change_apk_name( apk_name, channel_id, info_list )

    modify_package( package_name, channel_id, info_list )
    
    modify_Apkcode()
    
    package_signature( channel_info )
    
# 开始批量出包
def start():
    global g_apkfile_path
    global g_skin_path
    global g_pkg_last_filename
    global g_pkg_last_index
    
    #先解原始包
    g_apkfile_path = g_batch_conf_path + '/apkfile'
    g_skin_path = g_batch_conf_path + '/appskin'
    tool.rmtree(0, g_apkfile_path)

    apktool_param = 'apktool d '+ g_batch_conf_apk + ' -o ' + g_apkfile_path
    print("解包 apktool:", apktool_param)
    os.system(apktool_param)

    # 获取配置
    channel_list = ''
    info_list = ''

    if batch_server=='zs':
        channel_list = csv_info_script.load_channel_list(g_channel_csv)
        info_list = csv_info_script.load_channel_list(g_channel_info)

    elif batch_server=='cs':
        channel_list = csv_info_script.load_channel_list(g_channel_cs_csv)
        info_list = csv_info_script.load_channel_list(g_channel_info)
    else:
        print('未实现类型，暂时忽略')
        return

    # 按渠道打包
    i = 0
    for channel_info in channel_list:
        if len(channel_info)<5 or channel_info[0]=='0':
            i += 1
            continue
        
        tp_file_name = channel_info[4]
        if tp_file_name.count('#')>0:
            if tp_file_name!=g_pkg_last_filename:
                g_pkg_last_filename = tp_file_name
                g_pkg_last_index = 1
            else:
                g_pkg_last_index += 1

        create_package_bychannel(channel_info, info_list)
        i+=1

    if os.path.exists( g_apkfile_path ):
        tool.rmtree(0, g_apkfile_path)

if __name__ == '__main__':
    
    print('batch_auto_apk')
	
