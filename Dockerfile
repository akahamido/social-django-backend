FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
