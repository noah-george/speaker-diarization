from typing import List, Dict, Any
import whisper
import torch 
model_name: str='base'
device = 'cuda' if torch.cuda.is_available() else 'cpu'
hf_token='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'
if torch.cuda.is_available():
      model = whisper.load_model(model_name, device).cuda()
else:
    model = whisper.load_model(model_name, device)
async def transcribe_audio(audio_file: str) -> 'dict[str, Any]':
    result = model.transcribe(audio_file)

    language_code = result["language"]
    return {
        "segments": result["segments"],
        "language_code": language_code,
    }
