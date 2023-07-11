import torch
import PIL
import requests
try:
    from HashtagGenerator import model_utils
except:
    import model_utils

processor = model_utils.load_processor()
model = model_utils.load_model(from_local=True)

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)
model.eval()

@torch.no_grad()
def get_inference(url):
    try:
        raw_image = PIL.Image.open(requests.get(url, stream=True).raw)
    except:
        raw_image = url

    inputs = processor(raw_image, return_tensors="pt").to(device)

    multiple_output = model.generate(**inputs,max_length=15,do_sample=True,num_return_sequences=3)
    caption = processor.batch_decode(multiple_output,skip_special_tokens=True)

    hashtags = set()
    for i in caption:
        i = i.replace(',','')
        for j in i.split(' '):
            hashtags.add('#'+str(j))

    return hashtags


if __name__ == '__main__':
    print(get_inference('https://imgd.aeplcdn.com/1056x594/n/cw/ec/44686/activa-6g-right-front-three-quarter.jpeg?q=75'))
