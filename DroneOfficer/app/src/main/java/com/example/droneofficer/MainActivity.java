package com.example.droneofficer;

import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Color;
import android.os.Handler;
import android.os.Message;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.RelativeLayout;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {

    public enum appState {
        startScreen(0), streamScreen(1), controlScreen(2);
        private final int value;
        private appState(int value) { this.value = value; }
        public int value() { return value; }
    }

    private ImageButton settingBtn, connectBtn, reportBtn, streamBtn, profileBtn, controlBtn;
    private Button streamSwitch, streamCancel;
    private appState state = appState.startScreen;

    private Button takeoffBtn, disconnectBtn;
    private Buttons spinLeftBtn, forwardBtn, spinRightBtn;
    private Buttons leftBtn, backwardBtn, rightBtn;
    private Buttons upBtn, downBtn;
    private ImageView imgView;
    private Buttons[] arrayBtns = new Buttons[8];
    private boolean isFly = false, isConnected = false, isReport = false;
    private String type;
    private String detail;
    private String reportContent;

    private String serverHostName = "192.168.123.1";
    private int serverPortNum = 9000;
    private ChatServer echoServer;
    private final int reqCode4SettingActivity = 0;
    private final int reqCode4ReportActivity = 1;

    static byte[] fileData;
    static Bitmap bmp;
    private Handler hPeerViews = new Handler() {
        public void handleMessage(Message msg) {
            if (echoServer.isAvailable() == false) return;
            if (state == appState.startScreen) return;
            try {
                fileData =  (byte[])msg.obj;
                bmp = BitmapFactory.decodeByteArray(fileData, 0, fileData.length);
                if (bmp != null) imgView.setImageBitmap(bmp);

            } catch (Exception e) {
                e.printStackTrace();
            }
            return;
        }
    };

    protected void changeState(appState stateI){
        switch (stateI.value()){
            case 0:
                reportBtn.setVisibility(View.VISIBLE);
                profileBtn.setVisibility(View.VISIBLE);
                streamBtn.setVisibility(View.VISIBLE);
                controlBtn.setVisibility(View.VISIBLE);
                connectBtn.setVisibility(View.VISIBLE);
                settingBtn.setVisibility(View.VISIBLE);

                streamSwitch.setVisibility(View.GONE);
                streamCancel.setBackgroundColor(View.GONE);

                spinLeftBtn.setVisibility(View.GONE);
                forwardBtn.setVisibility(View.GONE);
                spinRightBtn.setVisibility(View.GONE);
                leftBtn.setVisibility(View.GONE);
                backwardBtn.setVisibility(View.GONE);
                rightBtn.setVisibility(View.GONE);
                upBtn.setVisibility(View.GONE);
                downBtn.setVisibility(View.GONE);
                takeoffBtn.setVisibility(View.GONE);

                state = appState.startScreen;
                break;
            case 1:
                reportBtn.setVisibility(View.GONE);
                profileBtn.setVisibility(View.GONE);
                streamBtn.setVisibility(View.GONE);
                controlBtn.setVisibility(View.GONE);
                connectBtn.setVisibility(View.GONE);
                settingBtn.setVisibility(View.GONE);

                streamSwitch.setVisibility(View.VISIBLE);
                streamCancel.setVisibility(View.VISIBLE);

                spinLeftBtn.setVisibility(View.GONE);
                forwardBtn.setVisibility(View.GONE);
                spinRightBtn.setVisibility(View.GONE);
                leftBtn.setVisibility(View.GONE);
                backwardBtn.setVisibility(View.GONE);
                rightBtn.setVisibility(View.GONE);
                upBtn.setVisibility(View.GONE);
                downBtn.setVisibility(View.GONE);
                takeoffBtn.setVisibility(View.GONE);

                state = appState.streamScreen;
                break;

            case 2:
                reportBtn.setVisibility(View.GONE);
                profileBtn.setVisibility(View.GONE);
                streamBtn.setVisibility(View.GONE);
                controlBtn.setVisibility(View.GONE);
                connectBtn.setVisibility(View.GONE);
                settingBtn.setVisibility(View.GONE);

                streamSwitch.setVisibility(View.VISIBLE);
                streamCancel.setVisibility(View.VISIBLE);

                spinLeftBtn.setVisibility(View.VISIBLE);
                forwardBtn.setVisibility(View.VISIBLE);
                spinRightBtn.setVisibility(View.VISIBLE);
                leftBtn.setVisibility(View.VISIBLE);
                backwardBtn.setVisibility(View.VISIBLE);
                rightBtn.setVisibility(View.VISIBLE);
                upBtn.setVisibility(View.VISIBLE);
                downBtn.setVisibility(View.VISIBLE);
                takeoffBtn.setVisibility(View.VISIBLE);

                state = appState.controlScreen;
                break;
        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_main);

        imgView = (ImageView) findViewById(R.id.streamView);

        settingBtn = (ImageButton) findViewById(R.id.settingBtn);
        connectBtn = (ImageButton) findViewById(R.id.connectBtn);
        streamBtn = (ImageButton) findViewById(R.id.streamBtn);
        reportBtn = (ImageButton) findViewById(R.id.reportBtn);
        controlBtn = (ImageButton) findViewById(R.id.controlBtn);
        profileBtn = (ImageButton) findViewById(R.id.profileBtn);

        streamSwitch = (Button) findViewById(R.id.streamSwitchBtn);
        streamCancel = (Button) findViewById(R.id.streamCancelBtn);

        settingBtn.setOnClickListener(OnClickListener);
        connectBtn.setOnClickListener(OnClickListener);
        streamBtn.setOnClickListener(OnClickListener);
        reportBtn.setOnClickListener(OnClickListener);
        controlBtn.setOnClickListener(OnClickListener);
        profileBtn.setOnClickListener(OnClickListener);
        streamSwitch.setOnClickListener(OnClickListener);
        streamCancel.setOnClickListener(OnClickListener);

        spinLeftBtn = (Buttons) findViewById(R.id.spinLeftBtn);
        forwardBtn = (Buttons) findViewById(R.id.forwardBtn);
        spinRightBtn = (Buttons) findViewById(R.id.spinRightBtn);
        leftBtn = (Buttons) findViewById(R.id.leftBtn);
        backwardBtn = (Buttons) findViewById(R.id.backwardBtn);
        rightBtn = (Buttons) findViewById(R.id.rightBtn);
        upBtn = (Buttons) findViewById(R.id.upBtn);
        downBtn = (Buttons) findViewById(R.id.downBtn);
        takeoffBtn = (Button) findViewById(R.id.takeoffBtn);

        echoServer = new ChatServer(hPeerViews, MainActivity.this);
        changeState(appState.startScreen);
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


    private void startSettingActivity(int reqCode) {
        Intent intent = new Intent(MainActivity.this, SettingActivity.class);
        intent.putExtra("serverHostName", serverHostName);
        intent.putExtra("serverPortNum", String.valueOf(serverPortNum));

        startActivityForResult(intent, reqCode);
    }

    private void startReportActivity(int reqCode) {
        Intent intent = new Intent(MainActivity.this, ReportActivity.class);

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
            case reqCode4ReportActivity:
                if (resultCode == RESULT_OK) {
                    type = data.getStringExtra("type");
                    detail = data.getStringExtra("detail");
                    Log.d("MainActivity", "ReportActivity returned ("+type+","+detail+")");
                    detail.replace('\n', '#');
                    reportContent = type + " " + detail;
                    isReport = true;
                }
                else if (resultCode == RESULT_CANCELED) {
                    Log.d("MainActivity", "ReportActivity canceled");
                }
                break;
        }
    }

    private View.OnClickListener OnClickListener = new View.OnClickListener() {
        public void onClick(View v){
            char key;
            int id = v.getId();

            switch (id) {

                case R.id.reportBtn:
                    if(!isConnected) {
                        Toast.makeText(MainActivity.this, "Connection Error!", Toast.LENGTH_SHORT).show();
                        return;
                    }
                    startReportActivity(reqCode4ReportActivity);
                    return;

                case R.id.profileBtn:
                    return;

                case R.id.streamBtn:
                    if(!isConnected) {
                        Toast.makeText(MainActivity.this, "Connection Error!", Toast.LENGTH_SHORT).show();
                        return;
                    }
                    changeState(appState.streamScreen);
                    return;

                case R.id.controlBtn:
                    if(!isConnected) {
                        Toast.makeText(MainActivity.this, "Connection Error!", Toast.LENGTH_SHORT).show();
                        return;
                    }
                    changeState(appState.controlScreen);
                    return;

                case R.id.settingBtn:
                    startSettingActivity(reqCode4SettingActivity);
                    return;

                case R.id.connectBtn:
                    if (!isConnected) {
                        if (echoServer.connect(serverHostName, serverPortNum) == false) {
                            Toast.makeText(MainActivity.this, "Connection Error!", Toast.LENGTH_SHORT).show();
                            isConnected = false;
                        } else {
                            Toast.makeText(MainActivity.this, "Connection Success!", Toast.LENGTH_SHORT).show();
                            isConnected = true;
                            init();
                        }
                    } else {
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
                    }
                    return;

                case R.id.streamSwitchBtn:
                    changeState(appState.controlScreen);
                    return;

                case R.id.streamCancelBtn:
                    changeState(appState.startScreen);
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


                default : return;
            }
        }
    };

    private boolean pastCmd = false;
    private int id = 8;
    Handler mHandler = new Handler() {
        public void handleMessage(Message msg) {
            int count = 0;

            if (isConnected && isReport) {
                if (!echoServer.send(reportContent)) {
                    Toast.makeText(MainActivity.this, "Connection Error!", Toast.LENGTH_SHORT).show();
                    isConnected = false;
                }
                isReport = false;
            }

            if (isConnected && isFly) {
                for (int i = 0; i < 8; i++) {
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
