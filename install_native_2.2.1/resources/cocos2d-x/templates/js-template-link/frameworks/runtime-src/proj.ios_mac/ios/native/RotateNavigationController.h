//
//  RotateNavigationController.h
//  RotateScreen
//
//  Created by obo on 16/1/28.
//  Copyright © 2016年 obo. All rights reserved.
//

#import <UIKit/UIKit.h>
#import <StoreKit/StoreKit.h>
#import <CoreMotion/CoreMotion.h>
#include "OCDefine.h"

@interface RotateNavigationController : UINavigationController< SKStoreProductViewControllerDelegate >

@property (nonatomic)UIInterfaceOrientation interfaceOrientation;
@property (nonatomic)UIInterfaceOrientationMask interfaceOrientationMask;

@property(nonatomic,assign)NSTimeInterval motionInterval;
@property(nonatomic,retain)CMMotionManager* motionManager;

+(id)getInstance;
+(void)changeScreenType:(UIInterfaceOrientation)cbOrientation;
+(void)resetScreenType;
//是否竖屏
+(BOOL)IsLandscapePortrait;
+(void)evaluate;

//重力监听
-(void)starMotionManager;
-(void)stopMotionManager;

#ifdef USING_SHANFU
+(void)callNativeHomeChat0:(NSString*)url p1:(NSString*)agentUserId p2:(NSString*)app_key p3:(NSString*)szChannelId p4:(NSString*)strUserID p5:(NSString*)strNameUtf8 p6:(NSString*)szMachineId p7:(NSString*)key;
#endif

@end
