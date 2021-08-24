
#import "UIFrameAlert.h"


@implementation UIFrameAlert

@synthesize backgroundView, alertLabel, buttonArray, alert_delegate;

- (id)init:(NSString*)home_desc
{
    CGRect bounds = [[UIScreen mainScreen] bounds];
    self = [super initWithFrame:bounds];
    
    auto img_bg = [UIImage imageNamed:@"alertbg.png"];
    
    //显示背景
    self.backgroundView = [[[UIImageView alloc] initWithImage:img_bg] autorelease];
    [self addSubview:self.backgroundView];
    
    self.backgroundView.userInteractionEnabled = YES;
    
    //背景居中
    auto img_width = img_bg.size.width*ALERTBG_SACLE;
    auto img_height = img_bg.size.height*ALERTBG_SACLE;
    auto centerx = (bounds.size.width-img_width ) / 2;
    auto centery = (bounds.size.height-img_height ) / 2;
    [self.backgroundView setFrame:CGRectMake(centerx, centery, img_width, img_height)];
    
    self.alertLabel = [[[UILabel alloc] init] autorelease];
    [self.backgroundView addSubview:self.alertLabel];
    
    self.alertLabel.font = [UIFont fontWithName:@"arial" size:24];
    self.alertLabel.textAlignment = NSTextAlignmentCenter;
    self.alertLabel.adjustsFontSizeToFitWidth = YES;
    
    NSDictionary *dic = @{NSFontAttributeName:[UIFont systemFontOfSize:24]};
    
    [self.alertLabel setText:home_desc];
    
    CGRect rect = [self.alertLabel.text boundingRectWithSize:CGSizeMake(280, 200) options:NSStringDrawingUsesLineFragmentOrigin | NSStringDrawingUsesFontLeading attributes:dic context:nil];
    
    rect.origin.x = (img_width-rect.size.width)/2;
    rect.origin.y = (img_height-rect.size.height)/2;
    
    [self.alertLabel setFrame:rect];
    [self.alertLabel setText:home_desc];
    
    //自定义按钮位置
    self.buttonArray = [NSMutableArray arrayWithCapacity:4];
    return self;
}

-(void)addButtonWithUIButton:(UIButton *) btn
{
    [btn addTarget:self action:@selector(buttonClicked:) forControlEvents:UIControlEventTouchUpInside];
    
    [self.buttonArray addObject:btn];
}

-(void)buttonClicked:(id)sender
{
    UIButton *btn = (UIButton *) sender;
    
    if (alert_delegate) {
        if ([alert_delegate respondsToSelector:@selector(alertView:clickedButtonAtIndex:)]){
            [alert_delegate alertView:self clickedButtonAtIndex:btn.tag];
        }
    }
    
    [super removeFromSuperview];
}

- (void)show:(UIView*)parent
{
    auto count = [self.buttonArray count];
    
    if( count==1 )
    {
        auto btn0 = (UIButton*)[self.buttonArray objectAtIndex:0];
        [self.backgroundView addSubview:btn0];
        
        auto bg_size = self.backgroundView.frame.size;
        auto bt_size0 = btn0.frame.size;
        [btn0 setFrame: CGRectMake( (bg_size.width-bt_size0.width)/2, bg_size.height-bt_size0.height-20, bt_size0.width, bt_size0.height) ];
    }
    
    else if( count==2 )
    {
        auto btn0 = (UIButton*)[self.buttonArray objectAtIndex:0];
        [self.backgroundView addSubview:btn0];
        
        auto bg_size = self.backgroundView.frame.size;
        auto bt_size0 = btn0.frame.size;
        [btn0 setFrame: CGRectMake( bg_size.width/2-20-bt_size0.width, bg_size.height-bt_size0.height-20, bt_size0.width, bt_size0.height) ];
        
        
        auto btn1 = (UIButton*)[self.buttonArray objectAtIndex:1];
        [self.backgroundView addSubview:btn1];
        [btn1 setFrame: CGRectMake( bg_size.width/2+20, bg_size.height-bt_size0.height-20, bt_size0.width, bt_size0.height) ];
    }
    
    [parent addSubview:self];
}


- (void)dealloc
{
    [self.buttonArray removeAllObjects];
    self.buttonArray=nil;
    self.alertLabel=nil;
    self.backgroundView=nil;
    
    [super dealloc];
}

@end

