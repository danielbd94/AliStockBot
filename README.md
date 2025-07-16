# AliExpress Stock Checker Bot (Final Fix)

This version fixes the last compatibility issue with `selenium 4+`:
✅ No use of deprecated `desired_capabilities`

## Features

- Forces browser to English with `lang=en` and Accept-Language
- Clears cookies/localStorage to avoid language override
- Waits for "Add to Cart" or "Buy Now" button
- Sends Telegram alert when item is in stock

## Setup

1. Put ChromeDriver in:
   `C:/chromedriver/chromedriver.exe`

2. Install dependencies:

```bash
pip install selenium requests
```

3. Run:

```bash
python main.py
```

Telegram token and chat ID are pre-filled.
