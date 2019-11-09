package com.example.myapplication34;

import android.graphics.Bitmap;
import android.util.JsonReader;
import android.util.Log;

import androidx.appcompat.app.AppCompatActivity;

import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.URL;
import java.nio.ByteBuffer;

import javax.net.ssl.HttpsURLConnection;


public class Volley_Call extends AppCompatActivity {


    public void requestAndGetResponse(Bitmap bitmap) {
        new Thread(new Runnable(){
            @Override
            public void run() {
                // Do network action in this function
                try {
                    URL url = new URL("https://digon-api.herokuapp.com/img");
                    HttpsURLConnection myConnection = (HttpsURLConnection) url.openConnection();
                    myConnection.setRequestMethod("POST");
                    int size = bitmap.getRowBytes() * bitmap.getHeight();
                    ByteBuffer b = ByteBuffer.allocate(size);
                    bitmap.copyPixelsToBuffer(b);
                    myConnection.setRequestProperty("image", b.toString());

                    if (myConnection.getResponseCode() == 200) {
                        // Success
                        // Further processing here
                        InputStream responseBody = myConnection.getInputStream();
                        InputStreamReader responseBodyReader = new InputStreamReader(responseBody, "UTF-8");
                        JsonReader jsonReader = new JsonReader(responseBodyReader);
                        Log.d("TAG", responseBody.toString());
                        jsonReader.beginObject(); // Start processing the JSON object
                        while (jsonReader.hasNext()) { // Loop through all keys
                            String key = jsonReader.nextName(); // Fetch the next key
                            if (key.equals("name")) { // Check if desired key
                                // Fetch the value as a String
                                String value = jsonReader.nextString();

                                // Do something with the value
                                // ...
                                Log.d("TAG", "******name" + value);

                                break; // Break out of the loop
                            } else {
                                jsonReader.skipValue(); // Skip values of other keys
                            }
                        }
                        jsonReader.close();
                    } else {
                        // Error handling code goes here
                    }
                    myConnection.disconnect();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }).start();
       // RequestQueue queue = Volley.newRequestQueue(this);

    }
//        JsonObjectRequest request = JsonObjectRequest(Request.Method.GET, url, null, new Response.Listener<JSONObject>() {
//            @Override
//            public void onResponse(JSONObject response) {
//                Toast.makeText(getApplicationContext(), "Response :" + response.toString(), Toast.LENGTH_LONG).show();//display the response on screen
//            }
//        }, new Response.ErrorListener() {
//            @Override
//            public void onErrorResponse(VolleyError error) {
//                Log.i("TAG", "Error :" + error.toString());
//            }
//        });
//    }
//    RequestQueue queue = Volley.newRequestQueue(this);

}
