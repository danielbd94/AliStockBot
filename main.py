import os
import time
import requests
from dotenv import load_dotenv
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Load environment variables from .env
load_dotenv()

PRODUCT_URLS = [
    "LINK1",
    "LINK2",
    "LINK3"
]

CHECK_INTERVAL = 120  # seconds
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
PROFILE_PATH = os.getenv("CHROME_PROFILE_PATH", "C:/chrome_profile")  # fallback to default

def send_telegram_alert(url):
    message = f"🎉 Product restocked!\n{url}"
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        requests.post(telegram_url, data=payload)
        print(f"[TELEGRAM] Alert sent for: {url}")
    except Exception as e:
        print(f"[ERROR] Failed to send Telegram alert: {e}")

def main():
    print("🟢 Starting AliExpress stock checker bot...")

    options = uc.ChromeOptions()
    options.user_data_dir = PROFILE_PATH
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

    driver = uc.Chrome(options=options, headless=False)

    try:
        while True:
            for url in PRODUCT_URLS[:]:
                try:
                    driver.get(url)
                    WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.XPATH,
                            "//button[contains(., 'Add to Cart') or contains(., 'Buy Now') or contains(., 'הוסיפו לעגלה') or contains(., 'קנה עכשיו')]"
                        ))
                    )
                    print(f"[✅] Product in stock: {url}")
                    send_telegram_alert(url)
                    PRODUCT_URLS.remove(url)
                except TimeoutException:
                    print(f"[WAIT] Still out of stock: {url}")
                except Exception as e:
                    print(f"[ERROR] Failed to check {url}: {e}")
            time.sleep(CHECK_INTERVAL)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
