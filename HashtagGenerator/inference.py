import model_utils
import torch
import PIL
import requests

processor = model_utils.load_processor()
model = model_utils.load_model(from_local=True)

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)
model.eval()

def get_inference(url):
    raw_image = PIL.Image.open(requests.get(url, stream=True).raw)
    inputs = processor(raw_image, return_tensors="pt").to(device)

    with torch.no_grad():
        multiple_output = model.generate(**inputs,max_length=15,do_sample=True,num_return_sequences=10)
        caption = processor.batch_decode(multiple_output,skip_special_tokens=True)

    hashtags = set()
    for i in caption:
        i = i.replace(',','')
        for j in i.split(' '):
            hashtags.add('#'+str(j))

    return hashtags


if __name__ == '__main__':
    get_inference('https://imgd.aeplcdn.com/1056x594/n/cw/ec/44686/activa-6g-right-front-three-quarter.jpeg?q=75')
