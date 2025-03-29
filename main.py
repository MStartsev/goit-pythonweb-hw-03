import json
import mimetypes
import os
import pathlib
import urllib.parse
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader

# Підготовка папки storage, якщо її не існує
os.makedirs("storage", exist_ok=True)

# Налаштування Jinja2
env = Environment(loader=FileSystemLoader("."))


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)

        if pr_url.path == "/":
            self.send_html_file("templates/index.html")
        elif pr_url.path == "/message":
            self.send_html_file("templates/message.html")
        elif pr_url.path == "/read":
            self.render_template()
        else:
            # Перевірка чи існує статичний файл
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file("templates/error.html", 404)

    def do_POST(self):
        pr_url = urllib.parse.urlparse(self.path)

        if pr_url.path == "/message":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            data_parse = urllib.parse.unquote_plus(post_data.decode())

            # Перетворення даних форми в словник
            data_dict = {
                key: value
                for key, value in [el.split("=") for el in data_parse.split("&")]
            }

            # Збереження даних у файл data.json
            self.save_data_to_json(data_dict)

            # Перенаправлення на сторінку повідомлень
            self.send_response(302)
            self.send_header("Location", "/read")
            self.end_headers()
        else:
            self.send_html_file("templates/error.html", 404)

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open(filename, "rb") as file:
            self.wfile.write(file.read())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", "text/plain")
        self.end_headers()
        with open(f".{self.path}", "rb") as file:
            self.wfile.write(file.read())

    def save_data_to_json(self, data):
        # Читання існуючих даних
        try:
            with open("storage/data.json", "r") as file:
                json_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            json_data = {}

        # Додавання нових даних з часовою міткою
        timestamp = str(datetime.now())
        json_data[timestamp] = {
            "username": data.get("username", ""),
            "message": data.get("message", ""),
        }

        # Запис у файл
        with open("storage/data.json", "w") as file:
            json.dump(json_data, file, indent=2)

    def render_template(self):
        # Читання даних з json файлу
        try:
            with open("storage/data.json", "r") as file:
                messages = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            messages = {}

        # Рендеринг шаблону
        template = env.get_template("templates/read.html")
        html_content = template.render(messages=messages)

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html_content.encode())


def run(server_class=HTTPServer, handler_class=HttpHandler, port=3000):
    server_address = ("", port)
    http = server_class(server_address, handler_class)
    print(f"Запуск сервера на порту {port}...")
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()
        print("Сервер зупинено")


if __name__ == "__main__":
    run()
