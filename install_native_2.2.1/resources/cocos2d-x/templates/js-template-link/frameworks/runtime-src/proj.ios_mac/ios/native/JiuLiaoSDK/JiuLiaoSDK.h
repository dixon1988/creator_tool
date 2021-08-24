//
//  JiuLiaoSDK.h
//  Mata
//
//  Created by Youssef on 2017/12/20.
//  Copyright © 2017年 yunio. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface JiuLiaoSDK : NSObject

+ (instancetype) shareInstance;

/**
 判断久聊是否可以打开

 @return 返回是否可以打开
 */
+ (BOOL)canOpenJiuLiao;

/**
 久聊的URLSchemes
 
 @return 返回久聊的URLSchemes
 */
+ (NSString *)jiuliaoURLSchemes;

/**
 将游戏分享到久聊

 @param title 分享的题目(分享气泡上最大的字),长度不能超过1K
 @param desc 描述内容,长度不能超过1K
 @param appDownloadUrl 你的App的下载链接安卓
 @param iOSDownloadUrl 你的App的下载链接iOS
 @param androidBackURL 你的App的URL Schemes (安卓)
 @param iOSBackUrl 你的App的URL Schemes (iOS)
 */
- (void)shareToJiuLiaoWithTitle:(NSString *)title description:(NSString *)desc appDownloadUrl:(NSString *)appDownloadUrl iOSDownloadUrl:(NSString *)iOSDownloadUrl androidBackURL:(NSString *)androidBackURL iOSBackUrl:(NSString *)iOSBackUrl;

/**
 向久聊分享图片
 @param images 需要分享的图片
 */
- (void)shareImages:(NSArray<UIImage *> *)images;


/**
 跳转到久聊转账
 @param gameUserId 游戏玩家的账号
 @param gameName 游戏包名称
 */
- (void)goToJiuLiaoTransfer:(NSString*)gameUserId gameName:(NSString*)gameName;

/**
 跳转到久聊支付
 @param gameUserId 游戏玩家的账号
 @param gameName 游戏包名称
 @param amoutMoney 充值金额 单位：分
 @param orderId 充值订单号，游戏为每笔充值订单生成的唯一订单号
 */
- (void)goToJiuLiaoPay:(NSString*)gameUserId gameName:(NSString*) gameName amoutMoney:(int)amoutMoney orderId:(NSString*) orderId;
@end
