import json

def read_json_file(file_path):
    """
    Читает JSON-файл и возвращает список объектов.
    :param file_path: Путь к JSON-файлу.
    :return: Список объектов из JSON или сообщение об ошибке.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read().strip()
            if not content:
                raise ValueError("JSON файл пуст.")
            data = json.loads(content)
            return data
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
    except ValueError as e:
        print(f"Ошибка: {e}")
    except json.JSONDecodeError:
        print("Ошибка декодирования JSON. Проверьте формат файла.")
    return None

# Пример использования
file_path = "output.json"
data = read_json_file(file_path)

if data:
    print("Данные успешно загружены:")
    for obj in data:
        print(obj)
else:
    print("Не удалось загрузить данные из JSON.")

