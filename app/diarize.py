import whisperx
from whisperx import DiarizationPipeline
from typing import Any
import torch
hf_token='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'
device="cpu"
diarization_pipeline = whisperx.DiarizationPipeline(
                                    use_auth_token=hf_token,device=device)
def diarize_fn(audio_file: str) -> 'dict[str, Any]':

    diarization_result = diarization_pipeline(audio_file) 
    return diarization_result
