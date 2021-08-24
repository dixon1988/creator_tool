//
//  RotateNavigationController.m
//  RotateScreen
//
//  Created by obo on 16/1/28.
//  Copyright © 2016年 obo. All rights reserved.
//

#import "RotateNavigationController.h"

#ifdef USING_SHANFU
#import <ChatKit/ChatSDK.h>
#endif

#import <CommonCrypto/CommonDigest.h>
#import "NativeClass.h"


static const char encodingTable[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

@implementation RotateNavigationController

@synthesize motionManager;
@synthesize motionInterval;

static RotateNavigationController* s_pNavigationController = nil;
+(id)getInstance
{
    return s_pNavigationController;
}

//设备方向
-(void)OnInit
{
    [[NSNotificationCenter defaultCenter] addObserver:self selector:@selector(orientChange:) name:UIDeviceOrientationDidChangeNotification object:nil];
}

//开始监听
-(void)starMotionManager
{
    if( self.motionManager==nil )
    {
        self.motionManager = [[[CMMotionManager alloc] init] autorelease];
        self.motionManager.deviceMotionUpdateInterval = 1/10.0;
        if(self.motionManager.deviceMotionAvailable)
        {
            [self.motionManager startDeviceMotionUpdatesToQueue:[NSOperationQueue currentQueue] withHandler:^(CMDeviceMotion* _Nullable motion, NSError* _Nullable error)
             {
                 [self handleDeviceMotion:motion];
             }];
        }
    }
}

-(void)updateMotionManager
{
    if( self.motionManager==nil ) return;
    [self.motionManager startDeviceMotionUpdatesToQueue:[NSOperationQueue currentQueue] withHandler:^(CMDeviceMotion* _Nullable motion, NSError* _Nullable error)
     {
         [self handleDeviceMotion:motion];
     }];
}

//停止监听
-(void)stopMotionManager
{
    [self.motionManager stopDeviceMotionUpdates];
    self.motionManager=nil;
}

-(void)handleDeviceMotion:(CMDeviceMotion*)motion
{
    double x = motion.gravity.x;
    double y = motion.gravity.y;
    
    //竖屏
    if( fabs(y) >= fabs(x) )
    {
        if( fabs(y)>0.7 )
        {
            if( UIInterfaceOrientationIsLandscape(self.interfaceOrientation) )
            {
                [NativeOcClass callNativeMotionManagerCallback:YQ_SUB_HOMEDOWN];
            }
        }
    }
    //横屏
    else
    {
        if(fabs(x)>0.7)
        {
            if( UIInterfaceOrientationIsPortrait(self.interfaceOrientation) )
            {
                [NativeOcClass callNativeMotionManagerCallback:YQ_SUB_HOMESIDE];
            }
        }
    }
}

- (void)orientChange:(NSNotification *)noti
{
    UIDeviceOrientation orient = [UIDevice currentDevice].orientation;
    switch (orient)
    {
        case UIDeviceOrientationPortrait:
        {
            break;
        }
        case UIDeviceOrientationLandscapeLeft:
        {
            if( UIInterfaceOrientationIsLandscape(self.interfaceOrientation) )
            {
                [RotateNavigationController changeScreenType:UIInterfaceOrientationLandscapeRight];
            }
            break;
        }
        case UIDeviceOrientationPortraitUpsideDown:
        {
            
            break;
        }
        case UIDeviceOrientationLandscapeRight:
        {
            if( UIInterfaceOrientationIsLandscape(self.interfaceOrientation) )
            {
                [RotateNavigationController changeScreenType:UIInterfaceOrientationLandscapeLeft];
            }
            break;
        }
        default:
            break;
    }
}

//跳转评价页
+(void)evaluate
{

}

//取消按钮监听
- (void)productViewControllerDidFinish:(SKStoreProductViewController *)viewController
{
    [viewController dismissViewControllerAnimated:YES completion:^{}];
    
//    [self dismissViewControllerAnimated:YES completion:^{
//    }];
}

+(void)changeScreenType:(UIInterfaceOrientation)cbOrientation
{
    RotateNavigationController *navigationController = [RotateNavigationController getInstance];
    
    //切换rootViewController的旋转方向
    if( cbOrientation==UIInterfaceOrientationLandscapeRight )
    {
        navigationController.interfaceOrientation = cbOrientation;
        navigationController.interfaceOrientationMask = UIInterfaceOrientationMaskLandscape;
        
        //设置屏幕的转向为横屏
        [[UIDevice currentDevice] setValue:@(UIDeviceOrientationLandscapeLeft) forKey:@"orientation"];
    }
    else if( cbOrientation==UIInterfaceOrientationLandscapeLeft )
    {
        navigationController.interfaceOrientation = cbOrientation;
        navigationController.interfaceOrientationMask = UIInterfaceOrientationMaskLandscape;
        
        //设置屏幕的转向为横屏
        [[UIDevice currentDevice] setValue:@(UIDeviceOrientationLandscapeRight) forKey:@"orientation"];
    }
    else
    {
        navigationController.interfaceOrientation = UIInterfaceOrientationPortrait;
        navigationController.interfaceOrientationMask = UIInterfaceOrientationMaskPortrait;
        
        //设置屏幕的转向为竖屏
        [[UIDevice currentDevice] setValue:@(UIDeviceOrientationPortrait) forKey:@"orientation"];
    }
    //刷新
    [UIViewController attemptRotationToDeviceOrientation];
}

+(void)resetScreenType
{
    RotateNavigationController *navigationController = [RotateNavigationController getInstance];
    
    UIInterfaceOrientation cbOrientation = [navigationController interfaceOrientation];
    
    //切换rootViewController的旋转方向
    if( cbOrientation==UIInterfaceOrientationLandscapeRight || cbOrientation==UIInterfaceOrientationLandscapeLeft )
    {
        navigationController.interfaceOrientation = cbOrientation;
        navigationController.interfaceOrientationMask = UIInterfaceOrientationMaskLandscape;
        
        //设置屏幕的转向为横屏
        [[UIDevice currentDevice] setValue:@(UIDeviceOrientationLandscapeLeft) forKey:@"orientation"];
    }
    else
    {
        navigationController.interfaceOrientation = UIInterfaceOrientationPortrait;
        navigationController.interfaceOrientationMask = UIInterfaceOrientationMaskPortrait;
        
        //设置屏幕的转向为竖屏
        [[UIDevice currentDevice] setValue:@(UIDeviceOrientationPortrait) forKey:@"orientation"];
    }
    //刷新
    [UIViewController attemptRotationToDeviceOrientation];
}

- (instancetype)initWithRootViewController:(UIViewController *)rootViewController
{
    self = [super initWithRootViewController:rootViewController];
    
    if (self)
    {
        self.interfaceOrientation = UIInterfaceOrientationLandscapeLeft;
        self.interfaceOrientationMask = UIInterfaceOrientationMaskLandscape;
    }
    
    if( s_pNavigationController==nil )
    {
        s_pNavigationController = self;
    }
    
    return self;
}


//设置是否允许自动旋转
- (BOOL)shouldAutorotate
{
    return YES;
}

//设置支持的屏幕旋转方向
- (UIInterfaceOrientationMask)supportedInterfaceOrientations
{
    return self.interfaceOrientationMask;
}

//设置presentation方式展示的屏幕方向
- (UIInterfaceOrientation)preferredInterfaceOrientationForPresentation
{
    return self.interfaceOrientation;
}


#ifdef USING_SHANFU
//拉起chartkit
+(NSString *)getNowTimeTimestamp{
    NSDateFormatter *formatter = [[NSDateFormatter alloc] init] ;
    
    [formatter setDateStyle:NSDateFormatterMediumStyle];
    
    [formatter setTimeStyle:NSDateFormatterShortStyle];
    
    [formatter setDateFormat:@"YYYY-MM-dd HH:mm:ss"]; // ----------设置你想要的格式,hh与HH的区别:分别表示12小时制,24小时制
    
    //设置时区,这个对于时间的处理有时很重要
    
    NSTimeZone* timeZone = [NSTimeZone timeZoneWithName:@"Asia/Beijing"];
    
    [formatter setTimeZone:timeZone];
    
    NSDate *datenow = [NSDate date];//现在时间,你可以输出来看下是什么格式
    
    NSString *timeSp = [NSString stringWithFormat:@"%ld", (long)[datenow timeIntervalSince1970]];
    
    return timeSp;
}
+(NSString*)presignString:(NSMutableDictionary*)params secret:(NSString*)secret{
    NSMutableArray *allKeys = [params.allKeys mutableCopy];
    if(allKeys.count==0){
        return @"";
    }
    [allKeys sortUsingSelector:@selector(compare:)];
    NSMutableArray *keyValue = [NSMutableArray array];
    for (NSString* key in allKeys) {
        //        if([key isEqualToString:@"id"] && [params[key] isEqualToString:@"-1"]){
        //            continue;
        //        }
        [keyValue addObject:[NSString stringWithFormat:@"%@=%@", key, params[key]]];
    }
    NSString* param = [[keyValue componentsJoinedByString:@"&"] stringByTrimmingCharactersInSet:[NSCharacterSet whitespaceCharacterSet]] ;
    
    NSString *saltString = [NSString stringWithFormat:@"%@%@", param, secret];
    NSString *presignString = [self MD5:saltString];
    return presignString;
}

+(NSString*) MD5:(NSString*)str {
    const char *cStr = [str UTF8String];
    unsigned char digest[CC_MD5_DIGEST_LENGTH];
    CC_MD5( cStr, strlen(cStr), digest );
    
    NSMutableString *output = [NSMutableString stringWithCapacity:CC_MD5_DIGEST_LENGTH * 2];
    
    for(int i = 0; i < CC_MD5_DIGEST_LENGTH; i++){
        [output appendFormat:@"%02x", digest[i]];
    }
    return output;
}

+(void)callNativeHomeChat0:(NSString*)url p1:(NSString*)agentUserId p2:(NSString*)app_key p3:(NSString*)szChannelId p4:(NSString*)strUserID p5:(NSString*)strNameUtf8 p6:(NSString*)szMachineId p7:(NSString*)key
{
    //测试参数，实际场景这些参数都要从服务端拉取
    NSMutableDictionary *params = [@{
                                     @"id":agentUserId
                                     ,@"app_key":app_key
                                     ,@"app_id":szChannelId
                                     ,@"user_id":strUserID
                                     ,@"user_name":strNameUtf8
                                     ,@"device_id":szMachineId
                                     ,@"timestamp": [self getNowTimeTimestamp]
                                     } mutableCopy];
    
    params[@"sign"] = [self presignString:params secret:key];
    
    //唤起聊天消息界面 授权页面url需要传递过来
    [ChatSDK showMessageChat:url params:params isLandscape:TRUE];
}
#endif

@end
