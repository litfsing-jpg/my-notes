# parsers/yandex_parser.py
"""Парсинг результатов поиска Яндекса"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import sys
from pathlib import Path
from typing import List

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.helpers import random_delay

logger = logging.getLogger(__name__)


def get_search_url(keyword: str) -> str:
    """Формирование URL поиска"""
    import urllib.parse
    encoded = urllib.parse.quote_plus(keyword)
    return f"https://yandex.ru/search/?text={encoded}"


def get_top_urls(driver, keyword: str, count: int = 10) -> List[str]:
    """
    Получить ТОП-N органических URL (без рекламы)
    
    Args:
        driver: WebDriver
        keyword: Поисковый запрос
        count: Количество результатов
        
    Returns:
        Список URL
    """
    try:
        url = get_search_url(keyword)
        logger.info(f"Открытие: {url}")
        
        driver.get(url)
        random_delay(3, 5)
        
        # Ждем результаты
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".serp-item, .VanillaReact")))
        
        # Все результаты
        results = driver.find_elements(By.CSS_SELECTOR, ".serp-item, .VanillaReact")
        
        urls = []
        seen = set()  # Для фильтрации дублей

        for result in results:
            try:
                # Проверка рекламы
                if is_ad(result):
                    continue

                # Извлечение ссылки
                link = result.find_element(By.TAG_NAME, "a")
                href = link.get_attribute("href")

                if href and href.startswith("http") and "yandex" not in href:
                    # Фильтрация дублей
                    if href not in seen:
                        urls.append(href)
                        seen.add(href)
                        logger.info(f"[{len(urls)}] {href}")

                if len(urls) >= count:
                    break

            except:
                continue
        
        logger.info(f"✅ Найдено {len(urls)} URL")
        return urls
        
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")
        return []


def is_ad(element) -> bool:
    """Проверка что элемент - реклама"""
    try:
        # Проверка по классам
        classes = element.get_attribute("class") or ""
        ad_markers = ["direct", "ad", "adv", "serp-adv"]
        
        for marker in ad_markers:
            if marker in classes.lower():
                return True
        
        # Проверка по тексту "Реклама"
        text = element.text.lower()
        if "реклама" in text or "спонсор" in text:
            return True
        
        return False
        
    except:
        return False


if __name__ == "__main__":
    print("=== ТЕСТ YANDEX_PARSER ===\n")
    
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    from utils.browser import init_driver
    
    try:
        print("1. Запуск браузера...")
        driver = init_driver()
        
        print("\n2. Парсинг ТОП-10 по запросу 'Python'...")
        urls = get_top_urls(driver, "Python", count=10)
        
        print(f"\n3. Результат ({len(urls)} URL):")
        for i, url in enumerate(urls, 1):
            print(f"   {i}. {url}")
        
        driver.quit()
        print("\n✅ ТЕСТ ПРОЙДЕН")
        
    except Exception as e:
        print(f"❌ {e}")
        import traceback
        traceback.print_exc()
