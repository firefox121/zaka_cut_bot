import os
import telebot

TOKEN = os.environ.get("TELEGRAM_TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "0"))

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: message.chat.id != ADMIN_ID)
def forward_to_admin(message):
    # --- ЛОГГИРУЕМ ТИП СООБЩЕНИЯ ---
    print(f"Получено сообщение от {message.from_user.id}, тип: {message.content_type}")
    
    # --- ПЕРЕСЫЛАЕМ КОПИЮ СООБЩЕНИЯ (работает для всех типов) ---
    try:
        bot.copy_message(ADMIN_ID, message.chat.id, message.message_id)
    except Exception as e:
        # Если copy_message не сработал — пробуем forward_message
        bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    
    # Отправляем ID отправителя
    user_id = message.from_user.id
    username = message.from_user.username if message.from_user.username else "нет ника"
    bot.send_message(
        ADMIN_ID,
        f"👤 Отправитель:\n• ID: `{user_id}`\n• Username: @{username}\n\nДля ответа используй: /reply {user_id} [текст]",
        parse_mode='Markdown'
    )
    
    bot.reply_to(message, "✅ Сообщение доставлено!")

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

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Пиши сюда, админ получит твое сообщение.")

if __name__ == "__main__":
    print("🚀 Бот запущен...")
    bot.infinity_polling()
