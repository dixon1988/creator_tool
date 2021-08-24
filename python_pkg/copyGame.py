import os,sys,json,uuid
import shutil
import tool

self_path = os.path.split(os.path.realpath(__file__))[0]
self_path = tool.path_replace(self_path)
self_out_path = os.path.abspath(os.path.join(self_path, ".."))
self_out_path = tool.path_replace(self_out_path)

# 路径脚本分析
def read_script_info( script_root, library_root, logOut):
    if logOut:
        print('')
        print('获取信息：', script_root)

    fileinfo = {
        'uuid':{}, 
        'type':{},
        'file':[],
        'newtype':{},
        'newname':{},
        'rp_uuid':{}
        }
 
    uuid_dic = fileinfo['uuid']
    type_dic = fileinfo['type']
    file_list = fileinfo['file']

    # 脚本关系 名字->uuid 名字->脚本密文
    for maindir, subdir, file_name_list in os.walk(script_root):
        for filename in file_name_list:
            #绝对路径
            apath = os.path.join(maindir, filename)
            tp_file_name = tool.get_file_name(apath)
            tp_file_ext = tool.get_file_ext(apath)

            # 获取ts文件的uuid
            if( tp_file_ext=='.ts' or tp_file_ext=='.js'):
                tp_file_meta = apath + ".meta"
                if( not os.path.exists(tp_file_meta) ):
                    tool.msgbox("运行替换脚本时，请先正常打开一次creator！")
                    return

                # 查找uuid
                ts_meta_json = tool.read_file_json(apath+'.meta')
                tp_uuid = ts_meta_json['uuid']

                uuid_dic[tp_file_name] = tp_uuid
                
                # 获取对应脚本密文
                tp_path = tool.path_replace(library_root)
                import_path = tp_path + "/imports/" + tp_uuid[0:2] + "/" + tp_uuid + '.js'

                if( not os.path.exists(import_path) ):
                    tool.msgbox("运行替换脚本时，请先正常打开一次creator！")
                    return

                tp_fp_content = tool.read_file_lines(import_path)
                tp_fp_line_2 = tp_fp_content[1]
                tp_group = tp_fp_line_2.split('\'')
                tp_type = tp_group[1]

                type_dic[tp_file_name] = tp_type
                file_list.append(tp_file_name)
                if logOut:
                    print( "filename = " + tp_file_name + "\t tp_uuid = " + tp_uuid + "\t  type = " + tp_type )
    
    return fileinfo

# 搜索信息
def search_script(run_root, old_script, new_script, path_lib, logOut=True):
    is_sys_exit = 0
    len0 = len(run_root); len1=len(old_script); len2=len(new_script);len3=len(path_lib)
    if len0==0 or len1==0 or len2==0 or len3==0:
        is_sys_exit=1

    if logOut or is_sys_exit==1:
        print('')
        print('分析生成匹配关系======================')
        print('run_root='+ run_root)
        print('old_script='+ old_script)
        print('new_script='+ new_script)
        print('path_lib='+ path_lib)
        if is_sys_exit==1:
            tool.msgbox("请检查路径输入")
            return

    old_file_info = read_script_info(old_script, path_lib, logOut)
    new_file_info = read_script_info(new_script, path_lib, logOut)

    file_list0 = old_file_info['file']
    file_list1 = new_file_info['file']
    file_type = new_file_info['type']
    newtype = old_file_info['newtype']
    newname = old_file_info['newname']

    if logOut:
        print()
        print("分析匹配关系")
    for i in range(len(file_list0)):
        tp_fname = file_list0[i]
        _pos = tp_fname.find('_')
        fp_tail = tp_fname[_pos+1:len(tp_fname)]

        for j in range(len(file_list1)):
            tp_fname1 = file_list1[j]
            _pos = tp_fname1.find('_')
            fp_tail1 = tp_fname1[_pos+1:len(tp_fname1)]
            if fp_tail==fp_tail1:
                newtype[tp_fname] = file_type[tp_fname1]
                newname[tp_fname] = tp_fname1
                if logOut:
                    print("匹配关系:" + tp_fname + ':' + tp_fname1 )
                break
    if logOut:
        print('分析完成，请仔细核对后再执行一键替换！')

    return old_file_info

# 替换所有匹配信息
def replace_script(run_root, old_script, new_script, path_lib):
    is_sys_exit = 0
    len0 = len(run_root); len1=len(old_script); len2=len(new_script);len3=len(path_lib)
    if len0==0 or len1==0 or len2==0 or len3==0:
        is_sys_exit=1

    if is_sys_exit==1:
        print('')
        print('分析生成匹配关系======================')
        print('run_root='+ run_root)
        print('old_script='+ old_script)
        print('new_script='+ new_script)
        print('path_lib='+ path_lib)
        tool.msgbox("请检查路径输入")
        return

    print('')
    print('执行替换')

    file_info = search_script(run_root, old_script, new_script, path_lib, False)

    file_list = file_info['file']
    old_type = file_info['type']
    new_type = file_info['newtype']
    new_name = file_info['newname']

    # 替换所有 scene 文件 替换所有 prefab 文件
    for maindir, subdir, file_name_list in os.walk(run_root):
        for filename in file_name_list:
            #绝对路径
            apath = os.path.join(maindir, filename)
            tp_file_name = tool.get_file_name(apath)
            tp_file_ext = tool.get_file_ext(apath)

            if tp_file_ext=='.fire' or tp_file_ext=='.prefab':
                fp_content = tool.read_file_string(apath)
                # print('tp_file_name:'+tp_file_name)

                # 所有替换一次
                for key in new_type:
                    tp_name = new_name[key]
                    tp_new = new_type[key]
                    tp_old = old_type[key]
                    if fp_content.find(tp_old)!=-1:
                        fp_content = fp_content.replace(tp_old, tp_new)
                        print( tp_file_name + tp_file_ext +' : replace = ' + key + ' -->> ' + tp_name + ' and key = ' + tp_old + ' -->> ' + tp_new )

                # 重新写入
                tool.write_file_json_indent4(apath, fp_content)
    print('执行替换成功')

# 创建uuid
def get_new_uuid(lib_uuid):
    new_uuid = uuid.uuid1().urn.split(':')[2]
    # print(new_uuid)
    if new_uuid in lib_uuid:
        new_uuid = get_new_uuid(lib_uuid)
    return new_uuid

# 给文件创建新的uuid
def create_new_uuid_path(run_root, new_name, lib_uuid, pathIdx):
    # 拷贝路径资源到 临时目录 temp
    tp_path = ['res', 'script']
    tp_run_root = tool.path_replace(run_root)
    tp_out_path = self_out_path + '/rpTemp/' + tp_path[pathIdx] + "/" + new_name
    tool.rmtree(0, tp_out_path)

    rcd_info = {}
    rcd_info['tp_out_path'] = tp_out_path;
    rcd_info['rp_uuid'] ={}
    rcd_uuid = rcd_info['rp_uuid']

    scene_list = []

    for maindir, subdir, file_list in os.walk(tp_run_root):
        for filename in file_list:
            #绝对路径
            apath = os.path.join(maindir, filename)
            apath = tool.path_replace(apath)

            #不是脚本目录时忽略脚本目录
            tp_ext = tool.get_file_ext(apath)
            if pathIdx==s_res_path:
                if tp_ext=='.ts' or tp_ext=='.js':continue
            
            # 拷贝文件到temp
            tp_dst_root = apath.replace(tp_run_root, tp_out_path)
            bakeup_target_dir = os.path.abspath(os.path.dirname(tp_dst_root))
            bakeup_target_dir = tool.path_replace(bakeup_target_dir)
            tool.mkdir(bakeup_target_dir)
            shutil.copy(apath, tp_dst_root)

            tp_name = tool.get_file_name(apath)

            # 拷贝后重新生成uuid
            if tp_ext=='.meta':
                tp_json = tool.read_file_json(tp_dst_root)
                old_uuid = tp_json['uuid']
                new_uuid = get_new_uuid(lib_uuid)
                tp_json['uuid'] = new_uuid
                rcd_uuid[old_uuid] = new_uuid

                if 'subMetas' in tp_json:
                    subMetas = tp_json['subMetas']
                    if tp_name in subMetas:
                        tp_obj = subMetas[tp_name]
                        obj_old_uuid = tp_obj['uuid']
                        obj_new_uuid = get_new_uuid(lib_uuid)
                        tp_obj['uuid'] = obj_new_uuid
                        tp_obj['rawTextureUuid'] = new_uuid

                        rcd_uuid[obj_old_uuid] = obj_new_uuid

                tool.write_file_json_indent4(tp_dst_root, tp_json)
                print('filename = ' + filename + ' uuid: ' + old_uuid + ' --> ' + new_uuid )

            if tp_ext=='.fire':
                scene_list.append([tp_dst_root, bakeup_target_dir])

    for item in scene_list:
        tp_dst_root = item[0]
        bakeup_target_dir = item[1]
        new_scene_name = bakeup_target_dir + '/' + new_name + '.fire'
        os.rename(tp_dst_root, new_scene_name)
        os.rename(tp_dst_root+'.meta', new_scene_name+'.meta')

    return rcd_info

# 修改脚本内容为新内容前缀
def write_script_replace_with_head(replace_root, new_head):
    tp_new_head = new_head + "_"

    rp_new = {}
    rp_list = []

    for maindir, subdir, file_list in os.walk(replace_root):
        for filename in file_list:
            apath = os.path.join(maindir, filename)
            apath = tool.path_replace(apath)
            tp_ext = tool.get_file_ext(apath)
            tp_name = tool.get_file_name(apath)

            _headpos = tp_name.find('_');
            if _headpos!=-1:

                # 替换文件名
                tp_headname = tp_name[0:_headpos+1]
                tp_new_path = apath.replace(tp_headname, tp_new_head)
                tp_new_name = tool.get_file_name(tp_new_path)

                # 替换文件内容
                print('rename: ' + tp_name + tp_ext + ' --> ' + tp_new_name + tp_ext )
                os.rename(apath, tp_new_path)
                
                if tp_ext=='.ts':
                    rp_new[tp_new_path] = tp_name + tp_ext;
                    rp_list.append(tp_new_name + tp_ext)

    # 打开文件替换内容
    max_len = len(rp_list)
    for tp_key in rp_new:
        tp_new_path = tp_key
        tp_content = tool.read_file_string(tp_new_path)
        tp_count = 0

        for rp_key in rp_new:
            old_file = rp_new[rp_key]
            tp_ext = tool.get_file_ext(rp_key)
            tp_name = tool.get_file_name(old_file)
            tp_new_name = tool.get_file_name(rp_key)

            tp_reCount = len(tp_content.split(tp_name)) - 1
            tp_count = tp_count + tp_reCount
            tp_content = tp_content.replace( tp_name, tp_new_name )

        tool.write_file_content(tp_new_path, tp_content);

        print('edit_file: ' + tp_new_name + tp_ext + ' replace_content: ' + tp_name + ' --> ' + tp_new_name + ' reCount = ' + str(tp_count) )

# 替换所有匹配信息
def replace_res_uuid(root_res, rcd_uuid):
    # 更新所有 scene 文件 替换所有 prefab 文件 资源id 指向
    for maindir, subdir, file_name_list in os.walk(root_res):
        for filename in file_name_list:
            #绝对路径
            apath = os.path.join(maindir, filename)
            tp_file_name = tool.get_file_name(apath)
            tp_file_ext = tool.get_file_ext(apath)

            if tp_file_ext=='.fire' or tp_file_ext=='.prefab':
                fp_content = tool.read_file_string(apath)

                # 所有替换一次
                for old_uuid in rcd_uuid:
                    new_uuid = rcd_uuid[old_uuid]
                    if fp_content.find(old_uuid)!=-1:
                        fp_content = fp_content.replace(old_uuid, new_uuid)
                        print( tp_file_name + tp_file_ext +' : replace :' + old_uuid + ' -->> ' + new_uuid )

                # 重新写入
                tool.write_file_json_indent4(apath, fp_content)
    print('执行替换成功')

#拷贝新游戏
s_res_path = 0
s_script_path = 1
def create_new_path(run_root, old_script, new_name, new_head, path_lib):
    print('')
    print('生成全新游戏======================')
    print('run_root = '+ run_root)
    print('old_script = '+ old_script)
    print('path_lib = '+ path_lib)
    print('new_head = '+ new_head)
    print('new_name = '+ new_name)

    len0 = len(run_root); len1=len(old_script); len2=len(new_name);len3=len(new_head);len4=len(path_lib)
    if len0==0 or len1==0 or len2==0 or len3==0 or len4==0:
        tool.msgbox('复制游戏参数不足，请检查输入')
        return

    lib_uuid = {};

    # 读取项目lib，作为uuid的重置依据
    for maindir, subdir, file_list in os.walk(path_lib):
        for filename in file_list:
            tp_uuid = tool.get_file_name(filename)
            lib_uuid[tp_uuid] = filename
            # print('uuid = ' + filename )

    # 重置资源 uuid
    print('')
    print('重置资源路径: ' + run_root)
    rcd_info_res = create_new_uuid_path(run_root, new_name, lib_uuid, s_res_path) 
    tp_root_res = rcd_info_res['tp_out_path']

    # 重置脚本 uuid
    print('')
    print('重置脚本路径: ' + old_script)
    rcd_info_script = create_new_uuid_path(old_script, new_name, lib_uuid, s_script_path)
    tp_root_script = rcd_info_script['tp_out_path']

    # 替换脚本前缀，以及脚本内容
    print('')
    print('修改脚本前缀和内容: ' + tp_root_script)
    write_script_replace_with_head(tp_root_script, new_head)

    # 重新指向新资源
    rcd_uuid = rcd_info_res['rp_uuid']
    replace_res_uuid(tp_root_res, rcd_uuid)

    # 导入目录
    rp_name_res = tool.get_file_name(run_root)
    rp_name_script = tool.get_file_name(old_script)

    new_root_res = run_root.replace(rp_name_res, new_name)
    new_root_script = old_script.replace(rp_name_script, new_name)

    print('执行拷贝')
    tool.copydir(tp_root_res, new_root_res)
    tool.copydir(tp_root_script, new_root_script)