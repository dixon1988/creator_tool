package org.cocos2dx.javascript;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.Message;

//WIFI change
public class MyNetChange extends BroadcastReceiver
{
    @SuppressWarnings("static-access")
    public void onReceive(Context context, Intent intent) {
        // TODO Auto-generated method stub
        // TODO Auto-generated method stub
        // TODO Auto-generated method stub
        //Toast.makeText(context, intent.getAction(), 1).show();
        ConnectivityManager manager = (ConnectivityManager) context.getSystemService(Context.CONNECTIVITY_SERVICE);

        NetworkInfo.State mobileInfo = null;
        NetworkInfo.State wifiInfo = null;

        if (manager != null)
        {
            mobileInfo = manager.getNetworkInfo(ConnectivityManager.TYPE_MOBILE).getState();
            wifiInfo = manager.getNetworkInfo(ConnectivityManager.TYPE_WIFI).getState();
        }

        int nState = 0;

        if (wifiInfo != null && mobileInfo != null
                && NetworkInfo.State.CONNECTED != wifiInfo
                && NetworkInfo.State.CONNECTED == mobileInfo)
        {
            nState = 606;
        }
        else if (wifiInfo != null && mobileInfo != null
                && NetworkInfo.State.CONNECTED != wifiInfo
                && NetworkInfo.State.CONNECTED != mobileInfo)
        {
            nState = 607;
        }

        else if (wifiInfo != null && NetworkInfo.State.CONNECTED == wifiInfo) {
            nState = 605;
        }


        JniHelper.m_stata = nState;
        JniHelper.m_sType = "Change";

        Message msgMessage = new Message();
        JniHelper.stateHandler.sendMessage(msgMessage);
    }
}