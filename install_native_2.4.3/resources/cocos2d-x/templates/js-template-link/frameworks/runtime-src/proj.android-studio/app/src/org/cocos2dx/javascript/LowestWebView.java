package org.cocos2dx.javascript;

public class LowestWebView {

//    public Cocos2dxActivity mainActivity;
//    public WebView MyWebView = null;
//
//    public LowestWebView(Cocos2dxActivity main)
//    {
//        mainActivity = main;
//    }
//
//    public void setUrl(String Url)
//    {
//        if(MyWebView != null)
//            MyWebView.loadUrl(Url);//加载url
//    }
//
//    public void close()
//    {
//        mainActivity.RemoveLowestView(MyWebView);
//    }
//
//    public void init()
//    {
//        Log.e("org.HTQP.game","---------------------------------------进入LowestWebview 初始化");
//        //将webView添加到底层
//        MyWebView = new WebView(mainActivity);
//        mainActivity.AddLowestView(MyWebView);
//
//        //初始设置
//        MyWebView.clearCache(true);
//        MyWebView.setFocusableInTouchMode(true);
//
//        MyWebView.clearHistory();
//        MyWebView.clearFormData();
//        MyWebView.requestFocus();
//        WebSettings webSettings = MyWebView.getSettings();
//        //允许js运行
//        webSettings.setJavaScriptEnabled(true);
//        webSettings.setSupportZoom(false);
//        webSettings.setDomStorageEnabled(true);
//
//        //缩放至屏幕大小
//        webSettings.setLoadWithOverviewMode(true);
//
//        MyWebView.setWebViewClient(new WebViewClient() {
//            @Override
//            public void onPageStarted(WebView view, String url, Bitmap favicon) {
//                super.onPageStarted(view, url, favicon);
//            }
//
//            @Override
//            public void onPageFinished(WebView view, String url) {
//                super.onPageFinished(view, url);
//                JniHelper.onVideoPlayerAssetCallback(1);
//            }
//
//            @Override
//            public void onReceivedError(WebView view, int errorCode,
//                                        String description, String failingUrl) {
//                super.onReceivedError(view, errorCode, description, failingUrl);
//                JniHelper.onVideoPlayerAssetCallback(2);
//            }
//        });
//
//        Log.e("org.HTQP.game","---------------------------------------LowestWebview 初始化结束");
//    }
}
