package org.cocos2dx.javascript;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.Bitmap.CompressFormat;
import android.graphics.Bitmap.Config;
import android.graphics.BitmapFactory;
import android.os.Environment;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;

public class FileUtils {
	/**
	 * sd卡的根目录
	 */
	private static String mSdRootPath = Environment.getExternalStorageDirectory().getPath();
	/**
	 * 手机的缓存根目录
	 */
	private static String mDataRootPath = null;
	/**
	 * 保存Image的目录名
	 */
	private final static String FOLDER_NAME = "/ccclubsdk";
	
	
	public FileUtils(Context context){
		mDataRootPath = context.getCacheDir().getPath();
	}
	

	/**
	 * 获取储存Image的目录
	 * @return
	 */
	public static String getStorageDirectory(){
		return Environment.getExternalStorageState().equals(Environment.MEDIA_MOUNTED) ?
				mSdRootPath + FOLDER_NAME : mDataRootPath + FOLDER_NAME;
	}
	/**
	 * 判断文件是否存在
	 * @param fileName
	 * @return
	 */
	public boolean isFileExists(String fileName){
		return new File(getStorageDirectory() + File.separator + fileName).exists();
	}
	
	/**
	 * 获取文件的大小
	 * @param fileName
	 * @return
	 */
	public long getFileSize(String fileName) {
		return new File(getStorageDirectory() + File.separator + fileName).length();
	}
	
	/**
	 *  判断给定图片的大小，并进行缩放
	 *  @param uri 图片路径
	 *  @param width  目标高度
	 *  @param  height  目标宽度
	 *  @param   config 配色方案       
	 */
	public static Bitmap GetBitMapFromUrlAndSize1(String uri,int width,int height,int config){
		BitmapFactory.Options options=new BitmapFactory.Options();
		options.inJustDecodeBounds=true;
		BitmapFactory.decodeFile(uri,options);
		int mwidth=options.outWidth;
		int mheight=options.outHeight;
		options.inSampleSize =1;
		//缩略图为 120*160
		options.inSampleSize= mwidth/width < mheight/height? mwidth/width:mheight/height;
		switch (config) {
		case 1:
			options.inPreferredConfig=Config.ALPHA_8;
			break;
			
		case 2:
			options.inPreferredConfig=Config.RGB_565;
			break;
			
		case 3:
			options.inPreferredConfig=Config.ARGB_8888;
			break;
			
		default:
			options.inPreferredConfig=Config.RGB_565;
			break;
		}

		options.inJustDecodeBounds=false;
		
		return BitmapFactory.decodeFile(uri,options);
	}
	
	
	
	/**
	 * 删除SD卡或者手机的缓存图片和目录
	 */
	public static void  deleteFile() {
		File dirFile = new File(getStorageDirectory());
		if(! dirFile.exists()){
			return;
		}
		if (dirFile.isDirectory()) {
			String[] children = dirFile.list();
			for (int i = 0; i < children.length; i++) {
				new File(dirFile, children[i]).delete();
			}
		}
		
		dirFile.delete();
	}

}
