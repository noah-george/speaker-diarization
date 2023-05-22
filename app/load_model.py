import whisper
import torch
model_name: str='base'
device: str = "cpu"
hf_token='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'

if torch.cuda.is_available():
    model = whisper.load_model(model_name, device).cuda()
else:
    model = whisper.load_model(model_name, device)