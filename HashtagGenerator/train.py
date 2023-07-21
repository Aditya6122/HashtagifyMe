import model_utils
from conceptual_caption_custom import get_train_dataset
from torch.utils.data import DataLoader
from conceptual_caption_custom import collate_fn
import torch
from tqdm import tqdm

device = "cuda" if torch.cuda.is_available() else "cpu"

processor = model_utils.load_processor()
model = model_utils.load_model(device, from_local=True)

train_dataset = get_train_dataset(processor)

BATCH_SIZE = 1
NUM_WORKERS = 0

train_dataloader =  DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=NUM_WORKERS,pin_memory=True, collate_fn = lambda batch :collate_fn(batch, train_dataset, batch_size=BATCH_SIZE))

model.to(device)
model.train()

for param in model.parameters():
    param.requires_grad = True

for vision_param in model.vision_model.parameters():
    vision_param.requires_grad = False

bert_params = model.text_decoder.bert.parameters()
cls_params = model.text_decoder.cls.parameters()

optimizer = torch.optim.AdamW([
                {'params': bert_params, 'lr': 1e-6},
                {'params': cls_params}
            ], lr=1e-5)

num_epochs = 3
running_loss = 0
subsection = len(train_dataloader)//4

for epoch in range(num_epochs):
    print(f"Epoch [{epoch + 1}/{num_epochs}]")
    print("-"*100)
    running_loss = 0
    progress_bar = tqdm(total=subsection)
    for idx, batch in enumerate(train_dataloader):
        input_ids = batch["input_ids"].to(device)
        pixel_values = batch["pixel_values"].to(device)

        outputs = model(input_ids=input_ids,
                        pixel_values=pixel_values,
                        labels=input_ids)

        loss = outputs.loss
        running_loss += loss
        if (idx % subsection == 0 and idx!=0) or (idx+1 == len(train_dataloader)):
            if(progress_bar):
                progress_bar.close()
            print(f"Epoch [{epoch + 1}/{num_epochs}], Batch [{idx + 1}/{len(train_dataloader)}], Loss: {running_loss/subsection}")
            running_loss = 0
            if(idx+1 != len(train_dataloader)):
              progress_bar = tqdm(total=subsection)

        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
        if(idx+1 != len(train_dataloader)):
          progress_bar.update(1)
    if(progress_bar):
        progress_bar.close()

torch.save(model.state_dict(), '../model/latest_model.pth')