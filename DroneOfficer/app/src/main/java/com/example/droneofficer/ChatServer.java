package com.example.droneofficer;

import android.os.Handler;
import android.os.Message;

public class ChatServer {
    private InetSocket inetSocket;

    public ChatServer(Handler h, MainActivity a) { inetSocket = new InetSocket(h, a); }
    public boolean isAvailable() {
        return inetSocket.isAvailable();
    }
    public boolean isAcknowledged() {
        return inetSocket.isAcknowledged();
    }
    public boolean connect(String hname, int hport) {
        if (inetSocket.connect(hname, hport) == false) return false;
        if (inetSocket.send("msg " + String.valueOf(300) + String.valueOf(' ')) == false) return false;
        return true;
    }

    public boolean send(int ch) {
        String string = "msg " + String.valueOf(ch) + String.valueOf(' ');
        return inetSocket.send(string);
    }

    public boolean send(String str) {
        String string = "msg " + str + String.valueOf(' ');
        return inetSocket.send(string);
    }

    public char getchar(Message msg) {
        String string = (String) msg.obj; // string delivered from peer
        string = string.replaceAll("msg ", ""); // remove color codes in the line

        return string.charAt(0);
    }
    public boolean disconnect() {
        return inetSocket.disconnect();
    }
}
