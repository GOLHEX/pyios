import re
from bs4 import BeautifulSoup
import json

def parse_image_filename(filename):
    pattern = r"360_F_(\d+)_(\w+)\.jpg"
    match = re.match(pattern, filename)
    if match:
        return {
            "imageID": match.group(1),
            "randomHash": match.group(2)
        }
    else:
        return "Invalid filename format"

# Открываем и читаем HTML‑файл
with open("temp_response.html", "r", encoding="utf-8") as f:
    html_content = f.read()
    # Определяем паттерн для поиска имен файлов по шаблону
    pattern = r"360_F_\d+_\w+\.jpg"

    # Ищем все совпадения в HTML‑контенте
    file_matches = re.findall(pattern, html_content)

    # Убираем дубликаты, если необходимо
    unique_files = sorted(set(file_matches))

    soup = BeautifulSoup(html_content, "html.parser")

    def extract_info_by_id(target_id, soup):
        # Ищем элемент с data-content-id равным target_id
        target_tag = soup.find(attrs={"data-content-id": target_id})
        if target_tag:
            # Извлекаем ссылку (contentUrl)
            meta_desc = target_tag.find("meta", itemprop="contentUrl")
            file_link = meta_desc.get("content", "").strip() if meta_desc and meta_desc.has_attr("content") else ""
            
            # Извлекаем описание (content)
            meta_desc = target_tag.find("meta", itemprop="name")
            description = meta_desc.get("content", "").strip() if meta_desc and meta_desc.has_attr("content") else ""
            
            # Извлекаем тайтл
            meta_desc = target_tag.find("meta", itemprop="acquireLicensePage")
            page = meta_desc.get("content", "").strip() if meta_desc and meta_desc.has_attr("content") else ""
            
            # Извлекаем альтернативный текст

            
            return {
                "id": target_id,
                "file_link": file_link,
                "description": description,
                "url": f"{page}?prev_url=detail",
            }
        else:
            return None

    # Сохраняем информацию в формате JSON
    result = []

    for filename in unique_files:
        parsed_info = parse_image_filename(filename)
        if isinstance(parsed_info, dict):
            target_id = parsed_info["imageID"]
            file_info = extract_info_by_id(target_id, soup)
            if file_info:
                result.append(file_info)
            else:
                print(f"Элемент с data-content-id = {target_id} не найден")
        else:
            print(f"Ошибка: неверный формат имени файла {filename}")

    # Сохраняем результат в файл JSON
    with open("output.json", "w", encoding="utf-8") as json_file:
        json.dump(result, json_file, ensure_ascii=False, indent=4)

        # Сохранить файл по ссылке
        for item in result:
            if item.get("file_link"):
                file_link = item["file_link"]
                # Здесь вы можете добавить код для загрузки файла по ссылке, если это необходимо

    print("Информация успешно сохранена в output.json")
