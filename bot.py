# bot.py
# Телеграм-бот, который шлет уведомления, когда scraper.py находит новые объявления

import time
import telebot
from scraper import fetch_listings
from config import TELEGRAM_TOKEN, CHAT_ID, CHECK_INTERVAL

bot = telebot.TeleBot(TELEGRAM_TOKEN)

seen_ads = set()  # чтобы не присылать одно и то же дважды

def notify_new_ads():
    ads = fetch_listings()
    for ad in ads:
        if ad["title"] not in seen_ads:
            seen_ads.add(ad["title"])
            message = f"Новое объявление: {ad['title']}\n{ad['link']}"
            bot.send_message(CHAT_ID, message)

if __name__ == "__main__":
    print("Бот запущен. Проверяю сайт каждые", CHECK_INTERVAL, "секунд.")
    while True:
        try:
            notify_new_ads()
        except Exception as e:
            print("Ошибка:", e)
        time.sleep(CHECK_INTERVAL)
