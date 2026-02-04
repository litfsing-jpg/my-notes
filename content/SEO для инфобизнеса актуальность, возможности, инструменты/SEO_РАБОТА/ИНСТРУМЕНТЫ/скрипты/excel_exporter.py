# excel_exporter.py
"""Экспорт результатов в Excel"""

import pandas as pd
from datetime import datetime
from typing import Dict, List
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def export_to_excel(results: List[Dict], analysis: Dict, keyword: str, output_dir: str = "output") -> str:
    """
    Экспорт результатов в Excel

    Args:
        results: Результаты парсинга
        analysis: Результаты анализа
        keyword: Ключевой запрос
        output_dir: Папка для сохранения

    Returns:
        Путь к созданному файлу
    """
    try:
        # Создать папку output
        Path(output_dir).mkdir(exist_ok=True)

        # Имя файла
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_keyword = keyword.replace(" ", "_")[:30]
        filename = f"{output_dir}/competitors_{safe_keyword}_{timestamp}.xlsx"

        # Создать Excel с 2 листами
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Лист 1: Конкуренты
            df_competitors = create_competitors_sheet(results)
            df_competitors.to_excel(writer, sheet_name='Конкуренты', index=False)

            # Лист 2: Анализ
            df_analysis = create_analysis_sheet(analysis, keyword)
            df_analysis.to_excel(writer, sheet_name='Анализ', index=False)

        logger.info(f"✅ Экспортировано в: {filename}")
        return filename

    except Exception as e:
        logger.error(f"❌ Ошибка экспорта: {e}")
        raise


def create_competitors_sheet(results: List[Dict]) -> pd.DataFrame:
    """Создать лист с данными конкурентов"""
    data = []

    for i, r in enumerate(results, 1):
        # Объединить H2/H3 в строки
        h2_str = "\n".join(r.get('h2', [])[:10]) if r.get('h2') else "-"
        h3_str = "\n".join(r.get('h3', [])[:15]) if r.get('h3') else "-"

        data.append({
            '№': i,
            'URL': r['url'],
            'H1': r.get('h1', '-'),
            'Кол-во H2': len(r.get('h2', [])),
            'H2 (первые 10)': h2_str,
            'Кол-во H3': len(r.get('h3', [])),
            'H3 (первые 15)': h3_str,
            'Символов (без пробелов)': r.get('chars', 0),
            'Статус': '✅ OK' if r.get('success') else f"❌ {r.get('error', 'Ошибка')}"
        })

    df = pd.DataFrame(data)

    return df


def create_analysis_sheet(analysis: Dict, keyword: str) -> pd.DataFrame:
    """Создать лист с анализом"""
    if 'error' in analysis:
        return pd.DataFrame([{'Ошибка': analysis['error']}])

    data = []

    # Общая информация
    data.append({'Параметр': 'Ключевой запрос', 'Значение': keyword})
    data.append({'Параметр': 'Дата анализа', 'Значение': datetime.now().strftime("%Y-%m-%d %H:%M")})
    data.append({'Параметр': '', 'Значение': ''})

    # Статистика
    data.append({'Параметр': 'СТАТИСТИКА', 'Значение': ''})
    data.append({'Параметр': 'Всего проанализировано', 'Значение': analysis['total']})
    data.append({'Параметр': 'Успешно спарсено', 'Значение': analysis['success_count']})
    data.append({'Параметр': '', 'Значение': ''})

    # Объем
    data.append({'Параметр': 'ОБЪЕМ СТАТЕЙ', 'Значение': ''})
    data.append({'Параметр': 'Средний объем', 'Значение': f"{analysis['avg_chars']} символов"})
    data.append({'Параметр': 'Минимум', 'Значение': f"{analysis['min_chars']} символов"})
    data.append({'Параметр': 'Максимум', 'Значение': f"{analysis['max_chars']} символов"})
    data.append({'Параметр': '', 'Значение': ''})

    # Подзаголовки
    data.append({'Параметр': 'ПОДЗАГОЛОВКИ', 'Значение': ''})
    data.append({'Параметр': 'H2 всего', 'Значение': analysis['h2_total']})
    data.append({'Параметр': 'H3 всего', 'Значение': analysis['h3_total']})
    data.append({'Параметр': '', 'Значение': ''})

    # Общие H2
    if analysis.get('common_h2'):
        data.append({'Параметр': 'ОБЩИЕ ПОДЗАГОЛОВКИ H2', 'Значение': '(встречаются у 3+ конкурентов)'})
        for h in analysis['common_h2'][:10]:
            data.append({'Параметр': f"[{h['count']}x]", 'Значение': h['text']})
    else:
        data.append({'Параметр': 'ОБЩИЕ ПОДЗАГОЛОВКИ H2', 'Значение': 'Не найдено (используются редко)'})

    data.append({'Параметр': '', 'Значение': ''})

    # Рекомендации
    data.append({'Параметр': 'РЕКОМЕНДАЦИИ', 'Значение': ''})
    data.append({'Параметр': 'Рекомендуемый объем', 'Значение': f"{analysis['avg_chars']} символов"})
    data.append({'Параметр': 'Заголовок H1', 'Значение': keyword.capitalize()})

    if analysis.get('common_h2'):
        data.append({'Параметр': 'Включить подзаголовки', 'Значение': ', '.join([h['text'] for h in analysis['common_h2'][:3]])})
    else:
        data.append({'Параметр': 'Включить подзаголовки', 'Значение': 'Создайте уникальные на основе конкурентов'})

    df = pd.DataFrame(data)

    return df


if __name__ == "__main__":
    print("=== ТЕСТ EXCEL_EXPORTER ===\n")

    logging.basicConfig(level=logging.INFO, format='%(message)s')

    # Моковые данные
    test_results = [
        {
            'url': 'https://example1.com',
            'h1': 'Почему не худею: основные причины',
            'h2': ['Проблемы с гормонами', 'Недостаток сна', 'Стресс'],
            'h3': ['Щитовидная железа', 'Кортизол', 'Инсулин'],
            'chars': 5000,
            'success': True
        },
        {
            'url': 'https://example2.com',
            'h1': 'Причины отсутствия похудения',
            'h2': ['Гормональные нарушения', 'Плохой сон'],
            'h3': [],
            'chars': 6000,
            'success': True
        }
    ]

    test_analysis = {
        'total': 2,
        'success_count': 2,
        'avg_chars': 5500,
        'min_chars': 5000,
        'max_chars': 6000,
        'h2_total': 5,
        'h3_total': 3,
        'common_h2': [
            {'text': 'Проблемы с гормонами', 'count': 2, 'variants': 2}
        ],
        'common_h3': []
    }

    print("1. Создание Excel файла...")
    filename = export_to_excel(test_results, test_analysis, "почему не худею", output_dir="output")

    print(f"\n✅ Файл создан: {filename}")
    print(f"   Листы: 'Конкуренты', 'Анализ'")
    print("\n✅ ТЕСТ ЗАВЕРШЕН")
