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

    outputs = model.generate(
                                **inputs,
                                do_sample=True,
                                num_return_sequences=5,
                                max_length=20,
                                temperature=0.7,
                                top_k=3
                            )

    caption = processor.batch_decode(outputs, skip_special_tokens=True)

    keywords = []
    for i in caption:
        for j in i.split(','):
            keywords.append(j.strip())

    keywords = set(i for i in keywords if i)
    return keywords

if __name__ == '__main__':
    print(get_inference('https://imgd.aeplcdn.com/1056x594/n/cw/ec/44686/activa-6g-right-front-three-quarter.jpeg?q=75'))
