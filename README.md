# Python Web Application

Простий веб-додаток на Python з використанням HTTP сервера та Jinja2 для шаблонізації.

## Запуск програми без Docker

1. Встановіть необхідні залежності:

   ```bash
   pip install jinja2
   ```

2. Запустіть основний файл:

   ```bash
   python main.py
   ```

3. Відкрийте у браузері адресу http://localhost:3000

## Запуск у Docker

### Варіант 1: Використання Docker команд

1. Зберіть Docker образ:

   ```bash
   docker build -t python-web-app .
   ```

2. Запустіть контейнер з використанням volume:

   ```bash
   docker run -d -p 3000:3000 -v ./storage:/app/storage --name python-web-app python-web-app
   ```

3. Щоб зупинити та видалити контейнер:
   ```bash
   docker stop python-web-app && docker rm python-web-app
   ```

### Варіант 2: Використання Docker Compose

1. Запустіть додаток через Docker Compose:

   ```bash
   docker-compose up -d
   ```

2. Щоб зупинити та видалити контейнер:
   ```bash
   docker-compose down
   ```

## Функціональність

- **Головна сторінка**: http://localhost:3000/
- **Надсилання повідомлень**: http://localhost:3000/message
- **Перегляд повідомлень**: http://localhost:3000/read

## Технічна інформація

- Веб-сервер працює на порту 3000
- Всі повідомлення зберігаються у файлі `storage/data.json`
- Використовується Jinja2 для шаблонізації
- Статичні файли: CSS та зображення
