package com.example.administrator.drone1;

import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Environment;
import android.os.Handler;
import android.os.Message;
import android.support.v4.app.ActivityCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.Toast;

import java.io.File;
import java.io.FileOutputStream;
import java.util.jar.Manifest;

public class MainActivity extends AppCompatActivity {

    private Button settingBtn, connectBtn, takeoffBtn, disconnectBtn;
    private Buttons spinLeftBtn, forwardBtn, spinRightBtn;
    private Buttons leftBtn, backwardBtn, rightBtn;
    private Buttons upBtn, downBtn;
    private ImageView imgView;
    private Buttons[] arrayBtns = new Buttons[8];
    private boolean isFly = false, isConnected = false;

    private String serverHostName = "192.168.123.1";
    private int serverPortNum = 9000;
    private ChatServer echoServer;
    private final int reqCode4SettingActivity = 0;

    private Handler hMyViews = new Handler();
    private Handler hPeerViews = new Handler() {
        public void handleMessage(Message msg) {
            if (echoServer.isAvailable() == false) return; // discard any key del ivered af\

            try {
                byte[] fileData =  (byte[])msg.obj;
                Bitmap bmp = BitmapFactory.decodeByteArray(fileData, 0, fileData.length);
                if (bmp != null) imgView.setImageBitmap(bmp);

                /* // extern save
                if(isExternalStorageWritable()) {
                    File file = getAlbumStorageDir("drone");
                    String path = file.getPath().toString();
                    String fileName = path + "/pic.jpg";
                    byte[] fileData =  (byte[])msg.obj;
                    FileOutputStream fos = new FileOutputStream(fileName);
                    fos.write(fileData);
                    fos.close();
                } */
                /*
                Log.d("MainActivity", "save" + getFilesDir());
                byte[] fileData =  (byte[])msg.obj;
                FileOutputStream fos = new FileOutputStream(getFilesDir() + "/testfile.jpeg");
                fos.write(fileData);
                fos.close();
                Log.d("MainActivity", "save");
*/
      //          File imgFile = new  File(getFilesDir() + "/testfile.jpeg");

//                if(imgFile.exists()){
  //                  Log.d("MainActivity", "open");
    //                Bitmap myBitmap = BitmapFactory.decodeFile(imgFile.getAbsolutePath());
//
  //                  imgView.setImageBitmap((Bitmap)msg.obj);
    //            }

            } catch (Exception e) {
                e.printStackTrace();
            }



            //imgView.setImageBitmap((Bitmap)msg.obj);

            //char key = echoServer.getchar(msg); // key delivered from peer
            //Toast.makeText(MainActivity.this, "Received : " + key, Toast.LENGTH_SHORT).show();
            return;
        };
    };

    public File getAlbumStorageDir(String albumName) {
        // Get the directory for the user's public pictures directory.
        File file = new File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_PICTURES), albumName);
        Log.d("MainActivity", file.getPath());
        if (!file.mkdirs()) {
            Log.d("MainActivity", "Directory not created");
        }
        return file;
    }

    /* Checks if external storage is available for read and write */
    public boolean isExternalStorageWritable() {
        String state = Environment.getExternalStorageState();
        if (Environment.MEDIA_MOUNTED.equals(state)) {
            return true;
        }
        return false;
    }

    /* Checks if external storage is available to at least read */
    public boolean isExternalStorageReadable() {
        String state = Environment.getExternalStorageState();
        if (Environment.MEDIA_MOUNTED.equals(state) ||
                Environment.MEDIA_MOUNTED_READ_ONLY.equals(state)) {
            return true;
        }
        return false;
    }

    private void startSettingActivity(int reqCode) {
        Intent intent = new Intent(MainActivity.this, SettingActivity.class);
        intent.putExtra("serverHostName", serverHostName);
        intent.putExtra("serverPortNum", String.valueOf(serverPortNum));
        startActivityForResult(intent, reqCode);
    }
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        switch (requestCode) {
            case reqCode4SettingActivity:
                if (resultCode == RESULT_OK) {
                    serverHostName = data.getStringExtra("serverHostName");
                    String s = data.getStringExtra("serverPortNum");
                    serverPortNum = Integer.parseInt(s);
                    Log.d("MainActivity", "SettingActivity returned ("+serverHostName+","+serverPortNum+")");
                }
                else if (resultCode == RESULT_CANCELED) {
                    Log.d("MainActivity", "SettingActivity canceled");
                }
                break;
        }
    }

    private View.OnClickListener OnClickListener = new View.OnClickListener() {
        public void onClick(View v){
            char key;
            int id = v.getId();
            switch (id) {
                case R.id.settingBtn:
                    startSettingActivity(reqCode4SettingActivity);
                    return;
                case R.id.connectBtn:
                    if (echoServer.connect(serverHostName, serverPortNum) == false) {
                        Toast.makeText(MainActivity.this, "Connection Error!", Toast.LENGTH_SHORT).show();
                        isConnected = false;
                    } else {
                        Toast.makeText(MainActivity.this, "Connection Success!", Toast.LENGTH_SHORT).show();
                        isConnected = true;
                        init();
                    }
                    return;
                case R.id.takeoffBtn:
                    if (isConnected) {
                        if (isFly) {
                            if (!echoServer.send(101)) {
                                Toast.makeText(MainActivity.this, "Connection Error!", Toast.LENGTH_SHORT).show();
                            } else {
                                takeoffBtn.setText("Take-off");
                                isFly = false;
                            }
                        } else {
                            if (!echoServer.send(100)) {
                                Toast.makeText(MainActivity.this, "Connection Error!", Toast.LENGTH_SHORT).show();
                            } else {
                                takeoffBtn.setText("Landing");
                                isFly = true;
                            }
                        }
                    } else {
                        Toast.makeText(MainActivity.this, "Connection Error!", Toast.LENGTH_SHORT).show();
                    }
                    return;
                case R.id.disconnectBtn:
                    if (isFly) {
                        if (!echoServer.send(101)) {
                            Toast.makeText(MainActivity.this, "Connection Error!", Toast.LENGTH_SHORT).show();
                            return;
                        } else {
                            takeoffBtn.setText("Take-off");
                            isFly = false;
                        }
                    }
                    if (isConnected) {
                        if (echoServer.isAvailable()) {
                            echoServer.send(200);
                            echoServer.disconnect();
                            isConnected = false;
                        }
                    }
                    return;
                default : return;
            }
        }
    };

    @Override
    protected void onDestroy() {
        super.onDestroy();
        Log.d("MainActivity", "onDestroy");
        echoServer.send(101);
        if (echoServer.isAvailable()) {
            echoServer.send(200);
            echoServer.disconnect();
        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        ActivityCompat.requestPermissions(this, new String[]{android.Manifest.permission.WRITE_EXTERNAL_STORAGE}, 1);

        setContentView(R.layout.activity_main);

        imgView = (ImageView) findViewById(R.id.imgView);

        spinLeftBtn = (Buttons) findViewById(R.id.spinLeftBtn);
        forwardBtn = (Buttons) findViewById(R.id.forwardBtn);
        spinRightBtn = (Buttons) findViewById(R.id.spinRightBtn);
        leftBtn = (Buttons) findViewById(R.id.leftBtn);
        backwardBtn = (Buttons) findViewById(R.id.backwardBtn);
        rightBtn = (Buttons) findViewById(R.id.rightBtn);
        upBtn = (Buttons) findViewById(R.id.upBtn);
        downBtn = (Buttons) findViewById(R.id.downBtn);

        settingBtn = (Button) findViewById(R.id.settingBtn);
        connectBtn = (Button) findViewById(R.id.connectBtn);
        takeoffBtn = (Button) findViewById(R.id.takeoffBtn);
        disconnectBtn = (Button) findViewById(R.id.disconnectBtn);

        settingBtn.setOnClickListener(OnClickListener);
        connectBtn.setOnClickListener(OnClickListener);
        takeoffBtn.setOnClickListener(OnClickListener);
        disconnectBtn.setOnClickListener(OnClickListener);

        echoServer = new ChatServer(hPeerViews, MainActivity.this);

    }
    private void init() {
        spinLeftBtn.init(0);
        arrayBtns[0] = spinLeftBtn;
        forwardBtn.init(1);
        arrayBtns[1] = forwardBtn;
        spinRightBtn.init(2);
        arrayBtns[2] = spinRightBtn;
        leftBtn.init(3);
        arrayBtns[3] = leftBtn;
        backwardBtn.init(4);
        arrayBtns[4] = backwardBtn;
        rightBtn.init(5);
        arrayBtns[5] = rightBtn;
        upBtn.init(6);
        arrayBtns[6] = upBtn;
        downBtn.init(7);
        arrayBtns[7] = downBtn;
        mHandler.sendEmptyMessageDelayed(0, 10);
    }

    boolean pastCmd = false;
    int id = 8;
    Handler mHandler = new Handler() {
        public void handleMessage(Message msg) {
            int count = 0;
            if (isConnected && isFly) {
                for (int i = 0; i < 8; i++) {
                    //Log.d("MainActivity", "" + id + " ; " + arrayBtns[i].isClicked );
                    if (arrayBtns[i].isClicked == true) {
                        count++;
                        id = i;
                        Log.d("MainActivity", "" + id );
                    }
                }
                if (count == 1 && !pastCmd ) {
                    if (!echoServer.send(id)) {
                        Toast.makeText(MainActivity.this, "Connection Error!", Toast.LENGTH_SHORT).show();
                        isConnected = false;
                        isFly = false;
                    } else {
                        pastCmd = true;
                    }
                } else if (count == 0) {
                    if (!echoServer.send(8)) {
                        Toast.makeText(MainActivity.this, "Connection Error!", Toast.LENGTH_SHORT).show();
                        isConnected = false;
                        isFly = false;
                    } else {
                        pastCmd = false;
                    }
                }
            }
            if (isConnected) {
                mHandler.sendEmptyMessageDelayed(0, 300);
            }
        }
    };
}
