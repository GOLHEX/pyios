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

# Read the URL from output.json
try:
    with open('./output.json', 'r') as file:
        content = file.read().strip()
        if not content:
            raise ValueError("JSON file is empty.")
        data = json.loads(content)

        # Iterate through the list of objects and search for the desired ID
        for index, obj in enumerate(data):
            if obj.get('id') == '1161782033':
                print(f"Found desired ID at index {index}: {obj}")
                file_id = obj.get('id')
                url = obj.get('url')
                break
        else:
            print("Desired ID not found in the JSON data.")

        file_id = data[index].get('id')  # Assuming the JSON file contains a key "id"
        print(f"File ID: {file_id}")
        url = (data[index].get('url'))  # Assuming the JSON file contains a key "url"
        if url:
            print(fetch_and_parse_keywords(url))
            # Append the fetched keywords to the JSON file
            with open('./output.json', 'w') as file:
                data[index]['keywords'] = fetch_and_parse_keywords(url)
                json.dump(data, file, indent=4, ensure_ascii=False)
        else:
            print("No URL found in the JSON file.")
except FileNotFoundError:
    print("The file output.json was not found.")
except ValueError as e:
    print(f"Error: {e}")
except json.JSONDecodeError:
    print("Error decoding JSON from the file.")