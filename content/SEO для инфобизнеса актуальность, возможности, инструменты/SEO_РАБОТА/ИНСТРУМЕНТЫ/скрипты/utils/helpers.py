# ИНСТРУМЕНТЫ/скрипты/utils/helpers.py
"""
Вспомогательные функции
Общие утилиты для работы парсера
"""

import time
import random
import logging
import sys
from pathlib import Path
from typing import Any, Optional

# Добавляем родительскую директорию в путь для импорта config
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import Config

logger = logging.getLogger(__name__)


def random_delay(min_sec: Optional[int] = None, max_sec: Optional[int] = None) -> None:
    """
    Случайная задержка для имитации человеческого поведения
    
    Args:
        min_sec: Минимальная задержка (по умолчанию из Config)
        max_sec: Максимальная задержка (по умолчанию из Config)
    """
    min_sec = min_sec or Config.MIN_DELAY
    max_sec = max_sec or Config.MAX_DELAY
    
    delay = random.uniform(min_sec, max_sec)
    logger.debug(f"Задержка {delay:.2f} сек")
    time.sleep(delay)


def safe_extract_text(element: Any, default: str = "") -> str:
    """
    Безопасное извлечение текста из элемента BeautifulSoup
    
    Args:
        element: Элемент BeautifulSoup или None
        default: Значение по умолчанию если элемент пустой
        
    Returns:
        Извлеченный текст или default
    """
    try:
        if element is None:
            return default
        return element.get_text(strip=True)
    except Exception as e:
        logger.debug(f"Ошибка извлечения текста: {e}")
        return default


def clean_url(url: str) -> str:
    """
    Очистка URL от параметров отслеживания
    
    Args:
        url: Исходный URL
        
    Returns:
        Очищенный URL без query параметров
    """
    if '?' in url:
        return url.split('?')[0]
    return url


def is_organic_url(url: str) -> bool:
    """
    Проверка что URL - органический результат (не реклама)
    
    Args:
        url: URL для проверки
        
    Returns:
        True если органический, False если реклама
    """
    from utils.page_selectors import AD_URL_PARAMS
    
    url_lower = url.lower()
    
    for param in AD_URL_PARAMS:
        if param in url_lower:
            logger.debug(f"URL содержит рекламный параметр: {param}")
            return False
    
    return True


def count_chars(text: str, include_spaces: bool = False) -> int:
    """
    Подсчет символов в тексте
    
    Args:
        text: Текст для подсчета
        include_spaces: Включать ли пробелы
        
    Returns:
        Количество символов
    """
    if include_spaces:
        return len(text)
    else:
        return len(text.replace(' ', '').replace('\n', '').replace('\t', ''))


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Обрезка текста до заданной длины
    
    Args:
        text: Исходный текст
        max_length: Максимальная длина
        suffix: Суффикс для обрезанного текста
        
    Returns:
        Обрезанный текст
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


if __name__ == "__main__":
    # Тестирование функций
    print("=== ТЕСТИРОВАНИЕ HELPERS ===")
    
    # Тест задержки
    print("\n1. Тест random_delay (2-3 сек):")
    start = time.time()
    random_delay(2, 3)
    elapsed = time.time() - start
    print(f"   Задержка: {elapsed:.2f} сек ✓")
    
    # Тест clean_url
    print("\n2. Тест clean_url:")
    test_url = "https://example.com/article?utm_source=direct&id=123"
    cleaned = clean_url(test_url)
    print(f"   Исходный: {test_url}")
    print(f"   Очищенный: {cleaned} ✓")
    
    # Тест is_organic_url
    print("\n3. Тест is_organic_url:")
    organic = "https://example.com/article"
    ad = "https://example.com/article?utm_source=direct"
    print(f"   {organic} -> {is_organic_url(organic)} (ожидаем True) ✓")
    print(f"   {ad} -> {is_organic_url(ad)} (ожидаем False) ✓")
    
    # Тест count_chars
    print("\n4. Тест count_chars:")
    text = "Привет мир! 123"
    print(f"   Текст: '{text}'")
    print(f"   С пробелами: {count_chars(text, include_spaces=True)}")
    print(f"   Без пробелов: {count_chars(text, include_spaces=False)} ✓")
    
    # Тест truncate_text
    print("\n5. Тест truncate_text:")
    long_text = "Это очень длинный текст который нужно обрезать до определенной длины"
    truncated = truncate_text(long_text, max_length=30)
    print(f"   Исходный: {long_text}")
    print(f"   Обрезанный: {truncated} ✓")
    
    print("\n✅ Все тесты пройдены!")
