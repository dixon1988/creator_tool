g_server_accounts = ""
g_server_password = ""
g_config_id = ""
g_task_add = ""
g_task_first = ""

g_is_svn_update = 0
g_is_ftp_up = 0
g_is_oss_up = 0 
g_is_share_up = 0

g_sever_batch= ""
g_hot_type = ''

def getBufData(obj):
    cmd_buf = {}
    for name in dir(obj):
        if name.find('g_')==0:
            value = getattr(obj, name)
            cmd_buf[name]=value
    return cmd_buf;