import requests
import json
import logging
import tkinter as tk
from tkinter import messagebox
import webbrowser
from bs4 import BeautifulSoup

try:
    html_view_available = True
except ImportError:
    html_view_available = False
import random
from methods.import_json import read_json_file

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AdobeStockSelector:
    def __init__(self):
        self.base_url = "https://stock.adobe.com/ua/search/images"
    
    def create_url(self, keywords, content_types, page=1, limit=100):
        keyword_str = '+'.join(keywords)
        filters = []
        
        # Установка фильтров по типу контента
        if 'photo' in content_types:
            filters.append('filters%5Bcontent_type%3Aphoto%5D=1')
        if 'illustration' in content_types:
            filters.append('filters%5Bcontent_type%3Aillustration%5D=1')
        if 'zip_vector' in content_types:
            filters.append('filters%5Bcontent_type%3Azip_vector%5D=1')
        if 'image' in content_types:
            filters.append('filters%5Bcontent_type%3Aimage%5D=1')

        filter_query = '&'.join(filters)

        # Конструкция URL с релевантностью по цене
        url = (f"{self.base_url}?{filter_query}&k={keyword_str}&order=relevance"
               f"&price%5B%24%5D=1&limit={limit}&search_page={page}&search_type=usertyped"
               f"&acp=&aco={keyword_str}&get_facets=0")
        
        return url

    def send_request(self, keywords, content_types, page=1, limit=100):
        url = self.create_url(keywords, content_types, page, limit)
        logging.info(f"Запрос по URL: {url}")
        try:
            response = requests.get(url)
            response.raise_for_status()
            try:
                # Попытка распарсить ответ как JSON
                data = response.json()
                logging.info("Запрос выполнен успешно")
                return data
            except json.JSONDecodeError:
                # Если не удалось распарсить как JSON, возвращаем текст
                logging.error("Ответ не является JSON. Содержимое ответа:")
                logging.error(response.text)
                return response.text
        except requests.exceptions.RequestException as req_err:
            logging.error(f"Ошибка запроса: {req_err}")
        except Exception as e:
            logging.error(f"Произошла неизвестная ошибка: {e}")
        return None

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Adobe Stock Selector")
        self.geometry("800x600")
        self.selector = AdobeStockSelector()
        self.create_widgets()

    def create_widgets(self):
        # Ввод ключевых слов
        tk.Label(self, text="Ключевые слова (через запятую):").pack(pady=5)
        default_keywords = random.sample(["nature", "technology", "art", "business", "travel", "food", "health"], 3)
        self.keywords_entry = tk.Entry(self, width=50)
        self.keywords_entry.insert(0, ", ".join(default_keywords))
        self.keywords_entry.pack()

        # Флажки для типов контента
        tk.Label(self, text="Выберите типы контента:").pack(pady=5)
        self.content_types_vars = {
            "photo": tk.BooleanVar(value=True),
            "illustration": tk.BooleanVar(value=True),
            "zip_vector": tk.BooleanVar(),
            "image": tk.BooleanVar()
        }
        frame = tk.Frame(self)
        frame.pack(pady=5)
        for content_type, var in self.content_types_vars.items():
            cb = tk.Checkbutton(frame, text=content_type, variable=var)
            cb.pack(side=tk.LEFT, padx=5)

        # Ввод номера страницы и лимита результатов
        page_frame = tk.Frame(self)
        page_frame.pack(pady=5)
        tk.Label(page_frame, text="Страница:").pack(side=tk.LEFT)
        self.page_entry = tk.Entry(page_frame, width=5)
        self.page_entry.pack(side=tk.LEFT, padx=5)
        tk.Label(page_frame, text="Лимит:").pack(side=tk.LEFT)
        self.limit_entry = tk.Entry(page_frame, width=5)
        self.limit_entry.pack(side=tk.LEFT, padx=5)

        # Кнопка отправки запроса
        tk.Button(self, text="Отправить запрос", command=self.send_request).pack(pady=10)
        # Текстовое поле для вывода результата (если не HTML)
        self.result_text = tk.Text(self, wrap=tk.NONE, height=10)
        self.result_text.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

    def send_request(self):
        keywords_raw = self.keywords_entry.get()
        if not keywords_raw:
            messagebox.showerror("Ошибка", "Введите ключевые слова")
            return
        keywords = [kw.strip() for kw in keywords_raw.split(",") if kw.strip()]
        selected_content = [ct for ct, var in self.content_types_vars.items() if var.get()]
        if not selected_content:
            messagebox.showerror("Ошибка", "Выберите хотя бы один тип контента")
            return

        try:
            page = int(self.page_entry.get())
        except ValueError:
            page = 1

        try:
            limit = int(self.limit_entry.get())
        except ValueError:
            limit = 100

        result = self.selector.send_request(keywords, selected_content, page, limit)
        self.result_text.delete(1.0, tk.END)
        if result:
            # Если ответ является строкой и начинается с <!DOCTYPE html PUBLIC, выводим его в HTML-виджете
            if isinstance(result, str) and result.strip().startswith("<!DOCTYPE html PUBLIC"):
                if html_view_available:
                    # Если модуль tkhtmlview установлен, используем его для отображения HTML
                    # СОХРАНИТЬ HTML ВРЕМЕННО В ФАЙЛ
                    with open("temp_response.html", "w", encoding="utf-8") as f:
                        f.write(result)
                    #self.result_text.delete(1.0, tk.END)
                    #self.show_html_document(result)
                else:
                    # Если модуль tkhtmlview не установлен, откроем HTML в браузере
                    with open("temp_response.html", "w", encoding="utf-8") as f:
                        f.write(result)
                    webbrowser.open_new_tab("temp_response.html")
            else:
                formatted = json.dumps(result, indent=4, ensure_ascii=False) if not isinstance(result, str) else result
                self.result_text.insert(tk.END, formatted)
        else:
                self.result_text.insert(tk.END, "Не удалось получить данные с сервера")
    
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


    def on_button_click(input_field):
        user_input = input_field.get()
        if user_input:
            messagebox.showinfo("Input Received", f"You entered: {user_input}")
        else:
            messagebox.showwarning("No Input", "Please enter something!")

        # Create the main window
        root = tk.Tk()
        root.title("Input and Button Example")

        # Create an input field
        input_field = tk.Entry(root, width=30)
        input_field.pack(pady=10)

        # Create a button
        submit_button = tk.Button(root, text="GetInfoByID", command=lambda: app.get_file_info_by_id(file_id))
        submit_button.pack(pady=10)

if __name__ == "__main__":
    app = Application()
    app.mainloop()