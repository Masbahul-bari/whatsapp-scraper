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




def initialize_webdriver(chrome_profile_path):
    option = Options()
    # option.add_argument("--headless")
    option.add_argument(f"user-data-dir={chrome_profile_path}")  # Use your actual profile path 
    option.add_experimental_option("detach", False)
    driver = webdriver.Chrome(options=option)
    driver.implicitly_wait(1)
    driver.maximize_window()
    url = "https://web.whatsapp.com/"
    driver.get(url)
    return driver

def create_post_data(channel, image_url, post_text, postTime, Number_of_rection):
    return{
        "Source_link":channel,
        "Post_text":image_url,
        "Post_image":post_text,
        "Post_time":postTime,
        "Post_reaction":Number_of_rection,
        "Post_scraping_time":date_time()
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

def number_of_new_posts(driver):
    try:
        number_of_new_posts = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='_ahlk']/span"))).text
        print(number_of_new_posts.text)
        return number_of_new_posts
        # //p[@class='selectable-text copyable-text x15bjb6t x1n2onr6']//span[@class='selectable-text copyable-text false']    
    except:
        number_of_new_posts = 1
        return number_of_new_posts        

def click_on_search_result(driver):
    click_on_search_result = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='matched-text _ao3e']")))
    click_on_search_result.click()
    time.sleep(3)

    try:
        click_on_Down_Arrow = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//span[@class='x1h7gb8d x1rg5ohu xq77vm1']")))
        click_on_Down_Arrow.click()
        time.sleep(1)
    except:
        pass

def collect_post(driver):
    try:
        all_posts = set()
        all_posts = driver.find_elements(By.XPATH, "//div[@class='_amjv _aotl']")  # //div[@class="x1y332i5 x1n2onr6 x6ikm8r x10wlt62"]/div   #b //div[@class='xlm9qay x1w7sdjq x1fcty0u xw2npq5']  Number of reaction.
        print("Number of last posts:", len(all_posts))
        return all_posts
    except:
        print(f"Post elements not found...!")
        all_posts = None
        return all_posts

def Reactions(post_element):
    try:
        reaction = post_element.find_element(By.XPATH, ".//button[@class='xo0jvv6']")
        aria_label_value_of_rection = reaction.get_attribute("aria-label")
        # Use regex to find the number before 'in total'
        match = re.search(r'(\d{1,3}(?:,\d{3})*)(?= in total)', aria_label_value_of_rection)
        if match:
            return match.group(1)
        return None
    except:
        pass

def post_time(post_element):
    try:
        date_and_time = post_element.find_element(By.XPATH, ".//span[@class='x1rg5ohu x16dsc37']").text
        return date_and_time
    except:
        date_and_time = None
        return date_and_time

def image(driver,post,get_element,counter):
    # counter = 1
    # folder = "post_screenshots"
    # if not os.path.exists(folder):
    #     os.makedirs(folder)

    # for post in all_posts:
        #-------element screen short----------#
        # try:
        #     filename = f"{folder}/post_{counter}.png"
        #     post.screenshot(filename)
        #     print(filename)
        # except:
        #     img_link = None
        #     print(img_link)
    try:
        # img = post.find_element(By.XPATH, ".//div[@class='_ahy5']//img")
        img = post.find_element(By.XPATH, ".//img")
        # img_link = img.get_attribute("src")
        img_link = (
            img.get_attribute("src") or
            img.get_attribute("data-src") or
            img.get_attribute("srcset")
            )
        folder="images"
        if img_link.startswith("data:image"):
            if not os.path.exists(folder):
                os.makedirs(folder)
            # Split the header from the base64 data
            date_now = datetime.now().isoformat()
            formatted_date = datetime.strptime(date_now, "%Y-%m-%dT%H:%M:%S.%f")  # Adjusted format
            date_now = formatted_date.strftime("%Y-%m-%d %H:%M:%S")
            # Split the header from the base64 data
            header, encoded = img_link.split(",", 1)
            file_ext = header.split(";")[0].split("/")[1]  # e.g., 'png' or 'jpeg'
            # filename = f"image_{date_now}_{counter}.{file_ext}"
            filename = f"{folder}/image_{get_element}_{date_now}_{counter}.{file_ext}"
            
            img_data = base64.b64decode(encoded)
            with open(filename, "wb") as f:
                f.write(img_data)
            print(f"Image saved as image_from_post.{file_ext}")
        return filename
    except:
        img_link = None
        return img_link

def text(driver,post):
    try:
        # Adjust the tag or class as needed for the text element
        # post_text = post.text
        #post_text = post.find_element(By.XPATH, ".//span[@class='_ao3e selectable-text copyable-text']").text
        # print(post_text)
        # text = post.find_element(By.XPATH, ".//div[@class='_akbu'")  # //div[@class="_akbu"]
        # post_text = text.text
        # print(post_text)

        span_elem = post.find_element(By.XPATH, ".//span[@class='_ao3e selectable-text copyable-text']")
        html = span_elem.get_attribute("innerHTML")

        soup = BeautifulSoup(html, "html.parser")
        post_text = ""
        for item in soup.contents:
            if isinstance(item, NavigableString):
                post_text += item
            elif item.name == "img":
                emoji = item.get("data-plain-text") or item.get("alt") or ""
                post_text += emoji
            elif item.name:
                post_text += item.get_text()
        return post_text
    except:
        post_text = None
        return post_text

def search_in_box(driver, get_element):
    try:
        search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "(//div[@class='x1n2onr6 xh8yej3 lexical-rich-text-input'])[1]//p")))
        search_box.click()
        time.sleep(1)
        search_box.send_keys(Keys.CONTROL + "a")
        search_box.send_keys(Keys.BACKSPACE) 
        search_box.send_keys(get_element)
        search_box.send_keys(Keys.ENTER)
    except Exception as e:
        print(f"Error interacting with search box: {e}")

def scrap(driver):
    Channels = source()
    for channel in Channels:
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(channel)

        get_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h3[@class='_9vd5 _9t2_']"))).text #driver.find_element(By.XPATH, "//h3[@class='_9vd5 _9t2_']")
        print(get_element)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        try:
            channel_icon = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//span[@data-icon='newsletter-outline']")))
            channel_icon.click()
        except:
            pass

        search_in_box(driver,get_element)
        new_post_number = number_of_new_posts(driver)
        click_on_search_result(driver)
        post_element = collect_post(driver)
        if post_element == None:
            continue
        else:
            counter = 1
            channel_posts = []
            for post in post_element:
                image_url = image(driver,post,get_element,counter)
                print(image_url)
                post_text = text(driver,post)
                print(post_text)
                postTime = post_time(post)
                print(postTime)
                Number_of_rection = Reactions(post)
                print(Number_of_rection)
                counter +=1
                post_data = create_post_data(channel, image_url, post_text, postTime, Number_of_rection)
                channel_posts.append(post_data)
            save_channel_posts(get_element, channel_posts)
        create_post_data(channel, image_url, post_text, postTime, Number_of_rection)
        input("Enter any key...")
        
        # (//div[@class='_ajv7 x1n2onr6 x1okw0bk x5yr21d x14yjl9h xudhj91 x18nykt9 xww2gxu xlkovuz x16j0l1c xyklrzc x1mh8g0r x1anpbxc x18wx58x xo92w5m'])[2]

def wait_for_chat_element(driver, retries=0, max_retries=10):
    try:
        time.sleep(1)
        element = driver.find_element(By.XPATH, "//h1[@class='x1qlqyl8 x1pd3egz xcgk4ki']")
        print("Element is visible.")
        return True
    except Exception as e:
        print(f"Exception occurred: {e}")
        if retries < max_retries:
            print("Element not yet visible, checking again...")
            return wait_for_chat_element(driver, retries + 1, max_retries)
        else:
            print("Max retries reached. Element not found.")
            return False

def is_login(driver):
    login_status = wait_for_chat_element(driver)
    if login_status == True:
        try:
            scrap(driver)
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Session is not Present. Please scan the QR code.")
        time.sleep(60)
        try:
            scrap(driver)
        except Exception as e:
            print(f"Error: {e}")

def source():
    Channels = ['https://whatsapp.com/channel/0029Va5nZToFSAt56yKM0C1f', 'https://whatsapp.com/channel/0029VaksqICDeON2lLebTt3L', 'https://whatsapp.com/channel/0029VakgKm5LdQeemosdqc0F', 'https://whatsapp.com/channel/0029Va3WSqz4SpkO04ZeQI1j']
    return Channels

def main():
    chrome_profile_path = "/home/mesba/.config/google-chrome/Default"
    driver = initialize_webdriver(chrome_profile_path)
    is_login(driver)
    
if __name__ == "__main__":
    main()