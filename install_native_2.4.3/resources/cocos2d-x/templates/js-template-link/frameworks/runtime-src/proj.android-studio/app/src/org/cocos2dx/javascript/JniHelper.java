package org.cocos2dx.javascript;

import android.Manifest;
import android.app.Activity;
import android.app.AlertDialog;
import android.bluetooth.BluetoothAdapter;
import android.content.BroadcastReceiver;
import android.content.ClipData;
import android.content.ClipDescription;
import android.content.ClipboardManager;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.pm.ActivityInfo;
import android.content.pm.PackageInfo;
import android.content.pm.PackageManager;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.hardware.Sensor;
import android.hardware.SensorManager;
import android.location.Location;
import android.net.ConnectivityManager;
import android.net.NetworkInfo.State;
import android.net.Uri;
import android.net.wifi.WifiInfo;
import android.net.wifi.WifiManager;
import android.os.Build;
import android.os.Environment;
import android.os.Handler;
import android.os.Message;
import android.provider.ContactsContract;
import android.provider.Settings;
import android.support.v4.app.ActivityCompat;
import android.telephony.TelephonyManager;
import android.text.TextUtils;
import android.util.Log;
import android.view.OrientationEventListener;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.RelativeLayout;

import org.cocos2dx.lib.Cocos2dxActivity;
import org.cocos2dx.lib.Cocos2dxJavascriptJavaBridge;
import org.json.JSONObject;

import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.DataInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URI;
import java.net.URL;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.ArrayList;
import java.util.List;

public class JniHelper extends Cocos2dxActivity{

	public static Activity m_mainActivity;
	public static String m_mac;
	public static int m_strength;
//	public static YunCengHelp yunCengHelp;
	//public static PayController sdkController;

	public static int m_iFirst;
	public static int m_iSecond;
	public static int m_iThird;
	public static double m_Longitude;
	public static double m_Latitude;
	public static Location m_location;
	public static Bitmap m_bitmap;

	public static String m_filenname;
	public static int m_stata = 0;
	public static String m_VersionName;
	public static int m_battery = 0;
	public static String m_sType = "set";
	public static CharSequence m_CopyTxt;
	public static int m_phone = 0;
	public static String m_phoneType = "set";

	public static Boolean m_isShowHomeView = false;

	//拖动home按钮
	private static RelativeLayout m_layout = null;
	private static String  m_HomeDesc = null;
	private static Button m_HomeBt;
	private static int screenWidth,screenHeight;

	private static OrientationEventListener orientationEventListener;
	// 这是记录当前角度
	private static int m_rotationFlag = 90;
	private static int m_rotationRecord = 90;

	private static final int REQUEST_EXTERNAL_STORAGE = 1;
	private static String[] PERMISSIONS_STORAGE = {
			Manifest.permission.READ_CONTACTS,
			Manifest.permission.WRITE_CONTACTS,
			Manifest.permission.SEND_SMS};

	//游戏盾数据记录
	public static String m_strDomain;

	/**
	 * 拍照的图片路径
	 */
	public static String m_strPath;
	public static String m_strUserID;
	public static File m_saveDirFile;

	public static Uri m_imageUri;
	public static String m_fileprovider = "";

	//动态获取权限监听
	private static MyPermissionListener m_Listener;
	public static CameraHelp m_CameraController;

	//最下层WebView
//	public static LowestWebView MayLowestWeb = null;
	
	public JniHelper(Activity main) {

		m_mainActivity = main;
        //sdkController = new PayController(main);
//		yunCengHelp = new YunCengHelp(main);

//		MayLowestWeb = new LowestWebView((Cocos2dxActivity)main);

//		String AppID = "wx490adb573d82274e";
//		String AppSecret = "9edfa349d28519fd8e23ac52fe1294e8";
//		String WXPartnerID = "";
//		String CreatePayOreder = "";
//		sdkController.setWXData(AppID, AppSecret, WXPartnerID, CreatePayOreder);
//		sdkController.WXinit();

		getDeviceId(main);

		//keep screen on
		m_mainActivity.getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);

		//旋转监听
		rotationListener();

		//网络变化 get netstate
		MyNetChange network = new MyNetChange();
		m_mainActivity.registerReceiver(network, new IntentFilter(ConnectivityManager.CONNECTIVITY_ACTION));

		//电量通知
		MyBattery battery = new MyBattery();
		m_mainActivity.registerReceiver(battery, new IntentFilter(Intent.ACTION_BATTERY_CHANGED));

		//wifi改变
		WifiChangeBroadcastReceiver wifiChange = new WifiChangeBroadcastReceiver();
		m_mainActivity.registerReceiver(wifiChange, new IntentFilter(WifiManager.RSSI_CHANGED_ACTION));

//		PhoneBroadcastReceiver phoneRecevier = new PhoneBroadcastReceiver();
//		m_mainActivity.registerReceiver(phoneRecevier, new IntentFilter());

		//剪贴板
		// testClipboard();

		getVerName(m_mainActivity);
	}

	//stop Simulator
	public static void OnStopSimulator()
	{
		getSimulator(m_mainActivity);
	}

	public static int GetStrength()
	{
		return m_strength;
	}
	public static String GetAppVersion()
	{
		return m_VersionName;
	}
	public static String GetMac() {
		return m_mac;
	}
	public static int GetBattery()
	{
		return m_battery;
	}

	 public static void getText() {  
		Message msgMessage = new Message();
		getCopyTxt.sendMessage(msgMessage);
	 }
	
	 public static void setConText(final String szText) {

		Message msgMessage = new Message();
		msgMessage.obj = szText;
		
		setCopyTxt.sendMessage(msgMessage);
	 }
	 public static void setTextNull()
	 {
		 ClipboardManager cm = (ClipboardManager)m_mainActivity.getSystemService(Context.CLIPBOARD_SERVICE);
		 cm.setPrimaryClip(null);
	 }

    public static void GetInstallBindData()
    {
//		final SharedPreferences sp = getSharedPreferences("openinstalldemo", MODE_PRIVATE);
//		boolean needInstall = sp.getBoolean("needInstall", true);
//
//		Log.e("needInstall", "needInstall :"+ needInstall + "------------------------------- ");
//		if (needInstall) {  //是否是第一次启动
//			//获取OpenInstall数据，推荐每次需要的时候调用，而不是自己保存数据
//			OpenInstall.getInstall(new AppInstallAdapter() {
//				@Override
//				public void onInstall( AppData appData) {
//					//获取渠道数据
//					String channelCode = appData.getChannel();
//					//获取个性化安装数据
//					final String strBindData = appData.getData();
//
//					Log.e("channelCode", "channelCode :"+ channelCode + " + strBindData:"+strBindData);
//
//					if (!appData.isEmpty())
//					{
//						((Cocos2dxActivity) JniHelper.m_mainActivity).runOnGLThread(new Runnable() {
//							public void run() {
//								String getInstall = "window.mfConfig.OnSetInstallDataCallback(\'"+strBindData+"\');";
//
//								Cocos2dxJavascriptJavaBridge.evalString( getInstall );
//							}
//						});
//
//						Log.e("OpenInstall", "getInstall : installData = " + strBindData );
//
//					}
//				}
//			});
//
//			//只有第一次启动App才去获取，以后将不再获取：将needInstall设置为false
////            sp.edit().putBoolean("needInstall", false).apply();
//		}
    }

	 //open App for packageName
	 public static void OpenAppForPackage( final String packName) 
	 {
		 //check app
		 if( isAvilible(packName) )
		 {
			 Intent intent = m_mainActivity.getPackageManager().getLaunchIntentForPackage(packName);
			 m_mainActivity.startActivity(intent);
		 }
		 else
		 {
			 Log.e("---------", " Not Installed"+packName );
			 ((Cocos2dxActivity) m_mainActivity).runOnGLThread(new Runnable() {
					public void run() {
						String DownResult = "window.mfConfig.IsInstall("+ "\""+ packName+ "\""+ ","+ "\""+ false+ "\""+ ");";
						Cocos2dxJavascriptJavaBridge.evalString(DownResult);
					}
				});
		 }
	 }

	 //Close App
	 public static void OnCloseApp( ) 
	 {
		 Log.e("---------", "CloseApp");
		 System.exit(0);
	 }
	 
	 //bInstalled from packName
 	public static boolean isAvilible( final String packName )
    {
        final PackageManager packageManager = m_mainActivity.getPackageManager();
        // check installed app information
        List<PackageInfo> pinfo = packageManager.getInstalledPackages(0);
        for ( int i = 0; i < pinfo.size(); i++ )
        {
            if(pinfo.get(i).packageName.equalsIgnoreCase(packName))
                return true;
        }
        return false;
    }
 	
 	//open App for Scheme
 	public static boolean OpenAppForScheme( final String strSchemeUrl, final String strAppName) 
 	{
 		URI uri = URI.create(strSchemeUrl);
 		String strScheme =  (uri != null) ? uri.getScheme()+"://" : "";
 		
 		//check app
 		if( IsInstallForScheme(strScheme) )
 		{
 			Log.e("OpenAppForScheme", "Installed app,SchemeUrl"+strSchemeUrl );
 			final PackageManager packageManager = m_mainActivity.getPackageManager();
 	        Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse(strSchemeUrl));
 	        intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_RESET_TASK_IF_NEEDED);
 			m_mainActivity.startActivity(intent);
 			return true;
 		}
 		else
 		{
 			Log.e("OpenAppForScheme", "Not Installed app,SchemeUrl"+strSchemeUrl );
 			((Cocos2dxActivity) m_mainActivity).runOnGLThread(new Runnable() {
 				public void run() {
 					String DownResult = "window.mfConfig.OpenAppForSchemeFail(\""+strAppName+"\");";
 					Cocos2dxJavascriptJavaBridge.evalString(DownResult);
 				}
 			});
 			return false;
 		}
 	}
 	
 	 //bInstalled from Scheme
 	public static boolean IsInstallForScheme( final String strScheme )
    {
        final PackageManager packageManager = m_mainActivity.getPackageManager();
        Intent in = new Intent(Intent.ACTION_VIEW, Uri.parse(strScheme));
        if (in.resolveActivity(packageManager) == null)
        	return false;
        else
        	return true;   	
    }
	
	//upload file
	@SuppressWarnings("unused")
	public static void UploadFileByHttpPost( final String fullpath_file, String fullreq_url) {

		Log.e("fullpath_file", "fullpath_file:" + fullpath_file);
		Log.e("fullreq_url", "fullreq_url:" + fullreq_url);

		final int nUploadSuccess = 740;
		final int nUploadFailure = 750;

		File tempFile =new File( fullpath_file.trim());
		String fileName = tempFile.getName();

		String strUploadUrl = fullreq_url + "?filename="+fileName;
		Log.e("---UploadFileByHttpPost","strUploadUrl:"+strUploadUrl);
        // TODO Auto-generated method stub
		int numReadByte=0;
		String result="";
        try
		{
            URL url=new URL(strUploadUrl);
            HttpURLConnection connection=(HttpURLConnection)url.openConnection();
            connection.setDoInput(true);
            connection.setDoOutput(true);
            connection.setRequestMethod("POST");
	        connection.addRequestProperty("FileName", fileName);
            connection.setRequestProperty("content-type", "text/html");
            BufferedOutputStream  out=new BufferedOutputStream(connection.getOutputStream());
            
            //read file upload
            File file=new File(fullpath_file);
            FileInputStream fileInputStream=new FileInputStream(file);
            byte[]bytes=new byte[1024];

			while((numReadByte=fileInputStream.read(bytes,0,1024))>0)
			{
				out.write(bytes, 0, numReadByte);
			}
			// 定义BufferedReader输入流来读取URL的响应
			BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
			String line = null;
			while ((line = reader.readLine()) != null)
			{
				result += line; //这里读取的是上边url对应的上传文件接口的返回值，读取出来后，然后接着返回到前端，实现接口中调用接口的方式
			}
			JSONObject jsonData = new JSONObject(result);
			int nResultCode = jsonData.getInt("code");
			final String strUoload_Path = jsonData.getJSONObject("data").getString("src");
			Log.e("--------strUoload_Path","strUoload_Path:"+strUoload_Path);
			//返回值0代表上传成功
			if( nResultCode == 0 )
			{
				((Cocos2dxActivity) m_mainActivity).runOnGLThread(new Runnable()
				{
					public void run()
					{
						Log.e("-------------upload","OK");
						String DownResult = "window.mfConfig.OnUpdateFileReq_AndroidDone(\""+nUploadSuccess+"\""+ "," +"\""+ strUoload_Path+ "\");";
						Cocos2dxJavascriptJavaBridge.evalString(DownResult);
					}
				});
			}
			//上传失败
			else
			{
				String strErrorMsg = jsonData.get("msg").toString();
				Log.e("---UploadPost","UoloadFaile,  msg :"+ strErrorMsg );
				((Cocos2dxActivity) m_mainActivity).runOnGLThread(new Runnable()
				{
					public void run()
					{
						String DownResult = "window.mfConfig.OnUpdateFileReq_AndroidDone(\""+nUploadFailure+"\");";
						Cocos2dxJavascriptJavaBridge.evalString(DownResult);
					}
				});
			}
            out.flush();
            fileInputStream.close();
//          read URLConnection callfun
            DataInputStream in=new DataInputStream(connection.getInputStream());
		}
		catch (Exception e)
		{
			System.out.println("发送POST请求出现异常！" + e);
			e.printStackTrace();
		}
		Log.e("-------------result","result:"+result );
    }


	//download file
	public static void DownLoad(String urlStr, final String fileName, String savePath) {
		try {
			URL url = new URL(urlStr);
			HttpURLConnection conn = (HttpURLConnection) url.openConnection();
			conn.setConnectTimeout(3 * 1000);
			conn.setRequestProperty("User-Agent", "Mozilla/4.0 (compatible; MSIE 5.0; Windows NT; DigExt)");
			InputStream inputStream = conn.getInputStream();

			byte[] getData = readInputStream(inputStream);

			File directory = new File(savePath);  
            if (!directory.exists()) {  
            	 directory.mkdirs();
            } 

			File file = new File(savePath , fileName);

			if (!file.isFile()) {  
				file.createNewFile();
            } 
			FileOutputStream fos = new FileOutputStream(savePath + fileName);
			fos.write(getData);
			if (fos != null) {
				fos.close();	
			}
			if (inputStream != null) {
				inputStream.close();

				((Cocos2dxActivity) m_mainActivity).runOnGLThread(new Runnable() {
					public void run() {
						String DownResult = "window.mfConfig.OnVoiceDownLoadBack("+ "\""+ 770+ "\""+ ","+ "\""+ fileName+ "\""+ ");";
						Cocos2dxJavascriptJavaBridge.evalString(DownResult);
					}
				});
			}
			else {

				((Cocos2dxActivity) m_mainActivity).runOnGLThread(new Runnable() {
					public void run() {
						String DownResult = "window.mfConfig.OnVoiceDownLoadBack("+ "\""+ 780+ "\""+ ","+ "\""+ fileName+ "\""+ ");";
						Cocos2dxJavascriptJavaBridge.evalString(DownResult);
					}
				});
			}
			Log.e("info:" ,"url:"+ url + " download success");
		} catch (Exception e) {
			// TODO: handle exception
			e.printStackTrace();
		}
	}

	/**
	 *
	 * 
	 * @param inputStream
	 * @return
	 * @throws IOException
	 */
	public static byte[] readInputStream(InputStream inputStream)
			throws IOException {
		byte[] buffer = new byte[1024];
		int len = 0;
		ByteArrayOutputStream bos = new ByteArrayOutputStream();
		while ((len = inputStream.read(buffer)) != -1) {
			bos.write(buffer, 0, len);
		}
		bos.close();
		return bos.toByteArray();
	}
	
	public static Handler stateHandler = new Handler(){
		public void handleMessage(final android.os.Message msg) {	
			((Cocos2dxActivity) m_mainActivity).runOnGLThread(new Runnable() {
				public void run() {
					String stateHandler = "NativeBridge.NetworkStateCallback(" + "'" + m_stata+ "'" + "," + "'" + m_sType+ "'" + ");";
					Cocos2dxJavascriptJavaBridge.evalString(stateHandler);
				}
			});
		};
	};
	
	public static Handler statePhone = new Handler(){
		public void handleMessage(final android.os.Message msg) {	
			((Cocos2dxActivity) m_mainActivity).runOnGLThread(new Runnable() {
				public void run() {
					// String stateHandler = "NativeBridge.NetworkStateCallback("+ "\""+ m_phone+ "\""+ ","+ "\""+ m_phoneType+ "\""+ ");";
					String stateHandler = "NativeBridge.NetworkStateCallback(" + "'" + m_phone+ "'" + "," + "'" + m_phoneType+ "'" + ");";
					Cocos2dxJavascriptJavaBridge.evalString(stateHandler);
				}
			});
		};
	};

	public static Handler HomeViewCall = new Handler();

	static Runnable HomeViewReturnRun = new Runnable() {
		@Override
		public void run() {
			JniHelper.OnHomeView_Callback();
		}
	};

	public  static  void  OnHomeView_Callback ( )
	{
		((Cocos2dxActivity) m_mainActivity).runOnGLThread(new Runnable() {
			public void run() {
				String stateHandler = "NativeBridge.OnAddHomeViewRet();";
				Cocos2dxJavascriptJavaBridge.evalString(stateHandler);
			}
		});
	}

	//getNetState
    public static void getNetState()
	{
		ConnectivityManager manager = (ConnectivityManager) m_mainActivity.getSystemService(Context.CONNECTIVITY_SERVICE); 
		
		State mobileInfo = null;
        State wifiInfo = null;
        if (manager != null) 
        { 
        	mobileInfo = manager.getNetworkInfo(ConnectivityManager.TYPE_MOBILE).getState();
        	wifiInfo = manager.getNetworkInfo(ConnectivityManager.TYPE_WIFI).getState();
        	
        	int nState = 0;
            // connect ok  
            if (wifiInfo != null && mobileInfo != null  
                    && State.CONNECTED != wifiInfo  
                    && State.CONNECTED == mobileInfo) 
            {  
            	nState = 606;
            } 
            // no connect  
            else if (wifiInfo != null && mobileInfo != null  
                    && State.CONNECTED != wifiInfo  
                    && State.CONNECTED != mobileInfo) 
            {  
            	nState = 607;
            }
            // wifi connect
            else if (wifiInfo != null && State.CONNECTED == wifiInfo) {  
            	nState = 605;
            }
            m_stata = nState;
            m_sType = "Get";
            Message msgMessage = new Message();
            stateHandler.sendMessage(msgMessage);
        } 
	}
	
	
	//net delay
	public static String netDelay(String szUrl)
	{
		@SuppressWarnings("unused")
		String lost = new String();  
        String delay = new String();  
        Process p = null;
		try {
			p = Runtime.getRuntime().exec("ping -c 4 " + szUrl);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}  
        BufferedReader buf = new BufferedReader(new InputStreamReader(p.getInputStream()));  
        String str = new String();  
        try {
			while((str=buf.readLine())!=null){  
//			       if(str.contains("packet loss")){  
//			           int i= str.indexOf("received");  
//			           int j= str.indexOf("%");     
//			           lost = str.substring(i+10, j+1);  
//			       }  
			       if(str.contains("avg")){  
			           int i=str.indexOf("/", 20);  
			           int j=str.indexOf(".", i);  
			           delay =str.substring(i+1, j);  
			        }  

			   }
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

		return delay; 
	}

	//打开相机和相册选择框
	public static void OnSaveImagePicker( String strUserID,  String strSaveDir )
	{
		File directory = new File(strSaveDir);
		m_saveDirFile = directory;
		m_strUserID = strUserID;

		Message msgMessage = new Message();
//		msgMessage.obj = m_strUserID;
		AlerDialogHandler.sendMessage(msgMessage);
	}

	public  static  void  OnSaveReq_DoneCallback ( final String strFullpathFile )
	{
        Log.e("OnSaveReq_DoneCallback","strFullpathFile"+strFullpathFile);
		((Cocos2dxActivity) m_mainActivity).runOnGLThread(new Runnable() {
			public void run() {
				String DownResult = "window.mfConfig.OnImagePickerReq_AndroidDone("+ "\""+ strFullpathFile +"\""+ ");";
				Cocos2dxJavascriptJavaBridge.evalString(DownResult);
			}
		});
	}

	//获取ip
	public static void OnGetIpByYunCeng( String strGroupname, String strDomain,  String strPort)
	{
		Log.e("==========游戏盾=========", "进入获取");
		m_strDomain = strDomain;
//		yunCengHelp.OnGetLoginAddress( strGroupname, strDomain, strPort );
	}


	public static void Test(String szLogDesc) {
		Log.e("123456789", "Test:" + szLogDesc);
	}


	//保存图片
	public static void SaveImage(String imgPath)
	{
		Bitmap bmp = BitmapFactory.decodeFile(imgPath);
		String fileName = System.currentTimeMillis() + ".jpg";

		m_bitmap  = bmp;
		if(isGrantExternalRW(m_mainActivity))
			saveImageToGallery(m_mainActivity,bmp);
	}



	//获取权限
	public static boolean isGrantExternalRW(Activity activity) {
		if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M && activity.checkSelfPermission(
				Manifest.permission.WRITE_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED)
		{
			activity.requestPermissions(new String[]{
					Manifest.permission.READ_EXTERNAL_STORAGE,
					Manifest.permission.WRITE_EXTERNAL_STORAGE
			}, 1);

			return false;
		}

		return true;
	}



	public static void saveImageToGallery(Context context, Bitmap bmp) {

		// 首先保存图片
		String storePath = Environment.getExternalStorageDirectory() + File.separator + "dearxy";

		File appDir = new File(storePath);
		if (!appDir.exists()) {
			appDir.mkdir();
		}

		String fileName = System.currentTimeMillis() + ".jpg";
		File file = new File(appDir, fileName);
		try {
			FileOutputStream fos = new FileOutputStream(file);
			//通过io流的方式来压缩保存图片
			boolean isSuccess = bmp.compress(Bitmap.CompressFormat.JPEG, 60, fos);
			fos.flush();
			fos.close();

			//把文件插入到系统图库
			//MediaStore.Images.Media.insertImage(context.getContentResolver(), file.getAbsolutePath(), fileName, null);

			//保存图片后发送广播通知更新数据库
			Uri uri = Uri.fromFile(file);

			context.sendBroadcast(new Intent(Intent.ACTION_MEDIA_SCANNER_SCAN_FILE, Uri.fromFile(new File(file.getPath()))));
			//context.sendBroadcast(new Intent(Intent.ACTION_MEDIA_SCANNER_SCAN_FILE, uri));

			if (isSuccess) {

				((Cocos2dxActivity) m_mainActivity).runOnGLThread(new Runnable() {
					public void run() {
						String LogonResult = "window.mfConfig.OnSaveImageCallback(\"" + 3000 + "\");";
						Cocos2dxJavascriptJavaBridge.evalString(LogonResult);
					}
				});

			} else {
				((Cocos2dxActivity) m_mainActivity).runOnGLThread(new Runnable() {
					public void run() {

						String LogonResult = "window.mfConfig.OnSaveImageCallback(\"" + 30001 + "\");";
						Cocos2dxJavascriptJavaBridge.evalString(LogonResult);

					}
				});
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	public interface MyPermissionListener {
		/**
		 * 成功获取权限
		 */
		void onGranted();

		/**
		 * 为获取权限
		 */
		void onDenied(List<String> deniedPermission);
	};

	//andrpoid 6.0 需要写运行时权限
	public static void requestRuntimePermission(String[] permissions, MyPermissionListener listener) {

		m_Listener = listener;
		List<String> permissionList = new ArrayList<>();
		for (String permission : permissions) {
			if (ActivityCompat.checkSelfPermission( JniHelper.m_mainActivity, permission)
					!= PackageManager.PERMISSION_GRANTED) {
				permissionList.add(permission);
			}
		}
		if (!permissionList.isEmpty()) {
			ActivityCompat.requestPermissions(JniHelper.m_mainActivity,
					permissionList.toArray(new String[permissionList.size()]), 1);
		} else {
			m_Listener.onGranted();
		}
	}

	public static Handler AlerDialogHandler = new Handler()
	{
		public void handleMessage(Message msg)
		{
			final String items[] = { "相机", "相册" };
			AlertDialog.Builder singleChoiceDialog = new AlertDialog.Builder( JniHelper.m_mainActivity );
			singleChoiceDialog.setTitle("请选择你的操作");
			// 第二个参数是默认选项，此处设置为0
			singleChoiceDialog.setItems( items,
					new DialogInterface.OnClickListener() {
						@Override
						public void onClick(DialogInterface dialog, int which)
						{
							//打开相机
							if( which == 0 )
							{
								String[] permissions = {
										Manifest.permission.CAMERA, Manifest.permission.READ_EXTERNAL_STORAGE,
										Manifest.permission.WRITE_EXTERNAL_STORAGE
								};

								requestRuntimePermission(permissions, new MyPermissionListener() {
									@Override public void onGranted()
									{
//                                       myTakePhotoFor7();
										m_CameraController.openCamera(JniHelper.m_mainActivity, CameraHelp.REQUEST_PHOTO_CARMERA );
									}

									@Override public void onDenied(List<String> deniedPermission) {
//                                        Toast.makeText(getBaseContext(), deniedPermission.toString()+"权限被拒绝",Toast.LENGTH_LONG).show();
										//有权限被拒绝，什么也不做好了，看你心情
									}
								});
							}
							//打开相册
							else
							{
								m_CameraController.openAlbum( JniHelper.m_mainActivity, CameraHelp.REQUEST_PHOTO_PICK  );
							}
						}
					});
			singleChoiceDialog.show();
		};
	};

	//打开webview
	public static void OnOpenhomeWebView(String URL,String Desc)
	{
		//打开一个带返回按钮的activity
//			Intent intent = new Intent(m_mainActivity,uihomeWebview.class);
//			intent.putExtra("URL",URL);
//			m_mainActivity.startActivity(intent);
//			m_isShowHomeView = true;
		m_HomeDesc = Desc;
		Message msgMessage = new Message();
		ShowHomeBt.sendMessage(msgMessage);
	}

	public static Handler ShowHomeBt = new Handler()
	{
		public void handleMessage(Message msg) {
			CreateHomeButton();
		};
	};

	//创建home按钮
	public static void CreateHomeButton()
	{
//		final LayoutInflater inflater = LayoutInflater.from(m_mainActivity);
//		if(m_layout != null)
//		{
//			ViewGroup vg = (ViewGroup) m_layout.getParent();
//			vg.removeView(m_layout);
//			m_layout = null;
//		}
//		m_layout = (RelativeLayout) inflater.inflate(
//				R.m_layout.home_view, null);
//
//		if(m_layout == null)
//			return;
//
//		m_mainActivity.addContentView(layout,  new WindowManager.LayoutParams(
//				WindowManager.LayoutParams.FLAG_FULLSCREEN,
//				WindowManager.LayoutParams.FLAG_FULLSCREEN));
//
//		m_HomeBt = m_layout.findViewById(R.id.HomeBut);
//		m_HomeBt.setOnClickListener(new View.OnClickListener() {
//			@Override
//			public void onClick(View view) {
//				//弹出询问框
//				String des = null;
//				if(m_HomeDesc != null) des = m_HomeDesc;
//				else des = "要返回游戏吗？";
//
//				new ExitAlertDialog(m_mainActivity).builder().setMsg(m_HomeDesc).setPositiveButton(new View.OnClickListener() {
//					@Override
//					public void onClick(View v) {
//						ViewGroup vg = (ViewGroup) m_HomeBt.getParent();
//						vg.removeView(m_HomeBt);
//
//						HomeViewCall.postDelayed(HomeViewReturnRun, 50);
//					}
//				}).setNegativeButton(new View.OnClickListener() {
//					@Override
//					public void onClick(View v) {
//						//取消事件
//					}
//				}).show();
//			}
//		});
//
//		//返回游戏拖动
//		DisplayMetrics dm = m_mainActivity.getResources().getDisplayMetrics();
//		screenWidth = dm.widthPixels;
//		screenHeight = dm.heightPixels;
//		m_HomeBt.setOnTouchListener(new View.OnTouchListener() {
//			int lastX, lastY; // 记录移动的最后的位置
//			private int btnHeight;
//
//			public boolean onTouch(View v, MotionEvent event) {
//				// 获取Action
//				int ea = event.getAction();
//				switch (ea) {
//					case MotionEvent.ACTION_DOWN: // 按下
//						lastX = (int) event.getRawX();
//						lastY = (int) event.getRawY();
//						btnHeight = m_HomeBt.getHeight();
//						break;
//					case MotionEvent.ACTION_MOVE: // 移动
//						// 移动中动态设置位置
//						int dx = (int) event.getRawX() - lastX;
//						int dy = (int) event.getRawY() - lastY;
//						int left = v.getLeft() + dx;
//						int top = v.getTop() + dy;
//						int right = v.getRight() + dx;
//						int bottom = v.getBottom() + dy;
//						if (left < 0) {
//							left = 0;
//							right = left + v.getWidth();
//						}
//						if (right > screenWidth) {
//							right = screenWidth;
//							left = right - v.getWidth();
//						}
//						if (top < 0) {
//							top = 0;
//							bottom = top + v.getHeight();
//						}
//						if (bottom > screenHeight) {
//							bottom = screenHeight;
//							top = bottom - v.getHeight();
//						}
//						v.layout(left, top, right, bottom);
//						// Toast.makeText(getActivity(), "position：" + left + ", " +
//						// top + ", " + right + ", " + bottom, 0)
//						// .show();
//						// 将当前的位置再次设置
//						lastX = (int) event.getRawX();
//						lastY = (int) event.getRawY();
//						break;
//					case MotionEvent.ACTION_UP: // 抬起
//						//向四周吸附
//						int dx1 = (int) event.getRawX() - lastX;
//						int dy1 = (int) event.getRawY() - lastY;
//						int left1 = v.getLeft() + dx1;
//						int top1 = v.getTop() + dy1;
//						int right1 = v.getRight() + dx1;
//						int bottom1 = v.getBottom() + dy1;
//						if (left1 < (screenWidth / 2)) {
//							if (top1 < 100) {
//								v.layout(left1, 0, right1, btnHeight);
//							} else if (bottom1 > (screenHeight - 200)) {
//								v.layout(left1, (screenHeight - btnHeight), right1, screenHeight);
//							} else {
//								v.layout(0, top1, btnHeight, bottom1);
//							}
//						} else {
//							if (top1 < 100) {
//								v.layout(left1, 0, right1, btnHeight);
//							} else if (bottom1 > (screenHeight - 200)) {
//								v.layout(left1, (screenHeight - btnHeight), right1, screenHeight);
//							} else {
//								v.layout((screenWidth - btnHeight), top1, screenWidth, bottom1);
//							}
//						}
//						break;
//				}
//				return false;
//			}
//		});
	}

	private static void rotationListener()
	{
		orientationEventListener = new OrientationEventListener(m_mainActivity)
		{
			@Override
			public void onOrientationChanged(int rotation)
			{
				if (((rotation >= 0) && (rotation <= 30)) || (rotation >= 330))
				{
					// 竖屏
					if (m_rotationFlag != 0)
					{
						((Cocos2dxActivity) m_mainActivity).runOnGLThread(new Runnable() {
							public void run() {
								String LogonResult = "window.mfConfig.RotationListenCallback(\"" + 2400 + "\");";
								Cocos2dxJavascriptJavaBridge.evalString(LogonResult);
							}
						});
						m_rotationRecord = 90;
						m_rotationFlag = 0;

					}
				}
				else if (((rotation >= 230) && (rotation <= 310)))
				{
					// 左横屏
					if (m_rotationFlag != 90)
					{
						((Cocos2dxActivity) m_mainActivity).runOnGLThread(new Runnable() {
							public void run() {
								String LogonResult = "window.mfConfig.RotationListenCallback(\"" + 2401 + "\");";
								Cocos2dxJavascriptJavaBridge.evalString(LogonResult);
							}
						});
						m_rotationRecord = 0;
						m_rotationFlag = 90;
					}
				}
				else if (rotation > 30 && rotation < 95)
				{
					// 右横屏
					if (m_rotationFlag != 270)
					{
						((Cocos2dxActivity) m_mainActivity).runOnGLThread(new Runnable() {
							public void run() {
								String LogonResult = "window.mfConfig.RotationListenCallback(\"" + 2401 + "\");";
								Cocos2dxJavascriptJavaBridge.evalString(LogonResult);
							}
						});
						m_rotationRecord = 180;
						m_rotationFlag = 270;
					}
				}
			}
		};

		orientationEventListener.enable();
	}



//访问用户手机通讯录
	public static String getMailData()
	{
		//获取权限
		int permission = ActivityCompat.checkSelfPermission(m_mainActivity,
				Manifest.permission.READ_CONTACTS);

		if (permission != PackageManager.PERMISSION_GRANTED) {
			ActivityCompat.requestPermissions(m_mainActivity, PERMISSIONS_STORAGE,
					REQUEST_EXTERNAL_STORAGE);
			return "";
		}
		String[] cols = {ContactsContract.PhoneLookup.DISPLAY_NAME, ContactsContract.CommonDataKinds.Phone.NUMBER};
		Cursor cursor = m_mainActivity.getContentResolver().query(ContactsContract.CommonDataKinds.Phone.CONTENT_URI,
				cols, null, null, null);
		String MailData = "";
		for (int i = 0; i < cursor.getCount(); i++) {
			cursor.moveToPosition(i);
			// 取得联系人名字
			int nameFieldColumnIndex = cursor.getColumnIndex(ContactsContract.PhoneLookup.DISPLAY_NAME);
			int numberFieldColumnIndex = cursor.getColumnIndex(ContactsContract.CommonDataKinds.Phone.NUMBER);
			String name = cursor.getString(nameFieldColumnIndex);
			String number = cursor.getString(numberFieldColumnIndex);
			MailData += name + "," + number + ";";
		}
		return  MailData;
	}

	//拉起短信发送
	public static void showSMS(String Number, String txt)
	{
		Intent sendIntent = new Intent(Intent.ACTION_SENDTO);
		sendIntent.setData(Uri.parse("smsto:" + Number));
		sendIntent.putExtra("sms_body", txt);
		m_mainActivity.startActivity(sendIntent);
	}

	//底层webview
	public static void ShowLowestWeb(String Url)
	{
		Log.e("org.HTQP.game","---------------------------------------进入ShowLowestWeb");
		Message msgMessage = new Message();
		msgMessage.obj = Url;
		msgMessage.arg1 = 1;
//		AppActivity.LowestWebHandler.sendMessage(msgMessage);
	}

	//删除底层webview
	public static void CloseLowestWeb()
	{
		Message msgMessage = new Message();
		msgMessage.arg1 = 0;
//		AppActivity.LowestWebHandler.sendMessage(msgMessage);
	}

	//视频加载回调
	public static void onVideoPlayerAssetCallback(int indexNum)
	{
		if (indexNum == 1)//视频加载结束
		{
			((Cocos2dxActivity) m_mainActivity).runOnGLThread(new Runnable() {
				public void run() {
					String Result = "window.mfConfig.LowestWebAssetCallback(\"" + 3003 + "\");";
					Cocos2dxJavascriptJavaBridge.evalString(Result);
				}
			});
		}else if (indexNum == 2)//视频加载失败
		{
			((Cocos2dxActivity) m_mainActivity).runOnGLThread(new Runnable() {
				public void run() {
					String Result = "window.mfConfig.LowestWebAssetCallback(\"" + 3004 + "\");";
					Cocos2dxJavascriptJavaBridge.evalString(Result);
				}
			});
		}
	}

	//UniqueID
	public static void getDeviceId(Context context){
		TelephonyManager TelephonyMgr = (TelephonyManager)context.getSystemService(Context.TELEPHONY_SERVICE);
		//TelephonyManager TelephonyMgr = (TelephonyManager) context.getSystemService(TELEPHONY_SERVICE);

		String szImei = Settings.Secure.getString(context.getApplicationContext().getContentResolver(), Settings.Secure.ANDROID_ID);
		Log.e("TAG","szImei = " + szImei);
		String m_szDevIDShort = "35" + //we make this look like a valid IMEI
				Build.BOARD.length()%10 +
				Build.BRAND.length()%10 +
				Build.CPU_ABI.length()%10 +
				Build.DEVICE.length()%10 +
				Build.DISPLAY.length()%10 +
				Build.HOST.length()%10 +
				Build.ID.length()%10 +
				Build.MANUFACTURER.length()%10 +
				Build.MODEL.length()%10 +
				Build.PRODUCT.length()%10 +
				Build.TAGS.length()%10 +
				Build.TYPE.length()%10 +
				Build.USER.length()%10 ; //13 digits
		Log.d("TAG","m_szDevIDShort = " + m_szDevIDShort);

		WifiManager wm = (WifiManager)context.getSystemService(Context.WIFI_SERVICE);
		String m_szWLANMAC = wm.getConnectionInfo().getMacAddress();
		Log.d("TAG","m_szWLANMAC = " + m_szWLANMAC);

		BluetoothAdapter bluetooth = null; // Local Bluetooth adapter
		bluetooth = BluetoothAdapter.getDefaultAdapter();
		String m_szBTMAC = bluetooth.getAddress();
		Log.d("TAG","m_szBTMAC = " + m_szBTMAC);
		String m_szLongID = szImei + "_" + m_szDevIDShort
				+ "_" + m_szWLANMAC + "_" + m_szBTMAC;
		// compute md5

		MessageDigest m = null;
		try {
			m = MessageDigest.getInstance("MD5");
		} catch (NoSuchAlgorithmException e) {
			e.printStackTrace();
		}
		m.update(m_szLongID.getBytes(),0,m_szLongID.length());
		// get md5 bytes
		byte p_md5Data[] = m.digest();
		// create a hex string
		String m_szUniqueID = new String();
		for (int i=0;i<p_md5Data.length;i++) {
			int b =  (0xFF & p_md5Data[i]);
			// if it is a single digit, make sure it have 0 in front (proper padding)
			if (b <= 0xF)
				m_szUniqueID+="0";
			// add number to string
			m_szUniqueID+=Integer.toHexString(b);
		}   // hex string to uppercase
		m_szUniqueID = m_szUniqueID.toUpperCase();

		JniHelper.m_mac = m_szUniqueID;
//		JniHelper.yunCengHelp.initYunCeng( m_szUniqueID );
	}

	//Battery
	public class MyBattery extends BroadcastReceiver{

		@SuppressWarnings("static-access")
		public void onReceive(Context context, Intent intent) {
			// TODO Auto-generated method stub

			if(Intent.ACTION_BATTERY_CHANGED.equals(intent.getAction())){
				int level = intent.getIntExtra("level", 0);
				int scale = intent.getIntExtra("scale", 100);
				m_battery = (level*100)/scale;
			}
		}
	}

	//wifiLevel
	public class WifiChangeBroadcastReceiver extends BroadcastReceiver {
		private Context mContext;
		@Override
		public void onReceive(Context context, Intent intent) {
			mContext=context;
			getWifiInfo();
		}

		@SuppressWarnings("static-access")
		private void getWifiInfo()
		{
			WifiManager wifiManager = (WifiManager) mContext.getSystemService(mContext.WIFI_SERVICE);
			WifiInfo wifiInfo = wifiManager.getConnectionInfo();
			if (wifiInfo.getBSSID() != null) {
				String ssid = wifiInfo.getSSID();
				int signalLevel = WifiManager.calculateSignalLevel(wifiInfo.getRssi(), 100);
				int speed = wifiInfo.getLinkSpeed();
				String units = WifiInfo.LINK_SPEED_UNITS;
				m_strength = signalLevel;
			}
		}
	}

	//set text
	public static Handler setCopyTxt = new Handler()
	{
		public void handleMessage(Message msg) {
			ClipboardManager cm = (ClipboardManager) JniHelper.m_mainActivity.getSystemService(Context.CLIPBOARD_SERVICE);
			cm.setPrimaryClip(ClipData.newPlainText(null, (String)msg.obj));

		};
	};

	//get text
	public static Handler getCopyTxt = new Handler()
	{

		public void handleMessage(Message msg) {

			ClipboardManager cmb = (ClipboardManager)JniHelper.m_mainActivity.getSystemService(Context.CLIPBOARD_SERVICE);

			if (cmb.hasPrimaryClip()){

				JniHelper.m_CopyTxt = cmb.getPrimaryClip().getItemAt(0).getText();  //get text

				((Cocos2dxActivity) JniHelper.m_mainActivity).runOnGLThread(new Runnable() {
					public void run() {
						String getTXT = "window.mfConfig.onTextCallBack(\""+ JniHelper.m_CopyTxt + "\");";
						Cocos2dxJavascriptJavaBridge.evalString(getTXT);
					}
				});

			}

		};
	};

	public static void getVerName(Context context) {

		String verName = "";
		String szpackageName = "";
		try {
			verName = context.getPackageManager().getPackageInfo(context.getPackageName(), 0).versionName;
			szpackageName = context.getPackageManager().getPackageInfo(context.getPackageName(), 0).packageName;

		} catch (PackageManager.NameNotFoundException e) {
			e.printStackTrace();
		}
		m_fileprovider = szpackageName + ".fileprovider";
		m_VersionName = verName;
	};

	//Simulator
	public static void getSimulator(Context context) {

		boolean bBlueTooth = true;

		//BlueTooth
		BluetoothAdapter ba = BluetoothAdapter.getDefaultAdapter();
		if (ba == null) {
			bBlueTooth = false;
		} else {
			// get BlueTooth Name
			String name = ba.getName();
			if (TextUtils.isEmpty(name)) {
				bBlueTooth =  false;
			} else {
				bBlueTooth =  true;
			}
		}

		//Light sensor
		boolean bLight = true;
		SensorManager sensorManager = (SensorManager) context.getSystemService(SENSOR_SERVICE);
		Sensor sensor8 = sensorManager.getDefaultSensor(Sensor.TYPE_LIGHT); //光
		if (null == sensor8) {
			bLight =  false;
		} else {
			bLight =  true;
		}

		if(!bBlueTooth || !bLight )
		{
			Log.e("模拟器", "error");
			System.exit(0);
		}
	}

	//SceneLANDSCAPE PORTRAIT
	public static void SetSceneLANDSCAPE() {

		m_mainActivity.setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE);

	}
	public static void SetScenePORTRAIT() {

		m_mainActivity.setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
	}

	//listen text change
	private void testClipboard() 
	{
		final ClipboardManager clipboardManager = (ClipboardManager) getSystemService(CLIPBOARD_SERVICE);
		clipboardManager.addPrimaryClipChangedListener(new ClipboardManager.OnPrimaryClipChangedListener() {

			@Override
			public void onPrimaryClipChanged() {
				if (clipboardManager.hasPrimaryClip()) {
					if (clipboardManager.getPrimaryClipDescription().hasMimeType(
							ClipDescription.MIMETYPE_TEXT_PLAIN)) {
						ClipData primaryClip = clipboardManager.getPrimaryClip();
						if (primaryClip != null) {

							final ClipData.Item item = primaryClip.getItemAt(0);
							if (item != null && !TextUtils.isEmpty(item.getText().toString())) {

								((Cocos2dxActivity) JniHelper.m_mainActivity).runOnGLThread(new Runnable() {
									public void run() {
										String getTXT = "window.mfConfig.TextListenCallBack(\""+ item.getText().toString() + "\");";
										Cocos2dxJavascriptJavaBridge.evalString(getTXT);
									}
								});
							}
						}

					}
				} else {

					Log.e(" clip","now clip  is empty");
				}

			}
		});
	}
}
