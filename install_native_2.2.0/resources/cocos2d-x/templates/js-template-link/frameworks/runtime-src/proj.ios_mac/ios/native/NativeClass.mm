
#import "NativeClass.h"
#import "SSKeychain.h"
#import "RotateNavigationController.h"

#ifdef USING_OPENINSTALL
    #import "OpenInstallSDK.h"
#endif

#import <CoreTelephony/CoreTelephonyDefines.h>
#import <CoreTelephony/CTCallCenter.h>
#import <CoreTelephony/CTCall.h>

#import <sys/utsname.h>

#ifdef USING_TONGXUNLU
#import <Contacts/Contacts.h>
#endif

#import <AdSupport/AdSupport.h>
#import "SimulateIDFA.h"
#import "OCDefine.h"

#import "IAPStore.h"
#import "JiuLiaoSDK.h"
#import "YunCeng/YunCeng.h"

#ifdef USING_WX
#import "WXApi.h"
#import "WXApiObject.h"
#endif


//调用
#include "cocos/scripting/js-bindings/manual/jsb_module_register.hpp"
#include "cocos/scripting/js-bindings/manual/jsb_global.h"
#include "cocos/scripting/js-bindings/jswrapper/SeApi.h"
#include "cocos/scripting/js-bindings/event/EventDispatcher.h"
#include "cocos/scripting/js-bindings/manual/jsb_classtype.hpp"



bool jsb_callback(int result)
{
    return jsb_callback(result, "0");
}

bool jsb_callback(int result, const char* szFileName)
{
    std::string ioscallback = "ios_callback";
    
    ioscallback = ioscallback + "(" + std::to_string(result) + ",\"" + szFileName + "\")";
    //找到一个更适合全局函数的方法
    return se::ScriptEngine::getInstance()->evalString( ioscallback.c_str() );
}

bool jsb_callback(int result, const char* szResult0, const char* szResult1 )
{
    std::string ioscallback = "ios_callback";
    
    ioscallback = ioscallback + "(" + std::to_string(result) + "," + szResult0 + "," + szResult1 + ")";
    
    //找到一个更适合全局函数的方法
    return se::ScriptEngine::getInstance()->evalString( ioscallback.c_str() );
}


BOOL waitUntilDone = NO;
NSString* kCTCallChange = @"kCTCallChange";


@implementation NativeOcClass

@synthesize eventResult;
@synthesize filename;
@synthesize voiceTime;
@synthesize gameID;
@synthesize upLoadUrl;

#ifdef USING_WX
@synthesize wxToken;
@synthesize wxOpenid;
@synthesize wxRefreshToken;
#endif

@synthesize wx_appid;
@synthesize wx_secret;
@synthesize openinstall_key;

@synthesize filedic;

@synthesize locationManager;

@synthesize screenDirType;

@synthesize imagePicker;
@synthesize nOperateCode;
@synthesize strOperateUser;

@synthesize rootView;
@synthesize cocosView;
@synthesize uiWebView;
@synthesize bReload;

//屏幕转换
+(int)callNativeWithCanChangeScreen:(NSString*)szDir
{
    [NativeOcClass getInstance].screenDirType = [szDir intValue];
    
    if( [NativeOcClass getInstance].screenDirType==2 )
    {
        //发送屏幕转换通知
        [RotateNavigationController changeScreenType:UIInterfaceOrientationLandscapeRight];
    }
    else
    {
        [RotateNavigationController changeScreenType:UIInterfaceOrientationPortrait];
    }
    return true;
}


static NativeOcClass* pNativeOcClass=nullptr;
+(NativeOcClass*)getInstance
{
    if( !pNativeOcClass )
        pNativeOcClass = [[NativeOcClass alloc] init];
    return pNativeOcClass;
}


-(id)init
{
    self = [super init];
    
    //登陆
    self.eventResult = YQ_SUB_EVENT;
    self.filename = @"";
    self.gameID = @"";
    self.upLoadUrl=@"";
    self.voiceTime=@"";
#ifdef USING_WX
    self.wxToken=@"";
    self.wxOpenid=@"";
    self.wxRefreshToken=@"";
#endif
    
    self.strOperateUser=@"";
    
    self.wx_appid=@"";
    self.wx_secret=@"";
    self.openinstall_key=@"";
    
    self.rootView = nil;
    self.cocosView = nil;
    self.uiWebView = nil;
    self.bReload = NO;
    
    self.bYunCengInit = NO;
    
    self.filedic = [NSMutableDictionary dictionary];
    
    
    [[NSNotificationCenter defaultCenter] addObserver:self
                                             selector:@selector(reachabilityChanged:)
                                                 name:kReachabilityChangedNotification
                                               object:nil];
    
    m_pReachability = [Reachability reachabilityForInternetConnection];
    m_initNetworkStatus = m_pReachability.currentReachabilityStatus;
    [m_pReachability startNotifier];
    
    //电话通知
    CTCallCenter *center = [[CTCallCenter alloc] init];
    center.callEventHandler = ^(CTCall *call)
    {
//        NSLog(@"call:%@", [call description]);
        if( [call callState] == CTCallStateDisconnected )
        {
            [[NativeOcClass getInstance] performSelectorOnMainThread:@selector(ctCallChanged:) withObject:onResultCmd(1) waitUntilDone:waitUntilDone];
        }
    };
    
    self.locationManager = [[CLLocationManager alloc]init];
    self.locationManager.delegate = self;
    self.locationManager.desiredAccuracy = kCLLocationAccuracyBest;
    self.locationManager.distanceFilter = 100.0f;
    
    
    
    return self;
}

//开始定位
-(void)startLocation
{
    if (![CLLocationManager locationServicesEnabled])
    {
        NSLog(@"定位服务当前可能尚未打开，请设置打开！");
        return;
    }
    
    //如果没有授权则请求用户授权
    if ([CLLocationManager authorizationStatus]==kCLAuthorizationStatusNotDetermined || [CLLocationManager authorizationStatus]==kCLAuthorizationStatusDenied)
    {
        [self.locationManager requestWhenInUseAuthorization];
    }
    else if([CLLocationManager authorizationStatus]==kCLAuthorizationStatusAuthorizedWhenInUse)
    {
        //设置代理
        self.locationManager.delegate=self;
        //设置定位精度
        self.locationManager.desiredAccuracy=kCLLocationAccuracyBest;
        
        //定位频率,每隔多少米定位一次
        CLLocationDistance distance=10.0;//十米定位一次
        self.locationManager.distanceFilter=distance;
        
        //启动跟踪定位
        [self.locationManager startUpdatingLocation];
    }
}

-(void)locationManager:(CLLocationManager *)manager didUpdateLocations:(NSArray *)locations
{
    CLLocation *location=[locations firstObject];//取出第一个位置
    CLLocationCoordinate2D coordinate=location.coordinate;//位置坐标
    NSLog(@"经度：%f,纬度：%f,海拔：%f,航向：%f,行走速度：%f", coordinate.longitude, coordinate.latitude, location.altitude, location.course, location.speed);
    
    //放大坐标比例
    jsb_callback(YQ_SUB_USER_POS, std::to_string(coordinate.longitude*ALVALUE).c_str(), std::to_string(coordinate.latitude*ALVALUE).c_str());
    
    //如果不需要实时定位，使用完即使关闭定位服务
    [self.locationManager stopUpdatingLocation];
}

- (void)didFailToLocateUserWithError:(NSError *)error
{
    jsb_callback(YQ_SUB_USER_POS, std::to_string(-1.0).c_str(), std::to_string(-1.0).c_str());
}

//查询距离
+(NSString*)callNativeWithGetDistance:(NSString*)lAccuracy0 lLatitude0:(NSString*)lLatitude0 lAccurac1:(NSString*)lAccuracy1 lLatitude1:(NSString*)lLatitude1
{
    //换算坐标比例
    CLLocationDegrees lfAccuracy0 = [lAccuracy0 doubleValue]/ALVALUE;
    CLLocationDegrees lfLatitude0 = [lLatitude0 doubleValue]/ALVALUE;
    CLLocationDegrees lfAccuracy1 = [lAccuracy1 doubleValue]/ALVALUE;
    CLLocationDegrees lfLatitude1 = [lLatitude1 doubleValue]/ALVALUE;
    
    CLLocation *current = [[CLLocation alloc] initWithLatitude:lfAccuracy0 longitude:lfLatitude0];
    CLLocation *before = [[CLLocation alloc] initWithLatitude:lfAccuracy1 longitude:lfLatitude1];
    
    CLLocationDistance distance = [current distanceFromLocation:before];
    
    return [NSString stringWithFormat:@"%lf", distance];
}


//网络变化通知
-(void)reachabilityChanged:(NSNotification*)notify
{
    Reachability* curReach = [notify object];
    NSParameterAssert([curReach isKindOfClass:[Reachability class]]);

    //通知立刻关闭连接
    m_initNetworkStatus = curReach.currentReachabilityStatus;
 
    int state = [NativeOcClass callNativeWithNetStatus];
    
    NSLog( @"网络通道发生变化:%d", state );
    
    jsb_callback(YQ_SUB_NET_CHANGE, std::to_string(state).c_str());
}

//电话变化通知
-(void)ctCallChanged:(id)value
{
    int state = [NativeOcClass callNativeWithNetStatus];
    
    NSLog(@"网络通道发生变化:%d", state );
    
    jsb_callback(YQ_SUB_NET_CHANGE, std::to_string(state).c_str());
}

+(int)callNativeWithStoreCallBack:(NSString*)storecallback
{
    [[CIAPStore getInstance] setStoreCallBack:storecallback];
    return 1;
}

//操作结果通知
-(void)onMainThreadEvent:(id)result
{
    int nEventResult = [[result objectAtIndex:0] intValue];
    std::string szEventString = "0";
    if ([result count]>1)
    {
        szEventString = [[result objectAtIndex:1] UTF8String];
    };

    jsb_callback(nEventResult, szEventString.c_str());
}

#ifdef USING_WX
//微信登陆结果
+(int)callNativeWithEventResult
{
    return [[NativeOcClass getInstance] eventResult];
}
+(NSString*)callNativeWithWXLogonToken
{
    return [[NativeOcClass getInstance] wxToken];
}
+(NSString*)callNativeWithWXLogonOpenid
{
    return [[NativeOcClass getInstance] wxOpenid];
}
+(NSString*)callNativeWithWXLogonRefreshToken
{
    return [[NativeOcClass getInstance] wxRefreshToken];
}
#endif


+(NSString*)callNativeWithMachineID
{
    //设备码获取
    NSString* pKey = [SSKeychain passwordForService:[[NSBundle mainBundle] bundleIdentifier] account:@"firedeviceid"];
    if(!pKey || [pKey length]<1)
    {
        if( [[ASIdentifierManager sharedManager] isAdvertisingTrackingEnabled] )
            pKey = [[[ASIdentifierManager sharedManager] advertisingIdentifier] UUIDString];
        else
            pKey = [SimulateIDFA createSimulateIDFA];
        [SSKeychain setPassword:pKey forService:[[NSBundle mainBundle] bundleIdentifier] account:@"firedeviceid"];
    }
    
    return pKey;
}

#ifdef USING_WX
+(int)callNativeWithWXInstall
{
    if( ![[UIApplication sharedApplication] canOpenURL:[NSURL URLWithString:@"weixin://"]]) return 0;
    return 1;
}
#endif
+(int)callNativeWithNetStatus
{
    if( [NativeOcClass getInstance]->m_initNetworkStatus==ReachableViaWiFi )
        return YQ_SUB_NETSTATE_WIFI;
        
    if( [NativeOcClass getInstance]->m_initNetworkStatus==ReachableViaWWAN )
        return YQ_SUB_NETSTATE_MOBILE;
            
    if( [NativeOcClass getInstance]->m_initNetworkStatus==NotReachable )
        return YQ_SUB_NETSTATE_NONE;
    
    return YQ_SUB_NETSTATE_NONE;
}

//查询电量
+(int)callNativeWithBattery
{
    UIDevice.currentDevice.batteryMonitoringEnabled = true;
    float batteryLevel = [UIDevice currentDevice].batteryLevel;
    UIDevice.currentDevice.batteryMonitoringEnabled = false;
    return batteryLevel*100;
}
//查询信号强度
+(int)callNativeWithStrength
{
    UIApplication *app = [UIApplication sharedApplication];
    NSArray *subviews = [[[app valueForKey:@"statusBar"] valueForKey:@"foregroundView"] subviews];
    NSString *dataNetworkItemView = nil;
    
    //UIStatusBarDataNetworkItemView
    //UIStatusBarSignalStrengthItemView
    for (id subview in subviews) {
        if([subview isKindOfClass:[NSClassFromString(@"UIStatusBarDataNetworkItemView") class]]) {
            dataNetworkItemView = subview;
            break;
        }
    }
    
    //_wifiStrengthBars
    //_signalStrengthBars
    int signalStrength = [[dataNetworkItemView valueForKey:@"_wifiStrengthBars"] intValue];
    
    NSLog(@"%d", signalStrength);
    
    return signalStrength;
}
//设置剪贴板
+(int)callNativeWithSetPasteboard:(NSString*)text
{
    UIPasteboard *pasteboard = [UIPasteboard generalPasteboard];
    pasteboard.string = text;
    
    return 1;
}
//获取剪贴板
+(NSString*)callNativeWithGetPasteboard
{
    UIPasteboard *pasteboard = [UIPasteboard generalPasteboard];
    return pasteboard.string;
}

//获取定位
+(int)callNativeWithCoordinate
{
    [[NativeOcClass getInstance] startLocation];
    
    return 1;
}

//打开其他app mainString:appname subString:param
+(BOOL)callNativeWithOpenApp:(NSString*)mainString sub:(NSString*)subString
{
    //温馨检测
    if( [[UIApplication sharedApplication] canOpenURL:[NSURL URLWithString:mainString]] )
    {
        [[UIApplication sharedApplication] openURL:[NSURL URLWithString:mainString]];
        return YES;
    }
    else
    {
        UIAlertView *alerView =  [[UIAlertView alloc] initWithTitle:@"提示"
                                                            message:[NSString stringWithFormat:@"打开失败，请先安装%@客户端", subString]
                                                           delegate:nil
                                                  cancelButtonTitle:@"确定"
                                                  otherButtonTitles:nil];
        [alerView show];
        [alerView release];
        return NO;
    }
}

//通过scheme判断应用是否安装
+(BOOL)callNativeWithInstall:(NSString*)mainString
{
    //温馨检测
    if( [[UIApplication sharedApplication] canOpenURL:[NSURL URLWithString:mainString]] )
        return YES;
    else
        return NO;
}

#ifdef USING_WX
+(BOOL)callNativeWithShare:(NSString*)title main:(NSString*)mainString sub:(NSString*)subString shareurl:(NSString*)shareurl
{
    //温馨检测
    if( ![[UIApplication sharedApplication] canOpenURL:[NSURL URLWithString:@"weixin://"]])
    {
        [[NativeOcClass getInstance] setEventResult:YQ_SUB_WXSHARE_FAILURE];
        UIAlertView *alerView =  [[UIAlertView alloc] initWithTitle:@"提示"
                                                            message:@"未安装微信客户端"
                                                           delegate:nil
                                                  cancelButtonTitle:@"确定"
                                                  otherButtonTitles:nil];
        [alerView show];
        [alerView release];
        
        return YES;
    }
    
    //文字 + 好友
    if( [title compare:@"wxsharetext"]==NSOrderedSame )
    {
        [[NativeOcClass getInstance] setEventResult:YQ_SUB_EVENT_BEGIN];
        
        id szGameNumber = mainString;
        id szMessage = subString;
        
        WXMediaMessage *message = [WXMediaMessage message];
        message.title = [NSString stringWithFormat:@"%@", szGameNumber];
        message.description = [NSString stringWithFormat:@"%@", szMessage];
        
        NSString *path = [[NSBundle mainBundle] pathForResource:@"AppIcon76x76~ipad" ofType:@"png"];
        UIImage* myImage = [UIImage imageWithContentsOfFile:path];
        [message setThumbImage:myImage];
        
        WXWebpageObject *ext = [WXWebpageObject object];
        ext.webpageUrl = shareurl;
        
        message.mediaObject = ext;
        
        SendMessageToWXReq* req = [[[SendMessageToWXReq alloc] init]autorelease];
        req.bText = NO;
        req.message = message;
        req.scene = WXSceneSession;
        
        [WXApi sendReq:req];
    }
    
    //链接 + 朋友圈
    if( [title compare:@"wxsharefriend"]==NSOrderedSame )
    {
        [[NativeOcClass getInstance] setEventResult:YQ_SUB_EVENT_BEGIN];
        
        id szGameNumber = mainString;
        id szMessage = subString;
        
        WXMediaMessage *message = [WXMediaMessage message];
        message.title = [NSString stringWithFormat:@"%@", szGameNumber];
        message.description = [NSString stringWithFormat:@"%@", szMessage];
        
        NSString *path = [[NSBundle mainBundle] pathForResource:@"AppIcon76x76~ipad" ofType:@"png"];
        UIImage* myImage = [UIImage imageWithContentsOfFile:path];
        [message setThumbImage:myImage];
        
        WXWebpageObject *ext = [WXWebpageObject object];
        ext.webpageUrl = shareurl;
        
        message.mediaObject = ext;
        
        SendMessageToWXReq* req = [[[SendMessageToWXReq alloc] init]autorelease];
        req.bText = NO;
        req.message = message;
        req.scene = WXSceneTimeline;
        
        [WXApi sendReq:req];
    }
    
    
    //图片 + 好友
    if( [title compare:@"wxshareimage"]==NSOrderedSame )
    {
        NSDictionary *infoDictionary = [[NSBundle mainBundle] infoDictionary];
        NSString *app_Name = [infoDictionary objectForKey:@"CFBundleDisplayName"];
        
        [[NativeOcClass getInstance] setEventResult:YQ_SUB_EVENT_BEGIN];
        
        id szFilePath = mainString;
        
        WXMediaMessage *message = [WXMediaMessage message];
        message.title = app_Name;
        message.description = @"";
        
        WXImageObject* ext = [WXImageObject object];
        ext.imageData = [NSData dataWithContentsOfFile:szFilePath];
        
        UIImage* image = [UIImage imageWithData:ext.imageData];
        
        ext.imageData = UIImageJPEGRepresentation(image, 0.1);
        
        message.mediaObject = ext;
        
        message.thumbData = [self scaleThumData:image w:80 h:80];
        
        SendMessageToWXReq* req = [[[SendMessageToWXReq alloc] init]autorelease];
        req.bText = NO;
        req.message = message;
        req.scene = WXSceneSession;
        
        [WXApi sendReq:req];
    }
    
    //图片 + 朋友圈
    if( [title compare:@"wxshareimagefriend"]==NSOrderedSame )
    {
        NSDictionary *infoDictionary = [[NSBundle mainBundle] infoDictionary];
        NSString *app_Name = [infoDictionary objectForKey:@"CFBundleDisplayName"];
        
        [[NativeOcClass getInstance] setEventResult:YQ_SUB_EVENT_BEGIN];
        
        id szFilePath = mainString;
        
        WXMediaMessage *message = [WXMediaMessage message];
        message.title = app_Name;
        message.description = @"";
        
        WXImageObject* ext = [WXImageObject object];
        ext.imageData = [NSData dataWithContentsOfFile:szFilePath];
        
        UIImage* image = [UIImage imageWithData:ext.imageData];
        
        ext.imageData = UIImageJPEGRepresentation(image, 0.1);
        
        message.mediaObject = ext;
        
        message.thumbData = [self scaleThumData:image w:80 h:80];
        
        SendMessageToWXReq* req = [[[SendMessageToWXReq alloc] init]autorelease];
        req.bText = NO;
        req.message = message;
        req.scene = WXSceneTimeline;
        
        [WXApi sendReq:req];
    }

    return YES;
}
#endif

//发起平台事件
+(BOOL)callNativeWithTitle:(NSString*)title main:(NSString*)mainString sub:(NSString*)subString
{
    //应用评分
    if( [title compare:@"OnAppPing"]==NSOrderedSame )
    {
        [RotateNavigationController evaluate];
    }
    #ifdef USING_WX
    //发起微信登陆
    if( [title compare:@"wxLogon"]==NSOrderedSame )
    {
        if ( [WXApi isWXAppInstalled] )
        {
            //标记登陆
            [[NativeOcClass getInstance] setEventResult:YQ_SUB_EVENT_BEGIN];
            
            //构造SendAuthReq结构体
            SendAuthReq* req =[[[SendAuthReq alloc ] init] autorelease];
            req.scope = @"snsapi_userinfo" ;
            req.state = @"org.HWQP.game";
            
            //第三方向微信终端发送一个SendAuthReq消息结构
            [WXApi sendReq:req];
        }
        else
        {
            [[NativeOcClass getInstance] setEventResult:YQ_SUB_WXLOGON_FAILURE];
            
            OnNativeMainThreadCmd( YQ_SUB_WXUNINSTALL );
        }
    }
    #endif
    
    //支付
    if( [title compare:@"Pay"]==NSOrderedSame )
    {
        NSError* error;
        NSData* jsonData = [mainString dataUsingEncoding:NSUTF8StringEncoding];
        id jsonObject = [NSJSONSerialization JSONObjectWithData:jsonData options:NSJSONReadingAllowFragments error:&error];
        //NSString* retcode = [jsonObject objectForKey:@"retcode"];
        
        int paytype = [[jsonObject objectForKey:@"PayType"] intValue];
        
        //store支付
        if( paytype==PAYTYPE_STORE )
        {
            [[NativeOcClass getInstance] setEventResult:YQ_SUB_IOSPAY_BEGIN];
            
            int price = [[jsonObject objectForKey:@"OrderAmount"] intValue];
            id proid = [jsonObject objectForKey:@"StoreID"];
            id orderid = [jsonObject objectForKey:@"OrderId"];
            
            [[CIAPStore getInstance] setOrderString: orderid];
            [[CIAPStore getInstance] setPrice:price];
            
            //发起购买
            [[CIAPStore getInstance] buy:proid];
        }
    }
    
    //数据设置
    if( [title compare:@"setGameID"]==NSOrderedSame )
    {
        [NativeOcClass getInstance].gameID = mainString;
    }
    
    //输出日志
    if( [title compare:@"log"]==NSOrderedSame )
    {
        NSLog(@"ios.log:---------------:%@", mainString);
    }
    
    return 0;
}



//录音事件
//开始录音
+(int)callNativeByVoiceStart:(NSString*)szFullPath GameId:(NSString*)GameId UpLoadUrl:(NSString*)szUpLoadUrl
{
    [[NativeOcClass getInstance] setEventResult:YQ_SUB_VOICE_START];
    
    //获取文件名
    [NativeOcClass getInstance].filename = [szFullPath lastPathComponent];
    [NativeOcClass getInstance].gameID = GameId;
    [NativeOcClass getInstance].upLoadUrl = szUpLoadUrl;
        
    [AQRecorderManager sharedManager].delegate = [NativeOcClass getInstance];
    [[AQRecorderManager sharedManager] startRecording:szFullPath];
    
    return 1;
}

//取消录音
+(int)callNativeByVoiceCancel
{
    [[AQRecorderManager sharedManager] cancelRecording];
    return 1;
}

//结束录音
+(int)callNativeByVoiceStoped
{
    [[AQRecorderManager sharedManager] stopRecording];
    return 1;
}
//录音时间
+(float)callNativeByVoiceTime
{
    return [[NativeOcClass getInstance].voiceTime floatValue];
}

//播放录音
+(int)callNativeByPlayStart:(NSString*)szFileName
{
    [[NativeOcClass getInstance] setEventResult:YQ_SUB_VOICE_PLAYSTART];
    
    [PlayerManager sharedManager].delegate = nil;
    [[PlayerManager sharedManager] playAudioWithFileName:szFileName delegate:[NativeOcClass getInstance]];

    return 1;
}
//停止播放 
+(int)callNativeByPlayStoped
{
    [[PlayerManager sharedManager] stopPlaying];
    return 1;
}


#pragma mark - Recording & Playing Delegate
//录音完成
- (void)recordingFinishedWithFileName:(NSString*)filePath time:(NSTimeInterval)interval
{
    //开始上传
    [NativeOcClass getInstance].voiceTime = [NSString stringWithFormat:@"%f", interval];
    
    if( interval<1.0 )
    {
        NSLog(@"录音时间太短！");
        
        //录音结束状态
        [[NativeOcClass getInstance] setEventResult:YQ_SUB_VOICE_ENDED];
        
        [[NativeOcClass getInstance] performSelectorOnMainThread:@selector(onMainThreadEvent:) withObject:onResultCmd(YQ_SUB_VOICE_ENDED) waitUntilDone:waitUntilDone];
    
        return;
    }
    
    //上传状态
    [[NativeOcClass getInstance] setEventResult:YQ_SUB_VOICE_UPLOAD];
    
    [[NativeOcClass getInstance] performSelectorOnMainThread:@selector(onMainThreadEvent:) withObject:onResultCmd(YQ_SUB_VOICE_UPLOAD) waitUntilDone:YES];
    
    [NativeOcClass callNativeByUpLoadFile:filePath];
    
    NSLog(@"%@", filePath);
}

//录音超时结束
- (void)recordingTimeout
{
    //self.isRecording = NO;
    //self.consoleLabel.text = @"录音超时";
    
    [[NativeOcClass getInstance] setEventResult:YQ_SUB_VOICE_ENDED];
    
    [[NativeOcClass getInstance] performSelectorOnMainThread:@selector(onMainThreadEvent:) withObject:onResultCmd(YQ_SUB_VOICE_ENDED) waitUntilDone:waitUntilDone];
    
    NSLog(@"recordingTimeout");
}

//录音结束回调
- (void)recordingStopped
{
    [[NativeOcClass getInstance] setEventResult:YQ_SUB_VOICE_ENDED];
    
    
    [[NativeOcClass getInstance] performSelectorOnMainThread:@selector(onMainThreadEvent:) withObject:onResultCmd(YQ_SUB_VOICE_ENDED) waitUntilDone:waitUntilDone];
    
    NSLog(@"recordingStopped");
}

//录音失败回调
- (void)recordingFailed:(NSString *)failureInfoString
{
    [[NativeOcClass getInstance] setEventResult:YQ_SUB_VOICE_ENDED];

    [[NativeOcClass getInstance] performSelectorOnMainThread:@selector(onMainThreadEvent:) withObject:onResultCmd(YQ_SUB_VOICE_ENDED) waitUntilDone:waitUntilDone];
    
    NSLog(@"录音失败");
}

- (void)levelMeterChanged:(float)levelMeter
{
    //self.levelMeter.progress = levelMeter;
    //NSLog(@"levelMeterChanged");
}

//播放结束回调
- (void)playingStoped
{
    //self.isPlaying = NO;
    //self.consoleLabel.text = [NSString stringWithFormat:@"播放完成: %@", [self.filename substringFromIndex:[self.filename rangeOfString:@"Documents"].location]];
    
    //播放完成
    [[NativeOcClass getInstance] setEventResult:YQ_SUB_VOICE_PALYENDED];
    
    [[NativeOcClass getInstance] performSelectorOnMainThread:@selector(onMainThreadEvent:) withObject:onResultCmd(YQ_SUB_VOICE_PALYENDED) waitUntilDone:waitUntilDone];
    
    NSLog(@"playingStoped");
}


//下载文件 0无效状态 1下载成功 2下载失败
+(int)callNativeByDownLoadFile:(NSString*)url savename:(NSString*)szFileName fullpath:(NSString*)szFullPath
{
    //添加下载
    [[NativeOcClass getInstance].filedic setObject:@"0" forKey:szFileName];
    
    NSString* szSubString = [szFileName stringByDeletingPathExtension];
    
    // 2 封装成NSURL
    NSURL* fullurl = [NSURL URLWithString:url];
    
    // 3 定义NSURLRquest
    NSMutableURLRequest *request = [[[NSMutableURLRequest alloc] init] autorelease];//注意这个是mutable，说明这个是可变的
    
    // 设置请求类型
    request.HTTPMethod = @"get";
    
    //添加url
    request.URL = fullurl;
    
    [NSURLConnection sendAsynchronousRequest:request queue:[[NSOperationQueue alloc] init] completionHandler:^(NSURLResponse * _Nullable response, NSData * _Nullable data, NSError * _Nullable connectionError)
    {
        BOOL isSuccecc = [data writeToFile:szFullPath atomically:YES];
        if(isSuccecc)
        {
            [[NativeOcClass getInstance] performSelectorOnMainThread:@selector(onMainThreadEvent:) withObject:onResultCmdString(YQ_SUB_VOICE_DL_SUCCEED, szSubString) waitUntilDone:waitUntilDone];
        }
        else
        {
            [[NativeOcClass getInstance] performSelectorOnMainThread:@selector(onMainThreadEvent:) withObject:onResultCmdString(YQ_SUB_VOIDE_DL_FAILURE, szSubString) waitUntilDone:waitUntilDone];
        }
        
     }];
    
    return 1;
}

//查询语音下载结果
+(int)callNativeByQueryDownRestlt:(NSString*)szFileName
{
    int result = [[[NativeOcClass getInstance].filedic objectForKey:szFileName] intValue];
    [[NativeOcClass getInstance].filedic removeObjectForKey:szFileName];
    
    return result;
}

//上传文件
+(int)callNativeByUpLoadFile:(NSString*)szFullPath
{
    NSString* filename = [szFullPath lastPathComponent];
    
    NSString* fullurl = [NSString stringWithFormat:@"%@?filename=%@&userid=%@", [NativeOcClass getInstance].upLoadUrl, filename, [NativeOcClass getInstance].gameID ];
    
    // 2 封装成NSURL
    NSURL* url = [NSURL URLWithString:fullurl];
    
    // 3 定义NSURLRquest
    NSMutableURLRequest *request = [[[NSMutableURLRequest alloc] init] autorelease];//注意这个是mutable，说明这个是可变的

    // 设置请求类型
    request.HTTPMethod = @"post";
    
    //添加url
    request.URL = url;
    
    //设置body内容
    NSData* bodyData = [NSData dataWithContentsOfFile:szFullPath];
    request.HTTPBody = bodyData;
    
    [NSURLConnection sendAsynchronousRequest:request queue:[[NSOperationQueue alloc] init] completionHandler:^(NSURLResponse * _Nullable response, NSData * _Nullable data, NSError * _Nullable connectionError)
    {
        if(data==nil)
        {
            [[NativeOcClass getInstance] setEventResult:YQ_SUB_VOICE_UL_FAILURE];

            [[NativeOcClass getInstance] performSelectorOnMainThread:@selector(onMainThreadEvent:) withObject:onResultCmd(YQ_SUB_VOICE_UL_FAILURE) waitUntilDone:waitUntilDone];
            
            NSLog(@"访问失败");
            return;
        }
        
         NSString* valueString = [NSString stringWithFormat:@"%s", [data bytes]];
         if( [valueString intValue]==0 )
         {
             //成功标记
             [[NativeOcClass getInstance] setEventResult:YQ_SUB_VOICE_UL_SUCCEED];
             
             [[NativeOcClass getInstance] performSelectorOnMainThread:@selector(onMainThreadEvent:) withObject:onResultCmd(YQ_SUB_VOICE_UL_SUCCEED) waitUntilDone:waitUntilDone];
             
             NSLog(@"成功");
         }
         else
         {
             [[NativeOcClass getInstance] setEventResult:YQ_SUB_VOICE_UL_FAILURE];
             
             [[NativeOcClass getInstance] performSelectorOnMainThread:@selector(onMainThreadEvent:) withObject:onResultCmd(YQ_SUB_VOICE_UL_FAILURE) waitUntilDone:waitUntilDone];
             NSLog(@"失败");
         }
     }];
    
    return 1;
}




//分享图片调整
+(NSData*)scaleThumData:(UIImage*)image w:(int)w h:(int)h
{
    UIGraphicsBeginImageContext(CGSizeMake(w, h));
    [image drawInRect:CGRectMake(0, 0, w, h)];
    UIImage* newImage = UIGraphicsGetImageFromCurrentImageContext();
    UIGraphicsEndImageContext();
    
    return UIImagePNGRepresentation(newImage);
    
}

//获取当前app版本
+(NSString*)callNativeByAppVersion
{
    NSDictionary *infoDic = [[NSBundle mainBundle] infoDictionary];
    NSString *appVersion = [infoDic objectForKey:@"CFBundleShortVersionString"];
    return appVersion;
}

//发起JLP
+(void)callNativeByJLP:(NSString*)appname GameId:(int)GameId amount:(int)iAamount orderid:(NSString*)orderidString
{
    NSString* GameIdString = [NSString stringWithFormat:@"%d",GameId];
    [[JiuLiaoSDK shareInstance] goToJiuLiaoPay:GameIdString gameName:appname amoutMoney:iAamount orderId:orderidString];
}

//久聊Transfer
+(void)callNativeByJLTransfer:(int)GameId appname:(NSString*)StringAppName;
{
    NSString* GameIdString = [NSString stringWithFormat:@"%d",GameId];
    [[JiuLiaoSDK shareInstance] goToJiuLiaoTransfer:GameIdString gameName:StringAppName];
}

//久聊分享应用
+(void)callNativeByJLShareApp:(NSString *)title description:(NSString *)desc appDownloadUrl:(NSString *)appDownloadUrl iOSDownloadUrl:(NSString *)iOSDownloadUrl androidBackURL:(NSString *)androidBackURL iOSBackUrl:(NSString *)iOSBackUrl
{
    [[JiuLiaoSDK shareInstance] shareToJiuLiaoWithTitle:title description:desc appDownloadUrl:appDownloadUrl iOSDownloadUrl:iOSDownloadUrl androidBackURL:androidBackURL iOSBackUrl:iOSBackUrl];
}

//初始化游戏盾 YunCeng
+(void)callNativebByInitYunCeng
{
    const char appkey[] = "3tODolGrtg7+d0aesg5vhudDG505KxM3pI+e5k9kUFEeT-nYV1rMwe9VhrOdXIHHzrNCqAxDPaelRO59Fr2GCSR0O6e6WtzbqsySe4l1POoHf8M-6wrLkiJbz8WHqWeLh74qlf2QXmEoQQW4cCRDBXmb3phjq+t5CDfnUaivhjFQ6ptLSpAWLQpOX47RJbplfGBsSA6Ps4WxR7ixBTELCv-Bf3l-sXTEHJepNWMHgS79OtF4TSCWo_RJ7w9zcHUAd53w7I7R2WKx2D1plqPzgPnmPEXtot3XwmdT2B83kGPDl6n4KDv8Z-ruJRBChP9vqnuGVQp6BN2z73PDbqCQyhe5aHmKtO6GCpcP0SE3WQqaUwuRSXpV-V+1N5yefW-pg9-H-mrt0qN9RDCcVEsj1zgPYkafuTymzrBqQIZscRVjyypNX";
    
    NSString* strToken = [NativeOcClass callNativeWithMachineID];
    
    int ret = [YunCeng initEx:appkey:[strToken UTF8String] ];
    if (0 != ret) {
        printf("init failed. \n");
        
        [NativeOcClass getInstance].bYunCengInit = NO;
        return;
    }
    else
    {
        printf("init successful\n");
        
        [NativeOcClass getInstance].bYunCengInit = YES;
    }
}


//通过端口获取 ip
+(void)callNativeGetIpByYunceng:(NSString*)strGroupname domain:(NSString *)strDomain port:(NSString*)strPort
{
    [NSThread detachNewThreadSelector:@selector(callNativeNewThreadByYunceng:) toTarget:self withObject:[NSArray arrayWithObjects:strGroupname, strDomain, strPort, nil]];
}

//建立新线程 调用游戏盾 防止界面卡顿
+(void)callNativeNewThreadByYunceng:(NSArray*)array
{
    if(![NativeOcClass getInstance].bYunCengInit)
        [NativeOcClass callNativebByInitYunCeng];
        
    NSString* strGroupname = [array objectAtIndex:0];
    NSString* strDomain = [array objectAtIndex:1];
    NSString* strPort = [array objectAtIndex:2];
    
    NSString* strToken = [NativeOcClass callNativeWithMachineID];
    char ip[128]= {0};
    char port[32] = {0};
    
    int ret = [YunCeng getProxyTcpByDomain : [strToken UTF8String]: [strGroupname UTF8String]: [strDomain UTF8String]: [strPort UTF8String] : ip : 128 : port:32];
    std::string strSucess = "false";
    NSLog(@"ret:%d", ret);
    if (0 != ret)
    {
        strSucess = "false";
        sprintf(ip, "127.0.0.1");
        sprintf(port, "0");
        printf("get next ip failed. err\n");
    }
    else
    {
        strSucess = "true";
        printf("get next ip success. %s, port:%s \n", ip, port);
    }
    
    std::string domain = [strDomain UTF8String];
    
    std::string ioscallback = "mfConfig.OnGetYunCengIpReq_AndroidDone";
    ioscallback = ioscallback + "(" + "\"" + domain + "\"" + "," + "\""+ strSucess + "\"" +"," + "\""+ ip+ "\"" + "," + "\""+port + "\""+ ")";
    
    [[NativeOcClass getInstance] performSelectorOnMainThread:@selector(onYuncengMainSelector:) withObject:[NSString stringWithUTF8String:ioscallback.c_str()] waitUntilDone:NO];
}

-(void)onYuncengMainSelector:(NSString*)ioscallback
{
    se::ScriptEngine::getInstance()->evalString( [ioscallback UTF8String] );
}


//拉起相册
+(int)callNativeBySaveImagePicker:(int)nOperateCode userId:(NSString*)strUserID
{
    //保存相册 操作类型
    [NativeOcClass getInstance].nOperateCode = nOperateCode;
    [NativeOcClass getInstance].strOperateUser = strUserID;
    
    //自定义消息框
    UIActionSheet *sheet = [[[UIActionSheet alloc] initWithTitle:@"选择图片" delegate:[NativeOcClass getInstance] cancelButtonTitle:nil destructiveButtonTitle:@"从相册选择" otherButtonTitles:@"拍照", @"取消", nil] autorelease];
    sheet.tag = 2550;
    
    //显示消息框
    [sheet showInView:[[RotateNavigationController getInstance] view]];
    return 1;
}

#pragma mark -消息框代理实现-
- (void)actionSheet:(UIActionSheet *)actionSheet clickedButtonAtIndex:(NSInteger)buttonIndex
{
    NSLog(@"buttonIndex:%ld", buttonIndex);
    
    if (actionSheet.tag == 2550)
    {
        UIImagePickerControllerSourceType sourceType = UIImagePickerControllerSourceTypePhotoLibrary;
        
        // 判断系统是否支持相机
        UIImagePickerController *imagePickerController = [[[UIImagePickerController alloc] init] autorelease];
        [imagePickerController setAllowsEditing:NO];
        
        if([UIImagePickerController isSourceTypeAvailable:UIImagePickerControllerSourceTypeCamera])
        {
            imagePickerController.delegate = self;
            imagePickerController.sourceType = sourceType;
            
            //图片来源
            if (buttonIndex == 2)
            {
                return;
                
            }
            else if (buttonIndex == 1)
            {
                //拍照
                sourceType = UIImagePickerControllerSourceTypeCamera;
                imagePickerController.sourceType = sourceType;
                
                [[RotateNavigationController getInstance] presentViewController:imagePickerController animated:YES completion:nil];
            }
            else
            {
                sourceType = UIImagePickerControllerSourceTypePhotoLibrary;
                imagePickerController.sourceType = sourceType;
                
                [[RotateNavigationController getInstance] presentViewController:imagePickerController animated:YES completion:nil];
                
            }
        }
    }
}

#pragma mark -实现图片选择器代理
- (void)imagePickerController:(UIImagePickerController *)picker didFinishPickingMediaWithInfo:(NSDictionary *)info
{
    //恢复视图
    [RotateNavigationController resetScreenType];
    
    [picker dismissViewControllerAnimated:YES completion:^{}];
    UIImage *image = [info objectForKey:UIImagePickerControllerOriginalImage];
    
    //通过key值获取到图片
    //_headerV.image = image;
    //给UIimageView赋值已经选择的相片 //上传图片到服务器--在这里进行图片上传的网络请求，这里不再介绍 ......
    id native_class = [NativeOcClass getInstance];
    if( [native_class nOperateCode]==YQ_SUB_SAVE_PHOTO )
    {
        //获取时间和时间戳
        NSDate* timeStamp = [NSDate dateWithTimeIntervalSinceNow:0];
        NSTimeInterval temp = [timeStamp timeIntervalSince1970];
        NSString* time = [NSString stringWithFormat:@"%.0f", temp];
        NSString* filename = [NSString stringWithFormat:@"%@_%@.jpg", strOperateUser, time];
        
        //存储图片
        NSString *path = [[NSHomeDirectory() stringByAppendingPathComponent:@"Documents"] stringByAppendingPathComponent:filename];
        [UIImageJPEGRepresentation(image,0.5) writeToFile:path atomically:YES];
        
        //返回js图片路径
        [native_class performSelectorOnMainThread:@selector(onMainThreadEvent:) withObject:onResultCmdString(YQ_SUB_SAVE_PHOTO_DONE, path) waitUntilDone:waitUntilDone];
    }
}

//当用户取消选择的时候，调用该方法
- (void)imagePickerControllerDidCancel:(UIImagePickerController *)picker
{
    //恢复视图
    [RotateNavigationController resetScreenType];
    
    [picker dismissViewControllerAnimated:YES completion:^{}];
    
    NSLog(@"用户取消选择");
}

//上传文件
+(int)callNativeByNewUpLoadFile:(NSString*)strFullpathFile url:(NSString*)strUpLoadUrl 
{
    NSString* filename = [strFullpathFile lastPathComponent];
    NSString* upload_url_req = [NSString stringWithFormat:@"%@?filename=%@", strUpLoadUrl,filename];
    NSLog(@"upload_url_req:%@",upload_url_req);
    
    // 2 封装成NSURL
    NSURL* url = [NSURL URLWithString:upload_url_req];
    
    // 3 定义NSURLRquest
    NSMutableURLRequest *request = [[[NSMutableURLRequest alloc] init] autorelease];//注意这个是mutable，说明这个是可变的
    
    // 设置请求类型
    request.HTTPMethod = @"post";
    
    //添加url
    request.URL = url;
    
    //设置body内容
    NSData* bodyData = [NSData dataWithContentsOfFile:strFullpathFile];
    request.HTTPBody = bodyData;

    
    [NSURLConnection sendAsynchronousRequest:request queue:[[NSOperationQueue alloc] init] completionHandler:^(NSURLResponse * _Nullable response, NSData * _Nullable data, NSError * _Nullable connectionError)
    {
        if(data==nil)
        {
            [[NativeOcClass getInstance] setEventResult:YQ_SUB_UPLOAD_FILE_FAILURE];

            [[NativeOcClass getInstance] performSelectorOnMainThread:@selector(onMainThreadEvent:) withObject:onResultCmd(YQ_SUB_UPLOAD_FILE_FAILURE) waitUntilDone:waitUntilDone];

            NSLog(@"访问失败");
            return;
        }

        NSString* ret_desc = [NSString stringWithFormat:@"%s", [data bytes]];
        NSError* error;
        NSDictionary* dic_data = [NSJSONSerialization JSONObjectWithData:data options:NSJSONReadingMutableContainers error:nil];
        if( dic_data )
        {
            //图片上传成功
            int code = [[dic_data objectForKey:@"code"] intValue];
            if( code==0 )
            {
                NSString* src = [[dic_data objectForKey:@"data"] objectForKey:@"src"];
                
                //成功标记
                [[NativeOcClass getInstance] setEventResult:YQ_SUB_UPLOAD_FILE_DONE];
                [[NativeOcClass getInstance] performSelectorOnMainThread:@selector(onMainThreadEvent:) withObject:onResultCmdString(YQ_SUB_UPLOAD_FILE_DONE, src) waitUntilDone:waitUntilDone];
                return;
            }
        }
        
        //上传失败
        [[NativeOcClass getInstance] setEventResult:YQ_SUB_UPLOAD_FILE_FAILURE];
        [[NativeOcClass getInstance] performSelectorOnMainThread:@selector(onMainThreadEvent:) withObject:onResultCmd(YQ_SUB_UPLOAD_FILE_FAILURE) waitUntilDone:waitUntilDone];
        NSLog(@"ret_desc:%@", ret_desc);
     }];
    
    return 1;
}

//保存图片到相册:fullFilePath图片完整路径
+(void)callNativeSavePhone:(NSString*)fullFilePath
{
    UIImage *image = [UIImage imageWithContentsOfFile:fullFilePath];
    UIImageWriteToSavedPhotosAlbum(image, nil, nil,nil);
}

//获取iphone名字
+(NSString*)callNativeGetDeviceType
{
    struct utsname systemInfo;
    uname(&systemInfo);
    NSString* platform = [NSString stringWithCString: systemInfo.machine encoding:NSASCIIStringEncoding];
    
    if([platform isEqualToString:@"iPhone5,1"])  return @"iPhone 5";
    if([platform isEqualToString:@"iPhone5,2"])  return @"iPhone 5";
    if([platform isEqualToString:@"iPhone5,3"])  return @"iPhone 5c";
    if([platform isEqualToString:@"iPhone5,4"])  return @"iPhone 5c";
    if([platform isEqualToString:@"iPhone6,1"])  return @"iPhone 5s";
    if([platform isEqualToString:@"iPhone6,2"])  return @"iPhone 5s";
    if([platform isEqualToString:@"iPhone7,1"])  return @"iPhone 6 Plus";
    if([platform isEqualToString:@"iPhone7,2"])  return @"iPhone 6";
    if([platform isEqualToString:@"iPhone8,1"])  return @"iPhone 6s";
    if([platform isEqualToString:@"iPhone8,2"])  return @"iPhone 6s Plus";
    
    return platform;
}


+(NSString*)callNativeGetMailData
{
#ifdef USING_TONGXUNLU
    CNAuthorizationStatus status = [CNContactStore authorizationStatusForEntityType:CNEntityTypeContacts];
    if (status == CNAuthorizationStatusNotDetermined) {
        CNContactStore *store = [[CNContactStore alloc] init];
        [store requestAccessForEntityType:CNEntityTypeContacts completionHandler:^(BOOL granted, NSError*  _Nullable error) {
            if (error) {
                NSLog(@"授权失败");
            }else {
                NSLog(@"成功授权");
            }
        }];
    }
    else if(status == CNAuthorizationStatusRestricted)
    {
        NSLog(@"用户拒绝");
        UIAlertController *alertController = [UIAlertController
                                              alertControllerWithTitle:@"请授权通讯录权限"
                                              message:@"请在iPhone的\"设置-隐私-通讯录\"选项中,允许APP访问你的通讯录"
                                              preferredStyle: UIAlertControllerStyleAlert];
        
        UIAlertAction *OKAction = [UIAlertAction actionWithTitle:@"好的" style:UIAlertActionStyleDefault handler:nil];
        [alertController addAction:OKAction];
        
        [[RotateNavigationController getInstance] presentViewController:alertController animated:YES completion:nil];
    }
    else if (status == CNAuthorizationStatusDenied)
    {
        NSLog(@"用户拒绝");
        UIAlertController *alertController = [UIAlertController
                                              alertControllerWithTitle:@"请授权通讯录权限"
                                              message:@"请在iPhone的\"设置-隐私-通讯录\"选项中,允许APP访问你的通讯录"
                                              preferredStyle: UIAlertControllerStyleAlert];
        
        UIAlertAction *OKAction = [UIAlertAction actionWithTitle:@"好的" style:UIAlertActionStyleDefault handler:nil];
        [alertController addAction:OKAction];
        
        [[RotateNavigationController getInstance] presentViewController:alertController animated:YES completion:nil];
    }
    else if (status == CNAuthorizationStatusAuthorized)//已经授权
    {
        //有通讯录权限-- 进行下一步操作
        // 获取指定的字段,并不是要获取所有字段，需要指定具体的字段
        NSArray *keysToFetch = @[CNContactGivenNameKey, CNContactFamilyNameKey, CNContactPhoneNumbersKey];
        CNContactFetchRequest *fetchRequest = [[[CNContactFetchRequest alloc] initWithKeysToFetch:keysToFetch] autorelease];
        CNContactStore *contactStore = [[[CNContactStore alloc] init] autorelease];
        
        NSMutableString *phonedesc = [[[NSMutableString alloc] init] autorelease];
        [contactStore enumerateContactsWithFetchRequest:fetchRequest error:nil usingBlock:^(CNContact * _Nonnull contact, BOOL * _Nonnull stop)
        {
            NSString *givenName = contact.givenName;
            NSString *familyName = contact.familyName;
//            NSLog(@"givenName=%@, familyName=%@", givenName, familyName);
            //拼接姓名
            NSString *nameStr = [NSString stringWithFormat:@"%@%@",contact.familyName,contact.givenName];
            NSArray *phoneNumbers = contact.phoneNumbers;
            
            for (CNLabeledValue *labelValue in phoneNumbers)
            {
                //遍历一个人名下的多个电话号码
                NSString *label = labelValue.label;
                CNPhoneNumber *phoneNumber = labelValue.value;
                
                NSString * string = phoneNumber.stringValue ;
                
                //去掉电话中的特殊字符
                string = [string stringByReplacingOccurrencesOfString:@"+86" withString:@""];
                string = [string stringByReplacingOccurrencesOfString:@"-" withString:@""];
                string = [string stringByReplacingOccurrencesOfString:@"(" withString:@""];
                string = [string stringByReplacingOccurrencesOfString:@")" withString:@""];
                string = [string stringByReplacingOccurrencesOfString:@" " withString:@""];
                string = [string stringByReplacingOccurrencesOfString:@" " withString:@""];
                
                [phonedesc appendFormat:@"%@,", nameStr];
                [phonedesc appendFormat:@"%@;", string];
                
//                NSLog(@"姓名=%@, 电话号码是=%@", nameStr, string);
            }
        }];
        
        return phonedesc;
    }
    
    return @"";
    
    #endif
    
    return @"";
}



//获取发送短信
+(int)callNativeSendMgs:(NSString*)number txt:(NSString*)mgs
{
//    NSLog(@"%@",number);
    
    if( [MFMessageComposeViewController canSendText]) {
//        MFMessageComposeViewController * controller = [[[MFMessageComposeViewController alloc] init] autorelease];
//        controller.recipients = @[number];//发送短信的号码，数组形式入参
//        controller.navigationBar.tintColor = [UIColor redColor];
//        controller.body = mgs; //此处的body就是短信将要发生的内容
//        controller.messageComposeDelegate = [NativeOcClass getInstance];
//        [[RotateNavigationController getInstance] presentViewController:controller animated:YES completion:nil];
////        [[[[controller viewControllers] lastObject] navigationItem] setTitle:@"title"];//修改短信界面标题
//
        
        NSString *urlStr = [NSString stringWithFormat:@"sms://%@&body=%@", number, mgs];
        urlStr = [urlStr stringByAddingPercentEncodingWithAllowedCharacters:[NSCharacterSet URLQueryAllowedCharacterSet]]; // 对中文进行编码
        NSURL *url = [NSURL URLWithString:urlStr];
        
        if (@available(iOS 10.0, *)) {
            [[UIApplication sharedApplication] openURL:url options:@{} completionHandler:nil];
        } else {
            [[UIApplication sharedApplication] openURL:url];
        }
    }
    else {
        UIAlertView *alert = [[[UIAlertView alloc] initWithTitle:@"提示信息"
                                                         message:@"该设备不支持短信功能"
                                                        delegate:nil
                                               cancelButtonTitle:@"确定"
                                               otherButtonTitles:nil, nil] autorelease];
        [alert show];
    }
    
    return 0;
}

-(void)messageComposeViewController:(MFMessageComposeViewController *)controller didFinishWithResult:(MessageComposeResult)result
{
    [[RotateNavigationController getInstance] dismissViewControllerAnimated:YES completion:nil];
    switch (result) {
        case MessageComposeResultSent:
            //信息传送成功
            break;
        case MessageComposeResultFailed:
            //信息传送失败
            break;
        case MessageComposeResultCancelled:
            //信息被用户取消传送
            break;
        default:
            break;
    }
}

//拉起homechat
+(void)callNativeHomeChat0:(NSString*)url p1:(NSString*)agentUserId p2:(NSString*)app_key p3:(NSString*)szChannelId p4:(NSString*)strUserID p5:(NSString*)strNameUtf8 p6:(NSString*)szMachineId p7:(NSString*)key
{
#ifdef USING_SHANFU
    [RotateNavigationController callNativeHomeChat0:url p1:agentUserId p2:app_key p3:szChannelId p4:strUserID p5:strNameUtf8 p6:szMachineId p7:key];
#else
    NSLog(@"未编译闪付代码");
#endif
}

//开始监听重力感应
+(void)callNativeStartMotionManager
{
    [[RotateNavigationController getInstance] starMotionManager];
}
+(void)callNativeStopMotionManager
{
    [[RotateNavigationController getInstance] stopMotionManager];
}
+(void)callNativeMotionManagerCallback:(int)orientation
{
    //YQ_SUB_HOMESIDE 横屏
    //YQ_SUB_HOMEDOWN 竖屏
    if( orientation==YQ_SUB_HOMEDOWN )
        NSLog(@"竖屏 mation:%d", orientation);
    else
        NSLog(@"横屏 mation:%d", orientation);
    
    [[NativeOcClass getInstance] performSelectorOnMainThread:@selector(onMainThreadEvent:) withObject:onResultCmd(orientation) waitUntilDone:waitUntilDone];
}

//获取邀请码
+(NSString*)callNativeGetOpenInstallParam
{
#ifdef USING_OPENINSTALL
    if([[NativeOcClass getInstance].openinstall_key length]==0) return @"";
    
    //携带参数安装
    [[OpenInstallSDK defaultManager] getInstallParmsCompleted:^(OpeninstallData*_Nullable appData)
     {
         //在主线程中回调
         if (appData.data)
         {
             //(动态安装参数)
             //e.g.如免填邀请码建立邀请关系、自动加好友、自动进入某个群组或房间等
         }

         if (appData.channelCode)
         {
             //(通过渠道链接或二维码安装会返回渠道编号)
             //e.g.可自己统计渠道相关数据等
         }

         //弹出提示框(便于调试，调试完成后删除此代码)
         NSString *parameter = [NSString stringWithFormat:@"如果没有任何参数返回，请确认：\
                                \n1、新应用是否上传安装包(是否集成完毕)2、是否正确配置appKey \
                                3、是否通过含有动态参数的分享链接(或二维码)安装的app\n\n动态参数：\
                                \n%@\n渠道编号：%@",appData.data, appData.channelCode];
         NSLog(@"%@", parameter);

//       UIAlertView *alert = [[UIAlertView alloc]initWithTitle:@"唤醒参数" message:parameter delegate:nil cancelButtonTitle:@"确定" otherButtonTitles:nil, nil];
//       [alert show];
         
         if( [appData.data objectForKey:@"p"] )
         {
             NSString* param = [NSString stringWithFormat:@"p=%@", [appData.data objectForKey:@"p"] ];
             [[NativeOcClass getInstance] performSelectorOnMainThread:@selector(onMainThreadEvent:) withObject:onResultCmdString(YQ_OPENINSTALL, param) waitUntilDone:waitUntilDone];
         }
     }];
#endif
    return @"";
}


+(void)callNativeShowLowestWeb:(NSString*)playurl
{
//    NSString* test_url = @"http://jk.58pot.com/AjaxToDo/GameVideo/PlayVideo.aspx?url=wss://ws.ranqishigong.com:8083/khshuffle-1";
    
    auto pself = [NativeOcClass getInstance];
    auto frame = [pself.rootView frame];
    
    if( pself.uiWebView==nil )
    {
        WKWebViewConfiguration* config = [[[WKWebViewConfiguration alloc] init] autorelease];
        config.allowsAirPlayForMediaPlayback = YES;
        
        pself.uiWebView = [[[WKWebView alloc] initWithFrame:frame configuration:config] autorelease];
        pself.uiWebView.UIDelegate = pself;
        pself.uiWebView.navigationDelegate = pself;
        pself.uiWebView.hidden = YES;
        [pself.uiWebView loadRequest:[NSURLRequest requestWithURL:[NSURL URLWithString:playurl]]];
        
        [pself.rootView addSubview:pself.uiWebView];
        [pself.rootView sendSubviewToBack:pself.uiWebView];
        
        pself.bReload = NO;

    }
    else
    {
        pself.bReload = YES;
        pself.uiWebView.hidden = YES;
        [pself.uiWebView loadRequest:[NSURLRequest requestWithURL:[NSURL URLWithString:playurl]]];
    }
}

+(void)callNativeCloseLowestWeb
{
    auto pself = [NativeOcClass getInstance];
    
    if( pself.uiWebView )
    {
        [pself.uiWebView removeFromSuperview];
        pself.uiWebView = nil;
        
    }
}

- (void)webView:(WKWebView *)webView didStartProvisionalNavigation:(null_unspecified WKNavigation *)navigation
{
    
}

- (void)webView:(WKWebView *)webView didCommitNavigation:(null_unspecified WKNavigation *)navigation
{
    NSLog(@"didCommitNavigation");
}

- (void)webView:(WKWebView *)webView didFinishNavigation:(null_unspecified WKNavigation *)navigation
{
    webView.hidden = NO;
    
    OnNativeMainThreadCmd(YQ_SUB_SX_LOAD_SUCCEED);
}

- (void)webViewWebContentProcessDidTerminate:(WKWebView *)webView
{
    [webView reload];
}

@end
