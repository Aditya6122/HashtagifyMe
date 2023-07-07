import requests
from bs4 import BeautifulSoup

def scrape_instagram_hashtags(url,output_file):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    entry_content = soup.find(class_="entry-content")
    ol_elements = entry_content.find_all("ol")
    hashtags = []
    for ol in ol_elements:
        li_elements = ol.find_all("li")
        for li in li_elements:
            hashtag = li.find(text=lambda t: t.startswith("#"))
            if hashtag:
                hashtags.append(hashtag)
    
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("\n".join(hashtags))


webpage_url = "https://www.mentionlytics.com/blog/top-instagram-hashtags/#for-your-posts" 
output_file = "top_hashtags.txt"
scrape_instagram_hashtags(webpage_url,output_file)