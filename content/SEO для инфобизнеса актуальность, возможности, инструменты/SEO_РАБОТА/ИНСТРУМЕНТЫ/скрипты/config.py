# ИНСТРУМЕНТЫ/скрипты/config.py
"""
Конфигурация проекта
Загружает настройки из .env файла и определяет базовые пути
"""

from dotenv import load_dotenv
import os
from pathlib import Path

# Загрузка переменных окружения из .env
load_dotenv()

# === БАЗОВЫЕ ПУТИ ===
BASE_DIR = Path(__file__).parent
COOKIES_DIR = BASE_DIR / "cookies"
LOGS_DIR = BASE_DIR / "logs"

# Создание директорий если не существуют
COOKIES_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)


class Config:
    """Конфигурация приложения"""

    # === БРАУЗЕР ===
    HEADLESS = os.getenv("HEADLESS", "False") == "True"
    CHROME_PROFILE = os.getenv("CHROME_PROFILE", "")
    CHROME_PROFILE_NAME = os.getenv("CHROME_PROFILE_NAME", "Default")

    # === ЯНДЕКС ===
    YANDEX_COOKIES_PATH = COOKIES_DIR / os.getenv("YANDEX_COOKIES_PATH", "yandex.pkl")

    # === ЗАДЕРЖКИ (антибот) ===
    MIN_DELAY = int(os.getenv("MIN_DELAY", "2"))
    MAX_DELAY = int(os.getenv("MAX_DELAY", "5"))

    # === ЛОГИРОВАНИЕ ===
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = LOGS_DIR / "scraper.log"

    # === USER-AGENT ===
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

    # === API КЛЮЧИ (опционально) ===
    CAPTCHA_API_KEY = os.getenv("CAPTCHA_API_KEY", "")
    CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY", "")


# Для удобства импорта
config = Config()


if __name__ == "__main__":
    # Тестирование конфигурации
    print("=== КОНФИГУРАЦИЯ ПРОЕКТА ===")
    print(f"BASE_DIR: {BASE_DIR}")
    print(f"COOKIES_DIR: {COOKIES_DIR}")
    print(f"LOGS_DIR: {LOGS_DIR}")
    print(f"\nHEADLESS: {Config.HEADLESS}")
    print(f"CHROME_PROFILE: {Config.CHROME_PROFILE}")
    print(f"CHROME_PROFILE_NAME: {Config.CHROME_PROFILE_NAME}")
    print(f"YANDEX_COOKIES_PATH: {Config.YANDEX_COOKIES_PATH}")
    print(f"MIN_DELAY: {Config.MIN_DELAY}")
    print(f"MAX_DELAY: {Config.MAX_DELAY}")
    print(f"LOG_LEVEL: {Config.LOG_LEVEL}")
    print(f"LOG_FILE: {Config.LOG_FILE}")
