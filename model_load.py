from transformers import BlipForConditionalGeneration
from transformers import AutoProcessor
from transformers import AutoConfig

model_url = 'Salesforce/blip-image-captioning-base'
print("loading processor")
processor = AutoProcessor.from_pretrained(model_url)
print("loading config")
config = AutoConfig.from_pretrained(model_url)
print("loading model")
model =  BlipForConditionalGeneration(config)
print("success")