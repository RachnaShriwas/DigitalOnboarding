package com.example.myapplication34;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.Window;

import androidx.appcompat.app.AppCompatActivity;

public class SuccessPage extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        setContentView(R.layout.success);

        Intent i = getIntent();
        Bundle bi = i.getBundleExtra("response");
        Log.d("TAG", bi.getString("response"));
    }

}
