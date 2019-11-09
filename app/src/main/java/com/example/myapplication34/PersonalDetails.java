package com.example.myapplication34;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import butterknife.BindView;
import butterknife.ButterKnife;

public class PersonalDetails extends AppCompatActivity {
    @BindView(R.id.textView2)
    TextView textView;

    @BindView(R.id.editText)
    EditText Name;

    @BindView(R.id.button2)
    Button next;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.personal_details);
        ButterKnife.bind(this);
        String name = Name.getText().toString();

        next.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {

                Intent scannerIntent = new Intent(getApplicationContext(), Scanner.class);
                scannerIntent.putExtra("name", name);
                startActivity(scannerIntent);
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
