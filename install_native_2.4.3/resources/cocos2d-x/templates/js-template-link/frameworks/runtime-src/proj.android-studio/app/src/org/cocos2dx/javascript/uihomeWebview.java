package org.cocos2dx.javascript;

import android.app.Activity;
import android.graphics.Bitmap;
import android.graphics.Color;
import android.os.Bundle;
import android.util.DisplayMetrics;
import android.view.MotionEvent;
import android.view.View;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Button;

public class uihomeWebview extends Activity {

//    public Button HomeBut = null;
//    public WebView mainWebView = null;
//    private int screenWidth,screenHeight;
//
//    @Override
//    protected void onCreate(@Nullable Bundle savedInstanceState) {
//        super.onCreate(savedInstanceState);
//        setContentView(R.layout.home_webview);
//
//        //取得传递过来的地址
//        String URL = getIntent().getExtras().getString("URL");
//
//        HomeBut = findViewById(R.id.HomeBut);
//        mainWebView = findViewById(R.id.webView);
//        mainWebView.setBackgroundColor(Color.TRANSPARENT);
//
//        // 清缓存和记录，缓存引起的白屏
//        mainWebView.clearCache(true);
//        mainWebView.clearHistory();
//
//        mainWebView.requestFocus();
//        WebSettings webSettings = mainWebView.getSettings();
//
//        // 缓存白屏
//        String appCachePath = getApplicationContext().getCacheDir().getAbsolutePath() + "/webcache";
//        // 设置 Application Caches 缓存目录
//        webSettings.setAppCachePath(appCachePath);
//
//
//        webSettings.setDomStorageEnabled(true);
//        webSettings.setAppCacheEnabled(false);
//
//
//        mainWebView.setWebViewClient(new WebViewClient() {
//            @Override
//            public void onPageStarted(WebView view, String url, Bitmap favicon) {
//                super.onPageStarted(view, url, favicon);
//            }
//
//            @Override
//            public void onPageFinished(WebView view, String url) {
//                super.onPageFinished(view, url);
//            }
//
//            @Override
//            public boolean shouldOverrideUrlLoading(WebView view, String url) {
//                // 重写此方法表明点击网页里面的链接还是在当前的webview里跳转，不另跳浏览器
//                // 在2.3上面不加这句话，可以加载出页面，在4.0上面必须要加入，不然出现白屏
//
//                if (url.startsWith("http://") || url.startsWith("https://")) {
//                    view.loadUrl(url);
//                    mainWebView.stopLoading();
//                    return true;
//                }
//                return false;
//            }
//
//            @Override
//            public void onReceivedError(WebView view, int errorCode,
//                                        String description, String failingUrl) {
//                super.onReceivedError(view, errorCode, description, failingUrl);
//            }
//
//
//        });
//
//        //为webview设置URL
//        mainWebView.loadUrl(URL);//加载url
//        HomeBut.setOnClickListener(clickEnent);
//
//        //返回游戏拖动
//        DisplayMetrics dm = getResources().getDisplayMetrics();
//        screenWidth = dm.widthPixels;
//        screenHeight = dm.heightPixels;
//        HomeBut.setOnTouchListener(new View.OnTouchListener() {
//            int lastX, lastY; // 记录移动的最后的位置
//            private int btnHeight;
//
//            public boolean onTouch(View v, MotionEvent event) {
//                // 获取Action
//                int ea = event.getAction();
//                switch (ea) {
//                    case MotionEvent.ACTION_DOWN: // 按下
//                        lastX = (int) event.getRawX();
//                        lastY = (int) event.getRawY();
//                        btnHeight = HomeBut.getHeight();
//                        break;
//                    case MotionEvent.ACTION_MOVE: // 移动
//                        // 移动中动态设置位置
//                        int dx = (int) event.getRawX() - lastX;
//                        int dy = (int) event.getRawY() - lastY;
//                        int left = v.getLeft() + dx;
//                        int top = v.getTop() + dy;
//                        int right = v.getRight() + dx;
//                        int bottom = v.getBottom() + dy;
//                        if (left < 0) {
//                            left = 0;
//                            right = left + v.getWidth();
//                        }
//                        if (right > screenWidth) {
//                            right = screenWidth;
//                            left = right - v.getWidth();
//                        }
//                        if (top < 0) {
//                            top = 0;
//                            bottom = top + v.getHeight();
//                        }
//                        if (bottom > screenHeight) {
//                            bottom = screenHeight;
//                            top = bottom - v.getHeight();
//                        }
//                        v.layout(left, top, right, bottom);
//                        // Toast.makeText(getActivity(), "position：" + left + ", " +
//                        // top + ", " + right + ", " + bottom, 0)
//                        // .show();
//                        // 将当前的位置再次设置
//                        lastX = (int) event.getRawX();
//                        lastY = (int) event.getRawY();
//                        break;
//                    case MotionEvent.ACTION_UP: // 抬起
//                        //向四周吸附
//                        int dx1 = (int) event.getRawX() - lastX;
//                        int dy1 = (int) event.getRawY() - lastY;
//                        int left1 = v.getLeft() + dx1;
//                        int top1 = v.getTop() + dy1;
//                        int right1 = v.getRight() + dx1;
//                        int bottom1 = v.getBottom() + dy1;
//                        if (left1 < (screenWidth / 2)) {
//                            if (top1 < 100) {
//                                v.layout(left1, 0, right1, btnHeight);
//                            } else if (bottom1 > (screenHeight - 200)) {
//                                v.layout(left1, (screenHeight - btnHeight), right1, screenHeight);
//                            } else {
//                                v.layout(0, top1, btnHeight, bottom1);
//                            }
//                        } else {
//                            if (top1 < 100) {
//                                v.layout(left1, 0, right1, btnHeight);
//                            } else if (bottom1 > (screenHeight - 200)) {
//                                v.layout(left1, (screenHeight - btnHeight), right1, screenHeight);
//                            } else {
//                                v.layout((screenWidth - btnHeight), top1, screenWidth, bottom1);
//                            }
//                        }
//                        break;
//                }
//                return false;
//            }
//        });
//    }
//
//    public View.OnClickListener clickEnent = new View.OnClickListener()
//    {
//        @Override
//        public void onClick(View v) {
//            switch (v.getId())
//            {
//                case R.id.HomeBut:
//                    {
//                        //弹出询问框
//                        new ExitAlertDialog(uihomeWebview.this).builder().setMsg("要返回游戏吗？").setPositiveButton(new View.OnClickListener() {
//                            @Override
//                            public void onClick(View v) {
//								finish();
//                            }
//                        }).setNegativeButton(new View.OnClickListener() {
//                            @Override
//                            public void onClick(View v) {
//                                //取消事件
//                            }
//                        }).show();
//                    }
//                    break;
//            }
//        }
//    };
}
