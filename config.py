# config.py — безопасные настройки через переменные окружения
import os
from zoneinfo import ZoneInfo

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID        = os.getenv("CHAT_ID")          # может быть "-100..." если канал/группа
TARGET_URL     = os.getenv("TARGET_URL", "https://example.com")

# Часовой пояс Ибицы
TZ = ZoneInfo("Europe/Madrid")

# Когда слать отчёты (локальное время TZ)
SCHEDULE_TIMES = ["07:00", "19:00"]
