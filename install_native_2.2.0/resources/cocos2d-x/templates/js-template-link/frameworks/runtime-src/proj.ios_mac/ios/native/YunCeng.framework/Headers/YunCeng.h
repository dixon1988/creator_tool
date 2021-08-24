//
//  YunCeng.h
//  YunCeng
//  ..
//  Created by chuanshi.zl on 15/5/19.
//  Copyright (c) 2015年 Alibaba Cloud Computing Ltd. All rights reserved.
//
#ifndef __IPHONE_5_0
#warning "This project uses features only available in iOS SDK 5.0 and later."
#endif

#ifdef __OBJC__
#import <UIKit/UIKit.h>
#import <Foundation/Foundation.h>
#import "YunCeng.h"

FOUNDATION_EXPORT double YunCengVersionNumber;

FOUNDATION_EXPORT const unsigned char YunCengVersionString[];

typedef NS_ENUM(NSInteger, YC_CODE) {
    YC_OK = 0,	 /* *< Success */
    
    YC_ERR_NETWORK      = 1000,       /* 网络通信异常 */
    YC_ERR_NETWORK_CONN = 1001,       /* 网络连接失败 */
    
    YC_ERR_KEY            = 2000,     /* appkey错误 */
    YC_ERR_KEY_SECBUF     = 2001,
    YC_ERR_KEY_LEN_MISMATCH   = 2002,
    YC_ERR_KEY_CLEN_MISMATCH  = 2003,
    
    YC_ERR_API_PROXY = 3000,          /* 3000~3999 服务端错误 */
    YC_ERR_RESP      = 4000,            /* 服务端响应错误        */
    YC_ERR_FORMAT    = 4001,            /* 服务端返回内容格式异常  */
    
    YC_ERR_INTR       = 9000,         /* SDK内部错误          */
    YC_ERR_INTR_NOMEM = 9001,         /* 内存不足    */
    YC_ERR_TIMED_WAITING = 9002,      /* 任务进行中，需等待 */
    YC_ERR_BUFFER_TOO_SMALL = 9003,   /* 缓冲区太小 */
    YC_ERR_PARAMETER  = 9004          /* 参数错误 */
};

@interface YunCeng : NSObject

/*!
 *@brief 初始化云层SDK
 *@param appKey 控制台对应的appkey
 *@param token 玩家唯一标识，类似与手机号
 *@return 函数成功返回0，否则返回错误码
 */
+(int) initEx:(const char *)appKey : (const char *) token;

/*!
 *@brief 获取动态IP地址
 *@param token 玩家账号信息
 *@param group_name 控制台上配置的用户分组ID
 *@param dip 目标ip
 *@param dport 目标端口
 *@param ip_buf 未开启隧道模式时，返回group_name对应的分组IP，开启隧道模式，则返回隧道IP
 *@param port_buf 未开启隧道模式时，返回传入的端口，开启隧道模式时，返回隧道端口
 *@return 当该函数调用成功时返回0，否则返回错误号码
 */
+(int) getProxyTcpByIp:(const char *)token : (const char *)group_name  :(const char *)dip :(const char *)dport : (char *)ip_buf : (int)ip_buf_len : (char *)port_buf : (int)port_buf_len;

/*!
 *@brief 获取动态IP地址
 *@param token 玩家账号信息
 *@param group_name 控制台上配置的用户分组ID
 *@param ddomain 目标domain
 *@param dport 目标端口
 *@param ip_buf 未开启隧道模式时，返回group_name对应的分组IP，开启隧道模式，则返回隧道IP
 *@param port_buf 未开启隧道模式时，返回传入的端口，开启隧道模式时，返回隧道端口
 *@return 当该函数调用成功时返回0，否则返回错误号码
 */
+(int) getProxyTcpByDomain:(const char *)token : (const char *)group_name  :(const char *)ddomain :(const char *)dport : (char *)ip_buf : (int)ip_buf_len : (char *)port_buf : (int)port_buf_len;

/*!
 *@brief 获取动态IP地址
 *@param token 玩家账号信息
 *@param group_name 控制台上配置的用户分组ID
 *@param dip 目标ip
 *@param dport 目标端口
 *@param ip_buf 未开启隧道模式时，返回group_name对应的分组IP，开启隧道模式，则返回隧道IP
 *@param port_buf 未开启隧道模式时，返回传入的端口，开启隧道模式时，返回隧道端口
 *@return 当该函数调用成功时返回0，否则返回错误号码
 */
+(int) getProxyUdpByIp:(const char *)token : (const char *)group_name  :(const char *)dip :(const char *)dport : (char *)ip_buf : (int)ip_buf_len : (char *)port_buf : (int)port_buf_len;

/*!
 *@brief 获取动态IP地址
 *@param token 玩家账号信息
 *@param group_name 控制台上配置的用户分组ID
 *@param ddomain 目标domain
 *@param dport 目标端口
 *@param ip_buf 未开启隧道模式时，返回group_name对应的分组IP，开启隧道模式，则返回隧道IP
 *@param port_buf 未开启隧道模式时，返回传入的端口，开启隧道模式时，返回隧道端口
 *@return 当该函数调用成功时返回0，否则返回错误号码
 */
+(int) getProxyUdpByDomain:(const char *)token : (const char *)group_name  :(const char *)ddomain :(const char *)dport : (char *)ip_buf : (int)ip_buf_len : (char *)port_buf : (int)port_buf_len;

/*!
 *@brief 获取动态IP地址
 *@param ip_buf 存放返回本地ip的buf
 *@param ip_buf_len ip_buf长度
 *@param ip_info_buf 存放ip info内容
 *@param ip_info_buf_len ip_info_buf的长度
 */
+(int) getLocalIpInfo : (char *)ip_buf : (int)ip_buf_len : (char *)ip_info_buf : (int)ip_info_buf_len; 

/**
 *@param data_type 自定义数据类型，请与开发人员联系，分配相关的Type
 *@param data_type = -1时，表示上报jaq的签名
 *@param report_msg 上报数据内容
 *@return 0表示成功，-1表示失败
 */
 + (int) reportUserData:(int) data_type : (const char *) report_msg : (int) sync;

/** 加解密函数总初始化接口
 *  fileName 加解密配置文件
 *  函数执行成功返回0，否则返回错误码
 */
 + (int) securityInit:(const char *) fileName;

 /** 白盒签名接口
 *  in 签名内容
 *  inlen in长度
 *  out 签名结果
 *  outlen out的长度
 *  函数执行成功返回签名结果长度，大于0表示成功
 */
 + (int) whiteboxSign:(const Byte *)in : (int) inlen : (Byte *)out : (int) outlen;

 /** 安全加密接口
 *  in 加密内容
 *  inlen in长度
 *  out 加密后的结果
 *  outlen out的长度
 *  函数执行成功返回加密结果长度，大于0表示成功
 */
 + (int) safeEncrypt:(const Byte *)in : (int) inlen : (Byte *)out : (int) outlen;

 /** 白盒解密接口
 *  in 解密内容
 *  inlen in长度
 *  out 解密结果
 *  outlen out的长度
 *  函数执行成功返回解密结果长度，大于0表示成功
 */
 + (int) safeDecrypt:(const Byte *)in : (int) inlen : (Byte *)out : (int) outlen;

 /** 白盒加密接口
 *  in 加密内容
 *  inlen in长度
 *  out 加密结果
 *  outlen out的长度
 *  函数执行成功返回加密结果长度，大于0表示成功
 */
 + (int) whiteboxEncrypt:(const Byte *)in : (int) inlen : (Byte *)out : (int) outlen;

 + (int) NetworkDiagnosiTask;

/**
 *@param session 要获取的session缓冲区
 *@param lenth   session缓冲区的长度，此值应不小于384
 *@return 0表示成功，其他表示失败
 */
 + (int) GetSession:(char *) session : (const int) lenth;

/**
 *@brief 在新线程中执行网络诊断，可用回调函数获取诊断结果
 *@param domain 网络诊断目标的域名/IP
 *@param port   网络诊断目标的端口号
 *@param thcb   网络诊断结果的回调函数
 */
 +(void) startNetworkDiagnosis:(NSString *)domain port:(int)port callback:(void (^) (NSString * result))thcb;

@end


FOUNDATION_EXPORT NSString *const YUNCENG_EXCEPTION_NAME;


@interface YunCengException : NSException {
}

@property(readonly) YC_CODE code;

-(instancetype) init:(YC_CODE) code;

+(instancetype) exceptionWithCode:(YC_CODE) code;
@end


#endif

/*! @brief 初始化云层SDK
 * appKey:控制台对应的appkey
 * token: 玩家唯一标识，类似与手机号
 * 函数成功返回0，否则返回错误码
 */
int YunCeng_InitEx(const char *app_key, const char *token);

/*!
 *@brief 获取动态IP地址
 *@param token 玩家账号信息
 *@param group_name 控制台上配置的用户分组ID
 *@param dip 目标ip
 *@param dport 目标端口
 *@param ip_buf 未开启隧道模式时，返回group_name对应的分组IP，开启隧道模式，则返回隧道IP
 *@param ip_buf_len 入参，ip_buf缓存的大小
 *@param port_buf 未开启隧道模式时，返回传入的端口，开启隧道模式时，返回隧道端口
 *@param port_buf_len, 入参， port_buf缓存的大小
 *@return 当该函数调用成功时返回0，否则返回错误号码
 */
int YunCeng_GetProxyTcpByIp(const char *token, const char *group_name, const char * dip,const char *dport,char *ip_buf,int ip_buf_len, char *port_buf, int port_buf_len);

/*!
 *@brief 获取动态IP地址
 *@param token 玩家账号信息
 *@param group_name 控制台上配置的用户分组ID
 *@param ddomain 目标domain
 *@param dport 目标端口
 *@param ip_buf 未开启隧道模式时，返回group_name对应的分组IP，开启隧道模式，则返回隧道IP
 *@param ip_buf_len 入参，ip_buf缓存的大小
 *@param port_buf 未开启隧道模式时，返回传入的端口，开启隧道模式时，返回隧道端口
 *@param port_buf_len, 入参， port_buf缓存的大小
 *@return 当该函数调用成功时返回0，否则返回错误号码
 */
int YunCeng_GetProxyTcpByDomain(const char *token, const char *group_name, const char * ddomain,const char *dport,char *ip_buf,int ip_buf_len, char *port_buf, int port_buf_len);

/*!
 *@brief 获取动态IP地址
 *@param token 玩家账号信息
 *@param group_name 控制台上配置的用户分组ID
 *@param dip 目标ip
 *@param dport 目标端口
 *@param ip_buf 未开启隧道模式时，返回group_name对应的分组IP，开启隧道模式，则返回隧道IP
 *@param ip_buf_len 入参，ip_buf缓存的大小
 *@param port_buf 未开启隧道模式时，返回传入的端口，开启隧道模式时，返回隧道端口
 *@param port_buf_len, 入参， port_buf缓存的大小
 *@return 当该函数调用成功时返回0，否则返回错误号码
 */
int YunCeng_GetProxyUdpByIp(const char *token, const char *group_name, const char * dip,const char *dport,char *ip_buf,int ip_buf_len, char *port_buf, int port_buf_len);

/*!
 *@brief 获取动态IP地址
 *@param token 玩家账号信息
 *@param group_name 控制台上配置的用户分组ID
 *@param ddomain 目标domain
 *@param dport 目标端口
 *@param ip_buf 未开启隧道模式时，返回group_name对应的分组IP，开启隧道模式，则返回隧道IP
 *@param ip_buf_len 入参，ip_buf缓存的大小
 *@param port_buf 未开启隧道模式时，返回传入的端口，开启隧道模式时，返回隧道端口
 *@param port_buf_len, 入参， port_buf缓存的大小
 *@return 当该函数调用成功时返回0，否则返回错误号码
 */
int YunCeng_GetProxyUdpByDomain(const char *token, const char *group_name, const char * ddomain,const char *dport,char *ip_buf,int ip_buf_len, char *port_buf, int port_buf_len);

/*! @brief 获取动态IP地址
 * ip_buf 出参，存放
 * ip_buf_len 入参，ip_buf缓存的大小
 * ip_info_buf 出参，存在动态分配的端口
 * ip_info_buf_len, 入参， ip_info_buf
 * @return YC_CODE
 */
int YunCeng_GetLocalIPInfo(char *ip_buf, int ip_buf_len, char *ip_info_buf, int ip_info_buf_len);

/*!
 * data_type 表示用户数据类型，请联系开发人员分配相关的type
 * data_type = -1时，表示上报jaq的签名
 * report_msg 用户上报数据
 * @return 0表示成功，-1表示失败
 */
 int YunCeng_ReportUserData(int data_type, const char *report_msg, int sync);
 
/** 加解密函数总初始化接口
 *  fileName 加解密配置文件
 *  函数执行成功返回0，否则返回错误码
 */
 int YunCeng_SecurityInit(const char * fileName);

 /** 白盒签名接口
 *  in 签名内容
 *  inlen in长度
 *  out 签名结果
 *  outlen out的长度
 *  函数执行成功返回签名结果长度，大于0表示成功
 */
 int YunCeng_WhiteboxSign(const Byte *in, int inlen, Byte *out, int outlen);

 /** 安全加密接口
 *  in 加密内容
 *  inlen in长度
 *  out 加密后的结果
 *  outlen out的长度
 *  函数执行成功返回加密结果长度，大于0表示成功
 */
 int YunCeng_SafeEncrypt(const Byte *in, int inlen, Byte *out, int outlen);

 /** 白盒解密接口
 *  in 解密内容
 *  inlen in长度
 *  out 解密结果
 *  outlen out的长度
 *  函数执行成功返回解密结果长度，大于0表示成功
 */
 int YunCeng_SafeDecrypt(const Byte *in, int inlen, Byte *out, int outlen);

 /** 白盒加密接口
 *  in 加密内容
 *  inlen in长度
 *  out 加密结果
 *  outlen out的长度
 *  函数执行成功返回加密结果长度，大于0表示成功
 */
 int YunCeng_WhiteboxEncrypt(const Byte *in, int inlen, Byte *out, int outlen);

/**
 *@param session 要获取的session缓冲区
 *@param lenth   session缓冲区的长度，此值应不小于384
 *@return 0表示成功，其他表示失败
 */
int YunCeng_GetSession(char * session, const int lenth);