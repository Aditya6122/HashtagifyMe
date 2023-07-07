from threading import local
from transformers import BlipForConditionalGeneration
from transformers import AutoProcessor
from transformers import AutoConfig
import torch

local_path = '../model/best_model.pth'
model_url = 'Salesforce/blip-image-captioning-base'

def load_processor():
    processor = AutoProcessor.from_pretrained(model_url)
    return processor

def load_model(from_local=True):
    config = AutoConfig.from_pretrained(model_url)

    if from_local:
        model =  BlipForConditionalGeneration(config)
        model.load_state_dict(torch.load(local_path))
    else:
        model =  BlipForConditionalGeneration.from_pretrained(model_url)
    
    return model

