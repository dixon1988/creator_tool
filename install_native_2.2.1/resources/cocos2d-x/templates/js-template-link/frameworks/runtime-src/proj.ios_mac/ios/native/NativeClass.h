//
//  OCHelp.h
//  GameProject
//
//  Created by Beck on 01/06/117.
//
//
#include <iostream>

#ifndef NativeCalss_h
#define NativeCalss_h

#import <MessageUI/MessageUI.h>
#import <WebKit/WebKit.h>

#import <StoreKit/StoreKit.h>
#import <CoreLocation/CoreLocation.h>

#import "AQRecorderManager.h"
#import "PlayerManager.h"
#import "Reachability.h"

#import "OCDefine.h"
#define ALVALUE 1000000.0

#define onResultCmd(cmd)                    [NSArray arrayWithObjects:[NSString stringWithFormat:@"%d", cmd], nil]
#define onResultCmdString(cmd, szStrting)   [NSArray arrayWithObjects:[NSString stringWithFormat:@"%d", cmd], szStrting, nil]
#define OnNativeMainThreadCmd(cmd)          [[NativeOcClass getInstance] performSelectorOnMainThread:@selector(onMainThreadEvent:) withObject:onResultCmd(cmd) waitUntilDone:NO]
#define OnNativeMainThreadCmdString(cmd,szString)   [[NativeOcClass getInstance] performSelectorOnMainThread:@selector(onMainThreadEvent:) withObject:onResultCmdString(cmd, szString) waitUntilDone:NO]


@interface NativeOcClass : NSObject< AQRecordingDelegate, PlayingDelegate, CLLocationManagerDelegate, UIActionSheetDelegate,UIImagePickerControllerDelegate,UINavigationControllerDelegate,MFMessageComposeViewControllerDelegate,WKUIDelegate,WKNavigationDelegate >
{
@public
    Reachability* m_pReachability;
    NetworkStatus m_initNetworkStatus;
}

//事件结果
@property(nonatomic, assign)int eventResult;
@property(nonatomic, retain)NSString* filename;
@property(nonatomic, retain)NSString* voiceTime;
@property(nonatomic, retain)NSString* gameID;
@property(nonatomic, retain)NSString* upLoadUrl;

#ifdef USING_WX
//登陆信息属性
@property(nonatomic, retain)NSString*  wxToken;
@property(nonatomic, retain)NSString*  wxOpenid;
@property(nonatomic, retain)NSString*  wxRefreshToken;
#endif


@property(nonatomic, retain)NSMutableDictionary* filedic;

@property(nonatomic, retain)CLLocationManager *locationManager;

@property(nonatomic, retain)NSString*  wx_appid;
@property(nonatomic, retain)NSString*  wx_secret;
@property(nonatomic, retain)NSString*  wx_universalLink;
@property(nonatomic, retain)NSString*  openinstall_key;

//屏幕方向
@property(nonatomic, assign)int screenDirType;

//声明全局的UIImagePickerController
@property(nonatomic,strong)UIImagePickerController *imagePicker;
@property(nonatomic)int nOperateCode;
@property(nonatomic, retain)NSString* strOperateUser;

@property(nonatomic, retain)UIView* rootView;
@property(nonatomic, retain)UIView* cocosView;
@property(nonatomic, retain)WKWebView* uiWebView;
@property(nonatomic)BOOL bReload;

@property(nonatomic)BOOL bYunCengInit;



//屏幕转换
+(int)callNativeWithCanChangeScreen:(NSString*)szDir;


+(NativeOcClass*)getInstance;

#ifdef USING_WX
//获取微信事件结果
+(int)callNativeWithEventResult;

//获取微信信息
+(NSString*)callNativeWithWXLogonToken;
+(NSString*)callNativeWithWXLogonOpenid;
+(NSString*)callNativeWithWXLogonRefreshToken;
+(NSString*)callNativeWithMachineID;

+(int)callNativeWithWXInstall;
+(int)callNativeWithNetStatus;
#endif

//查询电量
+(int)callNativeWithBattery;
//查询信号强度
+(int)callNativeWithStrength;
//设置剪贴板
+(int)callNativeWithSetPasteboard:(NSString*)text;
//获取剪贴板
+(NSString*)callNativeWithGetPasteboard;
//获取定位
+(int)callNativeWithCoordinate;
//查询距离
+(NSString*)callNativeWithGetDistance:(NSString*)lAccuracy0 lLatitude0:(NSString*)lLatitude0 lAccurac1:(NSString*)lAccuracy1 lLatitude1:(NSString*)lLatitude1;

//设置storecallback
+(int)callNativeWithStoreCallBack:(NSString*)storecallback;

//分享事件
+(BOOL)callNativeWithOpenApp:(NSString*)mainString sub:(NSString*)subString;

//通过scheme判断应用是否安装
+(BOOL)callNativeWithInstall:(NSString*)mainString;

//分享事件
+(BOOL)callNativeWithShare:(NSString*)title main:(NSString*)mainString sub:(NSString*)subString shareurl:(NSString*)shareurl;

//发起事件
+(BOOL)callNativeWithTitle:(NSString*)title main:(NSString*)mainString sub:(NSString*)subString;
//开始录音
+(int)callNativeByVoiceStart:(NSString*)szFullPath GameId:(NSString*)GameId UpLoadUrl:(NSString*)szUpLoadUrl;
//取消录音
+(int)callNativeByVoiceCancel;
//停止录音
+(int)callNativeByVoiceStoped;
//录音时间
+(float)callNativeByVoiceTime;

//播放录音
+(int)callNativeByPlayStart:(NSString*)szFileName;
//停止播放
+(int)callNativeByPlayStoped;
//上传文件
+(int)callNativeByUpLoadFile:(NSString*)szFullPath;
//下载文件
+(int)callNativeByDownLoadFile:(NSString*)url savename:(NSString*)szSaveName fullpath:(NSString*)szFullPath;

//查询下载结果
+(int)callNativeByQueryDownRestlt:(NSString*)szFileName;

//获取当前app版本
+(NSString*)callNativeByAppVersion;

//拉起相册
+(int)callNativeBySaveImagePicker:(int)nOperateCode userId:(NSString*)strUserID;
//上传文件
+(int)callNativeByNewUpLoadFile:(NSString*)strFullpathFile url:(NSString*)strUpLoadUrl;

//发起JLP
+(void)callNativeByJLP:(NSString*)appname GameId:(int)GameId amount:(int)amount orderid:(NSString*)orderidString;

//久聊Transfer
+(void)callNativeByJLTransfer:(int)GameId appname:(NSString*)StringAppName;

//久聊分享应用
+(void)callNativeByJLShareApp:(NSString *)title description:(NSString *)desc appDownloadUrl:(NSString *)appDownloadUrl iOSDownloadUrl:(NSString *)iOSDownloadUrl androidBackURL:(NSString *)androidBackURL iOSBackUrl:(NSString *)iOSBackUrl;

//初始化游戏盾 YunCeng
+(void)callNativebByInitYunCeng;

//通过端口获取 ip
+(void)callNativeGetIpByYunceng:(NSString*)strGroupname domain:(NSString *)strDomain port:(NSString*)strPort;

//建立新线程 调用游戏盾 防止界面卡顿
+(void)callNativeNewThreadByYunceng:(NSArray*)array;

//保存图片到相册:fullFilePath图片完整路径
+(void)callNativeSavePhone:(NSString*)fullFilePath;

//获取iphone名字
+(NSString*)callNativeGetDeviceType;

//获取通讯录
+(NSString*)callNativeGetMailData;

//获取邀请码
+(NSString*)callNativeGetOpenInstallParam;

//获取发送短信
+(int)callNativeSendMgs:(NSString*)number txt:(NSString*)mgs;

//拉起homechat
+(void)callNativeHomeChat0:(NSString*)url p1:(NSString*)agentUserId p2:(NSString*)app_key p3:(NSString*)szChannelId p4:(NSString*)strUserID p5:(NSString*)strNameUtf8 p6:(NSString*)szMachineId p7:(NSString*)key;

//重力感应监听
+(void)callNativeStartMotionManager;
+(void)callNativeStopMotionManager;
+(void)callNativeMotionManagerCallback:(int)orientation;

+(void)callNativeShowLowestWeb:(NSString*)playurl;
+(void)callNativeCloseLowestWeb;



@end


#endif /* OCHelp_h */
