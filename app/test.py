from pyannote.audio import Model
import torch
hf_token='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'

model = Model.from_pretrained("pyannote/segmentation",use_auth_token=hf_token)
# torch_mod=model.to_torch(device='cpu')
# print(type(model))
# print(torch_mod)
model.eval()
print(model.example_input_array.shape)
dum_inp = torch.randn(3,1,32000)
torch.onnx.export(model,dum_inp,'model.onnx')
mo.convert_model
