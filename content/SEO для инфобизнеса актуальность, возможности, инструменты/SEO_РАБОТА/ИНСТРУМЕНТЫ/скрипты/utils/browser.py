# ИНСТРУМЕНТЫ/скрипты/utils/browser.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pickle
import logging
import sys
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import Config

logger = logging.getLogger(__name__)


def init_driver(headless: bool = False) -> webdriver.Chrome:
    """Простая инициализация Chrome"""
    try:
        logger.info("Инициализация Chrome...")
        
        options = Options()
        
        if headless or Config.HEADLESS:
            options.add_argument("--headless=new")
        
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        options.add_argument("--start-maximized")
        options.add_argument(f"user-agent={Config.USER_AGENT}")
        
        # Простое создание драйвера (Selenium сам найдет ChromeDriver)
        driver = webdriver.Chrome(options=options)
        
        # Скрытие автоматизации
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        logger.info("✅ Chrome запущен")
        return driver
        
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")
        raise


def save_cookies(driver, filepath: Optional[Path] = None) -> bool:
    """Сохранить cookies"""
    filepath = filepath or Config.YANDEX_COOKIES_PATH
    try:
        with open(filepath, 'wb') as f:
            pickle.dump(driver.get_cookies(), f)
        logger.info("✅ Cookies сохранены")
        return True
    except Exception as e:
        logger.error(f"❌ {e}")
        return False


def load_cookies(driver, filepath: Optional[Path] = None) -> bool:
    """Загрузить cookies"""
    filepath = filepath or Config.YANDEX_COOKIES_PATH
    try:
        if not Path(filepath).exists():
            return False
        
        driver.get("https://yandex.ru")
        with open(filepath, 'rb') as f:
            for cookie in pickle.load(f):
                if 'expiry' in cookie:
                    del cookie['expiry']
                try:
                    driver.add_cookie(cookie)
                except:
                    pass
        driver.refresh()
        logger.info("✅ Cookies загружены")
        return True
    except Exception as e:
        logger.error(f"❌ {e}")
        return False


if __name__ == "__main__":
    print("=== ТЕСТ ===\n")
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    try:
        print("1. Запуск Chrome...")
        driver = init_driver()
        
        print("2. Открытие Яндекса...")
        driver.get("https://yandex.ru")
        
        import time
        time.sleep(3)
        
        print(f"\n3. Заголовок: {driver.title}")
        print(f"   URL: {driver.current_url}")
        
        if "Яндекс" in driver.title:
            print("   ✅ РАБОТАЕТ")
        else:
            print("   ⚠️ CAPTCHA или редирект")
        
        driver.quit()
        print("\n✅ ТЕСТ ПРОЙДЕН")
        
    except Exception as e:
        print(f"❌ {e}")
