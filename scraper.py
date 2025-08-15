# scraper.py
# Модуль, который будет забирать данные с сайта

import requests
from bs4 import BeautifulSoup
from config import TARGET_URL, FILTER_KEYWORDS

def fetch_listings():
    """
    Загружает HTML-страницу и вытаскивает объявления.
    Возвращает список словарей с найденными данными.
    """
    response = requests.get(TARGET_URL)
    response.raise_for_status()  # если ошибка — выбросит исключение

    soup = BeautifulSoup(response.text, "html.parser")

    # Пример: находим все элементы <div class="listing">
    items = soup.find_all("div", class_="listing")

    results = []
    for item in items:
        title = item.get_text(strip=True)
        link = item.find("a")["href"] if item.find("a") else None

        # Фильтруем по ключевым словам (если заданы)
        if any(keyword.lower() in title.lower() for keyword in FILTER_KEYWORDS):
            results.append({"title": title, "link": link})

    return results


# Для проверки локально:
if __name__ == "__main__":
    ads = fetch_listings()
    for ad in ads:
        print(ad)
