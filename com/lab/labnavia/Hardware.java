package com.lab.labnavia;
import org.renpy.android.PythonActivity;

import android.content.Context;
import android.os.Bundle;
import android.location.LocationListener;
import android.location.LocationManager;
import android.location.Location;
import android.util.Log;
import java.lang.Runnable;
import android.app.Activity;
import com.lab.labnavia.LocationInfo;

/*

public Location getLastKnownLocation (String provider)
Added in API level 1

Returns a Location indicating the data from the last known location fix obtained from the given provider.

This can be done without starting the provider. Note that this location could be out-of-date, for example if the device was turned off and moved to another location.

If the provider is currently disabled, null is returned.
Parameters
provider 	the name of the provider
Returns

    the last known location for the provider, or null

Throws
SecurityException 	if no suitable permission is present
IllegalArgumentException 	if provider is null or doesn't exist

*/

public class Hardware {
	public final LocationInfo location = new LocationInfo();
	public Context context;
	public LocationManager locationManager;
	
	public Location helloworld() {
		Context context = (Context) PythonActivity.mActivity;
		LocationManager locationManager = (LocationManager) context.getSystemService(Context.LOCATION_SERVICE);
		Location location = locationManager.getLastKnownLocation(LocationManager.GPS_PROVIDER);
		return location;
	}
	public LocationManager startLocationManager(){
		context = (Context) PythonActivity.mActivity;
		locationManager = (LocationManager) context.getSystemService(Context.LOCATION_SERVICE);
		return locationManager;
	}
	public void startLocationUpdater(final LocationManager locationManager,long tempo,float distancia){
		Activity context = (Activity) PythonActivity.mActivity;
		Log.i("LabNaVia", "Init");			
		try {
			context.runOnUiThread(new Runnable() {
				@Override
				public void run() {
					Log.i("LabNaVia", "Runnable run");
					LocationListener locationListener=new LocationListener(){
						@Override
						public void onLocationChanged(Location loc) {
							Log.i("LabNaVia", "Location: " + loc);
							location.longitude=(double)loc.getLongitude();
							location.latitude=(double)loc.getLatitude();
							Log.i("LabNaVia", "Lat: " + location.latitude + " long: " + location.longitude);
						}
						@Override
						public void onProviderDisabled(String provider) {
							Log.i("LabNaVia","provider disabled: "+provider);
						}
						@Override
						public void onProviderEnabled(String provider) {
							Log.i("LabNaVia","provider enabled: "+provider);
						}
						@Override
						public void onStatusChanged(String provider, int status, Bundle extras) {
							Log.i("LabNaVia","status chanched: "+provider+","+status+","+extras);
						}
					};
					locationManager.requestLocationUpdates(LocationManager.GPS_PROVIDER , 1000 , 1,  locationListener);
					locationManager.requestLocationUpdates(LocationManager.NETWORK_PROVIDER , 1000 , 1,  locationListener);
				}
			});
		}
		catch (Exception e) {
			Log.i("LabNaVia","Exception:" + e.toString());
		}
	}
	public Location getLocation(LocationManager locationManager) {
		Context context = (Context) PythonActivity.mActivity;
		Location location = locationManager.getLastKnownLocation(LocationManager.GPS_PROVIDER);
		return location;
	}
}
