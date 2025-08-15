//servicio en primer plano para grabar sin ser detenido
// android/app/RecordingService.java
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.Service;
import android.content.Intent;
import android.os.Build;
import android.os.IBinder;

public class RecordingService extends Service {
    public static final String CH_ID = "rec_channel";
    private AudioRecorder recorder;
    private String pcmPath, wavPath;

    @Override public void onCreate(){
        super.onCreate();
        if (Build.VERSION.SDK_INT >= 26){
            NotificationChannel ch = new NotificationChannel(CH_ID, "Grabación", NotificationManager.IMPORTANCE_LOW);
            ((NotificationManager)getSystemService(NOTIFICATION_SERVICE)).createNotificationChannel(ch);
        }
        Notification n = new Notification.Builder(this, CH_ID)
                .setContentTitle("Grabando audio…")
                .setSmallIcon(android.R.drawable.ic_btn_speak_now)
                .build();
        startForeground(1, n);
        recorder = new AudioRecorder();
    }

    @Override public int onStartCommand(Intent i, int f, int id){
        pcmPath = getExternalFilesDir(null)+"/rec.pcm";
        wavPath = getExternalFilesDir(null)+"/rec.wav";
        recorder.start(pcmPath, e -> stopSelf());
        return START_STICKY;
    }

    @Override public void onDestroy(){
        recorder.stop();
        try { AudioRecorder.pcm16ToWav(pcmPath, wavPath);} catch (Exception ignored) {}
        super.onDestroy();
    }

    @Override public IBinder onBind(Intent intent){ return null; }
}