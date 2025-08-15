//Graba audio PCM16 y lo convierte a WAV
// android/app/AudioRecorder.java
import android.media.AudioFormat;
import android.media.AudioRecord;
import android.media.MediaRecorder;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;

public class AudioRecorder {
    private static final int SR = 16000;
    private static final int CH = AudioFormat.CHANNEL_IN_MONO;
    private static final int ENC = AudioFormat.ENCODING_PCM_16BIT;

    private AudioRecord rec;
    private boolean running = false;

    public interface Listener { void onError(Exception e); }

    public void start(String pcmPath, Listener listener) {
        int minBuf = AudioRecord.getMinBufferSize(SR, CH, ENC);
        rec = new AudioRecord(MediaRecorder.AudioSource.VOICE_RECOGNITION, SR, CH, ENC, minBuf*2);
        rec.startRecording();
        running = true;
        new Thread(() -> {
            try (FileOutputStream fos = new FileOutputStream(pcmPath)) {
                byte[] buf = new byte[minBuf];
                while (running) {
                    int n = rec.read(buf, 0, buf.length);
                    if (n > 0) fos.write(buf, 0, n);
                }
            } catch (IOException e) { if (listener != null) listener.onError(e);}
        }).start();
    }

    public void stop() {
        running = false;
        if (rec != null) {
            rec.stop();
            rec.release();
        }
    }

    public static void pcm16ToWav(String pcmPath, String wavPath) throws IOException {
        java.io.File pcm = new java.io.File(pcmPath);
        int sampleRate = SR; int channels = 1; int bitsPerSample = 16;
        long pcmSize = pcm.length();
        long byteRate = sampleRate * channels * bitsPerSample/8;
        try (FileOutputStream out = new FileOutputStream(wavPath);
             java.io.FileInputStream in = new java.io.FileInputStream(pcm)) {
            // WAV header
            out.write("RIFF".getBytes());
            out.write(intLE((int)(36 + pcmSize)));
            out.write("WAVEfmt ".getBytes());
            out.write(intLE(16)); // PCM chunk size
            out.write(shortLE((short)1)); // PCM
            out.write(shortLE((short)channels));
            out.write(intLE(sampleRate));
            out.write(intLE((int)byteRate));
            out.write(shortLE((short)(channels * bitsPerSample/8)));
            out.write(shortLE((short)bitsPerSample));
            out.write("data".getBytes());
            out.write(intLE((int)pcmSize));
            // data
            byte[] buf = new byte[4096]; int n;
            while ((n = in.read(buf)) > 0) out.write(buf, 0, n);
        }
    }

    private static byte[] intLE(int v){ return ByteBuffer.allocate(4).order(ByteOrder.LITTLE_ENDIAN).putInt(v).array(); }
    private static byte[] shortLE(short v){ return ByteBuffer.allocate(2).order(ByteOrder.LITTLE_ENDIAN).putShort(v).array(); }
}