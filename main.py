import os
import time
import random
import requests
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime

# --- CONFIG ---
PRODUCT_URLS = [
    "https://www.aliexpress.com/item/1234567891234567.html",
    "https://www.aliexpress.com/item/1234567891234567.html"
]

CHECK_INTERVAL = 120  # seconds
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"
PROFILE_PATH = "C:/chrome_profile"  # persistent session
LOG_FILE = "aliexpress_stock_checker.log"

# --- CLEAR OLD LOG ---
if os.path.exists(LOG_FILE):
    os.remove(LOG_FILE)

# --- LOGGING ---
def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_msg = f"[{timestamp}] {message}"
    print(full_msg)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(full_msg + "\n")

# --- TELEGRAM NOTIFY ---
def send_telegram_alert(message):
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        response = requests.post(telegram_url, data=payload)
        if response.status_code != 200:
            log(f"[❌] Telegram error: {response.text}")
    except Exception as e:
        log(f"[❌] Telegram exception: {e}")

# --- BROWSER SETUP ---
log("🟢 Starting AliExpress stock checker bot...")

options = uc.ChromeOptions()
options.user_data_dir = PROFILE_PATH
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

driver = uc.Chrome(options=options, headless=False)

# --- MAIN LOOP ---
try:
    while True:
        captcha_count = 0
        total_checked = len(PRODUCT_URLS[:])

        for url in PRODUCT_URLS[:]:
            try:
                driver.get(url)
                time.sleep(random.uniform(2.5, 5.5))  # random delay

                if "captcha" in driver.page_source.lower() or "sorry, something went wrong" in driver.page_source.lower():
                    log(f"[⚠️] Captcha or error page detected: {url}")
                    captcha_count += 1
                    continue

                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.XPATH,
                        "//button[contains(., 'Add to Cart') or contains(., 'Buy Now') or contains(., 'הוסיפו לעגלה') or contains(., 'קנה עכשיו')]"
                    ))
                )

                log(f"[✅] Product in stock: {url}")
                send_telegram_alert(f"🎉 Product restocked!\n{url}")
                PRODUCT_URLS.remove(url)

            except TimeoutException:
                log(f"[⏳] Still out of stock: {url}")

        if captcha_count == total_checked:
            log("[🚨] All products blocked by CAPTCHA.")
            send_telegram_alert("🚨 All AliExpress product pages are blocked by CAPTCHA. Manual intervention may be needed!")

        log(f"[🔁] Waiting {CHECK_INTERVAL} seconds before next check...\n")
        time.sleep(CHECK_INTERVAL)

finally:
    driver.quit()
    log("[🔴] Bot stopped.")
