import datetime

import pandas as pd
import re
from typing import List, Dict, Any
import os


def extract_subjects_from_excel(file_path: str, list_index: int) -> List[Dict[str, Any]]:
    """
    Извлекает информацию о предметах из учебного плана Excel

    Args:
        file_path: путь к файлу Excel
        list_index: индекс страницы с данными для извлечения

    Returns:
        Список словарей с информацией о предметах
    """
    subjects = []

    # Читаем все листы Excel файла
    excel_file = pd.ExcelFile(file_path)
    sheet_name = excel_file.sheet_names[list_index]
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)

        # Ищем строки с предметами (содержат коды типа ОП, ПМ, МДК и т.д.)
        for idx, row in df.iterrows():
            subject_info = extract_subject_info(row, df, idx)
            if subject_info:
                subjects.append(subject_info)

    except Exception as e:
        print(f"Ошибка при обработке листа {sheet_name}: {e}")

    return subjects


def extract_subject_info(row: pd.Series, df: pd.DataFrame, row_idx: int) -> Dict[str, Any]:
    """
    Извлекает информацию о предмете из строки

    Args:
        row: строка DataFrame
        df: весь DataFrame
        row_idx: индекс текущей строки

    Returns:
        Словарь с информацией о предмете или None если строка не содержит предмет
    """
    # Паттерны для идентификации кодов предметов
    subject_patterns = [
        r'^(ОУД\.\d+)',  # ОУД.01, ОУД.02 и т.д.
        r'^(ОП\.\d+)',  # ОП.01, ОП.02 и т.д.
        r'^(ПМ\.\d+)',  # ПМ.01, ПМ.02 и т.д.
        r'^(МДК\.\d+\.\d+)',  # МДК.01.01, МДК.01.02 и т.д.
        r'^(УП\.\d+)',  # УП.01, УП.02 и т.д.
        r'^(ПП\.\d+)',  # ПП.01, ПП.02 и т.д.
        r'^(ЕН\.\d+)',  # ЕН.00 и т.д.
        r'^(ДУП\.\d+)',  # ДУП.01, ДУП.02 и т.д.
    ]

    # Проверяем ячейки на наличие кода предмета
    for cell in row:
        if pd.isna(cell):
            continue

        cell_str = str(cell).strip()
        for pattern in subject_patterns:
            match = re.match(pattern, cell_str)
            if match:
                subject_code = cell_str
                return parse_subject_details(subject_code, row, df, row_idx)

    return None


def parse_subject_details(subject_code: str, row: pd.Series, df: pd.DataFrame, row_idx: int) -> Dict[str, Any]:
    """
    Парсит детальную информацию о предмете

    Args:
        subject_code: код предмета
        row: строка с данными предмета
        df: весь DataFrame
        row_idx: индекс текущей строки

    Returns:
        Словарь с детальной информацией о предмете
    """
    subject = {
        'code': subject_code,
        'name': None,
        'total_hours': None,
        'independent_work': None,
        'contact_hours': None,
        'exams': None,
        'consultations': None,
        'practice': None,
        'theoretical_lessons': None,
        'lab_practical_lessons': None,
        'practical_training': None,
        'course_design': None,
        'semester_attestation': None,
        'control_work': None
    }

    # Извлекаем название предмета (обычно следующая ячейка после кода)
    for i, cell in enumerate(row):
        if str(cell).strip() == subject_code:
            if i + 1 < len(row) and not pd.isna(row[i + 1]):
                subject['name'] = str(row[i + 1]).strip()
            break

    # Пытаемся найти числовые параметры в строке
    numeric_values = []
    for cell in row:
        if pd.isna(cell):
            continue
        try:
            # Пробуем преобразовать в число
            if isinstance(cell, (int, float)):
                numeric_values.append(cell)
            elif isinstance(cell, str):
                # Убираем нечисловые символы и пробуем преобразовать
                clean_cell = re.sub(r'[^\d.,]', '', cell)
                if clean_cell:
                    numeric_values.append(float(clean_cell.replace(',', '.')))
        except (ValueError, TypeError):
            continue

    # Распределяем найденные числовые значения по параметрам
    if numeric_values:
        # Эвристика: предполагаем, что первое число - общее количество часов
        subject['total_hours'] = numeric_values[0] if len(numeric_values) > 0 else None

        # Дополнительные параметры можно извлекать по позициям
        # или искать в соседних строках/столбцах

    # Дополнительно: ищем информацию в соседних строках
    if row_idx + 1 < len(df):
        next_row = df.iloc[row_idx + 1]
        next_numeric_values = []
        for cell in next_row:
            if pd.isna(cell):
                continue
            try:
                if isinstance(cell, (int, float)):
                    next_numeric_values.append(cell)
                elif isinstance(cell, str):
                    clean_cell = re.sub(r'[^\d.,]', '', cell)
                    if clean_cell:
                        next_numeric_values.append(float(clean_cell.replace(',', '.')))
            except (ValueError, TypeError):
                continue

        if next_numeric_values and not subject['independent_work']:
            subject['independent_work'] = next_numeric_values[0] if len(next_numeric_values) > 0 else None

    return subject


def save_subjects_to_excel(subjects: List[Dict[str, Any]], output_path: str):
    """
    Сохраняет найденные предметы в Excel файл

    Args:
        subjects: список предметов
        output_path: путь для сохранения
    """
    df = pd.DataFrame(subjects)

    # Упорядочиваем колонки для лучшей читаемости
    columns_order = ['code', 'name', 'total_hours', 'independent_work',
                     'contact_hours', 'exams', 'consultations', 'practice',
                     'theoretical_lessons', 'lab_practical_lessons',
                     'practical_training', 'course_design', 'source_file']

    # Оставляем только существующие колонки
    existing_columns = [col for col in columns_order if col in df.columns]
    df = df[existing_columns]

    df.to_excel(output_path, index=False)
    print(f"Результаты сохранены в {output_path}")


# Пример использования
if __name__ == "__main__":

    subjects = extract_subjects_from_excel("../static/plan_docs/38.02.06_ДФ_9_25.xlsx", 2)

    # Пример вывода первых 5 предметов
    for i, subject in enumerate(subjects):
        print(f"{i + 1}. {subject.get('code')} - {subject.get('name')}: {subject.get('total_hours')} часов")