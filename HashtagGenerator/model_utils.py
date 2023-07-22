from transformers import BlipForConditionalGeneration
from transformers import AutoProcessor
from transformers import AutoConfig
import os
import gdown
import warnings
import torch

local_path = 'model/best_model.pth'
model_url = 'Salesforce/blip-image-captioning-base'

def load_processor():
    processor = AutoProcessor.from_pretrained(model_url)
    return processor

def load_model(device,from_local=True):
    print("Initiating to load model config")
    config = AutoConfig.from_pretrained(model_url)
    print("Model config loaded successfully")

    if from_local:
        print(os.listdir())
        model =  BlipForConditionalGeneration(config)
        if not os.path.isfile(local_path):
            print("No local model file found !!")
            print("Initiate to download from drive")
            try:
                remote_model_path = 'https://drive.google.com/uc?id=1vxmwsSSUQ0MTjfQ2uSAc9J96ezuoh9aa'
                gdown.download(url=remote_model_path ,output=local_path,quiet=False)
            except:
                raise Exception('Some unknown exception occured while fetching the remote model file. \n \
                    Check if file is present on the remote location')
        
        print("Loading model from local path")
        model.load_state_dict(torch.load(local_path,map_location=device))
        print("Model state dict loaded successfully")
        return model

    warnings.warn("You are about to download the original \"BlipForConditionalGeneration\"\n \
        This behaviour is not expected unless you are training the from scratch for Hashtag generation")
    model =  BlipForConditionalGeneration.from_pretrained(model_url)

    return model


