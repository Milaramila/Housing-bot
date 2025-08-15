# bot.py — фоновый воркер: два отчёта в день (07:00, 19:00)
import time
from datetime import datetime, timedelta
import telebot

from scraper import fetch_listings
from config import TELEGRAM_TOKEN, CHAT_ID, TZ, SCHEDULE_TIMES

bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode="HTML")
seen = set()  # простая защита от дублей за текущий запуск

def next_run_after(now):
    """Вернёт datetime ближайшего запуска согласно SCHEDULE_TIMES в TZ."""
    today = now.date()
    times_today = []
    for t in SCHEDULE_TIMES:
        h, m = map(int, t.split(":"))
        dt = datetime(now.year, now.month, now.day, h, m, tzinfo=TZ)
        times_today.append(dt)
    later = [dt for dt in times_today if dt > now]
    if later:
        return min(later)
    # иначе — первый слот завтрашнего дня
    h, m = map(int, SCHEDULE_TIMES[0].split(":"))
    return datetime(now.year, now.month, now.day, h, m, tzinfo=TZ) + timedelta(days=1)

def notify():
    ads = fetch_listings()
    new_lines, new_count = [], 0
    for ad in ads:
        key = ad.get("link") or ad.get("title")
        if key and key not in seen:
            seen.add(key)
            new_count += 1
            t = ad.get("title", "Без названия")
            l = ad.get("link", "")
            if l:
                new_lines.append(f"• <a href=\"{l}\">{t}</a>")
            else:
                new_lines.append(f"• {t}")
    now_str = datetime.now(TZ).strftime("%Y-%m-%d %H:%M")
    if new_count:
        text = f"📝 Отчёт {now_str}. Новые объявления: {new_count}\n" + "\n".join(new_lines[:30])
    else:
        text = f"📝 Отчёт {now_str}. Новых объявлений нет (нашёл всего на странице: {len(ads)})."
    bot.send_message(CHAT_ID, text, disable_web_page_preview=True)

if __name__ == "__main__":
    print("Worker started")
    while True:
        now = datetime.now(TZ)
        nxt = next_run_after(now)
        wait = max(1, int((nxt - now).total_seconds()))
        print(f"Сейчас {now}, следующий запуск {nxt}, сплю {wait} сек")
        time.sleep(wait)
        try:
            notify()
        except Exception as e:
            print("Ошибка в notify:", e)
            try:
                bot.send_message(CHAT_ID, f"⚠️ Ошибка бота: {e}")
            except Exception:
                pass
            time.sleep(5)
