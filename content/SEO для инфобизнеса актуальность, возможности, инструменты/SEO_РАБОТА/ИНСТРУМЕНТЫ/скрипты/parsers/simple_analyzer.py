# parsers/simple_analyzer.py
"""Анализ спарсенных данных конкурентов"""

import logging
from typing import Dict, List
from collections import Counter
from difflib import SequenceMatcher

logger = logging.getLogger(__name__)


def analyze_competitors(results: List[Dict]) -> Dict:
    """
    Анализ данных конкурентов

    Args:
        results: Список результатов парсинга

    Returns:
        dict с аналитикой
    """
    try:
        # Фильтр успешных
        success = [r for r in results if r.get('success', False)]

        if not success:
            return {
                'error': 'Нет успешных результатов',
                'total': len(results),
                'success_count': 0
            }

        # Базовая статистика
        chars = [r['chars'] for r in success if r['chars'] > 0]
        avg_chars = sum(chars) / len(chars) if chars else 0

        # Все подзаголовки
        all_h2 = []
        all_h3 = []
        for r in success:
            all_h2.extend(r.get('h2', []))
            all_h3.extend(r.get('h3', []))

        # Общие подзаголовки (встречаются у 3+ конкурентов)
        common_h2 = find_common_headings(all_h2, min_count=3)
        common_h3 = find_common_headings(all_h3, min_count=3)

        analysis = {
            'total': len(results),
            'success_count': len(success),
            'avg_chars': int(avg_chars),
            'min_chars': min(chars) if chars else 0,
            'max_chars': max(chars) if chars else 0,
            'h2_total': len(all_h2),
            'h3_total': len(all_h3),
            'common_h2': common_h2,
            'common_h3': common_h3,
            'top_urls': [r['url'] for r in success[:5]]
        }

        logger.info(f"✅ Анализ: {len(success)} страниц, средний объем {int(avg_chars)} символов")

        return analysis

    except Exception as e:
        logger.error(f"❌ Ошибка анализа: {e}")
        return {'error': str(e)}


def find_common_headings(headings: List[str], min_count: int = 3, similarity: float = 0.7) -> List[Dict]:
    """
    Найти часто встречающиеся подзаголовки с учетом схожести

    Args:
        headings: Список всех подзаголовков
        min_count: Минимальное количество повторений
        similarity: Порог схожести (0-1)

    Returns:
        Список общих подзаголовков с количеством
    """
    if not headings:
        return []

    # Кластеризация схожих заголовков
    clusters = []

    for heading in headings:
        # Игнорировать короткие/мусорные
        if len(heading) < 5 or len(heading) > 100:
            continue

        # Найти подходящий кластер
        found = False
        for cluster in clusters:
            if are_similar(heading, cluster[0], similarity):
                cluster.append(heading)
                found = True
                break

        if not found:
            clusters.append([heading])

    # Фильтр по min_count
    common = []
    for cluster in clusters:
        if len(cluster) >= min_count:
            # Самый частый вариант как представитель
            most_common = Counter(cluster).most_common(1)[0][0]
            common.append({
                'text': most_common,
                'count': len(cluster),
                'variants': len(set(cluster))
            })

    # Сортировка по частоте
    common.sort(key=lambda x: x['count'], reverse=True)

    return common


def are_similar(a: str, b: str, threshold: float = 0.7) -> bool:
    """Проверка схожести двух строк"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio() >= threshold


def generate_article_plan(analysis: Dict, keyword: str) -> Dict:
    """
    Генерация базового плана статьи

    Args:
        analysis: Результат анализа
        keyword: Ключевой запрос

    Returns:
        dict с планом
    """
    try:
        plan = {
            'keyword': keyword,
            'recommended_length': analysis['avg_chars'],
            'structure': []
        }

        # H1
        plan['structure'].append({
            'level': 'h1',
            'text': keyword.capitalize()
        })

        # Общие H2
        if analysis.get('common_h2'):
            for h2 in analysis['common_h2'][:5]:
                plan['structure'].append({
                    'level': 'h2',
                    'text': h2['text'],
                    'frequency': h2['count']
                })

        # Если нет общих - рекомендации
        if not analysis.get('common_h2'):
            plan['structure'].append({
                'level': 'h2',
                'text': '(Добавьте уникальные подзаголовки)'
            })

        return plan

    except Exception as e:
        logger.error(f"❌ Ошибка генерации плана: {e}")
        return {'error': str(e)}


if __name__ == "__main__":
    print("=== ТЕСТ SIMPLE_ANALYZER ===\n")

    logging.basicConfig(level=logging.INFO, format='%(message)s')

    # Тестовые данные (симуляция парсинга)
    test_results = [
        {
            'url': 'example1.com',
            'h1': 'Заголовок 1',
            'h2': ['Причины', 'Симптомы', 'Лечение'],
            'h3': ['Диета', 'Спорт'],
            'chars': 5000,
            'success': True
        },
        {
            'url': 'example2.com',
            'h1': 'Заголовок 2',
            'h2': ['Причины проблемы', 'Симптомы болезни', 'Методы лечения'],
            'h3': ['Питание', 'Физическая активность'],
            'chars': 6000,
            'success': True
        },
        {
            'url': 'example3.com',
            'h1': 'Заголовок 3',
            'h2': ['Основные причины', 'Признаки', 'Как лечить'],
            'h3': [],
            'chars': 4500,
            'success': True
        }
    ]

    print("1. Анализ тестовых данных...")
    analysis = analyze_competitors(test_results)

    print(f"\n✅ Результат анализа:")
    print(f"   Успешно: {analysis['success_count']}/{analysis['total']}")
    print(f"   Средний объем: {analysis['avg_chars']} символов")
    print(f"   Диапазон: {analysis['min_chars']} - {analysis['max_chars']}")
    print(f"   H2 всего: {analysis['h2_total']}")
    print(f"   H3 всего: {analysis['h3_total']}")

    if analysis['common_h2']:
        print(f"\n   Общие H2 (мин. 3 повтора):")
        for h in analysis['common_h2']:
            print(f"      - {h['text']} ({h['count']}x)")

    print("\n2. Генерация плана статьи...")
    plan = generate_article_plan(analysis, "тестовый запрос")

    print(f"\n✅ План статьи:")
    print(f"   Запрос: {plan['keyword']}")
    print(f"   Объем: ~{plan['recommended_length']} символов")
    print(f"   Структура:")
    for item in plan['structure']:
        level = item['level'].upper()
        freq = f" [{item.get('frequency', '')}x]" if item.get('frequency') else ""
        print(f"      {level}: {item['text']}{freq}")

    print("\n✅ ТЕСТ ЗАВЕРШЕН")
