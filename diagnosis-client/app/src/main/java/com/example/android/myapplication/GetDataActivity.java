package com.example.android.myapplication;

import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;

public class GetDataActivity extends AppCompatActivity {

    private static final String TAG = "GetDataActivity";



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_get_data);

        Button getDataButton = (Button) findViewById(R.id.buttonRetrieve);
        getDataButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                get_data();
            }
        });
    }

    private void get_data() {

        class RetrieveData extends AsyncTask<Void, Void, String> {

            ProgressBar progressBar ;
            TextView textViewBpmResults;
            TextView textViewCOResults;
            String bpm, cardiac_output;

            @Override
            protected void onPreExecute() {
                super.onPreExecute();


                progressBar = (ProgressBar) findViewById(R.id.progressBar);
                progressBar.setVisibility(View.VISIBLE);

                textViewBpmResults = (TextView) findViewById(R.id.textViewBpmResults);
                textViewCOResults = (TextView) findViewById(R.id.textViewCOResults);

                textViewBpmResults.setText("");
                textViewCOResults.setText("");
            }

            @Override
            protected void onPostExecute(String s) {
                super.onPostExecute(s);
                progressBar.setVisibility(View.GONE);
                Log.d(TAG, "onPostExecute: "+s);

                try {
                    JSONArray jsonArray = new JSONArray(s);
                    JSONObject jsonObject = (JSONObject) jsonArray.get(0);
                    bpm = jsonObject.getString("bpm");
                    cardiac_output = jsonObject.getString("cardiac_output");

                    if (cardiac_output.equals("")) {
                        Toast.makeText(GetDataActivity.this, "Timeout...", Toast.LENGTH_SHORT).show();
                    }
                    //update on device
                    textViewCOResults.setText(cardiac_output);
                    textViewBpmResults.setText(bpm);



                } catch (JSONException e) {
                    e.printStackTrace();
                }



            }

            @Override
            protected String doInBackground(Void... voids) {
                RequestHandler requestHandler = new RequestHandler();

                SharedPrefManager prefManager = new SharedPrefManager(GetDataActivity.this);
                String token = prefManager.getKeyAuthtoken();

                HashMap<String, String> params = new HashMap<>();

                //bpm and co
                return requestHandler.sendRequest(GetDataActivity.this, URLs.DATA, params, "GET", 1);
            }
        }

        RetrieveData r = new RetrieveData();
        r.execute();
    }
}
