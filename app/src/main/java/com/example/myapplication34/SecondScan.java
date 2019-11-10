package com.example.myapplication34;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import androidx.appcompat.app.AppCompatActivity;

import butterknife.BindView;
import butterknife.ButterKnife;

public class SecondScan extends AppCompatActivity {
    @BindView(R.id.button3)
    Button scanNext;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.scan_next);
        ButterKnife.bind(this);

        scanNext.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent scanner = new Intent(getApplicationContext(), Scanner1.class);
                startActivity(scanner);
            }
        });
    }
}
