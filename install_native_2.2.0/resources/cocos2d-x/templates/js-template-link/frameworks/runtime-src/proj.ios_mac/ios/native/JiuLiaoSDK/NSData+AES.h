//
//  NSData+AES.h
//  Mata
//
//  Created by Youssef on 2017/12/20.
//  Copyright © 2017年 yunio. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface NSData (AES)
//加密
- (NSData *)AES256EncryptWithKey:(NSString *)key;

//解密
- (NSData *)AES256DecryptWithKey:(NSString *)key;

@end
