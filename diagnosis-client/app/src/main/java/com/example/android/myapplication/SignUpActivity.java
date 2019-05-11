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

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;

public class SignUpActivity extends AppCompatActivity {

    EditText editTextUserName, editTextEmail, editTextPassword;
    String username, email, password;
    Button buttonRegister;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_sign_up);

        buttonRegister = (Button) findViewById(R.id.buttonRegister);

        buttonRegister.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                editTextUserName = (EditText) findViewById(R.id.editTextUsername);
                editTextEmail = (EditText) findViewById(R.id.editTextEmail);
                editTextPassword = (EditText) findViewById(R.id.editTextPassword);

                username = editTextUserName.getText().toString();
                email = editTextEmail.getText().toString();
                password = editTextPassword.getText().toString();
                signup(username, email, password);
            }
        });
    }

    private void signup(final String username, final String email, final String password) {

        class CreateAccount extends AsyncTask<Void, Void, String> {

            ProgressBar progressBar;
            RequestHandler requestHandler = new RequestHandler();
            private static final String TAG = "CreateAccount";

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
                    String authToken = jsonObject.getString("token");

                    SharedPrefManager prefManager = new SharedPrefManager(SignUpActivity.this);
                    prefManager.storeAuthToken(authToken);

                    Intent intent = new Intent(SignUpActivity.this, ProfileActivity.class);
                    startActivity(intent);
                    Log.d(TAG, "onPostExecute: " + prefManager.isLoggedIn());

                } catch (JSONException e) {
                    e.printStackTrace();
                }



            }


            @Override
            protected String doInBackground(Void... voids) {
                //Storing username, email and password in hashmap
                HashMap<String, String> params = new HashMap<>();
                params.put("username", username);
                params.put("email", email);
                params.put("password", password);


                return requestHandler.sendRequest(SignUpActivity.this, URLs.CREATE_ACCOUNT, params, "POST", 0);
            }
        }

        CreateAccount createAccount = new CreateAccount();
        createAccount.execute();
    }
}
