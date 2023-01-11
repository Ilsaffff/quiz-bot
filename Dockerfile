FROM python:3.10.7

WORKDIR /app

COPY . .

CMD ["python", "bot.py"]