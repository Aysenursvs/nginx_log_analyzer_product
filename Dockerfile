FROM python:3.12-slim

WORKDIR /nginx_analyzer

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /nginx_analyzer

CMD ["python", "main.py"]
