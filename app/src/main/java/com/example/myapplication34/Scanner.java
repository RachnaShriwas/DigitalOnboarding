package com.example.myapplication34;

import android.content.Intent;
import android.graphics.Bitmap;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Base64;
import android.util.Log;
import android.view.View;
import android.widget.Button;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import com.example.myapplication34.GraphicUtils.GraphicOverlay;
import com.example.myapplication34.GraphicUtils.TextGraphic;
import com.google.android.gms.tasks.OnFailureListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.firebase.ml.vision.FirebaseVision;
import com.google.firebase.ml.vision.common.FirebaseVisionImage;
import com.google.firebase.ml.vision.text.FirebaseVisionText;
import com.google.firebase.ml.vision.text.FirebaseVisionTextDetector;
import com.wonderkiln.camerakit.CameraKitError;
import com.wonderkiln.camerakit.CameraKitEvent;
import com.wonderkiln.camerakit.CameraKitEventListener;
import com.wonderkiln.camerakit.CameraKitImage;
import com.wonderkiln.camerakit.CameraKitVideo;
import com.wonderkiln.camerakit.CameraView;

import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.BasicResponseHandler;
import org.apache.http.impl.client.DefaultHttpClient;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.util.ArrayList;
import java.util.List;

import butterknife.BindView;
import butterknife.ButterKnife;

public class Scanner extends AppCompatActivity {
    @BindView(R.id.camView)
    CameraView mCameraView;
    @BindView(R.id.cameraBtn)
    Button mCameraButton;
    @BindView(R.id.graphic_overlay)
    GraphicOverlay mGraphicOverlay;
    @BindView(R.id.next)
    Button nextButton;

    Bitmap bitmap;
    public void setBitmap(Bitmap bitmap) {
        this.bitmap = bitmap;
    }
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        ButterKnife.bind(this);

        mCameraView.addCameraKitListener(new CameraKitEventListener() {
            @Override
            public void onEvent(CameraKitEvent cameraKitEvent) {

            }

            @Override
            public void onError(CameraKitError cameraKitError) {

            }

            @Override
            public void onImage(CameraKitImage cameraKitImage) {

                Bitmap bitmap = cameraKitImage.getBitmap();
                bitmap = Bitmap.createScaledBitmap(bitmap, mCameraView.getWidth(), mCameraView.getHeight(), false);
                mCameraView.stop();
                runTextRecognition(bitmap);
                setBitmap(bitmap);
                Log.d("TAG", "*****in SCANNER bitmap object: " + bitmap.getHeight() + bitmap.getWidth());
               // ModelDocumentSelector.getDocumentType(bitmap);
            }

            @Override
            public void onVideo(CameraKitVideo cameraKitVideo) {

            }
        });

        mCameraButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mGraphicOverlay.clear();
                mCameraView.start();
                mCameraView.captureImage();
            }
        });

        nextButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                try {
                    ByteArrayOutputStream baos = new ByteArrayOutputStream();
                    bitmap.compress(Bitmap.CompressFormat.PNG, 100, baos);
                    byte[] b = baos.toByteArray();
                    String temp = Base64.encodeToString(b, Base64.DEFAULT);
                    JSONObject json = new JSONObject();
                    json.put("image", temp);
                    final String json_string = json.toString();

                    new AsyncTask<Void, Void, String>() {
                        @Override
                        protected String doInBackground(Void... params) {
                            return getResponse(json_string);
                        }

                        @Override
                        protected void onPostExecute(String result) {
                            Log.d("TAG", "*************" + result);
                            Intent intent = new Intent(getApplicationContext(), SuccessPage.class);
                            intent.putExtra("response", result);
                            startActivity(intent);
                        }
                    }.execute();
                }catch (Exception e){
                    e.printStackTrace();
                }

            }
        });

    }

    public String getResponse(String json) {
        HttpPost post = new HttpPost("http://172.20.4.96:5000/img");
        try {
            StringEntity stringEntity = new StringEntity(json);

            post.setEntity(stringEntity);
            post.setHeader("Content-type", "application/json");

            DefaultHttpClient defaultHttpClient = new DefaultHttpClient();

            BasicResponseHandler basicResponseHandler = new BasicResponseHandler();
            return defaultHttpClient.execute(post, basicResponseHandler);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    @Override
    public void onResume() {
        super.onResume();
        mCameraView.start();
    }
    @Override
    public void onPause() {
        mCameraView.stop();
        super.onPause();
    }

    private void runTextRecognition(Bitmap bitmap) {
        FirebaseVisionImage image = FirebaseVisionImage.fromBitmap(bitmap);
        FirebaseVisionTextDetector detector = FirebaseVision.getInstance()
                .getVisionTextDetector();
        detector.detectInImage(image)
                .addOnSuccessListener(
                        new OnSuccessListener<FirebaseVisionText>() {
                            @Override
                            public void onSuccess(FirebaseVisionText texts) {
                                processTextRecognitionResult(texts);
                            }
                        })
                .addOnFailureListener(
                        new OnFailureListener() {
                            @Override
                            public void onFailure(@NonNull Exception e) {
                                // Task failed with an exception
                                e.printStackTrace();
                            }
                        });

    }

    private void processTextRecognitionResult(FirebaseVisionText texts) {
        List<FirebaseVisionText.Block> blocks = texts.getBlocks();
        if (blocks.size() == 0) {
            Log.d("TAG", "No text found");
            return;
        }
        List<String> textResult = new ArrayList<String>();
        mGraphicOverlay.clear();
        for (int i = 0; i < blocks.size(); i++) {
            List<FirebaseVisionText.Line> lines = blocks.get(i).getLines();
            for (int j = 0; j < lines.size(); j++) {
                List<FirebaseVisionText.Element> elements = lines.get(j).getElements();
                String textS = "";
                for (int k = 0; k < elements.size(); k++) {
                    GraphicOverlay.Graphic textGraphic = new TextGraphic(mGraphicOverlay, elements.get(k));
                    mGraphicOverlay.add(textGraphic);

                    textS += elements.get(k).getText() + " ";
                    Log.d("TAG", "*********" + (elements.get(k).getBoundingBox()));
                }
                textResult.add(textS);
                Log.d("TAG", "*******************" + textS);
            }
        }
    }
}
