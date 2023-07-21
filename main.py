from flask import Flask, request, render_template
from flask_cors import CORS
from PIL import Image
from InstagramScraping import credentials
from HashtagGenerator.inference import get_inference
from InstagramScraping.webdrivers import WebDriver

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
     driver.login_instagram(credentials.USERNAME,credentials.PASSWORD)
     app.run(port=5000)