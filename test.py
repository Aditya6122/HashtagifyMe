import requests
from urllib.request import urlopen

url = "http://localhost:5000/predict" 
image_path = "demo.png" 

time = 0
flag = True
while(time<60 and flag):
    try:
        html = urlopen(url)
        flag = False
    except:
        print("waiting..from",time+1,"seconds")
        time += 1 

with open(image_path, "rb") as file:
    files = {"image": file}
    response = requests.post(url, files=files, timeout=60)

print(response.text)