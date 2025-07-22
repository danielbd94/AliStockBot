# 🛍️ AliExpress Stock Checker Bot

This Python bot automatically checks a list of AliExpress product pages and sends a Telegram alert when:
- An item comes back in stock (Buy/Add to Cart detected)
- **All product pages are blocked by CAPTCHA** (manual intervention likely needed)

---

## 🚀 Features

- ✅ Monitors multiple product URLs continuously  
- 📦 Sends Telegram alerts when "Add to Cart" or "Buy Now" buttons appear  
- 🌐 Supports both English and Hebrew button labels  
- 🧠 Avoids bot detection using `undetected-chromedriver`  
- 🔁 Retries checks every few minutes (configurable)  
- 🔔 Sends alert if **all products are blocked by CAPTCHA**  
- 🗂 Logs all events to a file  

---

## 🛠️ Requirements

- Python 3.8+
- Google Chrome browser
- A valid Telegram bot token and chat ID
- Chrome profile path with saved login to AliExpress

---

## 📦 Installation

### 1. Clone the Repo

```bash
git clone https://github.com/danielbd94/AliStockBot.git
cd AliStockBot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Create a `.env` File

Create a `.env` file in the root folder and add:

```ini
TELEGRAM_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id
CHROME_PROFILE_PATH=C:/chrome_profile
```

💡 Make sure the specified Chrome profile has logged into AliExpress at least once.

---

## ▶️ Usage

Run the bot with:

```bash
python main.py
```

You’ll receive a Telegram message when:
- A product is restocked (Buy/Add button appears)
- All product pages return a CAPTCHA or error page

The script runs in a loop with a configurable delay (`CHECK_INTERVAL`).

---

## 🧪 How to Get Your Telegram Chat ID

1. Start a chat with your bot on Telegram.  
2. Visit the following in your browser (replace `<TOKEN>` with your bot token):

```
https://api.telegram.org/bot<TOKEN>/getUpdates
```

3. Look for the `"chat":{"id":12345678}` section — that’s your `TELEGRAM_CHAT_ID`.

---

## 📁 File Structure

```
aliexpress-stock-checker/
├── main.py              # Bot script
├── requirements.txt     # Python packages
├── .env                 # Your credentials (DO NOT SHARE)
└── README.md            # This file
```

---

## ⚠️ Notes

- The `.env` file must remain private and never be committed to GitHub.  
- If CAPTCHA blocks become frequent, consider rotating your IP or using different Chrome sessions.  
- The script uses a persistent Chrome profile to bypass login issues.

---

## 📄 License

MIT License
