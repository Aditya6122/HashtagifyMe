import requests
from urllib.request import urlopen
from urllib.error import *

url = "http://localhost:5000/predict" 
image_path = "demo.png" 

try:
    html = urlopen(url)
     
except HTTPError as e:
    print("HTTP error", e)
     
except URLError as e:
    print("Opps ! Page not found!", e)

# with open(image_path, "rb") as file:
#     files = {"image": file}
#     response = requests.post(url, files=files, timeout=60)

# print(response)
# print(response.text)
# print(response.content)