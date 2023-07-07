from torch.utils.data import Dataset
from torch.nn.utils.rnn import pad_sequence
import torch
import numpy as np
from datasets import load_dataset
from datasets.utils.file_utils import get_datasets_user_agent
import io
import urllib
import PIL.Image

USER_AGENT = get_datasets_user_agent()

dataset_name = "conceptual_captions"
labeled_config = "labeled"
whole_dataset = load_dataset(dataset_name,labeled_config,split='train')
dataset = whole_dataset.select(range(8))
dataset = dataset.train_test_split(test_size=0.10, shuffle=True, seed=42)
dataset['train'] = dataset['train'].train_test_split(test_size=0.12, shuffle=True, seed=42)
data = {}
data['train'] = dataset['train']['train']
data['train'].set_format("torch")
data['eval'] = dataset['train']['test']
data['eval'].set_format("torch")
data['test'] = dataset['test']
data['test'].set_format("torch")

def fetch_single_image(image_url, timeout=10, retries=0):
    for _ in range(retries + 1):
        try:
            request = urllib.request.Request(
                image_url,
                data=None,
                headers={"user-agent": USER_AGENT},
            )
            with urllib.request.urlopen(request, timeout=timeout) as req:
                image = PIL.Image.open(io.BytesIO(req.read()))
            break
        except Exception:
            image = None
    return image


class ConceptualCaptionCustom(Dataset):
    def __init__(self, dataset, processor):
        self.dataset = dataset
        self.processor = processor

    def __getitem__(self, idx):
        item = self.dataset[idx]
        img_url = item['image_url']
        label = item['labels']
        img = fetch_single_image(img_url)

        if img is None:
            return None

        target = [label[0]]
        for i in label[1:]:
            target.append(',')
            target.append(i)

        target = ' '.join([i for i in target])
        item = {"image": img, "text": target}
        try:
            encoding = self.processor(images=item["image"], text=item["text"],return_tensors="pt")
            encoding = {k:v.squeeze() for k,v in encoding.items()}
            return encoding
        except:
            return None

    def __len__(self):
        return len(self.dataset)

def collate_fn(batch, dataset, batch_size):
    pixel_values = []
    input_ids = []

    for i in batch:
        if(i is not None):
            pixel_values.append(i['pixel_values'])
            input_ids.append(i['input_ids'])

    missing = 0
    if(len(batch) != batch_size):
        missing = batch_size - len(batch)

    while missing!=0:
        rand_idx = np.random.randint(0, len(dataset))
        rand_ele = dataset[rand_idx]
        if(rand_ele != None):
            pixel_values.append(rand_ele['pixel_values'])
            input_ids.append(rand_ele['input_ids'])
            missing -=1

    validated_batch = {}
    validated_batch['input_ids'] = pad_sequence(input_ids).permute(1,0)
    validated_batch['pixel_values'] = torch.stack(pixel_values)

    return validated_batch

def get_train_dataset(processor):
    return ConceptualCaptionCustom(data['train'],processor)

def get_val_dataset(processor):
    return ConceptualCaptionCustom(data['eval'],processor)

def get_test_dataset(processor):
    return ConceptualCaptionCustom(data['test'],processor)