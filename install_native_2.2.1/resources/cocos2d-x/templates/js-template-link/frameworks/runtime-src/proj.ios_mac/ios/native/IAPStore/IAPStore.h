

#ifndef YYGameProject_IAPSTORE_H
#define YYGameProject_IAPSTORE_H

#import "cocos2d.h"
#import <UIKit/UIKit.h>
#import <StoreKit/StoreKit.h>

@interface CIAPStore : NSObject<SKProductsRequestDelegate, SKPaymentTransactionObserver>
{

}

@property (nonatomic, retain)NSString*  ItunesID;       //道具 I D
@property (nonatomic, retain)NSString*  OrderString;    //订单 号
@property (nonatomic)int  Price;                        //价格
@property (nonatomic, retain)NSString*  StoreCallBack;  //回调callback


+(id)getInstance;
-(void)requestProUpgradeProductData;
-(void)RequestProductData:(NSString*)proid;
-(bool)CanMakePay;
-(void)buy:(NSString*)proid;
-(void)paymentQueue:(SKPaymentQueue *)queue updatedTransactions:(NSArray *)transactions;

-(void)PurchasedTransaction: (SKPaymentTransaction *)transaction;
-(void)completeTransaction: (SKPaymentTransaction *)transaction;
-(void)failedTransaction: (SKPaymentTransaction *)transaction;
-(void)paymentQueueRestoreCompletedTransactionsFinished: (SKPaymentTransaction *)transaction;
-(void)paymentQueue:(SKPaymentQueue *) paymentQueue restoreCompletedTransactionsFailedWithError:(NSError *)error;
-(void)restoreTransaction: (SKPaymentTransaction *)transaction;
-(void)provideContent:(NSString *)product;
-(void)recordTransaction:(NSString *)product;
-(void)paymentQueue:(SKPaymentQueue *)queue removedTransactions:(NSArray *)transactions;

+(void)PayCompleteTransaction:(bool)bCheck id:(NSString*)tranIdentifier reqUrl:(NSString*)reqUrl encoding:(NSString*) tranbase64Encoding;

@end

#endif
