//
//  UIView+FrameView.h
//  mofang-mobile
//
//  Created by mac on 4/20/19.
//

#import <UIKit/UIKit.h>
#import "NativeClass.h"
#import "UIHomeView.h"
#include "platform/CCApplication.h"
#import "RotateNavigationController.h"


@implementation UIHomeView

@synthesize btnHome;
@synthesize frameAlert;
@synthesize home_desc;

@synthesize bTouchHome;
@synthesize bTouchMove;
@synthesize location;

- (id)init:(NSString*)home_desc
{
    //CGRect bounds = [[UIScreen mainScreen] bounds];
    
    auto img_home = [UIImage imageNamed:@"homebtn.png"];
    auto rect = CGRectMake(0, 0, img_home.size.width * SCALE_DEF, img_home.size.height * SCALE_DEF);
    
    self = [super initWithFrame:rect];
    
    //添加home按钮
    auto btnHome = [[[UIHomeButton alloc] initWithFrame:rect] autorelease];
    [btnHome setImage:img_home forState:UIControlStateNormal];
    [self addSubview:btnHome];
    
    self.btnHome = btnHome;
    [self.btnHome initData:self];
    
    self.home_desc = home_desc;
    
    self.bTouchHome=false;
    self.bTouchMove=false;
    
    return self;
}

-(float)distance:(CGPoint)point1 point2:(CGPoint)point2
{
    return sqrtf(powf(point1.x - point2.x, 2) + powf(point1.y - point2.y, 2));
}

- (void)touchesBegan:(NSSet *)touches withEvent:(UIEvent *)event
{
    auto touchPoint = [[[touches allObjects] objectAtIndex:0] locationInView:self];
    touchPoint = [self convertPoint:touchPoint toView:[self superview]];
//
//    auto newRect = [self.btnHome convertRect:self.btnHome.bounds toView:nil];
//
//    if( CGRectContainsPoint(newRect, touchPoint) )
//    {
        self.location = touchPoint;
        self.bTouchHome = true;
//    }
}
- (void)touchesMoved:(NSSet *)touches withEvent:(UIEvent *)event
{
    auto touchPoint = [[[touches allObjects] objectAtIndex:0] locationInView:self];
    touchPoint = [self convertPoint:touchPoint toView:[self superview]];
    
    if( self.bTouchHome )
    {
        auto distance = [self distance:self.location point2:touchPoint];
        
        if( distance>5.0f )
        {
            auto btnframe =  [self frame];
            
            btnframe.origin.x = touchPoint.x;
            btnframe.origin.y = touchPoint.y;
            
            [self setFrame:btnframe];
            
            self.bTouchMove=true;
        }
    }
}

#define HOME_MOVE 0.0f

- (void)touchesEnded:(NSSet *)touches withEvent:(UIEvent *)event
{
    if( self.bTouchHome )
    {
        //拖动
        if( self.bTouchMove )
        {
            auto btnframe =  [self frame];
            auto viewframe = [[self superview] frame];
            auto lasty = btnframe.origin.y;
            if( lasty<0 ) lasty = 0;
            if( lasty>viewframe.size.height-btnframe.size.height ) lasty = viewframe.size.height-btnframe.size.height;
            
            //向左靠
            if( btnframe.origin.x < viewframe.size.width/2 )
            {
                [UIView animateWithDuration: 0.5 animations: ^{
                    self.frame = CGRectMake(-btnframe.size.width*HOME_MOVE, lasty, btnframe.size.width, btnframe.size.height);
                } completion: nil];
            }
            else
            {
                [UIView animateWithDuration: 0.5 animations: ^{
                    self.frame = CGRectMake(viewframe.size.width-btnframe.size.width*(1.0f-HOME_MOVE), lasty, btnframe.size.width, btnframe.size.height);
                } completion: nil];
            }
            
        }
        //点击
        else
        {
            [self homeEventShow:nil];
        }
    }
        
    self.bTouchHome = false;
    self.bTouchMove = false;
}

- (void)touchesCancelled:(NSSet *)touches withEvent:(UIEvent *)event
{
    [self touchesEnded:touches withEvent:event];
}

-(void)dealloc
{
    [[RotateNavigationController getInstance] stopMotionManager];
    
    [self.frameAlert removeFromSuperview];
    self.frameAlert=nil;
    
    self.btnHome = nil;
    self.home_desc = nil;
    self.homeViewDelegate = nil;
    
    [super dealloc];
}


-(void)homeEventShow:(id)sender
{
    [self cancelAlert:self.home_desc];
}

-(void)cancelAlert:(NSString*)home_desc
{
    if(self.frameAlert){
        return;
    }
    UIFrameAlert* alert = [[[UIFrameAlert alloc] init:home_desc] autorelease];
    [alert setAlert_delegate:self];
    
    self.frameAlert = alert;
    
    //添加确定
    auto image_sure = [UIImage imageNamed:@"alertbtn0.png"];
    UIButton* btn0 = [[[UIButton alloc] initWithFrame:CGRectMake(0, 0, image_sure.size.width * SCALE_DEF, image_sure.size.height * SCALE_DEF)] autorelease];
    [btn0 setImage:image_sure forState:UIControlStateNormal];
    [btn0 setTag:0];
    
    //添加取消
    auto image_cancel = [UIImage imageNamed:@"alertbtn1.png"];
    UIButton* btn1 = [[[UIButton alloc] initWithFrame:CGRectMake(0, 0, image_cancel.size.width * SCALE_DEF, image_cancel.size.height * SCALE_DEF)] autorelease];
    [btn1 setImage:image_cancel forState:UIControlStateNormal];
    [btn1 setTag:1];
    
    //添加取消
    [alert addButtonWithUIButton:btn0];
    [alert addButtonWithUIButton:btn1];
    
    [alert show:[self superview]];
}

//弹窗确定
- (void)alertView:(UIAlertView *)alertView clickedButtonAtIndex:(NSInteger)buttonIndex
{
    //确定
    if( buttonIndex==0 )
    {
        //通知关闭
        [[NativeOcClass getInstance] performSelectorOnMainThread:@selector(onMainThreadEvent:) withObject:onResultCmd(YQ_SUB_WEBVIEW_ALERT_CANCEL) waitUntilDone:NO];
    }
    else
    {
        [[NativeOcClass getInstance] performSelectorOnMainThread:@selector(onMainThreadEvent:) withObject:onResultCmd(YQ_SUB_WEBVIEW_ALERT_SURE) waitUntilDone:NO];
        
        [self removeFromSuperview];
    }
    
    self.frameAlert=nil;
}

//拉起home_view
+(void)callNativeByHomeView:(NSString*)home_desc
{
    auto homeView = [[[UIHomeView alloc] init:home_desc] autorelease];
    auto eaglview = (UIView*)cocos2d::Application::getInstance()->getView();
    [eaglview addSubview:homeView];
}

//开启横竖屏监听
+(void)callNativeByMotionstar:(NSString*)param
{
    [[RotateNavigationController getInstance] starMotionManager];
}

//停止陀螺仪安装
+(void)callNativeByMotionStop
{
    [[RotateNavigationController getInstance] stopMotionManager];
}

//拉起home_view alert_desc
+(void)callNativeByHomeViewAlert:(NSString*)alert_desc
{
    
        
}



@end
