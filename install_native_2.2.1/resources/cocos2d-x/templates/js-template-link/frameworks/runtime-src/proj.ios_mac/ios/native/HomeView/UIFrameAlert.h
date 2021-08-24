
#import <UIKit/UIKit.h>

#define ALERTBG_SACLE 0.35

@protocol UIFrameAlertDelegate <NSObject>

@optional
- (void)alertView:(UIAlertView *)alertView clickedButtonAtIndex:(NSInteger)buttonIndex;
@end

@interface UIFrameAlert : UIAlertView
{
   
}

@property(nonatomic, retain) UILabel* alertLabel;
@property(nonatomic, retain) NSMutableArray* buttonArray;
@property(readwrite, retain) UIImageView* backgroundView;

@property(nonatomic, assign) id alert_delegate;

-(id)init:(NSString*)home_desc;
- (void)show:(UIView*)parent;
-(void)addButtonWithUIButton:(UIButton*) btn;

@end
