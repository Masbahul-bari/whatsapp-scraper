from selenium import webdriver
from selenium.webdriver.common.by import By
import time
driver = webdriver.Chrome()

driver.get("https://web.whatsapp.com")

time.sleep(10)

driver.quit()