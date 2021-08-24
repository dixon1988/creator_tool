//
//  NSData+AES.m
//  Mata
//
//  Created by Youssef on 2017/12/20.
//  Copyright © 2017年 yunio. All rights reserved.
//

#import "NSData+AES.h"
#import <CommonCrypto/CommonCryptor.h>

@implementation NSData (AES)

- (NSData *)AES256EncryptWithKey:(NSString *)key {
    return [self AES256operation:kCCEncrypt key:key];
}

- (NSData *)AES256DecryptWithKey:(NSString *)key {
    return [self AES256operation:kCCDecrypt key:key];
}

- (NSData *)AES256operation:(CCOperation)operation key:(NSString *)key {
    
    char keyPtr[kCCKeySizeAES256 + 1];
    bzero(keyPtr, sizeof(keyPtr));
    [key getCString:keyPtr maxLength:sizeof(keyPtr) encoding:NSUTF8StringEncoding];
    
    size_t bufferSize = [self length] + kCCBlockSizeAES128;
    void *buffer = malloc(bufferSize);
    size_t numBytesEncrypted = 0;
    
    CCCryptorStatus cryptorStatus = CCCrypt(operation, kCCAlgorithmAES128, kCCOptionPKCS7Padding,
                                            keyPtr, kCCKeySizeAES256,
                                            NULL,
                                            [self bytes], [self length],
                                            buffer, bufferSize,
                                            &numBytesEncrypted);
    
    if(cryptorStatus == kCCSuccess){
        return [NSData dataWithBytesNoCopy:buffer length:numBytesEncrypted];
    }else{
        NSLog(@"AES256operation Error");
    }
    free(buffer);
    return nil;
}

@end

