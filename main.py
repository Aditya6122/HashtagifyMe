from flask import Flask, request, render_template
from flask_cors import CORS
from PIL import Image
from HashtagGenerator.inference import get_inference
from InstagramScraping.webdrivers import WebDriver
import os
from dotenv import load_dotenv

load_dotenv()

app=Flask(__name__)
CORS(app)

@app.route('/')
def home():
     return render_template("index.html")

@app.route('/predict',methods=['POST'])
def predict():
     file = request.files['image']
     raw_image = Image.open(file)
     keywords = list(get_inference(raw_image))
     hashtags = list(set(driver.generate_hashtags(keywords)))
     return hashtags

if __name__ == '__main__':
     driver = WebDriver()
     instagram_username = os.getenv('INSTA_USERNAME')
     instagram_password = os.getenv('INSTA_PASSWORD')
     driver.login_instagram(instagram_username,instagram_password)
     app.run(port=5000)