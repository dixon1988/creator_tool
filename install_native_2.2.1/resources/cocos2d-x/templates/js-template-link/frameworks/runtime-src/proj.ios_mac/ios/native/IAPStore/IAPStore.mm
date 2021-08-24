#import "IAPStore.h"
#import "OCDefine.h"
#import "NativeClass.h"

USING_NS_CC;

@implementation CIAPStore

@synthesize ItunesID;
@synthesize OrderString;
@synthesize Price;
@synthesize StoreCallBack;

static CIAPStore* s_IapStore = nil;
+(id)getInstance
{
    if( !s_IapStore )
        s_IapStore = [[CIAPStore alloc] init];
    return s_IapStore;
}

+(id)GetPayResult:(int)getIndex remove:(NSString*)removeid
{
    NSArray *documentPaths = NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES);
    NSString* doc = [documentPaths objectAtIndex:0];
    NSString* docfile = [doc stringByAppendingString:@"/payStore.plist"];
    
    //是否删除
    if( removeid!=nil )
    {
        //存储订单
        NSMutableArray* pRootArray = [NSMutableArray arrayWithContentsOfFile:docfile];
        for (int i=0; i<[pRootArray count]; i++)
        {
            NSMutableDictionary* dictionary = [pRootArray objectAtIndex:i];
            NSString* strId = [dictionary objectForKey:@"id"];
            if( [strId compare:removeid]==NSOrderedSame )
            {
                [pRootArray removeObjectAtIndex:i];
                break;
            }
        }
        
        [pRootArray writeToFile:docfile atomically:YES];
        return @"";
    }
    
    //存储订单
    NSMutableArray* pRootArray = [NSMutableArray arrayWithContentsOfFile:docfile];
    if( [pRootArray count] )
    {
        return [pRootArray objectAtIndex:0];
    }
    return nil;
}

+(void)SavePayResult:(NSString*)tempId reqUrl:(NSString*)reqUrl tempEncoding:(NSString*)tempEncoding
{
    NSArray *documentPaths = NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES);
    NSString* doc = [documentPaths objectAtIndex:0];
    NSString* docfile = [doc stringByAppendingString:@"/payStore.plist"];
    
    //存储订单
    NSMutableArray* pRootArray = [NSMutableArray arrayWithContentsOfFile:docfile];
    if( !pRootArray )
        pRootArray = [NSMutableArray array];
    
    //存储订单
    NSMutableDictionary* dictionary = [NSMutableDictionary dictionary];
    [dictionary setObject:tempId forKey:@"id"];
    [dictionary setObject:reqUrl forKey:@"reqUrl"];
    [dictionary setObject:tempEncoding forKey:@"encoding"];
    [pRootArray addObject:dictionary];
    
    BOOL bSave = [pRootArray writeToFile:docfile atomically:YES];
    if( !bSave )
    {
        NSLog(@" 11111 ");
    }
}

+(void)PayCompleteTransaction:(bool)bCheck id:(NSString*)tranIdentifier reqUrl:(NSString*)reqUrl encoding:(NSString*) tranbase64Encoding
{
    bool bMustCheck = true;
    NSString* tempReqUrl = reqUrl;
    NSString* tempEncoding = tranbase64Encoding;
    NSString* tempId = tranIdentifier;
    
    //不是检查 存储订单
    if( !bCheck )
    {
        [CIAPStore SavePayResult:tempId reqUrl:tempReqUrl tempEncoding:tempEncoding];
    }
    //检查漏单
    else
    {
        //存储订单
        NSMutableDictionary* dictionary = [CIAPStore GetPayResult:0 remove:nil];
        if( dictionary!=nil )
        {
            tempId = [dictionary objectForKey:@"id"];
            tempReqUrl = [dictionary objectForKey:@"reqUrl"];
            tempEncoding = [dictionary objectForKey:@"encoding"];
        }
        else
        {
            //不需要验证
            bMustCheck = false;
        }
    }
    
    if( !bMustCheck ) return;
    
    // 2 封装成NSURL
    NSURL *url = [NSURL URLWithString:tempReqUrl];
    
    // 3 定义NSURLRquest
    NSMutableURLRequest *request = [[NSMutableURLRequest alloc] init];//注意这个是mutable，说明这个是可变的
    
    // 设置请求类型
    request.HTTPMethod   = @"post";//默认是 get
    
    //添加url
    request.URL = url;
    
    //设置body内容
    NSString *bodyString = tempEncoding;
    NSData   *bodyData   = [bodyString dataUsingEncoding:NSUTF8StringEncoding];
    request.HTTPBody     = bodyData;
    
    [NSURLConnection sendAsynchronousRequest:request queue:[[NSOperationQueue alloc] init] completionHandler:^(NSURLResponse * _Nullable response, NSData * _Nullable data, NSError * _Nullable connectionError)
     {
         NSError* error=nil;
         id jsonObject = [NSJSONSerialization JSONObjectWithData:data options:NSJSONReadingAllowFragments error:&error];
         int retcode = [[jsonObject objectForKey:@"retcode"] intValue];
         
         //已处理成功
         if( retcode==103 )
         {
             //订单记录
             if( bMustCheck )
             {
                 [CIAPStore GetPayResult:0 remove:tempId];
             }
         }
         
         //充值成功
         else if( retcode==100 )
         {
             if( !bCheck )
             {
                 //支付成功 可以刷新页面
                 [[NativeOcClass getInstance] setEventResult:YQ_SUB_IOSPAY_SUCCEED];
                 OnNativeMainThreadCmd(YQ_SUB_IOSPAY_SUCCEED);
             }
             
             //订单记录
             if( bMustCheck )
             {
                 [CIAPStore GetPayResult:0 remove:tempId];
             }
         }
         //充值成功，验证失败，等待下次打开app时自动再次验证
         else
         {
             if( !bCheck )
             {
                 //充值成功验证失败，请联系客服或稍后重试
                 [[NativeOcClass getInstance] setEventResult:YQ_SUB_IOSPAY_NOSUCCEED];
                 OnNativeMainThreadCmd(YQ_SUB_IOSPAY_NOSUCCEED);
             }
         }
     }];
}

-(id)init
{
    if ((self = [super init]))
    {
        //----监听购买结果
        [[SKPaymentQueue defaultQueue] addTransactionObserver:self];
    
        
        self.ItunesID = @"";
        self.OrderString = @"";
        self.Price = 0;
        self.StoreCallBack=@"";
    }
    return self;
}

-(void)buy:(NSString*)proid
{
    
    self.ItunesID = proid;
    
    //获取产品信息
    [self RequestProductData:proid];
    
    /*
    //直接发起购买
    if ([SKPaymentQueue canMakePayments])
    {
        GetFrameManager()->SetLockScreenString("正在连接，请稍后");
        
        //允许购买，直接购买
        SKPayment *payment = nil;
        
        payment  = [SKPayment paymentWithProductIdentifier:pItunesID];
 
        //添加购买
        [[SKPaymentQueue defaultQueue] addPayment:payment];
    }
    else
    {
        UIAlertView *alerView =  [[UIAlertView alloc] initWithTitle:@"系统提示"
                                                            message:@"不允许应用程序内购买"
                                                           delegate:nil
                                                  cancelButtonTitle:@"确定"
                                                  otherButtonTitles:nil];
        
        [alerView show];
        [alerView release];
    }*/
}

-(bool)CanMakePay
{
    return [SKPaymentQueue canMakePayments];
}


-(void)RequestProductData:(NSString*)proid;
{
    NSArray *product = nil;
    
    product=[[NSArray alloc] initWithObjects:proid, nil];
    
    NSSet *nsset = [NSSet setWithArray:product];
    SKProductsRequest *request=[[SKProductsRequest alloc] initWithProductIdentifiers: nsset];
    request.delegate=self;
    [request start];
    [product release];
    
    NSLog(@"---------请求对应的产品信息------------");
}

//<SKProductsRequestDelegate> 请求协议
//收到的产品信息
-(void)productsRequest:(SKProductsRequest *)request didReceiveResponse:(SKProductsResponse *)response
{
    NSLog(@"-----------收到产品反馈信息--------------");
    NSArray *myProduct = response.products;
    NSLog(@"产品Product ID:%@",response.invalidProductIdentifiers);
    NSLog(@"产品付费数量: %d", (int)[myProduct count]);
    
    SKProduct* buyproduct = nil;
    
    // populate UI
    for(SKProduct *product in myProduct)
    {
        NSLog(@"product info");
        NSLog(@"SKProduct 描述信息%@", [product description]);
        NSLog(@"产品标题 %@" , product.localizedTitle);
        NSLog(@"产品描述信息: %@" , product.localizedDescription);
        NSLog(@"价格: %@" , product.price);
        NSLog(@"Product id: %@" , product.productIdentifier);
        
        if( [product.productIdentifier compare:self.ItunesID]==NSOrderedSame )
        {
            buyproduct = product;
            break;
        }
    }
    
    if( !buyproduct )
    {
        [[NativeOcClass getInstance] setEventResult:YQ_SUB_IOSPAY_FAILURE];
        jsb_callback(YQ_SUB_IOSPAY_FAILURE);
        return;
    }
    
    //发起购买
    SKPayment *payment = [SKPayment paymentWithProduct:buyproduct];
    [[SKPaymentQueue defaultQueue] addPayment:payment];
    [request autorelease];
}


-(void)requestProUpgradeProductData
{
    NSLog(@"------请求升级数据---------");
    NSSet *productIdentifiers = [NSSet setWithObject:@"com.productid"];
    SKProductsRequest* productsRequest = [[SKProductsRequest alloc] initWithProductIdentifiers:productIdentifiers];
    productsRequest.delegate = self;
    [productsRequest start];
    
}
//弹出错误信息
-(void)request:(SKRequest *)request didFailWithError:(NSError *)error
{
    NSLog(@"-------弹出错误信息----------");
    UIAlertView *alerView =  [[UIAlertView alloc] initWithTitle:NSLocalizedString(@"Alert",NULL) message:[error localizedDescription] delegate:nil cancelButtonTitle:NSLocalizedString(@"Close",nil) otherButtonTitles:nil];
    [alerView show];
    [alerView release];
}

-(void)requestDidFinish:(SKRequest *)request
{
    NSLog(@"----------反馈信息结束--------------");
    
}

-(void) PurchasedTransaction: (SKPaymentTransaction *)transaction
{
    NSLog(@"-----PurchasedTransaction----");
    NSArray *transactions =[[NSArray alloc] initWithObjects:transaction, nil];
    [self paymentQueue:[SKPaymentQueue defaultQueue] updatedTransactions:transactions];
    [transactions release];
}


//<SKPaymentTransactionObserver> 千万不要忘记绑定，代码如下：
//----监听购买结果
//[[SKPaymentQueue defaultQueue] addTransactionObserver:self];
-(void)paymentQueue:(SKPaymentQueue *)queue updatedTransactions:(NSArray *)transactions //交易结果
{
    NSLog(@"-----paymentQueue--------");

    for (SKPaymentTransaction *transaction in transactions)
    {
        switch (transaction.transactionState)
        {
            case SKPaymentTransactionStatePurchased:        //交易完成
                
                [self completeTransaction:transaction];
                NSLog(@"-----交易完成 --------");
                break;
                
            case SKPaymentTransactionStateFailed:           //交易失败
                [self failedTransaction:transaction];
                break;
                
            case SKPaymentTransactionStateRestored:         //已经购买过该商品
                
                [self restoreTransaction:transaction];
                
                NSLog(@"-----已经购买过该商品 --------");
                
            case SKPaymentTransactionStatePurchasing:       //商品添加进列表
                
                NSLog(@"-----商品添加进列表 --------");
                
                break;
            default:
                break;
        }
    }
}
-(void)completeTransaction:(SKPaymentTransaction *)transaction
{
    NSLog(@"-----completeTransaction--------");
    
    if( [self.StoreCallBack compare:@""]==NSOrderedSame )
    {
        NSLog(@"验证回调错误");
        return;
    }
    
    // 1 需要请求的URL String
    NSString *urlString = [NSString stringWithFormat:@"%@?orderid=%@&price=%d", self.StoreCallBack, self.OrderString, self.Price];
    
    //发起验证
    [CIAPStore PayCompleteTransaction:false id:transaction.transactionIdentifier reqUrl:urlString encoding:[transaction.transactionReceipt base64Encoding]];

    // Remove the transaction from the payment queue.
    [[SKPaymentQueue defaultQueue] finishTransaction: transaction];
}

//记录交易
-(void)recordTransaction:(NSString *)product
{
    CCLOG("-----记录交易--------");
}

//处理下载内容
-(void)provideContent:(NSString *)product
{
    CCLOG("-----下载--------");
}

-(void) failedTransaction:(SKPaymentTransaction *)transaction
{
    if (transaction.error.code != SKErrorPaymentCancelled)
    {
        //支付失败
        [[NativeOcClass getInstance] setEventResult:YQ_SUB_IOSPAY_FAILURE];
        jsb_callback(YQ_SUB_IOSPAY_FAILURE);
    }
    else
    {
        //支付失败
        [[NativeOcClass getInstance] setEventResult:YQ_SUB_IOSPAY_WAITCANCEL];
        jsb_callback(YQ_SUB_IOSPAY_WAITCANCEL);
    }
    
    [[SKPaymentQueue defaultQueue] finishTransaction: transaction];
    
}

-(void)paymentQueueRestoreCompletedTransactionsFinished:(SKPaymentTransaction *)transaction
{
    
    
}


-(void)restoreTransaction:(SKPaymentTransaction *)transaction
{
    NSLog(@" 交易恢复处理");
    
    //重试验证
    [self completeTransaction:transaction];
    
}

-(void)paymentQueue:(SKPaymentQueue*)paymentQueue restoreCompletedTransactionsFailedWithError:(NSError *)error
{
    CCLOG("-------paymentQueue----");
}

#pragma mark connection delegate
-(void)connection:(NSURLConnection *)connection didReceiveData:(NSData *)data
{
    NSLog(@"%@",  [[[NSString alloc] initWithData:data encoding:NSUTF8StringEncoding] autorelease]);
}

-(void)connectionDidFinishLoading:(NSURLConnection *)connection
{
    
}

-(void)connection:(NSURLConnection *)connection didReceiveResponse:(NSURLResponse *)response
{
    switch([(NSHTTPURLResponse *)response statusCode])
    {
        case 200:
        case 206:
            break;
        case 304:
            break;
        case 400:
            break;
        case 404:
            break;
        case 416:
            break;
        case 403:
            break;
        case 401:
        case 500:
            break;
        default:
            break;
    }
}

- (void)connection:(NSURLConnection *)connection didFailWithError:(NSError *)error
{
    NSLog(@"test");
}

-(void)dealloc
{
    
    [super dealloc];
}

- (void)paymentQueue:(SKPaymentQueue *)queue removedTransactions:(NSArray *)transactions
{
    NSLog(@"Purchase removedTransactions");
 
    //[[SKPaymentQueue defaultQueue] removeTransactionObserver:self]; //解除监听
    
    // Release the transaction observer since transaction is finished/removed.
    //[[SKPaymentQueue defaultQueue] removeTransactionObserver:self];
}
@end
