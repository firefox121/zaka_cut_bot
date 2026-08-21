import os
import telebot

# Берем секреты из переменных окружения
TOKEN = os.environ.get("TELEGRAM_TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "0"))  # "0" - значение по умолчанию, если ID не найден

bot = telebot.TeleBot(TOKEN)

# Команда для проверки, что бот жив
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Бот запущен и работает!")

# Обработка всех остальных сообщений
@bot.message_handler(func=lambda message: message.chat.id != ADMIN_ID)
def forward_to_admin(message):
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    bot.reply_to(message, "✅ Сообщение доставлено!")

# Команда для ответа пользователю (только для админа)
@bot.message_handler(commands=['reply'])
def reply_to_user(message):
    if message.chat.id != ADMIN_ID:
        bot.reply_to(message, "❌ У тебя нет прав.")
        return
    try:
        parts = message.text.split(maxsplit=2)
        if len(parts) < 3:
            bot.reply_to(message, "❌ Формат: /reply ID_пользователя Текст")
            return
        user_id = int(parts[1])
        reply_text = parts[2]
        bot.send_message(user_id, f"👤 Админ: {reply_text}")
        bot.reply_to(message, f"✅ Ответ отправлен пользователю {user_id}")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling()