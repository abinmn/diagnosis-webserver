package com.example.android.myapplication;

import android.app.Activity;
import android.content.Context;
import android.util.Log;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.DataOutputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.util.HashMap;
import java.util.Map;

import javax.net.ssl.HttpsURLConnection;

import static android.content.ContentValues.TAG;

/**
 * Created by Belal on 9/5/2017.
 */

public class RequestHandler {


    //this method will send a post request to the specified url
    //in the hashmap we have the data to be sent to the server in keyvalue pairs
    public String sendRequest(Context context, String requestURL, HashMap<String, String> postDataParams, String method, int t) {
        URL url;
        String authToken;


        StringBuilder sb = new StringBuilder();
        try {
            url = new URL(requestURL);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setReadTimeout(30000);
            conn.setConnectTimeout(30000);
            conn.setRequestMethod(method);
            conn.setRequestProperty("Content-Type", "application/json; charset=utf-8");
            conn.setDoInput(true);
            conn.setDoOutput(false);

            SharedPrefManager prefManager = new SharedPrefManager(context);
            Activity activity = (Activity) context;
            String activity_name = activity.getLocalClassName();
//            if (activity_name != "LoginActivity" && activity_name!="SignUpActivity") {
//                authToken = prefManager.getKeyAuthtoken();
//                conn.setRequestProperty("Authorization", "Token " + authToken);
//            }

            if (method == "POST") {

                if (t==1) {

                    authToken = prefManager.getKeyAuthtoken();
                    conn.setRequestProperty("Authorization", "Token " + authToken);
                }

                DataOutputStream os = new DataOutputStream(conn.getOutputStream());
                os.writeBytes(getPostDataString(postDataParams));
                os.flush();
                os.close();

            }

            else {
                authToken = prefManager.getKeyAuthtoken();
                conn.setRequestProperty("Authorization", "Token " + authToken);
            }

            int responseCode = conn.getResponseCode();

            if (responseCode == HttpsURLConnection.HTTP_OK) {

                BufferedReader br = new BufferedReader(new InputStreamReader(conn.getInputStream()));
                sb = new StringBuilder();
                String response;

                while ((response = br.readLine()) != null) {
                    sb.append(response);
                }
            }

            else {

                BufferedReader br = new BufferedReader(new InputStreamReader(conn.getErrorStream()));
                sb = new StringBuilder();
                String response;

                while ((response = br.readLine()) != null) {
                    sb.append(response);

                    Log.d(TAG, "sendRequest: error");
                }


            }

        } catch (Exception e) {
            e.printStackTrace();
        }
        return sb.toString();
    }


    //this method is converting keyvalue pairs data into a query string as needed to send to the server
    private String getPostDataString(HashMap<String, String> params) throws UnsupportedEncodingException, JSONException {
        JSONObject jsonParam = new JSONObject();
        boolean first = true;
        for (Map.Entry<String, String> entry : params.entrySet()) {

            jsonParam.put(entry.getKey(), entry.getValue());
        }
        Log.d(TAG, "getPostDataString: "+jsonParam.toString());
        return jsonParam.toString();
    }


}