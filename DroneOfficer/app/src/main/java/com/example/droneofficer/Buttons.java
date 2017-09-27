package com.example.droneofficer;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.util.AttributeSet;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;

import java.io.Serializable;
import java.util.Random;

public class Buttons extends View implements Serializable {
    public Buttons(Context context, AttributeSet attrs) {
        super(context, attrs);
    }
    protected void onSizeChanged(int wScreen, int hScreen, int oldw, int oldh) {
        super.onSizeChanged(wScreen, hScreen, oldw, oldh);

        this.wScreen = wScreen;
        this.hScreen = hScreen;
    }

    private boolean isRun = false;
    public boolean isClicked = false;
    public int id;
    private int wScreen, hScreen;
    private Paint paint = new Paint();
    private int i;
    private Random random = new Random();

    public void buttonPause() {
        isRun = false;
    }
    public void buttonResume() {
        isRun = true;
    }

    public void init(int id) {
        isRun = true;
        isClicked = false;
        this.id = id;
    }

    public boolean onTouchEvent(MotionEvent event) {
        if (isRun) {
            if (event.getAction() == MotionEvent.ACTION_DOWN) {
                isClicked = true;
                Log.d("Buttons", "" + id + " : " + isClicked);
            }
            if (event.getAction() == MotionEvent.ACTION_UP) {
                isClicked = false;
                Log.d("Buttons", "" + id + " : " + isClicked);
            }
            if (event.getAction() == MotionEvent.ACTION_OUTSIDE) {
                isClicked = false;
                Log.d("Buttons", "" + id + " : " + isClicked);
            }
            return true;
        }
        return false;
    }
    @Override
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);
        paint.setStyle(Paint.Style.FILL);
        if (i == 0) paint.setColor(Color.BLACK);
        else {
            switch (random.nextInt(8)) {
                case 0:
                    paint.setColor(Color.BLACK);
                    break;
                case 1:
                    paint.setColor(Color.LTGRAY);
                    break;
                case 2:
                    paint.setColor(Color.GREEN);
                    break;
                case 3:
                    paint.setColor(Color.CYAN);
                    break;
                case 4:
                    paint.setColor(Color.BLUE);
                    break;
                case 5:
                    paint.setColor(Color.YELLOW);
                    break;
                case 6:
                    paint.setColor(Color.RED);
                    break;
                case 7:
                    paint.setColor(Color.MAGENTA);
                    break;
            }
        }
    }
}
