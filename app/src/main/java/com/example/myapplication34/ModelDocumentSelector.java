package com.example.myapplication34;

import android.graphics.Bitmap;
import android.graphics.Color;
import android.util.Log;

import androidx.annotation.NonNull;

import com.google.android.gms.tasks.OnFailureListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.firebase.ml.common.FirebaseMLException;
import com.google.firebase.ml.custom.FirebaseModelDataType;
import com.google.firebase.ml.custom.FirebaseModelInputOutputOptions;
import com.google.firebase.ml.custom.FirebaseModelInputs;
import com.google.firebase.ml.custom.FirebaseModelInterpreter;
import com.google.firebase.ml.custom.FirebaseModelManager;
import com.google.firebase.ml.custom.FirebaseModelOptions;
import com.google.firebase.ml.custom.FirebaseModelOutputs;
import com.google.firebase.ml.custom.model.FirebaseLocalModelSource;

public class ModelDocumentSelector {
    static FirebaseModelInterpreter interpreter;
    static FirebaseModelInputOutputOptions inputOutputOptions;

    public void loadModel() {
        FirebaseLocalModelSource localSource = new FirebaseLocalModelSource.Builder("document_selector")
                .setAssetFilePath("model.tflite")  // Or setFilePath if you downloaded from your host
                .build();
        FirebaseModelManager.getInstance().registerLocalModelSource(localSource);

        FirebaseModelOptions options = new FirebaseModelOptions.Builder()
                .setLocalModelName("document_selector")
                .build();

        try {
            interpreter = FirebaseModelInterpreter.getInstance(options);

            inputOutputOptions =
                    new FirebaseModelInputOutputOptions.Builder()
                            .setInputFormat(0, FirebaseModelDataType.FLOAT32, new int[]{1, 224, 224, 3})
                            .setOutputFormat(0, FirebaseModelDataType.FLOAT32, new int[]{1, 5})
                            .build();
            Log.d("TAG", "*****Model successfully loaded**********");
        } catch (FirebaseMLException e) {
            e.printStackTrace();
        }
    }

    public static void getDocumentType(Bitmap bitmap) {
        bitmap = Bitmap.createScaledBitmap(bitmap, 224, 224, true);
       // bitmap=Bitmap.createBitmap(1980, 1000, Bitmap.Config.ALPHA_8);
        int batchNum = 0;
        float[][][][] input = new float[1][224][224][3];
        for (int x = 0; x < 224; x++) {
            for (int y = 0; y < 224; y++) {
                int pixel = bitmap.getPixel(x, y);
                // Normalize channel values to [-1.0, 1.0]. This requirement varies by
                // model. For example, some models might require values to be normalized
                // to the range [0.0, 1.0] instead.
                input[batchNum][x][y][0] = (Color.red(pixel) - 127) / 128.0f;
                input[batchNum][x][y][1] = (Color.green(pixel) - 127) / 128.0f;
                input[batchNum][x][y][2] = (Color.blue(pixel) - 127) / 128.0f;
            }
        }

        Log.d("TAG", "*****input: " + input[0][0].length + " " + input[0][0][0].length);

        try {
            FirebaseModelInputs inputs = new FirebaseModelInputs.Builder()
                    .add(input)  // add() as many input arrays as your model requires
                    .build();
            Log.d("TAG", "*****inputs : " + inputs.zzff().length);
            Log.d("TAG", "********inputoutput " + inputOutputOptions.zzfe().entrySet().iterator().next().getValue());
            interpreter.run(inputs, inputOutputOptions)
                    .addOnSuccessListener(
                            new OnSuccessListener<FirebaseModelOutputs>() {
                                @Override
                                public void onSuccess(FirebaseModelOutputs result) {
                                    float[][] output = result.getOutput(0);
                                    Log.d("TAG", "!!!!!!!!!!!!!! output: " + output[0][0]);
                                }
                            })
                    .addOnFailureListener(
                            new OnFailureListener() {
                                @Override
                                public void onFailure(@NonNull Exception e) {
                                    // Task failed with an exception
                                    // ...
                                    Log.d("TAG", "!!!!!!!!in FAilure");
                                    e.printStackTrace();
                                }
                            });
        } catch (FirebaseMLException e) {
            e.printStackTrace();
        }

    }
}
