import telebot
import os
from telebot import types

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🔮 Horoscope du jour")
    btn2 = types.KeyboardButton("❤️ Compatibilité amoureuse")
    btn3 = types.KeyboardButton("⭐ Bonus quotidien")
    btn4 = types.KeyboardButton("💎 Mode Premium")
    markup.add(btn1, btn2, btn3, btn4)

    bot.send_message(
        message.chat.id,
        "Bienvenue dans *AstroVibeAI* ✨\n\nChoisis une option ci‑dessous :",
        parse_mode="Markdown",
        reply_markup=markup
    )

@bot.message_handler(func=lambda m: True)
def menu(message):
    if message.text == "🔮 Horoscope du jour":
        bot.send_message(message.chat.id, "✨ Horoscope du jour :\nTu vas recevoir une belle énergie aujourd’hui.")
    elif message.text == "❤️ Compatibilité amoureuse":
        bot.send_message(message.chat.id, "❤️ Compatibilité :\nDonne-moi deux signes astrologiques.")
    elif message.text == "⭐ Bonus quotidien":
        bot.send_message(message.chat.id, "⭐ Bonus :\nTu gagnes +5 points aujourd’hui !")
    elif message.text == "💎 Mode Premium":
        bot.send_message(message.chat.id, "💎 Premium :\nAccès aux prédictions avancées et aux compatibilités détaillées.")

bot.polling()
import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
