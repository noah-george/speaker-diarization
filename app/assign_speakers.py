from whisperx import assign_word_speakers 
from typing import Any
def assign_speakers_fn(
    diarization_result, aligned_segments
):


    result_segments= assign_word_speakers(
        diarization_result, aligned_segments
    )
    
    for item in result_segments["segments"]:
        del item["words"]
    return result_segments