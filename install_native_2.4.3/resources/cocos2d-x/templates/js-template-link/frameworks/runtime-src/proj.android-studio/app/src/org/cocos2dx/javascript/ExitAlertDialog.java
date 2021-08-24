package org.cocos2dx.javascript;

import android.app.Dialog;
import android.content.Context;
import android.view.Display;
import android.view.LayoutInflater;
import android.view.View;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import android.widget.TextView;

public class ExitAlertDialog {

//    private Dialog dialog;
//    private Context context;
//    private Display display;
//
//    private LinearLayout lineLayout;
//    private TextView txt_msg;
//    private TextView txt_line;
//    private Button YesBut;
//    private Button NoBut;
//
//    private boolean showPosBtn = false;
//    private boolean showNegBtn = false;
//
//    public ExitAlertDialog(Context context)
//    {
//        this.context = context;
//        WindowManager windowManager = (WindowManager) context
//                .getSystemService(Context.WINDOW_SERVICE);
//        display = windowManager.getDefaultDisplay();
//    }
//
//    public ExitAlertDialog builder() {
//        // 获取Dialog布局
//        View view = LayoutInflater.from(this.context).inflate(
//                R.layout.exit_alert_dialog, null);
//
//        // 获取自定义Dialog布局中的控件
//        lineLayout = (LinearLayout) view.findViewById(R.id.lLayout_bg);
//        txt_msg = (TextView) view.findViewById(R.id.txt_msg);
//        txt_line = (TextView) view.findViewById(R.id.line);
//        txt_line.setVisibility(View.GONE);
//        YesBut = (Button) view.findViewById(R.id.btn_yes);
//        YesBut.setVisibility(View.GONE);
//        NoBut = (Button) view.findViewById(R.id.btn_no);
//        NoBut.setVisibility(View.GONE);
//
//        // 定义Dialog布局和参数
//        dialog = new Dialog(context, R.style.AlertDialogStyle);
//        dialog.setContentView(view);
//
//        // 调整dialog背景大小
//        if(display.getWidth() > display.getHeight())
//        {
//            lineLayout.setLayoutParams(new FrameLayout.LayoutParams((int) (display
//                    .getWidth() * 0.60), (int) (display.getWidth() * 0.60 * 0.66)));
//        }
//        else
//        {
//            lineLayout.setLayoutParams(new FrameLayout.LayoutParams((int) (display
//                    .getWidth() * 0.90), (int) (display.getWidth() * 0.90 * 0.66)));
//
//			android.view.ViewGroup.LayoutParams lp=YesBut.getLayoutParams();
//            lp.width*=0.8;
//            lp.height*=0.8;
//            YesBut.setLayoutParams(lp);
//            android.view.ViewGroup.LayoutParams lp2=NoBut.getLayoutParams();
//            lp2.width*=0.8;
//            lp2.height*=0.8;
//            NoBut.setLayoutParams(lp2);
//        }
//
//        return this;
//    }
//
//    public ExitAlertDialog setMsg(String msg) {
//        if ("".equals(msg)) {
//            txt_msg.setText("内容");
//        } else {
//            txt_msg.setText(msg);
//        }
//        return this;
//    }
//
//    public ExitAlertDialog setPositiveButton(final View.OnClickListener listener) {
//        showPosBtn = true;
//        YesBut.setOnClickListener(new View.OnClickListener() {
//            @Override
//            public void onClick(View v) {
//                listener.onClick(v);
//                dialog.dismiss();
//            }
//        });
//        return this;
//    }
//
//    public ExitAlertDialog setNegativeButton(final View.OnClickListener listener) {
//        showNegBtn = true;
//        NoBut.setOnClickListener(new View.OnClickListener() {
//            @Override
//            public void onClick(View v) {
//                listener.onClick(v);
//                dialog.dismiss();
//            }
//        });
//        return this;
//    }
//
//    private void setLayout() {
//
//        if (!showPosBtn && !showNegBtn) {
//            YesBut.setVisibility(View.VISIBLE);
//            YesBut.setOnClickListener(new View.OnClickListener() {
//                @Override
//                public void onClick(View v) {
//                    dialog.dismiss();
//                }
//            });
//        }
//
//        if (showPosBtn && showNegBtn) {
//            YesBut.setVisibility(View.VISIBLE);
//            NoBut.setVisibility(View.VISIBLE);
//            txt_line.setVisibility(View.VISIBLE);
//        }
//
//        if (showPosBtn && !showNegBtn) {
//            YesBut.setVisibility(View.VISIBLE);
//        }
//
//        if (!showPosBtn && showNegBtn) {
//            NoBut.setVisibility(View.VISIBLE);
//        }
//    }
//
//    public void show() {
//        setLayout();
//        dialog.show();
//    }
}
