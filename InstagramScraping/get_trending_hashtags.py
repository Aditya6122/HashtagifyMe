from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class WebDriver:
    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.service = Service('./chromedriver')
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(service=self.service,options=self.options)
        
    def login_instagram(self):
        self.driver.get('https://www.instagram.com/')
        username_input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']")))
        password_input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='password']")))
        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.RETURN)
        try:
            dont_save_info = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, '//div[@class="_ac8f"]')))
            dont_save_info.click()
        except:
            print("Save Information pop didn't showed up or not found")
        
        try:
            not_now = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, '//button[@class="_a9-- _a9_1"]')))
            not_now.click()
        except:
            print("Get notifications pop up didn't showed up or not found")
            
    
    def get_search_bar(self):
        self.driver.set_window_size(width=720, height=1000)
        search_bar = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, '//input[@class="x1lugfcp x19g9edo x6umtig x1b1mbwd xaqea5y xav7gou x1lq5wgf xgqcy7u x30kzoy x9jhf4c x9f619 x5n08af xl565be x5yr21d x1a2a7pz xyqdw3p x1pi30zi xg8j3zb x1swvt13 x1yc453h xh8yej3 xhtitgo xs3hnx8 x1dbmdqj xoy4bel x7xwk5j"]')))
        return search_bar
    
    def generate_hashtags(self,keywords):
        search_bar = self.get_search_bar()
        final_hashtags = []
        for keyword in keywords:
            search_bar.clear()
            search_bar.send_keys(str('#'+keyword))
            elements = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x2lah0s x193iq5w xeuugli x1iyjqo2"]')))
            hashtags_dict = dict((key, int(value.replace(',', ''))) for key, value in (item.text[:-6].split('\n') for item in elements[:10]))
            clear_box = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div._aawn._9-lv[aria-label="Clear the Search Box"]')))
            clear_box.click()
            hashtags_dict = {key: value for key, value in hashtags_dict.items() if value >= 1000000}
            hashtags = list(dict(sorted(hashtags_dict.items(), key=lambda item: item[1], reverse=True)).keys())[:3]
            final_hashtags += hashtags
        return final_hashtags
    
    def close_driver(self):
        self.driver.close()