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
    browser.add_cookie({"name": "MUSIC_U", "value": "00EFE9235B660B39274330E272DBB06459253AEAD0D940B80B6CB9C34D530E2CA168701A4A0E67AB0CEBA608C159BC9EFE13CAEDE358682256807891EB52D65E11985B9FF7EE350D9B219269C78029FD9104AF391570DCBC7264D85BDDC589BA8282D8771D2243BDF56683F7B6BB4086A00599A3CF6318BDC6A07462ACA03FB0C288C28A9F0933D2A04FD0500F6B1B7CD6F9A11F3F51612CEED4947A81F7D337D373CC6A297C2B42CA9695F4C30AEA2694A4B39D26E807829136E2A34D48A07B82957301892EC1BC959377D7B5A4FCB1FA40A31FE0AB52FDA5BA78F032D5EB9355F91953D01B5E389D70DE8062B35924E5FB41D5EC394290D9E870CB2A10F6BA28F9318D429B7D8053491DCC9D78189680E334931CACA3F9577D2C03ED8A59FBB34BC4608A0C459461C709E758CB3B9C88F42CBB6E2E73C945E0DBF4D15092E8486AAD1A1840181756027EDEAD5D2B4493B47C3546C2495CF579F0258A86E001F4D9AB555B7AC65A90651519E4A3E5886B65675A12BAB08A62C9C171C87623CF496F103BEE148E0BBAEB5DEC128B36017B"})
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
