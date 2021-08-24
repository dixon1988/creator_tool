//
//  JiuLiaoSDK.m
//  Mata
//
//  Created by Youssef on 2017/12/20.
//  Copyright © 2017年 yunio. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "JiuLiaoSDK.h"
#import "NSData+AES.h"
/*******************需要配置的地方*************************************************/

// 久聊信息传输的加密的密钥
static NSString *jiuliaoSDKSecurity = @"909848C30844A1D64BD19983849A3481";

// 久聊服务器分配给本应用的的App Id
static const NSString *jiuliaoAppID = @"200002";//@"kl1hhjqd1amf3kse5e";

//久聊的AppStore下载地址
static const NSString *jiuliaoDownloadUrl = @"https://itunes.apple.com/us/app/久聊/id1389695427?l=zh&ls=1&mt=8";

//久聊的URLTypes，需要加在工程白名单中，在info.plist属性LSApplicationQueriesSchemes添加 “jiuliao”
static const NSString *jiuliaoRULSchemes = @"jiuliao://";

//游戏的URLSchemes，用在分享成功后跳转返回地址
static const NSString *backURL = @"testdemo://";
/********************************************************************************/

static JiuLiaoSDK * _instance = nil;
@implementation JiuLiaoSDK
+ (instancetype)shareInstance {
    static dispatch_once_t onceToken ;
    dispatch_once(&onceToken, ^{
        _instance = [[super allocWithZone:NULL] init] ;
    }) ;
    
    return _instance ;
}

+ (id)allocWithZone:(struct _NSZone *)zone {
    return [JiuLiaoSDK shareInstance] ;
}

- (id)copyWithZone:(struct _NSZone *)zone {
    return [JiuLiaoSDK shareInstance] ;
}

+ (BOOL)canOpenJiuLiao {
    return [[UIApplication sharedApplication] canOpenURL:[NSURL URLWithString:[self jiuliaoURLSchemes]]];
}

+(NSString *)jiuliaoURLSchemes{
    return jiuliaoRULSchemes;
}

- (void)shareToJiuLiaoWithTitle:(NSString *)title description:(NSString *)desc appDownloadUrl:(NSString *)appDownloadUrl iOSDownloadUrl:(NSString *)iOSDownloadUrl androidBackURL:(NSString *)androidBackURL iOSBackUrl:(NSString *)iOSBackUrl {

    NSDictionary * dic = @{@"title": title,
                           @"desc": desc,
                           @"appDownloadUrl": appDownloadUrl,
                           @"iOSDownloadUrl": iOSDownloadUrl,
                           @"androidBackURL": androidBackURL,
                           @"iOSBackUrl"    : iOSBackUrl};
    NSData * data = [NSJSONSerialization dataWithJSONObject:dic options:NSJSONWritingPrettyPrinted error:nil];
    data = [data AES256EncryptWithKey:jiuliaoSDKSecurity];
    UInt8 buf[data.length];
    [data getBytes:buf length:data.length];
    NSString * dataString = @"";
    for (int i = 0; i < data.length; ++i) {
        UInt8 by = buf[i];
        dataString = [dataString stringByAppendingString:[NSString stringWithFormat:@"%02x", by]];
    }
    if ([JiuLiaoSDK canOpenJiuLiao]) {
        NSString * strURL = [NSString stringWithFormat:@"%@%@&%@", jiuliaoRULSchemes, jiuliaoAppID, dataString];
        NSURL * url = [NSURL URLWithString:strURL];
        if (![[UIApplication sharedApplication] openURL:url]) {
            NSLog(@"JiuLiaoSDK Error: can not open JiuLiao");
        }
    } else {
        [self installJiuLiao];
        NSLog(@"JiuLiaoSDK Error: can not open JiuLiao");
    }
}

- (void)installJiuLiao {
    NSURL *url = [NSURL URLWithString:[jiuliaoDownloadUrl stringByAddingPercentEncodingWithAllowedCharacters:[NSCharacterSet URLQueryAllowedCharacterSet]]];
    if ([[UIApplication sharedApplication] canOpenURL: url]) {
        [[UIApplication sharedApplication] openURL:url];
    } else {
        NSLog(@"Can not download JiuLiao!");
    }
}

- (void)shareImages:(NSArray<UIImage *> *)images {
    if (images.count == 0) {
        NSLog(@"You may need input a image at least!");
        return;
    }

    if ([JiuLiaoSDK canOpenJiuLiao]) {

        UIPasteboard *pasteboard = [UIPasteboard generalPasteboard];
        pasteboard.images = images;
       
        [[UIApplication sharedApplication] openURL:[NSURL URLWithString:[NSString stringWithFormat:@"%@%@&shareImages%@", [JiuLiaoSDK jiuliaoURLSchemes], jiuliaoAppID, backURL]]];
    } else {
        [self installJiuLiao];
        NSLog(@"JiuLiaoSDK Error: can not open JiuLiao");
    }
}

- (void)goToJiuLiaoTransfer:(NSString*)gameUserId gameName:(NSString*) gameName {
    NSDictionary * dic = @{@"gameName":gameName,
                           @"gameUserId": gameUserId,
                           @"iOSBackUrl":backURL};
    
    NSData * data = [NSJSONSerialization dataWithJSONObject:dic options:NSJSONWritingPrettyPrinted error:nil];
    data = [data AES256EncryptWithKey:jiuliaoSDKSecurity];
    UInt8 buf[data.length];
    [data getBytes:buf length:data.length];
    NSString * dataString = @"";
    for (int i = 0; i < data.length; ++i) {
        UInt8 by = buf[i];
        dataString = [dataString stringByAppendingString:[NSString stringWithFormat:@"%02x", by]];
    }
    
    if ([JiuLiaoSDK canOpenJiuLiao]) {
        [[UIApplication sharedApplication] openURL:[NSURL URLWithString:[NSString stringWithFormat:@"%@%@&JiuLiaoTransfer%@", [JiuLiaoSDK jiuliaoURLSchemes], jiuliaoAppID, dataString]]];
    } else {
        [self installJiuLiao];
        NSLog(@"JiuLiaoSDK Error: can not open JiuLiao");
    }
}

- (void)goToJiuLiaoPay:(NSString*)gameUserId gameName:(NSString*) gameName amoutMoney:(int)amoutMoney orderId:(NSString*) orderId{
    NSDictionary * dic = @{@"gameName": gameName,
                           @"gameUserId": gameUserId,
                           @"gameMoney": [NSString stringWithFormat:@"%i",amoutMoney],
                           @"orderId": orderId,
                           @"iOSBackUrl":backURL};
    
    NSData * data = [NSJSONSerialization dataWithJSONObject:dic options:NSJSONWritingPrettyPrinted error:nil];
    data = [data AES256EncryptWithKey:jiuliaoSDKSecurity];
    UInt8 buf[data.length];
    [data getBytes:buf length:data.length];
    NSString * dataString = @"";
    for (int i = 0; i < data.length; ++i) {
        UInt8 by = buf[i];
        dataString = [dataString stringByAppendingString:[NSString stringWithFormat:@"%02x", by]];
    }
    
    if ([JiuLiaoSDK canOpenJiuLiao]) {
        [[UIApplication sharedApplication] openURL:[NSURL URLWithString:[NSString stringWithFormat:@"%@%@&JiuLiaoPay%@", [JiuLiaoSDK jiuliaoURLSchemes], jiuliaoAppID, dataString]]];
    } else {
        [self installJiuLiao];
        NSLog(@"JiuLiaoSDK Error: can not open JiuLiao");
    }
}

@end

