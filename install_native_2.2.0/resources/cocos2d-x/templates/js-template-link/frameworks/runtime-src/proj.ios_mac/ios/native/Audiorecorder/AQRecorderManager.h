//
//  RecorderManager.h
//  OggSpeex
//
//  Created by Jiang Chuncheng on 6/25/13.
//  Copyright (c) 2013 Sense Force. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "Encapsulator.h"

@protocol AQRecordingDelegate <NSObject>

- (void)recordingFinishedWithFileName:(NSString *)filePath time:(NSTimeInterval)interval;
- (void)recordingTimeout;
- (void)recordingStopped;  //录音机停止采集声音
- (void)recordingFailed:(NSString *)failureInfoString;

@optional
- (void)levelMeterChanged:(float)levelMeter;

@end

@interface AQRecorderManager : NSObject <EncapsulatingDelegate> {
    
    Encapsulator *encapsulator;
    NSDate *dateStartRecording;
    NSDate *dateStopRecording;
    NSTimer *timerLevelMeter;
    NSTimer *timerTimeout;
}

@property (nonatomic, retain) id<AQRecordingDelegate> delegate;
@property (nonatomic, retain) NSString *filename;
@property (nonatomic, strong) Encapsulator *encapsulator;
@property (nonatomic, strong) NSDate *dateStartRecording, *dateStopRecording;
@property (nonatomic, strong) NSTimer *timerLevelMeter;
@property (nonatomic, strong) NSTimer *timerTimeout;

+ (AQRecorderManager *)sharedManager;

- (void)startRecording:(NSString*) szFileName;;

- (void)stopRecording;

- (void)cancelRecording;

- (NSTimeInterval)recordedTimeInterval;

@end
