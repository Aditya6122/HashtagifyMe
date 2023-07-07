import re
import pandas as pd

with open('separated_hashtags.txt','r') as f:
    hashtags = f.readlines()

def clean_text(text):
    text = re.sub(r'^.*?#', '#', text)
    hashtag, words = text.split(":")
    words = re.sub(r'\s',' ',words)
    words = re.sub(r',',' ',words)
    words = words.split(' ')
    words = [i for i in words if len(i)!=0]
    return hashtag, words

data = {}
for i in range(len(hashtags)):
    hashtag,words = clean_text(hashtags[i])
    data[hashtag] = words

df = pd.DataFrame(list(data.items()),columns=['hashtag','words'])
df.to_csv('hashtag_vocab_new.csv',index=False)