//
//  ChatSDK.h
//  Chat
//
//  Created by User on 2019/3/7.
//  Copyright © 2019年 User. All rights reserved.
//

#import <Foundation/Foundation.h>

@class UIViewController;

NS_ASSUME_NONNULL_BEGIN

@interface ChatSDK : NSObject
/**
 调用此方法唤起聊天界面，自动登录
 POST xxx/index/login/auto_login
 参数params包括:
 id           登录后自动对话的用户id(非必须)， 场景: 存在时，用户点击一个代理商后直接和代理商聊天，不存在时显示聊天记录
 app_key      分配的app_key (项目组id)
 app_id       app id
 user_id      客户端用户ID (客户端提供)
 user_name    客户端用户昵称 (客户端提供)
 device_id    客户端设备码 (客户端提供)
 timestamp    客户端时间戳(秒)
 sign         签名,为保证安全，在项目组服务器端做好签名后再获取传入
 签名规则:
 先对所有参数的key进行字符串ASCII码升序排序
 然后拼接成带签名的字符串 k1=v1&k2=v2
 在待签名的字符串后面拼接上密钥（一个app_key 对应一个密钥）进行 md5 得到小写 sign
 */

+ (void)showMessageChat: (NSString*)url params:(NSDictionary*)params isLandscape:(BOOL) isLandscape;

@end

NS_ASSUME_NONNULL_END
