from pathlib import Path
import torch
from openvino.tools import mo
from openvino.runtime import serialize, Core
from openvino.runtime import Core
import numpy as np
from pyannote.audio import Pipeline
import whisperx
hf_token='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'

pipeline = whisperx.DiarizationPipeline(use_auth_token=hf_token)
def infer_segm(chunks: torch.Tensor) -> np.ndarray:
    """
    Inference speaker segmentation mode using OpenVINO
    Parameters:
        chunks (torch.Tensor) input audio chunks
    Return:
        segments (np.ndarray)
    """
    res = ov_seg_model(chunks)
    return res[ov_seg_out]




core = Core()

ov_speaker_segmentation_path = Path("serialized.xml")

ov_speaker_segmentation = core.read_model(ov_speaker_segmentation_path)
print(f"Model successfully loaded from {ov_speaker_segmentation_path}")
ov_seg_model = core.compile_model(ov_speaker_segmentation)
infer_request = ov_seg_model.create_infer_request()
ov_seg_out = ov_seg_model.output(0)
