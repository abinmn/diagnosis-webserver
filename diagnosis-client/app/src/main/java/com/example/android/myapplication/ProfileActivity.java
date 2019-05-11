package com.example.android.myapplication;

import android.content.Intent;
import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ProgressBar;
import android.widget.Spinner;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;

public class ProfileActivity extends AppCompatActivity {

    String name, height, age, gender, weight, blood;
    private static final String TAG = "ProfileActivity";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_profile);

        Button buttonHeight = (Button) findViewById(R.id.buttonHeight);
        buttonHeight.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                EditText editTextName = (EditText) findViewById(R.id.editTextName);
                EditText editTextAge = (EditText) findViewById(R.id.editTextAge);
                EditText editTextHeight = (EditText) findViewById(R.id.editTextHieght);
                Spinner spinnerGender = (Spinner) findViewById(R.id.spinnerGender);
                EditText editTextWeight = (EditText) findViewById(R.id.editTextWeight);
                Spinner spinnerBlood = (Spinner) findViewById(R.id.spinnerBlood);

                name = editTextName.getText().toString();
                age = editTextAge.getText().toString();
                gender = String.valueOf(spinnerGender.getSelectedItem());
                height = editTextHeight.getText().toString();
                weight = editTextWeight.getText().toString();
                blood = String.valueOf(spinnerBlood.getSelectedItem());
                submitProfile();
            }
        });
    }

    private void submitProfile() {

        class Profile extends AsyncTask<Void, Void, String> {

            ProgressBar progressBar;

            @Override
            protected void onPreExecute() {
                super.onPreExecute();
                progressBar = (ProgressBar) findViewById(R.id.progressBar);
                progressBar.setVisibility(View.VISIBLE);
            }

            @Override
            protected void onPostExecute(String s) {
                super.onPostExecute(s);
                progressBar.setVisibility(View.GONE);

                try {
                    JSONObject jsonObject = new JSONObject(s);
                    String status = jsonObject.getString("status");
                    Log.d(TAG, "onPostExecute: "+ status);
                    Toast.makeText(ProfileActivity.this, "Profile Updated", Toast.LENGTH_SHORT).show();

                    //Go to getDataActivity
                    Intent intent = new Intent(ProfileActivity.this, GetDataActivity.class);
                    startActivity(intent);

                } catch (JSONException e) {
                    e.printStackTrace();
                    Toast.makeText(ProfileActivity.this, "An error occured", Toast.LENGTH_SHORT).show();
                    Log.d(TAG, "onPostExecute: " + s);
                }

            }

            @Override
            protected String doInBackground(Void... voids) {
                RequestHandler requestHandler = new RequestHandler();

                SharedPrefManager prefManager = new SharedPrefManager(ProfileActivity.this);
                String token = prefManager.getKeyAuthtoken();

                HashMap<String, String> params = new HashMap<>();
                params.put("name", name);
                params.put("age", age);
                params.put("gender", gender);
                params.put("height", height);
                params.put("weight", weight);
                params.put("blood_group", blood);


                return requestHandler.sendRequest(ProfileActivity.this, URLs.PROFILE, params, "POST", 1);
            }
        }

        Profile h = new Profile();
        h.execute();
    }
}
