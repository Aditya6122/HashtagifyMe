import time
import credentials
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import warnings

def create_webdriver():
    service = Service('./chromedriver')
    driver = webdriver.Chrome(service=service)
    return driver

def login_instagram(driver):
    driver.get('https://www.instagram.com/')
    username_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']")))
    password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='password']")))
    username_input.send_keys(credentials.USER_NAME)
    password_input.send_keys(credentials.PASSWORD)
    password_input.send_keys(Keys.RETURN)
    not_now = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//button[@class="_a9-- _a9_1"]')))
    not_now.click()
    return driver

def get_hashtags(file_path):
    data = pd.read_csv(file_path)
    hashtags = data['hashtag']
    hashtag_list = list(hashtags.sample(frac = 1))
    return hashtag_list

def get_hashtag_data(hashtag,driver):
    num_posts = 9
    driver.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
    post = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="_aabd _aa8k  _al3l"]')))
    post.click()
    time.sleep(5)
    posts = []
    for i in range(num_posts):
        post = {}
        given_hashtags = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//a[@class="x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz  _aa9_ _a6hd"]')))
        # given_hashtags = driver.find_elements(By.XPATH, '//a[@class="x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz  _aa9_ _a6hd"]')
        img = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//img[@class="x5yr21d xu96u03 x10l6tqk x13vifvy x87ps6o xh8yej3"]')))
        #img = driver.find_elements(By.XPATH, '//img[@class="x5yr21d xu96u03 x10l6tqk x13vifvy x87ps6o xh8yej3"]')
        img = img[i]
        post['hashtag'] = hashtag
        post['other_hashtags'] = [i.text for i in given_hashtags]
        post['image_url'] = img.get_attribute('src')
        post['caption'] = img.get_attribute('alt')
        if(post['caption'] != ''):
            posts.append(post)
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class=" _aaqg _aaqh"]')))[-1].click()
            #driver.find_elements(By.XPATH, '//div[@class=" _aaqg _aaqh"]')[-1].click()
        except:
            print('early')
        time.sleep(2)
        img = None
    return pd.DataFrame(posts)

driver = create_webdriver()
driver = login_instagram(driver)

hashtag_list = pd.read_csv('hashtags_shuffled.csv')
hashtag_list = hashtag_list['0'].to_list()
start_from = 0

data = pd.read_csv('instagram_data.csv')

for i in hashtag_list[start_from:]:
    INSTAGRAM_DATA = pd.DataFrame(columns=['hashtag','image_url','caption','other_hashtags'])

    try:
        hashtag_data = get_hashtag_data(i[1:],driver)
    except:
        warnings.warn('Some problem occured while scraping data for hashtag: '+i[1:])

    INSTAGRAM_DATA = pd.concat([INSTAGRAM_DATA,hashtag_data],ignore_index=True)
    data = pd.concat([data,INSTAGRAM_DATA],ignore_index=True,axis=0)
    data.to_csv('latest_data.csv',index=False)

driver.close()