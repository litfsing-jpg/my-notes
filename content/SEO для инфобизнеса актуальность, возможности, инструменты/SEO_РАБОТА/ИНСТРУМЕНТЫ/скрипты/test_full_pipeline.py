#!/usr/bin/env python3
"""Полный тест: Яндекс → Парсинг контента"""

import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from utils.browser import init_driver
from parsers.yandex_parser import get_top_urls
from parsers.content_parser import parse_multiple
from parsers.simple_analyzer import analyze_competitors, generate_article_plan
from excel_exporter import export_to_excel

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def main():
    keyword = "почему не худею"
    top_n = 5  # Меньше для теста

    print("=" * 60)
    print(f"ТЕСТ: Анализ конкурентов по запросу '{keyword}'")
    print("=" * 60)

    driver = None

    try:
        # Этап 1: Парсинг Яндекса
        print(f"\n[1/3] Парсинг ТОП-{top_n} из Яндекса...")
        print("-" * 60)

        driver = init_driver()
        urls = get_top_urls(driver, keyword, count=top_n)
        driver.quit()
        driver = None

        if not urls:
            print("\n❌ Не удалось получить URL из Яндекса")
            return

        print(f"\n✅ Получено {len(urls)} URL:\n")
        for i, url in enumerate(urls, 1):
            print(f"   {i}. {url}")

        # Этап 2: Парсинг контента
        print(f"\n[2/3] Парсинг контента страниц...")
        print("-" * 60)

        results = parse_multiple(urls)

        # Вывод результатов
        print("\n" + "=" * 60)
        print("РЕЗУЛЬТАТЫ")
        print("=" * 60)

        for i, r in enumerate(results, 1):
            status = "✅" if r['success'] else "❌"
            print(f"\n{status} [{i}] {r['url']}")
            print(f"   H1: {r['h1'][:70]}")
            print(f"   H2: {len(r['h2'])} шт | H3: {len(r['h3'])} шт | Символов: {r['chars']}")

            if r['h2']:
                print(f"   Примеры H2:")
                for h2 in r['h2'][:3]:
                    print(f"      - {h2[:60]}")

        # Этап 3: Анализ
        print(f"\n[3/3] Анализ конкурентов...")
        print("-" * 60)

        analysis = analyze_competitors(results)

        if 'error' in analysis:
            print(f"\n❌ Ошибка анализа: {analysis['error']}")
        else:
            print("\n" + "=" * 60)
            print("АНАЛИЗ")
            print("=" * 60)
            print(f"Успешно: {analysis['success_count']}/{analysis['total']}")
            print(f"Средний объем: {analysis['avg_chars']} символов")
            print(f"Диапазон: {analysis['min_chars']} - {analysis['max_chars']}")
            print(f"H2 всего: {analysis['h2_total']}")
            print(f"H3 всего: {analysis['h3_total']}")

            if analysis['common_h2']:
                print(f"\nОбщие подзаголовки H2 (встречаются у 3+ конкурентов):")
                for h in analysis['common_h2'][:5]:
                    print(f"   [{h['count']}x] {h['text']}")
            else:
                print(f"\n⚠️ Общих подзаголовков не найдено (H2 редко используются)")

            # План статьи
            print("\n" + "=" * 60)
            print("РЕКОМЕНДАЦИИ")
            print("=" * 60)

            plan = generate_article_plan(analysis, keyword)
            print(f"Объем статьи: ~{plan['recommended_length']} символов")
            print(f"Структура:")
            for item in plan['structure'][:7]:
                level = item['level'].upper()
                freq = f" [{item.get('frequency')}x]" if item.get('frequency') else ""
                print(f"   {level}: {item['text']}{freq}")

            # Экспорт в Excel
            print("\n" + "=" * 60)
            print("ЭКСПОРТ")
            print("=" * 60)

            try:
                filename = export_to_excel(results, analysis, keyword)
                print(f"✅ Результаты сохранены: {filename}")
            except Exception as e:
                print(f"❌ Ошибка экспорта: {e}")

        print(f"\n✅ ТЕСТ ЗАВЕРШЕН")

    except KeyboardInterrupt:
        print("\n⚠️ Прервано пользователем")

    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()

    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    main()
