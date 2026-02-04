#!/usr/bin/env python3
"""
SEO Конкурентный анализ - Главный скрипт
Анализ ТОП-10 конкурентов из Яндекса
"""

import sys
from pathlib import Path
import logging
import argparse

sys.path.insert(0, str(Path(__file__).parent))

from utils.browser import init_driver
from parsers.yandex_parser import get_top_urls
from parsers.content_parser import parse_multiple
from parsers.simple_analyzer import analyze_competitors
from excel_exporter import export_to_excel

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger(__name__)


def print_header():
    """Вывод заголовка"""
    print("\n" + "=" * 70)
    print("  SEO АНАЛИЗ КОНКУРЕНТОВ - Яндекс")
    print("  Парсинг ТОП-10 → Анализ контента → Excel отчет")
    print("=" * 70)


def main():
    """Главная функция"""

    # Парсинг аргументов
    parser = argparse.ArgumentParser(
        description='Анализ конкурентов в Яндексе',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  python3 main.py "почему не худею"
  python3 main.py "как похудеть" --count 15
  python3 main.py "диета для похудения" --output results/
        """
    )

    parser.add_argument(
        'keyword',
        type=str,
        help='Ключевой запрос для анализа'
    )

    parser.add_argument(
        '-c', '--count',
        type=int,
        default=10,
        help='Количество конкурентов (по умолчанию: 10)'
    )

    parser.add_argument(
        '-o', '--output',
        type=str,
        default='output',
        help='Папка для сохранения (по умолчанию: output/)'
    )

    args = parser.parse_args()

    print_header()
    print(f"\n📍 Запрос: {args.keyword}")
    print(f"📊 ТОП: {args.count}")
    print(f"💾 Папка: {args.output}/\n")

    driver = None

    try:
        # ШАГ 1: Парсинг Яндекса
        print(f"[1/3] Парсинг ТОП-{args.count} из Яндекса...")
        print("-" * 70)

        driver = init_driver()
        urls = get_top_urls(driver, args.keyword, count=args.count)
        driver.quit()
        driver = None

        if not urls:
            print("\n❌ Не удалось получить URL из Яндекса")
            print("   Возможные причины:")
            print("   - CAPTCHA от Яндекса")
            print("   - Проблемы с сетью")
            print("   - Изменилась структура страницы")
            return 1

        print(f"\n✅ Получено {len(urls)} URL\n")

        # ШАГ 2: Парсинг контента
        print(f"[2/3] Парсинг контента ({len(urls)} страниц)...")
        print("-" * 70)

        results = parse_multiple(urls)

        success = sum(1 for r in results if r.get('success'))
        print(f"\n✅ Спарсено: {success}/{len(results)}\n")

        # ШАГ 3: Анализ
        print(f"[3/3] Анализ конкурентов...")
        print("-" * 70)

        analysis = analyze_competitors(results)

        if 'error' in analysis:
            print(f"\n❌ Ошибка анализа: {analysis['error']}")
            return 1

        # Краткая статистика
        print(f"\n📊 СТАТИСТИКА:")
        print(f"   Средний объем: {analysis['avg_chars']} символов")
        print(f"   Диапазон: {analysis['min_chars']} - {analysis['max_chars']}")
        print(f"   H2 всего: {analysis['h2_total']}")
        print(f"   H3 всего: {analysis['h3_total']}")

        if analysis.get('common_h2'):
            print(f"\n📝 ОБЩИЕ ТЕМЫ (3+ конкурентов):")
            for h in analysis['common_h2'][:5]:
                print(f"   [{h['count']}x] {h['text']}")

        # ШАГ 4: Экспорт
        print("\n" + "-" * 70)
        print("💾 Сохранение Excel отчета...")

        filename = export_to_excel(results, analysis, args.keyword, output_dir=args.output)

        print("\n" + "=" * 70)
        print(f"✅ ГОТОВО!")
        print(f"📄 Отчет: {filename}")
        print("=" * 70)

        return 0

    except KeyboardInterrupt:
        print("\n\n⚠️ Прервано пользователем")
        return 130

    except Exception as e:
        print(f"\n❌ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()
        return 1

    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    sys.exit(main())
