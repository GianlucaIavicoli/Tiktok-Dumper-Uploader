import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import *

from webdriver_manager.chrome import ChromeDriverManager

import pyautogui


def get_driver(url="https://www.instagram.com"):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument(f"--lang=en")
    chrome_options.add_argument(
        '--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option(
        'excludeSwitches', ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)
    time.sleep(3)
    return driver


def login(driver, usr, pwd):
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Allow all cookies')]"))).click()
    print("[i] Cookie skipped successfully")

    # Username and Password fields
    username = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
    password = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

    username.clear()
    username.send_keys(usr)

    password.clear()
    password.send_keys(pwd)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[type='submit']"))).click()
    time.sleep(3)

    print("[i] Logged in successfully")
    return


def upload(driver, file_path, post_caption):
    # Upload photo [svg aria-label="New Post"]
    time.sleep(3)

    # Click on New post
    newPost = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[7]/div/span/div/a/div')))
    newPost.click()
    time.sleep(3)

    selectFromPC = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Select from computer')]")))
    selectFromPC.click()
    time.sleep(3)

    # Upload file

    pyautogui.write(file_path)
    pyautogui.press('enter')
    time.sleep(3)

    # Check if file is a video
    # TODO: fix "OK" notification
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Ok')]"))).click()
    except:
        pass

    # Next
    nextBtn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Next')]")))
    nextBtn.click()
    time.sleep(3)

    # Edit
    nextBtn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Next')]")))
    nextBtn.click()
    time.sleep(3)

    # Caption
    captionBox = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div[1]/p")))
    captionBox.click()
    time.sleep(3)

    pyautogui.write(post_caption)
    time.sleep(3)

    # Share
    shareBtn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Share')]")))
    shareBtn.click()
    time.sleep(3)

    time.sleep(30)
    pyautogui.press('exit')
    return


if __name__ == "__main__":
    driver = get_driver()
    login(driver, "anime.lover.0_", "Tommasononcimettereilnaso")
    upload(driver, "C:\\Users\\Matte\\Downloads\\crux.mp4", "Test")
