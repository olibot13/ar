from flask import Flask, render_template_string, request, redirect, send_file
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Web Archive</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 20px;
            background-color: #f7f7f7;
            color: #333;
        }
        h1, h2 {
            color: #0066cc;
        }
        form {
            margin-bottom: 20px;
            background-color: #fff;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        label {
            display: block;
            margin-bottom: 10px;
        }
        input {
            width: 100%;
            padding: 10px;
            margin-bottom: 10px;
            box-sizing: border-box;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        button {
            background-color: #0066cc;
            color: #fff;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #0052a3;
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        li {
            margin-bottom: 10px;
            background-color: #fff;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        a {
            color: #0066cc;
            text-decoration: none;
            font-weight: bold;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <h1>Welcome to Web Archive</h1>
    <form action="/archive" method="post">
        <label for="url">Enter URL:</label>
        <input type="text" id="url" name="url" required>
        <button type="submit">Archive</button>
    </form>
    <h2>Saved Files</h2>
    <ul>
        {% for file_name in files %}
            <li><a href="{{ url_for('load_file', file_name=file_name) }}">{{ file_name }}</a></li>
        {% endfor %}
    </ul>
</body>
</html>
"""

@app.route('/')
def index():
    # List all saved files in the directory
    files = [file for file in os.listdir() if file.endswith(".html")]
    return render_template_string(html_template, files=files)

@app.route('/archive', methods=['POST'])
def archive():
    url = request.form['url']
    save_web_page(url)
    return redirect('/')

def save_web_page(url):
    try:
        response = requests.get(url)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{timestamp}_{url.replace('http://', '').replace('https://', '').replace('/', '_')}.html"
        soup = BeautifulSoup(response.text, 'html.parser')
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(str(soup))
        print(f"Web page saved: {url}")
    except Exception as e:
        print(f"Error saving web page {url}: {e}")

@app.route('/load/<file_name>')
def load_file(file_name):
    return send_file(file_name, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
