//UI minima con boton para grabar/subir
// android/app/MainActivity.java
import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import java.io.File;
import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.RequestBody;
import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class MainActivity extends AppCompatActivity {
    private boolean recording = false;
    private ApiService api;

    @Override protected void onCreate(Bundle s){
        super.onCreate(s);
        Button btn = new Button(this);
        btn.setText("Grabar / Parar");
        setContentView(btn);

        api = ApiService.create("http://192.168.1.105:8000");

        btn.setOnClickListener((View v) -> {
            if (!recording){
                askPerms();
                startService(new Intent(this, RecordingService.class));
                recording = true; btn.setText("Parar y Subir");
            } else {
                stopService(new Intent(this, RecordingService.class));
                recording = false; btn.setText("Grabar / Parar");
                File wav = new File(getExternalFilesDir(null), "rec.wav");
                upload(wav);
            }
        });
    }

    private void askPerms(){
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED){
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.RECORD_AUDIO}, 123);
        }
    }

    private void upload(File wav){
        RequestBody rb = RequestBody.create(MediaType.parse("audio/wav"), wav);
        MultipartBody.Part part = MultipartBody.Part.createFormData("file", wav.getName(), rb);
        RequestBody lang = RequestBody.create(MediaType.parse("text/plain"), "es");
        api.upload(part, lang).enqueue(new Callback<>(){
            @Override public void onResponse(Call<ResponseBody> call, Response<ResponseBody> resp){
                // TODO: mostrar respuesta JSON (transcripción + resumen)
            }
            @Override public void onFailure(Call<ResponseBody> call, Throwable t){
                // TODO: mostrar error
            }
        });
    }
}