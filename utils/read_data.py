import json
import os


def read_test_data_json(filename) -> list:
    """
        Чтение данных из JSON-файла.
        Если файл не найден или повреждён, возвращает пустой список.
    """
    if not os.path.isfile(filename):
        return []

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []