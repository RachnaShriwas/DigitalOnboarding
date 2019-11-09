package com.example.myapplication34;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;

import androidx.appcompat.app.AppCompatActivity;

import butterknife.BindView;
import butterknife.ButterKnife;

public class MainActivity extends AppCompatActivity {

    @BindView(R.id.start)
    Button startButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        ModelDocumentSelector modelDocumentSelector = new ModelDocumentSelector();
        modelDocumentSelector.loadModel();
        Log.d("TAG", "*****in MAIN model loaded******");

        setContentView(R.layout.main);
        ButterKnife.bind(this);

        startButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                Intent intent = new Intent(getApplicationContext(), Scanner.class);
                startActivity(intent);
            }
        });

    }

    @Override
    public void onResume() {
        super.onResume();

    }
    @Override
    public void onPause() {

        super.onPause();
    }


}
