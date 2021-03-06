/****************************************************************************
 Copyright (c) 2010-2013 cocos2d-x.org
 Copyright (c) 2013-2016 Chukong Technologies Inc.
 Copyright (c) 2017-2018 Xiamen Yaji Software Co., Ltd.
 
 http://www.cocos2d-x.org
 
 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:
 
 The above copyright notice and this permission notice shall be included in
 all copies or substantial portions of the Software.
 
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 THE SOFTWARE.
 ****************************************************************************/

#import "AppController.h"
#import "IAPStore.h"

#import "cocos2d.h"
#import "AppDelegate.h"
#import "RootViewController.h"
#import "SDKWrapper.h"
#import "platform/ios/CCEAGLView-ios.h"

#import "OCDefine.h"
#import "NativeClass.h"
#import "RotateNavigationController.h"

using namespace cocos2d;

@implementation AppController

Application* app = nullptr;
@synthesize window;

#pragma mark -
#pragma mark Application lifecycle

- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions {
    [[SDKWrapper getInstance] application:application didFinishLaunchingWithOptions:launchOptions];
    // Add the view controller's view to the window and display.
    float scale = [[UIScreen mainScreen] scale];
    CGRect bounds = [[UIScreen mainScreen] bounds];
    window = [[UIWindow alloc] initWithFrame: bounds];
    
    // cocos2d application instance
    app = new AppDelegate(bounds.size.width * scale, bounds.size.height * scale);
    app->setMultitouch(true);
    
    RotateNavigationController *viewController = [[RotateNavigationController alloc] initWithRootViewController:[[RootViewController alloc] init]];
    [viewController setNavigationBarHidden:YES];
    viewController.wantsFullScreenLayout = YES;
    viewController.edgesForExtendedLayout = UIRectEdgeAll;
    [viewController OnInit];

    // Set RootViewController to window
    if ( [[UIDevice currentDevice].systemVersion floatValue] < 6.0)
    {
        // warning: addSubView doesn't work on iOS6
        [window addSubview: viewController.view];
    }
    else
    {
        // use this method on ios6
        [window setRootViewController:viewController];
    }
    
    auto cocoView = (UIView*)app->getView();
    [NativeOcClass getInstance].cocosView = cocoView;
    [NativeOcClass getInstance].rootView = viewController.view;
    cocoView.backgroundColor = [UIColor clearColor];
    
    [window makeKeyAndVisible];
    
    [[UIApplication sharedApplication] setStatusBarHidden:YES];
    [[UIApplication sharedApplication] setIdleTimerDisabled:YES];
    
    //??????????????????
    [NativeOcClass callNativebByInitYunCeng];
    
    //run the cocos2d-x game scene
    app->start();
    
#ifdef USING_WX
    id info_dic = [[NSBundle mainBundle] infoDictionary];
    id url_ary = [info_dic objectForKey:@"CFBundleURLTypes"];
    for ( id url_info in url_ary)
    {
        if( [[url_info objectForKey:@"CFBundleURLName"] compare:@"weixin"]==NSOrderedSame )
        {
            id info_ary = [url_info objectForKey:@"CFBundleURLSchemes"];
            if([info_ary count]>0)
            {
               [NativeOcClass getInstance].wx_appid = info_ary[0];
            }
            
            if([info_ary count]>1)
            {
                [NativeOcClass getInstance].wx_secret = info_ary[1];
            }
        }
        
        if( [[url_info objectForKey:@"CFBundleURLName"] compare:@"openinstall"]==NSOrderedSame )
        {
            id info_ary = [url_info objectForKey:@"CFBundleURLSchemes"];
            if([info_ary count]>0)
            {
                [NativeOcClass getInstance].openinstall_key = info_ary[0];
            }
        }
    }
    
    if([[NativeOcClass getInstance].wx_appid length]>0){
        [WXApi registerApp:[NativeOcClass getInstance].wx_appid];
    }
#endif
    
    //????????????
    [CIAPStore PayCompleteTransaction:true id:nil reqUrl:nil encoding:nil];
    
#ifdef USING_OPENINSTALL
    if([[NativeOcClass getInstance].openinstall_key length]>0){
        [OpenInstallSDK initWithDelegate:self];
    }
#endif

    return YES;
}

-(BOOL)application:(UIApplication *)application handleOpenURL:(NSURL *)url
{
#ifdef USING_OPENINSTALL
    //??????????????????OpenInstall URL Scheme ??????App
    if  ([OpenInstallSDK handLinkURL:url]){//??????
        return YES;
    }
#endif
    
#ifdef USING_WX
    return [WXApi handleOpenURL:url delegate:self];
#else
    return true;
#endif
}

-(BOOL)application : (UIApplication*)application openURL : (NSURL *)url sourceApplication : (NSString *)sourceApplication annotation:(id)annotation
{
#ifdef USING_OPENINSTALL
    //??????????????????OpenInstall URL Scheme ??????App
    if  ([OpenInstallSDK handLinkURL:url]){//??????
        return YES;
    }
#endif
    
#ifdef USING_WX
    if([url.host isEqualToString:@"oauth"])
    {
        //????????????
        [WXApi handleOpenURL:url delegate:self];
    }
    //????????????
    else if( [url.host isEqualToString:@"platformId=wechat"] )
    {
        //????????????
        [WXApi handleOpenURL:url delegate:self];
    }
    
    //????????????
    else if( [url.host isEqualToString:@"wechat"] )
    {
        
    }
    //????????????
    else if( [url.host isEqualToString:@"one.app"] )
    {
        NSLog(@"oone.app");
    }
#endif
   
    NSString* openurl = url.absoluteString;
    NSRange range = [openurl rangeOfString:@"://"];
    NSString* param = [openurl substringWithRange:NSMakeRange(range.location+range.length, openurl.length-range.location-range.length)];
    
#ifdef USING_WX
    #else
        OnNativeMainThreadCmdString(YQ_SUB_OPENSELFAPP, [param copy]);
#endif
    
    
    return TRUE;
}

#ifdef USING_WX
-(void) onResp:(BaseResp*) resp
{
    //NSString *strMsg = [NSString stringWithFormat:@"errcode:%d", resp.errCode];
    

    //????????????
    if( [resp isKindOfClass:[SendMessageToWXResp class]])
    {
        //??????
        if( resp.errCode==0 )
        {
            //????????????
            [[NativeOcClass getInstance] setEventResult:YQ_SUB_WXSHARE_SUCCEED];
            
            OnNativeMainThreadCmd(YQ_SUB_WXSHARE_SUCCEED);
        }
        
        //??????
        else
        {
            //????????????
            [[NativeOcClass getInstance] setEventResult:YQ_SUB_WXSHARE_FAILURE];
            
            OnNativeMainThreadCmd(YQ_SUB_WXSHARE_FAILURE);
        }
    }
    
    else
    {
        //??????????????????
        //????????????
        if( resp.errCode==0 )
        {
            //?????? code ?????? access_token
            SendAuthResp* pAuthResp = (SendAuthResp*)resp;
            NSString* pAutoCode = [pAuthResp code];
            const char* code = [pAutoCode UTF8String];
            
            const char* wxappid = [[NativeOcClass getInstance].wx_appid UTF8String];
            const char* wxsecret = [[NativeOcClass getInstance].wx_secret UTF8String];
            
            std::stringstream streamUrl("");
            streamUrl<< "https://api.weixin.qq.com/sns/oauth2/access_token?appid="<< wxappid << "&secret=" << wxsecret << "&code=" << code << "&grant_type=authorization_code";
            
            //??????????????????url
            NSURL *url = [NSURL URLWithString:[NSString stringWithUTF8String:streamUrl.str().c_str()]];
            //????????????????????????
            NSURLRequest *request = [[NSURLRequest alloc] initWithURL:url cachePolicy:NSURLRequestUseProtocolCachePolicy timeoutInterval:10];
            //???????????????????????????
            NSURLConnection *connection = [[NSURLConnection alloc] initWithRequest:request delegate:self];
            
            //????????????
            [[NativeOcClass getInstance] setEventResult:YQ_SUB_WXLOGON_SUCCEED];
            
            OnNativeMainThreadCmd(YQ_SUB_WXLOGON_SUCCEED);
            
            //[[NativeOcClass getInstance] performSelectorOnMainThread:@selector(onMainThreadEvent:) withObject:onResultCmd(YQ_SUB_WXLOGON_SUCCEED) waitUntilDone:NO];
            
        }
        else
        {
            [[NativeOcClass getInstance] setEventResult:YQ_SUB_WXLOGON_FAILURE];
            
            OnNativeMainThreadCmd(YQ_SUB_WXLOGON_FAILURE);
            
            //[[NativeOcClass getInstance] performSelectorOnMainThread:@selector(onMainThreadEvent:) withObject:onResultCmd(YQ_SUB_WXLOGON_FAILURE) waitUntilDone:NO];
        }
    }
}
#endif
//????????????????????????????????????????????????
- (void)connection:(NSURLConnection *)connection didReceiveResponse:(NSURLResponse *)response
{
    NSHTTPURLResponse *res = (NSHTTPURLResponse *)response;
    NSLog(@"%@",[res allHeaderFields]);
}
//??????????????????????????????????????????????????????????????????????????????????????????
-(void)connection:(NSURLConnection *)connection didReceiveData:(NSData *)data
{
    //NSString *jsonData = [[[NSString alloc] initWithData:data encoding:NSUTF8StringEncoding] autorelease];
#ifdef USING_WX
    NSError* error;
    id jsonObject = [NSJSONSerialization JSONObjectWithData:data options:NSJSONReadingAllowFragments error:&error];
    
    [NativeOcClass getInstance].wxToken = [jsonObject objectForKey:@"access_token"];
    [NativeOcClass getInstance].wxOpenid = [jsonObject objectForKey:@"openid"];
    [NativeOcClass getInstance].wxRefreshToken = [jsonObject objectForKey:@"refresh_token"];
    
    //token????????????
    [[NativeOcClass getInstance] setEventResult:YQ_SUB_WXLOGON_TOKEN];
    
    OnNativeMainThreadCmd(YQ_SUB_WXLOGON_TOKEN);
#endif
}
//?????????????????????????????????
-(void)connectionDidFinishLoading:(NSURLConnection *)connection
{
    
}
//??????????????????????????????????????????????????????????????????????????????????????????
-(void)connection:(NSURLConnection *)connection didFailWithError:(NSError *)error
{
    NSLog(@"%@",[error localizedDescription]);
}

- (void)applicationWillResignActive:(UIApplication *)application {
    /*
     Sent when the application is about to move from active to inactive state. This can occur for certain types of temporary interruptions (such as an incoming phone call or SMS message) or when the user quits the application and it begins the transition to the background state.
     Use this method to pause ongoing tasks, disable timers, and throttle down OpenGL ES frame rates. Games should use this method to pause the game.
     */
    [[SDKWrapper getInstance] applicationWillResignActive:application];
}

- (void)applicationDidBecomeActive:(UIApplication *)application {
    /*
     Restart any tasks that were paused (or not yet started) while the application was inactive. If the application was previously in the background, optionally refresh the user interface.
     */
    [[SDKWrapper getInstance] applicationDidBecomeActive:application];
    if( [[NativeOcClass getInstance] eventResult]==YQ_SUB_EVENT_BEGIN )
    {
        [[NativeOcClass getInstance] setEventResult:YQ_SUB_EVENT_CANCEL];
        
        OnNativeMainThreadCmd(YQ_SUB_EVENT_CANCEL);
    }
}

- (void)applicationDidEnterBackground:(UIApplication *)application {
    /*
     Use this method to release shared resources, save user data, invalidate timers, and store enough application state information to restore your application to its current state in case it is terminated later.
     If your application supports background execution, called instead of applicationWillTerminate: when the user quits.
     */
    [[SDKWrapper getInstance] applicationDidEnterBackground:application];
    app->applicationDidEnterBackground();
    
}

- (void)applicationWillEnterForeground:(UIApplication *)application {
    /*
     Called as part of  transition from the background to the inactive state: here you can undo many of the changes made on entering the background.
     */
    [[SDKWrapper getInstance] applicationWillEnterForeground:application];
    app->applicationWillEnterForeground();
    
}

- (void)applicationWillTerminate:(UIApplication *)application
{
    [[SDKWrapper getInstance] applicationWillTerminate:application];
    delete app;
    app = nil;
}

- (BOOL)application:(UIApplication *)application continueUserActivity:(NSUserActivity *)userActivity restorationHandler:(void (^)(NSArray * _Nullable))restorationHandler{
    
#ifdef USING_OPENINSTALL
    //??????????????????OpenInstall Universal Link ??????App
    if ([OpenInstallSDK continueUserActivity:userActivity]){//???????????????Universal link ??????????????????
        return YES;
    }
#endif
    //????????????????????????
    return YES;
}

#pragma mark -
#pragma mark Memory management

- (void)applicationDidReceiveMemoryWarning:(UIApplication *)application {
    /*
     Free up as much memory as possible by purging cached data objects that can be recreated (or reloaded from disk) later.
     */
}

#ifdef USING_OPENINSTALL
//??????OpenInstall??????????????????App?????????????????????????????????????????????????????????App??????????????????????????????
-(void)getWakeUpParams:(OpeninstallData *)appData
{
    if (appData.data)
    {
        //(??????????????????)
        //e.g.?????????????????????????????????????????????????????????????????????????????????????????????
    }
    if (appData.channelCode)
    {
        //(?????????????????????????????????????????????????????????)
        //e.g.????????????????????????????????????
    }
    
    //???????????????(?????????????????????????????????????????????)
//    NSLog(@"OpenInstallSDK:\n???????????????%@;\n???????????????%@",appData.data, appData.channelCode);
//    NSString *parameter = [NSString stringWithFormat:@"?????????????????????????????????????????????\n?????????????????????????????????????????????(????????????)?????????app\n\n???????????????\n%@\n???????????????%@",appData.data,appData.channelCode];
//    UIAlertView *alert = [[UIAlertView alloc]initWithTitle:@"????????????" message:parameter delegate:nil cancelButtonTitle:@"??????" otherButtonTitles:nil, nil];
//    [alert show];
}
#endif

@end
