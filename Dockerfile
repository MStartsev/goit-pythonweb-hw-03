FROM python:3.10-slim

WORKDIR /app

RUN pip install --no-cache-dir jinja2

COPY *.html /app/
COPY style.css /app/
COPY logo.png /app/

COPY main.py /app/

RUN mkdir -p /app/storage

EXPOSE 3000

CMD ["python", "main.py"]