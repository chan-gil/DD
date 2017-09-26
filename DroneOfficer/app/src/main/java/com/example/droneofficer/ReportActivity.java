package com.example.droneofficer;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.TextView;

public class ReportActivity extends AppCompatActivity {
    private EditText detail;
    private String type;
    private Spinner reportType;
    private String serverHostName, serverPortNum;
    private String myNickName, peerNickName;
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_report);
        detail = (EditText)findViewById(R.id.editview2);

        reportType = (Spinner) findViewById(R.id.reportType);
        String[] item = new String[] {"Fire", "Criminal Car"};

        ArrayAdapter<String> adapter = new ArrayAdapter<String>(this, android.R.layout.simple_spinner_dropdown_item, item);
        reportType.setAdapter(adapter);
        reportType.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> arg0, View arg1, int arg2, long arg3) {
                int index = arg0.getSelectedItemPosition();
                switch (index){
                    case 0:
                        type = "Fire";
                        detail.setText("Number of floors : \nFire type : \nEtc : ");
                        break;
                    case 1:
                        type = "Car";
                        detail.setText("Car number : 1234\nType of vehicle : \nColor : \nEtc : ");
                        break;
                }
            }

            @Override
            public void onNothingSelected(AdapterView<?> arg0) {
            }
        });
    }


    public void onClick(View v) {
        switch (v.getId()) {
            case R.id.confirm:
                Intent intent = new Intent();
                intent.putExtra("type", type);
                intent.putExtra("detail", detail.getText().toString());
                setResult(RESULT_OK, intent);
                break;
            case R.id.cancel:
                setResult(RESULT_CANCELED);
                break;
        }
        finish();
    }


}
