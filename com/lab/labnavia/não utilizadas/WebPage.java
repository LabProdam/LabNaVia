package com.lab.labnavia;
import org.renpy.android.PythonActivity;

import android.content.Context;
		
//import android.webkit.WebView;
 
import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
 
public class OpenURL extends Activity {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        Context context = (Context) PythonActivity.mActivity;
        super.onCreate(savedInstanceState);
        String url = "http://www.google.com/";
        Intent i = new Intent(Intent.ACTION_VIEW);
        i.setData(Uri.parse(url));
        startActivity(i);
    }
}
/*
public class WebViewActivity extends Activity {
 
	private WebView webView;
 
	public void onCreate(Bundle savedInstanceState) {
		Context context = (Context) PythonActivity.mActivity;
		super.onCreate(savedInstanceState);
		setContentView(R.layout.webview);
 
		webView = (WebView) findViewById(R.id.webView1);
		webView.getSettings().setJavaScriptEnabled(true);
		webView.loadUrl("http://www.google.com");
 
	}
 
}
*/
