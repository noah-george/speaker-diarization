import wave
import numpy as np
import soundfile as sf
import pyloudnorm as pyln
def loudness(file):

    w = wave.open(file)
    sample_rate = w.getframerate()
    sam = w.readframes(w.getnframes())
    sam = np.frombuffer(sam, dtype=np.int16)

    bigpos = np.where( sam > 20000 )
    bigneg = np.where( sam < -20000 )
    print("loud:",bigpos)
    print("soft:",bigneg)
    print(bigpos[0].shape)
    print(bigneg[0].shape)
    loud_timestamps = bigpos[0] / sample_rate
    print("Loud Timestamps:", loud_timestamps)

    w.close()

#write a function to extract loud regions in an audio file using pyloudnorm

# def loudness(file):
#     data, rate = sf.read(file)
#     meter = pyln.Meter(rate) # create BS.1770 meter
#     loudness = meter.integrated_loudness(data)
#     print(loudness)

loudness("example2.wav")

    