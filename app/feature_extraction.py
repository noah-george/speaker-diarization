import wave
import numpy as np
import librosa
import matplotlib.pyplot as plt
def loudness(file):

    w = wave.open(file)
    sample_rate = w.getframerate()
    sam = w.readframes(w.getnframes())
    sam = np.frombuffer(sam, dtype=np.int16)
    bigpos = np.where( sam > 20000 )
    print("loud:",bigpos)
    print(bigpos[0].shape)
    loud_timestamps = bigpos[0] / sample_rate
    print("Loud Timestamps:", loud_timestamps)
    

# Load the audio file
    audio_path = file
    audio, sr = librosa.load(audio_path)

# Get the time axis
    time = librosa.times_like(audio)

# Plot the amplitude waveform
    plt.figure(figsize=(10, 4))
    plt.plot(time, audio)
    plt.title('Amplitude Waveform')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.tight_layout()
    plt.show()
    plt.savefig('amplitude.png')
 




def mfcc(file):
    print("ex")
    y, sr = librosa.load(file)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
    print(mfccs)
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(mfccs, x_axis='time')
    plt.colorbar()
    plt.title('MFCC')
    plt.tight_layout()
    plt.show()
    plt.savefig('mfcc.png')



loudness("example2.wav")
mfcc("example2.wav")


    