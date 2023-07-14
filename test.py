import requests

url = "http://localhost:5000/predict" 
image_path = "demo.png" 

with open(image_path, "rb") as file:
    files = {"image": file}
    response = requests.post(url, files=files)

print(response.text)
