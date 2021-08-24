//
//  OCHelp.h
//  GameProject
//
//  Created by Beck on 01/06/117.
//
//
#include <iostream>

#ifndef OCDEFINE_H
#define OCDEFINE_H

//事件标记
//子命令码控制============================================================================
#define YQ_SUB_EVENT                0       //无效子事件

#define YQ_SUB_EVENT_BEGIN          1       //子事件开始
#define YQ_SUB_EVENT_ENDED          2       //子事件结束
#define YQ_SUB_EVENT_CANCEL         3       //子事件退出

//微信登陆
#define YQ_MDM_WXLOGON_BEGIN    	100     //微信登陆
#define YQ_MDM_STOREPAY_STORE       201     //store支付
#define YQ_MDM_WXSHARE_BEGIN    	300     //微信分享
#define YQ_MDM_MACHINE_BEGIN    	400     //设备码获取
#define YQ_MDM_VOICE_BEGIN          500     //录音事件


//微信登陆结果
#define YQ_SUB_WXLOGON_SUCCEED      100     //登陆成功
#define YQ_SUB_WXLOGON_FAILURE      101     //登陆失败
#define YQ_SUB_WXLOGON_TOKEN        102     //token成功
#define YQ_SUB_WXUNINSTALL          103     //安装微信客户端

//微信分享结果
//微信分享结果
#define YQ_SUB_WXSHARE_SUCCEED      300     //分享成功
#define YQ_SUB_WXSHARE_FAILURE      301     //分享失败
#define YQ_SUB_WXSHARE_BACK         302     //分享取消

//语音上传结果
#define YQ_SUB_POSTRECORD_START     309     //语音上传开始
#define YQ_SUB_POSTRECORDER_SUCCEED 310     //语音上传成功
#define YQ_SUB_POSTRECORDER_FAILURE 311     //语音上传失败

//语音下载结果
#define YQ_SUB_DOWNRECORDER_SUCCEED 320     //语音下载成功
#define YQ_SUB_DOWNRECORDER_FAILURE 321     //语音下载失败

//ios支付结果
#define YQ_SUB_IOSPAY_BEGIN         398     //store支付开始
#define YQ_SUB_IOSPAY_WAITCANCEL    399     //关闭等待
#define YQ_SUB_IOSPAY_SUCCEED       400     //ios支付成功
#define YQ_SUB_IOSPAY_NOSUCCEED     401     //ios支付成功 但验证失败，请联系客服
#define YQ_SUB_IOSPAY_FAILURE       402     //ios支付失败

//设备码获取结果
#define YQ_SUB_MACHINE_SUCCEED      500     //设备码获取成功
#define YQ_SUB_MACHINE_FAILURE      501     //设备码获取失败

//游戏包模式
#define YQ_SUB_GAME_MODEL_TEST      600     //开发版
#define YQ_SUB_GAME_MODEL_PUBILC    601     //发布版
#define YQ_SUB_GAME_MODEL_DEBUG     602     //调试模式

//网络状态
#define YQ_SUB_NETSTATE_WIFI		605		//wifi
#define YQ_SUB_NETSTATE_MOBILE      606		//手机网络
#define YQ_SUB_NETSTATE_NONE		607		//无网络

//音频类型
#define YQ_AUDIO_TYPE_MUSIC         610     //音乐
#define YQ_AUDIO_TYPE_SOUND         611     //音效

//录音状态
//录音状态
#define YQ_SUB_VOICE_START          700     //录音开始
#define YQ_SUB_VOICE_CANCEL     	710     //录音取消
#define YQ_SUB_VOICE_ENDED      	720     //录音结束
#define YQ_SUB_VOICE_PLAYSTART      721     //录音播放
#define YQ_SUB_VOICE_PALYENDED      722     //播放结束

//录音使用状态
#define YQ_SUB_VOICESTATUS_NONE     725		//空闲状态
#define YQ_SUB_VOICESTATUS_RECORD   726		//录音状态
#define YQ_SUB_VOICESTATUS_PLAYED   727		//播放状态

//录音上传状态
#define YQ_SUB_VOICE_UPLOAD     	730     //录音上传
#define YQ_SUB_VOICE_UL_SUCCEED     740		//上传成功
#define YQ_SUB_VOICE_UL_FAILURE 	750     //上传失败

//录音下载状态
#define YQ_SUB_VOICE_DOWNLOAD       760		//录音下载
#define YQ_SUB_VOICE_DL_SUCCEED     770		//下载成功
#define YQ_SUB_VOIDE_DL_FAILURE     780		//下载失败

//网络产生变化
#define YQ_SUB_NET_CHANGE           900     //网络产生变化

#define YQ_CallStateDialing         901		//播号
#define YQ_CallStateIncoming		902		//来电
#define YQ_CallStateConnected       903		//通话中
#define YQ_CallStateDisconnected    904		//断开

#define YQ_SUB_USER_POS             1000    //用户定位坐标

#define YQ_SUB_OPENSELFAPP          2000    //打开自己app

#define YQ_SUB_SAVE_PHOTO           2100    //保存相册图片
#define YQ_SUB_SAVE_PHOTO_DONE      2101    //保存完成

#define YQ_SUB_UPLOAD_FILE          2110    //图片上传
#define YQ_SUB_UPLOAD_FILE_DONE     2111    //图片上传完成
#define YQ_SUB_UPLOAD_FILE_FAILURE  2112    //图片上传失败

#define YQ_SUB_CHANGESCREEN_NOTIFY  2200    //通知改变

#define YQ_SUB_HOMEDOWN             2400    //手机竖屏
#define YQ_SUB_HOMESIDE             2401    //手机横屏

#define YQ_OPENINSTALL              2500    //openinstall
#define YQ_SXLOADCALLBACK           2510    //视讯加载回调

//加载成功3003//加载错误3004
#define YQ_SUB_SX_LOAD_SUCCEED      3003     //加载成功
#define YQ_SUB_SX_LOAD_FAILURE      3004     //加载失败

//支付类型
#define PAYTYPE_STORE               4       //store支付

//事件回调
extern bool jsb_callback(int result);
extern bool jsb_callback(int result, const char* szFileName);

//不使用时 关闭宏，免得参与编译报错
//是否使用游戏盾
#define USING_YUNDUN

//是否使用闪付
#define USING_SHANFU

//是否编译微信相关代码
#define USING_WX

//是否开启通讯录权限
#define USING_TONGXUNLU

//是否编译openinstall
//#define USING_OPENINSTALL

#endif /* OCHelp_h */
