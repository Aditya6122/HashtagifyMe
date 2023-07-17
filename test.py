from time import time
import requests
from urllib.request import urlopen
import time

url = "http://localhost:5000/predict" 
image_path = "demo.png" 

timeout = 0
flag = True
while(timeout<60 and flag):
    try:
        html = urlopen(url)
        flag = False
    except:
        print("waiting..from",timeout+1,"seconds")
        time.sleep(1)
        timeout += 1 

# with open(image_path, "rb") as file:
#     files = {"image": file}
#     response = requests.post(url, files=files, timeout=60)

# print(response.text)