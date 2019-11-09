package com.example.myapplication34;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.Window;
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
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        ModelDocumentSelector modelDocumentSelector = new ModelDocumentSelector();
        modelDocumentSelector.loadModel();
        Log.d("TAG", "*****in MAIN model loaded******");

        setContentView(R.layout.main);
        ButterKnife.bind(this);

        startButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                Intent intent = new Intent(getApplicationContext(), PersonalDetails.class);
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
