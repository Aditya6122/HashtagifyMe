import pandas as pd

data = pd.read_csv('instagram_data.csv')
unique_hashtags = list(data['hashtag'].unique())
unique_hashtags = ['#' + i for i in unique_hashtags]

hashtags = pd.read_csv('hashtag_vocab_new.csv')
unscraped_hashtags = hashtags[~hashtags['hashtag'].isin(unique_hashtags)]['hashtag']
unscraped_hashtags = unscraped_hashtags.sample(frac = 1)
unscraped_hashtags = list(unscraped_hashtags)
unscraped_hashtags = pd.DataFrame(unscraped_hashtags)

unscraped_hashtags.to_csv('hashtags_shuffled.csv',index = False)
