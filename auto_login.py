# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00F4A4FA5065B6F0CB2A00B2AF20C545ABA5C4580245255BAFCCA3951FDA00F0655852F3D144C9834CAA549CAD761F5022079EC98DB4303A87C3E74421D5A5D8E9087A51AF778D4568120599598E1FFEBE506DA8DF454BAC8DAB948428FAC4CF05B8A907AA8DDE33A80AAB2E0F6CE9F99821C724D566A9F52385FD5A1F43584DFFD0F7B71163EC3E678992EBFA140BD8AB0999B2441E52A994F27673F05813764604B63C043A1DF6D1D25F887E8E21446A427671FE98A3423D0B994D93E05CFC823C73DFC4FB2F2F31E284435311F55A36F05E92D2C8536E08A217B8B23CE0148ECB7768E6AB76CA0FDD43AFA5B4469402D0A70723886C609AB32691F9981437465BC0DB3B603F43F0452A9EAF156E3CDC53E44A4D07990390AAC298E6286640A633962DC99095F855C48A17DD0ADAF43496186C095E8564BD468C673338F9CC0D65F17C463FBC403CE925FFC49E62BD71703749114196D5C6FE70C4CCEED3127B46D14CB18719C77090B30D6B539D352DB90778F5069279E357F1F1B34D48A7A953EA43018E2480176BE297968C637918"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
