# Используем официальный образ Python
FROM python:3.10-slim

# Устанавливаем зависимости
RUN apt-get update && apt-get install -y libpq-dev
RUN pip install --upgrade pip

# Копируем ваш проект в контейнер
WORKDIR /app
COPY . /app

# Устанавливаем все зависимости проекта
RUN pip install -r requirements.txt

# Открываем порт, на котором будет работать FastAPI
EXPOSE 8000

# Запускаем сервер Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
