//
//  UIView+FrameView.h
//  mofang-mobile
//
//  Created by mac on 4/20/19.
//

#import <UIKit/UIKit.h>
#import "UIHomeButton.h"
#import "UIFrameAlert.h"



#define SCALE_DEF 0.35
#define YQ_SUB_WEBVIEW_ALERT_SURE   2200    //webview alert sure
#define YQ_SUB_WEBVIEW_ALERT_CANCEL 2201    //webview alert sure

@protocol UIHomeViewDelegate <NSObject>
@optional
-(void)removeHomeView:(NSString*)remove_desc;
@end

@interface UIHomeView : UIView<UIFrameAlertDelegate>


@property(nonatomic)bool bTouchHome;
@property(nonatomic)bool bTouchMove;
@property(nonatomic)CGPoint location;


@property(nonatomic, retain)id homeViewDelegate;
@property(nonatomic, retain)UIHomeButton* btnHome;
@property(nonatomic, retain)UIFrameAlert* frameAlert;
@property(nonatomic, retain)NSString* home_desc;


//拉起home_view
+(void)callNativeByHomeView:(NSString*)home_desc;

//开启重力陀螺仪
+(void)callNativeByMotionstar:(NSString*)param;

//停止陀螺仪安装
+(void)callNativeByMotionStop;

//拉起home_view alert_desc
+(void)callNativeByHomeViewAlert:(NSString*)alert_desc;
    
@end

