from datetime import datetime
import json
import re
from selenium.webdriver.chrome.options import Options
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import base64
import os
from bs4 import BeautifulSoup,NavigableString



def initialize_webdriver(selector):
    option = Options()
    # option.add_argument("--headless")
    option.add_argument(f"user-data-dir={selector['chrome_profile_path']}")  # Use your actual profile path 
    option.add_experimental_option("detach", False)
    driver = webdriver.Chrome(options=option)
    driver.implicitly_wait(1)
    driver.maximize_window()
    url = "https://web.whatsapp.com/"
    driver.get(url)
    return driver

def config():
    with open('config.json') as f:
        data = json.load(f)
        return data['XPATH']
         
def create_post_data(get_element, channel, image_url, post_text, postTime, Number_of_rection, number_of_follower, profile_picture_url):
    return{
        "Source_name":get_element,
        "Source_link":channel,
        "Post_text":post_text,
        "Post_image":image_url,
        "Post_time":postTime,
        "Post_reaction":Number_of_rection,
        "Post_scraping_time":date_time(),
        "Followers": number_of_follower,
        "Profile_picture": profile_picture_url
    }

def save_channel_posts(channel_name, posts_data, folder="channel_jsons"):
    if not os.path.exists(folder):
        os.makedirs(folder)
    safe_channel_name = "".join(c if c.isalnum() else "_" for c in channel_name)
    filename = f"{folder}/{safe_channel_name}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(posts_data, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(posts_data)} posts to {filename}")

def date_time():
    date_now = datetime.now().isoformat()
    formatted_date = datetime.strptime(date_now, "%Y-%m-%dT%H:%M:%S.%f")
    date_now = formatted_date.strftime("%Y-%m-%d %H:%M:%S")
    return date_now

def number_of_new_posts(driver,selector):
    try:
        number_of_new_posts = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, selector['number_of_new_posts']))).text
        print(number_of_new_posts.text)
        return number_of_new_posts
        # //p[@class='selectable-text copyable-text x15bjb6t x1n2onr6']//span[@class='selectable-text copyable-text false']    
    except:
        number_of_new_posts = 1
        return number_of_new_posts        

def click_on_search_result(driver,selector):
    click_on_search_result = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, selector['click_on_search_result'])))
    click_on_search_result.click()
    time.sleep(3)

    try:
        click_on_Down_Arrow = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, selector['click_on_Down_Arrow'])))
        click_on_Down_Arrow.click()
        time.sleep(1)
    except:
        pass

def collect_post(driver,selector):
    try:
        all_posts = set()
        all_posts = driver.find_elements(By.XPATH, selector['all_posts_elements'])  # //div[@class="x1y332i5 x1n2onr6 x6ikm8r x10wlt62"]/div   #b //div[@class='xlm9qay x1w7sdjq x1fcty0u xw2npq5']  Number of reaction.
        print("Number of last posts:", len(all_posts))
        return all_posts
    except:
        print(f"Post elements not found...!")
        all_posts = None
        return all_posts

def Reactions(post_element,selector):
    try:
        reaction = post_element.find_element(By.XPATH, selector['reaction'])
        aria_label_value_of_rection = reaction.get_attribute("aria-label")
        # Use regex to find the number before 'in total'
        match = re.search(r'(\d{1,3}(?:,\d{3})*)(?= in total)', aria_label_value_of_rection)
        if match:
            return match.group(1)
        return None
    except:
        pass

def post_time(post_element,selector):
    try:
        date_and_time = post_element.find_element(By.XPATH, selector['date_and_time']).text
        return date_and_time
    except:
        date_and_time = None
        return date_and_time

def image(driver,selector,post,get_element,counter):
    try:
        try:
            img = post.find_element(By.XPATH, selector['img_1'])
        except:
            try:
                img = post.find_element(By.XPATH, selector['img_2'])
            except:
                try:
                    img = post.find_element(By.XPATH, selector['img_3'])
                except:
                    img = None  
        img_link = (
            img.get_attribute("src") or
            img.get_attribute("data-src") or
            img.get_attribute("srcset")
            )
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(img_link)
        time.sleep(2)

        folder = selector['folder']
        if not os.path.exists(folder):
            os.makedirs(folder)

        filename = f"{folder}/post_{get_element}_{counter}.png"
        driver.save_screenshot(filename)
        time.sleep(2)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        return filename
    except:
        filename = None
        return filename

def text(driver,selector,post):
    try:
        span_elem = post.find_element(By.XPATH, selector['text'])
        html = span_elem.get_attribute("innerHTML")

        soup = BeautifulSoup(html, "html.parser")
        post_text = ""
        for item in soup.contents:
            if isinstance(item, NavigableString):
                post_text += item
            # elif item.name == "img":
            elif item.findChildren() == "img":    
                emoji = item.get("data-plain-text") or item.get("alt") or ""
                post_text += emoji
            elif item.name:
                post_text += item.get_text()
        return post_text
    except:
        post_text = None
        return post_text

def search_in_box(driver, get_element,selector):
    try:
        search_box = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, selector['search_box'])))
        search_box.click()
        time.sleep(1)
        search_box.send_keys(Keys.CONTROL + "a")
        search_box.send_keys(Keys.BACKSPACE) 
        search_box.send_keys(get_element)
        search_box.send_keys(Keys.ENTER)
    except Exception as e:
        print(f"Error interacting with search box: {e}")

def scrap(driver,selector):
    Channels = source()
    for channel in Channels:
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(channel)

        get_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, selector['get_element']))).text
        print(get_element)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        try:
            channel_icon = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, selector['channel_icon'])))
            channel_icon.click()
        except:
            pass

        search_in_box(driver,get_element,selector)
        new_post_number = number_of_new_posts(driver,selector)
        click_on_search_result(driver,selector)
        post_element = collect_post(driver,selector)
        if post_element == None:
            continue
        else:
            counter = 1
            channel_posts = []
            number_of_follower = None
            profile_picture_url = ""
            for post in post_element:
                image_url = image(driver,selector,post,get_element,counter)
                print(image_url)
                post_text = text(driver,selector,post)
                print(post_text)
                postTime = post_time(post,selector)
                print(postTime)
                Number_of_rection = Reactions(post,selector)
                print(Number_of_rection)
                try:
                    if counter == 1:
                        number_of_follower, profile_picture_url = number_of_follower_profile_picture(driver,selector)
                except:
                    pass
                counter +=1
                post_data = create_post_data(get_element, channel, image_url, post_text, postTime, Number_of_rection, number_of_follower, profile_picture_url)
                channel_posts.append(post_data)
            save_channel_posts(get_element, channel_posts)
        input("Enter any key...")
        
        # (//div[@class='_ajv7 x1n2onr6 x1okw0bk x5yr21d x14yjl9h xudhj91 x18nykt9 xww2gxu xlkovuz x16j0l1c xyklrzc x1mh8g0r x1anpbxc x18wx58x xo92w5m'])[2]
def number_of_follower_profile_picture(driver,selector):
    try:
        driver.find_element(By.XPATH, selector['profile']).click()
        time.sleep(2)
        follower_text = driver.find_element(By.XPATH, selector['followers']).text
        # Extract just the number using regex
        follower_number = re.search(r'(\d{1,3}(?:,\d{3})*)', follower_text)
        follower = follower_number.group(1) if follower_number else "0"
        profile_picture = driver.find_element(By.XPATH, selector['profile_picture']).get_attribute("src")
        driver.find_element(By.XPATH, selector['X_button']).click()
        return follower,profile_picture
    except:
        follower = None
        return follower


def wait_for_chat_element(driver, selector, retries=0, max_retries=30):
    try:
        time.sleep(1)
        element = driver.find_element(By.XPATH, selector['chat_element'])
        print("Element is visible.")
        return True
    except Exception as e:
        print(f"Exception occurred: {e}")
        if retries < max_retries:
            print("Element not yet visible, checking again...")
            return wait_for_chat_element(driver, selector, retries + 1, max_retries)
        else:
            print("Max retries reached. Element not found.")
            return False

def is_login(driver,selector):
    login_status = wait_for_chat_element(driver,selector)
    if login_status == True:
        try:
            scrap(driver,selector)
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Session is not Present. Please scan the QR code.")
        time.sleep(60)
        try:
            scrap(driver,selector)
        except Exception as e:
            print(f"Error: {e}")

def source():
    Channels = ['https://whatsapp.com/channel/0029Vb1u54S60eBnTNoJ8G0H', 'https://whatsapp.com/channel/0029Va3WSqz4SpkO04ZeQI1j', 'https://whatsapp.com/channel/0029Va5nZToFSAt56yKM0C1f', 'https://whatsapp.com/channel/0029VaksqICDeON2lLebTt3L', 'https://whatsapp.com/channel/0029VakgKm5LdQeemosdqc0F']
    return Channels

def main():
    selector = config()
    # print(selector['chrome_profile_path'])
    # chrome_profile_path = "/home/mesba/.config/google-chrome/Default"
    driver = initialize_webdriver(selector)
    is_login(driver,selector)

    
if __name__ == "__main__":
    main()