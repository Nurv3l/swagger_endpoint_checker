import requests
import json
import re
import tkinter as tk
from tkinter import filedialog

def browse_file():
    if file_path:
        file_content = read_text_file_line_by_line(file_path)
        if file_content is not None:
            pass
    browse_file()
    
def extract_string_between_slashes(url):
    pattern = r'//(.+?)/'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None
    

def fetch_swagger(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            content_type = response.headers.get('content-type')
            if 'application/json' in content_type:
                return response.json()
            else:
                raise ValueError("Invalid content type. Only JSON or YAML supported.")
        else:
            raise requests.HTTPError(f"Error fetching Swagger: {response.status_code}")
    except requests.RequestException as e:
        raise requests.RequestException(f"Error fetching Swagger: {str(e)}")

def get_endpoints(swagger_doc):
    endpoints = []
    paths = swagger_doc.get('paths', {})
    for path, methods in paths.items():
        for method, _ in methods.items():
            endpoint = f"{method.upper()} {path}"
            endpoints.append(endpoint)
    return endpoints

def create_text_file(file_path, content):
    try:
        with open(file_path, "a", encoding="utf-8") as file:
            file.write(content + "\n")
    except Exception as e:
        print(f"Error: {str(e)}")
        
def read_text_file_line_by_line(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
        return lines
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw() 
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    file_lines = read_text_file_line_by_line(file_path)
    if file_lines is not None:
        for line in file_lines:
            swagger_url = line.strip()
            result = extract_string_between_slashes(swagger_url)
            
            try:
                swagger_doc = fetch_swagger(swagger_url)
                endpoints = get_endpoints(swagger_doc)
                for endpoint in endpoints:
                    if result:
                        file_path = f"{result}.txt"
                        file_content = endpoint
                        create_text_file(file_path, file_content)
                print("Process successful!!")
            except Exception as e:
                print(f"An error occurred: {str(e)}")
