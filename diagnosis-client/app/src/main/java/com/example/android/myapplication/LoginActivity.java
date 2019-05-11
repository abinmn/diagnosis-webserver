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
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;

public class LoginActivity extends AppCompatActivity {

    private static final String TAG = "LoginActivity";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);


        final EditText usernameField = (EditText) findViewById(R.id.editTextUsername);
        final EditText passwordField = (EditText) findViewById(R.id.editTextPassword);
        final Button loginButton = (Button) findViewById(R.id.buttonLogin);



        loginButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String username, password;
                username = usernameField.getText().toString();
                password = passwordField.getText().toString();
                getAuthToken(username, password);

            }
        });



    }

    private void getAuthToken(final String username, final String password) {

        class UserLogin extends AsyncTask<Void, Void, String> {

            ProgressBar progressBar;

            @Override
            protected void onPreExecute() {
                super.onPreExecute();
                //Show login progress
                progressBar = (ProgressBar) findViewById(R.id.progressBar);
                progressBar.setVisibility(View.VISIBLE);
                Log.d(TAG, "onPreExecute: ");
            }

            @Override
            protected void onPostExecute(String s) {
                super.onPostExecute(s);
                Log.d(TAG, "onPostExecute: "+ s);
                //Disable progress bar after sending data
                progressBar.setVisibility(View.GONE);

                //Store token to preference manager
                try {
                    JSONObject jsonObject = new JSONObject(s);
                    String authToken = jsonObject.getString("token");

                    SharedPrefManager prefManager = new SharedPrefManager(LoginActivity.this);
                    prefManager.storeAuthToken(authToken);

                    //TODO result screen intent
                    Intent intent = new Intent(LoginActivity.this, GetDataActivity.class);
                    startActivity(intent);

                } catch (JSONException e) {
                    e.printStackTrace();
                    Log.d(TAG, "onPostExecute: " + s);
                    Toast.makeText(LoginActivity.this, "Login Failed", Toast.LENGTH_SHORT).show();
                }


            }

            @Override
            protected String doInBackground(Void... voids) {
                RequestHandler requestHandler = new RequestHandler();
                //Stroing username and password in hashmap
                HashMap<String,String> params = new HashMap<>();
                params.put("username", username);
                params.put("password", password);

                //return requestObject
                Log.d(TAG, "doInBackground: "+password);
                return requestHandler.sendRequest(LoginActivity.this,
                        URLs.AUTH_TOKEN, params, "POST", 0);

            }
        }

        UserLogin ul = new UserLogin();
        ul.execute();
    }
}
