//
//  UIButton+UIHomeButton.h
//  HuoteYule-mobile
//
//  Created by mac on 7/14/19.
//

#import <UIKit/UIKit.h>
#import "UIHomeButton.h"

@implementation UIHomeButton

@synthesize touch_node;

-(void)initData:(id)touch_node
{
    self.touch_node = touch_node;
    self.userInteractionEnabled = YES;
}


- (void)touchesBegan:(NSSet *)touches withEvent:(UIEvent *)event
{
    [self.touch_node touchesBegan:touches withEvent:event];
}
- (void)touchesMoved:(NSSet *)touches withEvent:(UIEvent *)event
{
    [self.touch_node touchesMoved:touches withEvent:event];
}

- (void)touchesEnded:(NSSet *)touches withEvent:(UIEvent *)event
{
    [self.touch_node touchesEnded:touches withEvent:event];
}

- (void)touchesCancelled:(NSSet *)touches withEvent:(UIEvent *)event
{
    [self.touch_node touchesCancelled:touches withEvent:event];
}

-(void)dealloc
{
    [super dealloc];
}

@end


