## HashtagifyMe

A webapp that generates hashtags based on the image sentiment and trends of instagram.

### Concept

- Uses BLIP: Image Captioning Base model from transformers.
- After given an Image the model generates the labels describing the image or given scenario.
- The extracted labels or description are sent to the instagram and trending hashtags relevant to the particular image are fetched and given as output.

### Tech Stack

- **Languages** - Python, HTML, CSS, JavaScript
- **Frameworks** - Pytorch, Flask, BootStrap
- **Libraries** - Transformers

### Run Locally

Step 1. Clone the project

```cmd
  git clone https://github.com/Aditya6122/HashtagifyMe.git
```

Step 2. Go to the project directory

```cmd
  cd HashtagifyMe
```

Step 3. Create and activate a python virtual environment

```cmd
  python -m venv venv
  venv\Scripts\activate
```

Step 4. Install dependencies

```cmd
  pip install -r local_env.txt
```

Step 5. Add the Instagram credentials

- Create InstagramScraping/credentials.py
- Add your Instagram login credentials

```python
  USERNAME = <your-username>
  PASSWORD = <your-password>
```
Step 6. Creat a folder for model file

- When you are running the program for the first time. It will download the model state dict from remote drive link.

```cmd
  mkdir model
```

Step 7. Make sure you have chromedriver installed.

Step 8. Run the server

```python
  python main.py
```
Step 9. Getting the Inference

- Go to the localhost 
```
http://127.0.0.1:5000/
```
- Choose an Image
- Click on Submit

![image](https://github.com/Aditya6122/HashtagifyMe/assets/78961497/1c036ca9-d368-4e41-be17-3828c6523129)

🎉🎉 Hurray !!! It's Working...

