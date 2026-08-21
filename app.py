from flask import Flask
import threading
import bot  # импортируем твой основной файл с ботом
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Бот запущен!"

def run_bot():
    # Запускаем бота в отдельном потоке, чтобы он не блокировал Flask
    bot.bot.infinity_polling()

if __name__ == "__main__":
    # Запускаем бота в фоновом потоке
    thread = threading.Thread(target=run_bot)
    thread.start()
    # Запускаем Flask сервер на порту, который дает Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
