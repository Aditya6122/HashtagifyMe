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
        html = urlopen("http://localhost:5000")
        flag = False
    except:
        print("waiting..from",timeout+1,"seconds")
        time.sleep(1)
        timeout += 1 

if(flag):
    raise Exception("There is some problem with the running \n\
        Check if its running properly...")

with open(image_path, "rb") as file:
    files = {"image": file}
    response = requests.post(url, files=files, timeout=60)

print(response.text)