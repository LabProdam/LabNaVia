package com.lab.labnavia;
import org.renpy.android.PythonActivity;

import android.content.Context;
import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;

public class OpenURL {
    public void press(String url){
        Context context = (Context) PythonActivity.mActivity;
        //String url = "https://www.google.com/";
        Intent i = new Intent(Intent.ACTION_VIEW);
        i.setData(Uri.parse(url));
        context.startActivity(i);
    	
    }
}
