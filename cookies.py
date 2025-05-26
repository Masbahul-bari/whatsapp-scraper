import pickle
from selenium import webdriver

cookies_path="W_cookies.pkl"

def load_cookies(driver: webdriver.Chrome):        
    try:
        with open(cookies_path, "rb") as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)
        print("Cookies loaded successfully.")
        driver.refresh()
    except FileNotFoundError:
        print("Cookies file not found.")
        raise

def save_cookies(driver):
    with open(cookies_path, "wb") as file:
        pickle.dump(driver.get_cookies(), file)
    print(f"Cookies saved to {cookies_path}")
