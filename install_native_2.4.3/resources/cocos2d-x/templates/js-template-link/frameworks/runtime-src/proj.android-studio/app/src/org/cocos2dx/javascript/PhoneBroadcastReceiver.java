package org.cocos2dx.javascript;

import org.cocos2dx.javascript.JniHelper;
import android.app.Service;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.Message;
import android.telephony.TelephonyManager;
import android.util.Log;

public class PhoneBroadcastReceiver extends BroadcastReceiver {

    private static boolean mIncomingFlag = false;
    private static String mIncomingNumber = null;

	@Override
	public void onReceive(Context context, Intent intent) {
		// TODO Auto-generated method stub
		// if call phone

		Log.e("-----BroadcastReceiver", "check call phone");
        if (intent.getAction().equals(Intent.ACTION_NEW_OUTGOING_CALL)) {
            mIncomingFlag = false;
            String phoneNumber = intent.getStringExtra(Intent.EXTRA_PHONE_NUMBER);
            Log.e("-----BroadcastReceiver", "call number:" + phoneNumber);

        } else {
            //If it's a call.
            TelephonyManager tManager = (TelephonyManager) context
                    .getSystemService(Service.TELEPHONY_SERVICE);
            switch (tManager.getCallState()) {

            case TelephonyManager.CALL_STATE_RINGING:
                mIncomingNumber = intent.getStringExtra("incoming_number");
                break;
            case TelephonyManager.CALL_STATE_OFFHOOK:
                Log.e("-----BroadcastReceiver", "BroadcastReceiver-ing:" + mIncomingNumber);
                break;
            case TelephonyManager.CALL_STATE_IDLE:
                	Log.e("-----BroadcastReceiver", "BroadcastReceiver-free");

                	//callend callfun 605:wifi,606:mobile,607:none
                	JniHelper.m_phone = 606;
                    JniHelper.m_phoneType = "Change";
                    Message msgMessage = new Message();
                    JniHelper.statePhone.sendMessage(msgMessage);

                break;
            }
        }
	}
}
