package org.cocos2dx.javascript;

import android.Manifest;
import android.app.Activity;
import android.content.Intent;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.Build;
import android.provider.MediaStore;
import android.support.v4.content.FileProvider;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;
import java.util.UUID;

/**
 * 图像处理bitmap&Camera
 * Created by fj on 2017/4/17.
 */
public class CameraHelp {

    public static final int REQUEST_PHOTO_CARMERA = 11;    //open carmera
    public static final int REQUEST_PHOTO_PICK = 12;       //pick


    public static Activity m_mainActivity;

    public static String FileUri = "";

    public CameraHelp( Activity main )
    {
        m_mainActivity = main;
    }

    // 所需的全部权限
    public static final String[] PERMISSIONS = new String[]{
            Manifest.permission.CAMERA,
            Manifest.permission.WRITE_EXTERNAL_STORAGE,
            Manifest.permission.READ_EXTERNAL_STORAGE,
    };


    public static final int SET_PERCODE = 10;  //设置权限回调代码

    /**
     * 跳转到相册
     */
    public static void openAlbum(Activity activity, int flag)
    {
        Intent takePictureIntent = new Intent(Intent.ACTION_PICK, MediaStore.Images.Media.EXTERNAL_CONTENT_URI);
        if (takePictureIntent.resolveActivity(activity.getPackageManager()) != null) {// 相机被卸载时不会崩溃
            activity.startActivityForResult(takePictureIntent, flag);
        }
    }

    /**
     * 跳转到相机
     */
    public static void  openCamera( Activity activity, int flag )
    {
        String mUUID = UUID.randomUUID().toString();
        JniHelper.m_strPath = FileUtils.getStorageDirectory() + mUUID;
        File cameraFile = new File(JniHelper.m_strPath + ".jpg");
        Intent intent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);

        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.N)
        {
            JniHelper.m_imageUri = Uri.fromFile(cameraFile);
        }
        else
        {
            intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
            JniHelper.m_imageUri = FileProvider.getUriForFile(activity, JniHelper.m_fileprovider, cameraFile);
        }
        // 启动相机程序 更改系统默认存储路
        intent.putExtra(MediaStore.EXTRA_OUTPUT, JniHelper.m_imageUri);
        activity.startActivityForResult(intent, flag);
    }


    /**
     * 保存bitmap图像到本地文件
     *
     * @param bitMap
     * @return返回一个file类型的uri
     */
    public static File saveBitMapToFile(Bitmap bitMap) {
        //保存的文件file
        File imageFile = createImageFile();
        try {
            FileOutputStream fos = new FileOutputStream(imageFile);
            /**
             * 将图像压缩--图像格式--图像压缩质量--输出流
             */
            bitMap.compress(Bitmap.CompressFormat.JPEG, 50, fos);
            fos.flush();
            fos.close();
            bitMap.recycle();
            return imageFile;
        } catch (FileNotFoundException e) {
            e.printStackTrace();
            return null;
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }
    }

    public static Uri bitmap2uri(Bitmap bitmap, Activity activity) {
        return Uri.parse(MediaStore.Images.Media.insertImage(activity.getContentResolver(), bitmap, null, null));
    }

    public static Bitmap uri2bitmap(Uri uri, Activity activity) {
        Bitmap bitmap = null;
        try {
            bitmap = MediaStore.Images.Media.getBitmap(activity.getContentResolver(), uri);
        } catch (IOException e) {
            e.printStackTrace();
        }
        return bitmap;
    }

    public static File uri2File(Uri uri){
        File file = null;
        try {
            file = new File(new URI(uri.toString()));
        } catch (URISyntaxException e) {
            e.printStackTrace();
        }
        return file;
    }

    /**
     * 创建一个保存图片的文件
     * @return
     */
    public static File createImageFile() {
        //获取保存到的文件夹路劲
        File dir = JniHelper.m_saveDirFile;
        if (!dir.exists())
            dir.mkdirs();
        File file = new File(dir, getPhotoPath());//
        return file;
    }

    /**
     * 保存文件的名字
     * @return
     */
    public static String getPhotoPath()
    {
        String imageFileName = ""+ JniHelper.m_strUserID + "_" + ( System.currentTimeMillis()/1000) + ".jpg";
        return imageFileName;
    }

    /**
     * 创建一个文件用于存放拍摄的照片
     *
     * @return
     * @throws IOException
     */
    public static File createImageFile(String fileName,File storageDir) {
        if (!storageDir.exists())
            storageDir.mkdirs();
        File file = new File(storageDir, fileName);//localTempImgDir和localTempImageFileName是自己定义的名字
        return file;
    }



}