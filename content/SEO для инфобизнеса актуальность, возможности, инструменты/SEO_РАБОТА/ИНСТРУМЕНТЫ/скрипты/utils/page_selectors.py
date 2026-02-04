# ИНСТРУМЕНТЫ/скрипты/utils/selectors.py
"""
CSS селекторы для парсинга
Содержит все селекторы для Яндекс поиска и парсинга статей
"""


class YandexSelectors:
    """CSS селекторы для Яндекс поиска (актуально на 2026)"""

    # === РЕЗУЛЬТАТЫ ПОИСКА ===
    SERP_ITEM = ".serp-item"  # Основной результат поиска
    SERP_ITEM_ALT = "[data-cid]"  # Альтернативный селектор (fallback)

    # === ССЫЛКИ РЕЗУЛЬТАТОВ ===
    RESULT_LINK = "a.link"  # Ссылка на страницу
    RESULT_LINK_ALT = ".organic__url"  # Альтернативная ссылка

    # === МАРКЕРЫ РЕКЛАМЫ (Яндекс.Директ) ===
    # КРИТИЧНО: Эти элементы нужно ПРОПУСКАТЬ!
    AD_MARKERS = [
        ".label_theme_direct",  # Метка "Реклама"
        ".serp-adv__item",  # Рекламный блок
        "[data-fast-name='direct']",  # React компонент Direct
        ".VanillaReact[data-fast-name='direct']",  # Новый формат
        ".serp-item_type_direct",  # Тип результата = реклама
        ".organic_type_direct",  # Органика с рекламой
    ]

    # === МАРКЕРЫ ВИДЕО ===
    # Видео тоже пропускаем (не релевантно для анализа статей)
    VIDEO_MARKERS = [
        ".serp-item_type_video",
        ".video-thumb",
        "[data-fast-name='video']",
    ]

    # === МАРКЕРЫ НОВОСТЕЙ ===
    NEWS_MARKERS = [
        ".serp-item_type_news",
        "[data-fast-name='news']",
    ]


class ArticleSelectors:
    """CSS селекторы для парсинга контента статей"""

    # === ЗАГОЛОВОК H1 ===
    # Множественные варианты для разных CMS
    TITLE_SELECTORS = [
        "h1",  # Стандартный
        ".title",  # Общий класс
        ".article-title",  # WordPress, Medium
        ".post-title",  # Блоги
        ".entry-title",  # WordPress
        "[itemprop='headline']",  # Schema.org разметка
        ".article__title",  # Новостные сайты
        ".content-title",  # CMS
    ]

    # === ПОДЗАГОЛОВКИ ===
    HEADINGS = ["h2", "h3"]  # H2 и H3 для структуры

    # === ТЕГИ ДЛЯ УДАЛЕНИЯ (мусор) ===
    UNWANTED_TAGS = [
        "script",  # JavaScript
        "style",  # CSS
        "nav",  # Навигация
        "footer",  # Футер
        "header",  # Шапка
        "aside",  # Сайдбар
        "iframe",  # Встроенные фреймы
        "noscript",  # NoScript блоки
        "svg",  # SVG графика
        "form",  # Формы
        "button",  # Кнопки
        "input",  # Поля ввода
        "select",  # Селекты
    ]

    # === КЛАССЫ ДЛЯ УДАЛЕНИЯ (реклама, комментарии) ===
    # Используется частичное совпадение (contains)
    UNWANTED_CLASS_KEYWORDS = [
        "ad",  # Реклама
        "advertisement",  # Реклама
        "banner",  # Баннеры
        "sidebar",  # Сайдбар
        "comment",  # Комментарии
        "related",  # Похожие статьи
        "social",  # Соцсети
        "share",  # Поделиться
        "popup",  # Попапы
        "modal",  # Модальные окна
        "promo",  # Промо блоки
    ]


# === ПАРАМЕТРЫ РЕКЛАМНЫХ URL ===
# Используется для дополнительной проверки
AD_URL_PARAMS = [
    "utm_source=direct",  # Яндекс.Директ
    "yclid=",  # Yandex Click ID
    "from=direct",  # Источник = Директ
    "ad_id=",  # ID рекламы
]


if __name__ == "__main__":
    # Тестирование селекторов
    print("=== ЯНДЕКС СЕЛЕКТОРЫ ===")
    print(f"Основной селектор результата: {YandexSelectors.SERP_ITEM}")
    print(f"Маркеры рекламы ({len(YandexSelectors.AD_MARKERS)}):")
    for marker in YandexSelectors.AD_MARKERS:
        print(f"  - {marker}")
    print(f"\nМаркеры видео ({len(YandexSelectors.VIDEO_MARKERS)}):")
    for marker in YandexSelectors.VIDEO_MARKERS:
        print(f"  - {marker}")

    print("\n=== СЕЛЕКТОРЫ СТАТЕЙ ===")
    print(f"Селекторы заголовков ({len(ArticleSelectors.TITLE_SELECTORS)}):")
    for selector in ArticleSelectors.TITLE_SELECTORS:
        print(f"  - {selector}")
    print(f"\nТеги для удаления ({len(ArticleSelectors.UNWANTED_TAGS)}):")
    for tag in ArticleSelectors.UNWANTED_TAGS:
        print(f"  - {tag}")
