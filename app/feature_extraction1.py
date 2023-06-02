import wave
import numpy as np

def get_audio_intervals(file, threshold):
    w = wave.open(file, 'rb')
    sample_rate = w.getframerate()
    print(sample_rate)
    sam = w.readframes(w.getnframes())
    sam = np.frombuffer(sam, dtype=np.int16)

    # Find indices of loud regions
    loud_indices = np.where(sam > threshold)[0]

    # Calculate intervals of loudness
    loud_intervals = get_intervals(loud_indices, sample_rate)

    w.close()

    return loud_intervals


def get_intervals(indices, sample_rate):
    intervals = []
    start_index = indices[0]
    for i in range(1, len(indices)):
        if indices[i] != indices[i-1] + 1:
            end_index = indices[i-1]
            start_time = start_index / sample_rate
            end_time = end_index / sample_rate
            intervals.append((start_time, end_time))
            start_index = indices[i]
    # Handle the last interval
    end_index = indices[-1]
    start_time = start_index / sample_rate
    end_time = end_index / sample_rate
    intervals.append((start_time, end_time))

    return intervals


# Usage example
threshold = 20000  # Adjust this threshold based on your audio characteristics
loud_intervals = get_audio_intervals("example1.wav", threshold)

print("Loud Intervals:",loud_intervals)
loudlist=[]
check=0
start=0
end=0.1
for interval in range(len(loud_intervals)-1):
    x=round(loud_intervals[0][interval],2)
    y=round(loud_intervals[1][interval],2)
    if(x+0.01==y):
        if(check==0):
            start=x
            end=y
            check=1
            continue
        else:
            end=y
            continue
    elif(x==y):
        continue
    check=0
    loudlist.append(f"Start Time: {start:.2f}s, End Time: {end:.2f}s")        
    print(loudlist)