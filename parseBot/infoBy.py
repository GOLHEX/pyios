import requests
from bs4 import BeautifulSoup
import json

def fetch_and_parse_keywords(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all elements with the specified wrapper
        keyword_elements = soup.find_all('div', class_='fx8d1q_spectrum-Tag-cell')

        # Extract text content from each element and store in a list
        keywords = [element.get_text(strip=True) for element in keyword_elements]

        # Return the list of keywords
        return keywords if keywords else "No keywords found on the page."
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

def get_file_info_by_id(file_id, json_file_path='./output.json'):
    """
    Получает информацию о файле по его ID из JSON-файла.
    
    :param file_id: ID файла, который нужно найти.
    :param json_file_path: Путь к JSON-файлу.
    :return: Словарь с информацией о файле или сообщение об ошибке.
    """
    try:
        # Открываем JSON-файл
        with open(json_file_path, 'r', encoding='utf-8') as file:
            content = file.read().strip()
            if not content:
                raise ValueError("JSON файл пуст.")
            data = json.loads(content)

        # Ищем объект с указанным ID
        for obj in data:
            if obj.get('id') == file_id:
                return obj  # Возвращаем найденный объект

        # Если объект с указанным ID не найден
        return f"Файл с ID {file_id} не найден в JSON."
    except FileNotFoundError:
        return f"Файл {json_file_path} не найден."
    except ValueError as e:
        return f"Ошибка: {e}"
    except json.JSONDecodeError:
        return "Ошибка декодирования JSON. Проверьте формат файла."

# Пример использования
file_id = "976219320"  # ID файла, который нужно найти
file_info = get_file_info_by_id(file_id)

if isinstance(file_info, dict):
    print("Информация о файле:")
    print(json.dumps(file_info, indent=4, ensure_ascii=False))
else:
    print(file_info)