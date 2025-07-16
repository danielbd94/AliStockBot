import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# --- CONFIG ---
PRODUCT_URLS = [
    "https://www.aliexpress.com/item/1005009371982773.html?lang=en"
]
CHECK_INTERVAL = 5  # seconds
TELEGRAM_TOKEN = "7448321825:AAG0tonJV_8IZPq4X7j_UnpwG-bUW8zfacw"
CHAT_ID = "499209783"
CHROMEDRIVER_PATH = "C:/chromedriver/chromedriver.exe"

# --- TELEGRAM NOTIFY ---
def send_telegram_alert(url):
    message = f"🎉 Product restocked!\n{url}"
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(telegram_url, data=payload)

# --- CHECK STOCK WITH SELENIUM ---
def is_in_stock(url):
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--lang=en-US")
    options.add_experimental_option("prefs", {
        "intl.accept_languages": "en,en_US"
    })

    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    time.sleep(3)
    driver.delete_all_cookies()
    driver.execute_script("window.localStorage.clear();")
    driver.execute_script("window.sessionStorage.clear();")
    driver.refresh()
    time.sleep(5)

    try:
        wait = WebDriverWait(driver, 10)
        add_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Add to Cart') or contains(., 'Buy Now') or contains(., 'הוסיפו לעגלה') or contains(., 'קנה עכשיו')]")))

        if add_btn.is_enabled():
            driver.quit()
            return True
        else:
            driver.quit()
            return False
    except TimeoutException:
        print("[ERROR] Button not found in time.")
        driver.quit()
        return False

# --- MAIN LOOP ---
print("🟢 Starting AliExpress stock checker bot (Final Fix)...")
while True:
    for url in PRODUCT_URLS:
        if is_in_stock(url):
            print(f"[ALERT] Product in stock: {url}")
            send_telegram_alert(url)
            PRODUCT_URLS.remove(url)
        else:
            print(f"[WAIT] Still out of stock: {url}")
    time.sleep(CHECK_INTERVAL)
