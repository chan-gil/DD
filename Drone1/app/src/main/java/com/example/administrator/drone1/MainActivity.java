package com.example.administrator.drone1;

import android.content.Intent;
import android.os.Handler;
import android.os.Message;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {

    private Button settingBtn, connectBtn, takeoffBtn, disconnectBtn;
    private Buttons spinLeftBtn, forwardBtn, spinRightBtn;
    private Buttons leftBtn, backwardBtn, rightBtn;
    private Buttons upBtn, downBtn;
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
            char key = echoServer.getchar(msg); // key delivered from peer
            Toast.makeText(MainActivity.this, "Received : " + key, Toast.LENGTH_SHORT).show();
            return;
        };
    };

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
        setContentView(R.layout.activity_main);

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
                    } else {
                        pastCmd = true;
                    }
                } else if (count == 0) {
                    if (!echoServer.send(8)) {
                        Toast.makeText(MainActivity.this, "Connection Error!", Toast.LENGTH_SHORT).show();
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
