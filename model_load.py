from transformers import BlipForConditionalGeneration
from transformers import AutoProcessor
from transformers import AutoConfig

model_url = 'Salesforce/blip-image-captioning-base'
processor = AutoProcessor.from_pretrained(model_url)
config = AutoConfig.from_pretrained(model_url)
model =  BlipForConditionalGeneration(config)