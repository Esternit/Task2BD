FROM python:3.11

# Устанавливаем рабочую директорию
WORKDIR /script/src

# Копируем все файлы из текущей директории в контейнер
COPY ./ /script

# Обновляем apt-get и устанавливаем необходимые зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-pip \
    gcc \
    libffi-dev \
    libpq-dev \
    libssl-dev \
    libuv1-dev && \
    pip install --upgrade pip && \
    pip install -r /script/requirements.txt

# Даем исполняемые права скрипту controller.py
RUN chmod +x /script/src/controller.py

# Команда для запуска приложения
CMD ["sh", "-c", "sleep 5 && uvicorn controller:app --host 0.0.0.0 --port 8000 --reload"]
