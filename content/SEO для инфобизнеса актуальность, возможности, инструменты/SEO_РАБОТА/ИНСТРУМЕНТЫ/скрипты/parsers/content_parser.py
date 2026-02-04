# parsers/content_parser.py
"""Парсинг контента страниц (H1, H2, H3)"""

import requests
from bs4 import BeautifulSoup
import logging
import sys
from pathlib import Path
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import Config
from utils.helpers import count_chars, random_delay

logger = logging.getLogger(__name__)


def parse_page(url: str, use_selenium: bool = False) -> Optional[Dict]:
    """
    Парсинг контента страницы

    Args:
        url: URL страницы
        use_selenium: Использовать Selenium (для Cloudflare)

    Returns:
        dict с данными или None
    """
    try:
        logger.info(f"Парсинг: {url}")

        # Попытка через requests (быстро)
        if not use_selenium:
            html = fetch_with_requests(url)
            if not html:
                logger.warning("Fallback на Selenium")
                return parse_page(url, use_selenium=True)
        else:
            html = fetch_with_selenium(url)
            if not html:
                return None

        # Парсинг HTML
        soup = BeautifulSoup(html, 'html.parser')
        soup = clean_html(soup)

        # Извлечение контента
        result = {
            'url': url,
            'h1': extract_title(soup),
            'h2': extract_headings(soup, 'h2'),
            'h3': extract_headings(soup, 'h3'),
            'chars': count_text(soup),
            'success': True
        }

        logger.info(f"✅ H1: {result['h1'][:50]}... | H2: {len(result['h2'])} | H3: {len(result['h3'])} | Символов: {result['chars']}")
        return result

    except Exception as e:
        logger.error(f"❌ {url}: {e}")
        return {
            'url': url,
            'h1': 'ОШИБКА',
            'h2': [],
            'h3': [],
            'chars': 0,
            'success': False,
            'error': str(e)
        }


def fetch_with_requests(url: str) -> Optional[str]:
    """Получить HTML через requests"""
    try:
        headers = {
            'User-Agent': Config.USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.9',
            'Referer': 'https://yandex.ru/'
        }

        response = requests.get(url, headers=headers, timeout=15)

        # Проверка Cloudflare
        if response.status_code == 403 or 'cf-browser-verification' in response.text:
            logger.warning("Cloudflare обнаружен")
            return None

        response.raise_for_status()
        return response.text

    except requests.RequestException as e:
        logger.debug(f"Requests ошибка: {e}")
        return None


def fetch_with_selenium(url: str) -> Optional[str]:
    """Получить HTML через Selenium (fallback)"""
    try:
        from utils.browser import init_driver

        driver = init_driver(headless=True)
        driver.get(url)
        random_delay(2, 3)

        html = driver.page_source
        driver.quit()

        return html

    except Exception as e:
        logger.error(f"Selenium ошибка: {e}")
        return None


def clean_html(soup):
    """Удалить мусорные элементы"""
    # Удалить теги
    unwanted_tags = [
        'script', 'style', 'nav', 'footer', 'header',
        'aside', 'iframe', 'noscript', 'svg', 'form'
    ]
    for tag in soup(unwanted_tags):
        tag.decompose()

    # Удалить по классам
    unwanted = [
        '[class*="ad"]', '[class*="banner"]', '[class*="sidebar"]',
        '[class*="comment"]', '[id*="comments"]'
    ]
    for selector in unwanted:
        for elem in soup.select(selector):
            elem.decompose()

    return soup


def extract_title(soup) -> str:
    """Извлечь H1 с fallback"""
    # H1
    h1 = soup.find('h1')
    if h1:
        return h1.get_text(strip=True)

    # Частые классы
    selectors = [
        '.title', '.article-title', '.post-title',
        '.entry-title', '[itemprop="headline"]'
    ]
    for sel in selectors:
        elem = soup.select_one(sel)
        if elem:
            return elem.get_text(strip=True)

    # Title как последняя надежда
    title = soup.find('title')
    if title:
        return title.get_text(strip=True).split('|')[0].strip()

    return "Заголовок не найден"


def extract_headings(soup, tag: str) -> List[str]:
    """Извлечь подзаголовки (H2 или H3)"""
    try:
        headings = soup.find_all(tag)
        return [h.get_text(strip=True) for h in headings if h.get_text(strip=True)]
    except:
        return []


def count_text(soup) -> int:
    """Подсчет символов без пробелов"""
    try:
        # Ищем основной контент
        main_selectors = [
            'article', 'main', '.content', '.post-content',
            '.article-content', '[role="main"]'
        ]

        content = None
        for sel in main_selectors:
            content = soup.select_one(sel)
            if content:
                break

        # Если не нашли main, берем весь body
        if not content:
            content = soup.find('body')

        if content:
            text = content.get_text(separator=' ', strip=True)
            return count_chars(text, include_spaces=False)

        return 0

    except:
        return 0


def parse_multiple(urls: List[str]) -> List[Dict]:
    """
    Парсинг нескольких страниц

    Args:
        urls: Список URL

    Returns:
        Список результатов
    """
    results = []

    for i, url in enumerate(urls, 1):
        logger.info(f"\n[{i}/{len(urls)}] Парсинг...")
        result = parse_page(url)

        if result:
            results.append(result)

        # Задержка между страницами
        if i < len(urls):
            random_delay(2, 4)

    return results


if __name__ == "__main__":
    print("=== ТЕСТ CONTENT_PARSER ===\n")

    logging.basicConfig(level=logging.INFO, format='%(message)s')

    # Тест на простом сайте
    test_url = "https://habr.com/ru/articles/"

    print("1. Тест парсинга одной страницы...")
    result = parse_page(test_url)

    if result and result['success']:
        print(f"\n✅ Результат:")
        print(f"   H1: {result['h1']}")
        print(f"   H2: {len(result['h2'])} подзаголовков")
        print(f"   H3: {len(result['h3'])} подзаголовков")
        print(f"   Символов: {result['chars']}")
    else:
        print(f"\n❌ Ошибка парсинга")

    print("\n✅ ТЕСТ ЗАВЕРШЕН")
