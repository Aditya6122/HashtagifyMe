from transformers import BlipForConditionalGeneration
from transformers import AutoProcessor
from transformers import AutoConfig
import torch
import gdown
import os
import warnings

local_path = 'model/new_model.pth'
model_url = 'Salesforce/blip-image-captioning-base'

def load_processor():
    processor = AutoProcessor.from_pretrained(model_url)
    return processor

def load_model(from_local=True):
    config = AutoConfig.from_pretrained(model_url)

    if from_local:
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
        
        model.load_state_dict(torch.load(local_path))
        return model

    warnings.warn("You are about to download the original \"BlipForConditionalGeneration\"\n \
        This behaviour is not expected unless you are training the from scratch for Hashtag generation")

    model =  BlipForConditionalGeneration.from_pretrained(model_url)

    return model


