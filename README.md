# 🛍️ AliExpress Stock Checker Bot

This bot automatically checks a list of AliExpress product pages and sends a Telegram alert when an item comes back in stock.

## 🚀 Features

- Monitors multiple product URLs.
- Sends Telegram alerts when "Add to Cart" or "Buy Now" buttons appear.
- Supports both English and Hebrew button labels.
- Avoids bot detection using `undetected-chromedriver`.

## 🛠️ Requirements

- Python 3.8+
- Google Chrome installed
- Chrome profile path (for persistent login session)

## 📦 Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/aliexpress-stock-checker.git
   cd aliexpress-stock-checker
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file:
   ```ini
   TELEGRAM_TOKEN=your_telegram_bot_token
   TELEGRAM_CHAT_ID=your_chat_id
   CHROME_PROFILE_PATH=C:/chrome_profile
   ```

4. Run the bot:
   ```bash
   python main.py
   ```

## ⚠️ Notes

- Make sure you're logged into AliExpress with the Chrome profile you specified.
- Do **not** share your `.env` file publicly.
- To obtain your `chat_id`, you can message your bot and use `https://api.telegram.org/bot<token>/getUpdates`.

## 📄 License

MIT License
