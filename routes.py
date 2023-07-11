from flask import Flask, request
from flask_cors import CORS
from PIL import Image
from HashtagGenerator.inference import get_inference

app=Flask(__name__)
CORS(app)

@app.route('/',methods=['POST'])
def predict():
     file = request.files['image']
     raw_image = Image.open(file)
     hashtags = list(get_inference(raw_image))
     print(hashtags)
     return hashtags
