import os
import threading
import telebot
from telebot import types
from flask import Flask

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Liste des 12 signes
SIGNS = [
    "♈ Bélier",
    "♉ Taureau",
    "♊ Gémeaux",
    "♋ Cancer",
    "♌ Lion",
    "♍ Vierge",
    "♎ Balance",
    "♏ Scorpion",
    "♐ Sagittaire",
    "♑ Capricorne",
    "♒ Verseau",
    "♓ Poissons"
]

# Temporaire : mémorise le signe tant que le serveur reste actif
user_signs = {}


def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton("🔮 Horoscope du jour")
    btn2 = types.KeyboardButton("❤️ Compatibilité amoureuse")
    btn3 = types.KeyboardButton("⭐ Bonus quotidien")
    btn4 = types.KeyboardButton("💎 Mode Premium")

    markup.add(btn1, btn2)
    markup.add(btn3, btn4)

    return markup


def signs_menu():
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
    )

    for i in range(0, len(SIGNS), 2):
        markup.row(
            types.KeyboardButton(SIGNS[i]),
            types.KeyboardButton(SIGNS[i + 1])
        )

    return markup


@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id

    if user_id not in user_signs:
        bot.send_message(
            message.chat.id,
            "✨ Bienvenue dans AstroVibe ✨\n\n"
            "Pour commencer, quel est ton signe astrologique ?",
            reply_markup=signs_menu()
        )
    else:
        bot.send_message(
            message.chat.id,
            "✨ Bienvenue dans AstroVibe ✨\n\n"
            f"Ton signe : {user_signs[user_id]}\n\n"
            "Que souhaites-tu découvrir aujourd'hui ?",
            reply_markup=main_menu()
        )


@bot.message_handler(func=lambda message: message.text in SIGNS)
def save_sign(message):
    user_id = message.from_user.id
    user_signs[user_id] = message.text

    bot.send_message(
        message.chat.id,
        f"✅ Ton signe est enregistré : {message.text}\n\n"
        "Bienvenue dans ton univers AstroVibe ✨",
        reply_markup=main_menu()
    )


@bot.message_handler(commands=["horoscope"])
def horoscope_command(message):
    show_horoscope(message)


def show_horoscope(message):
    user_id = message.from_user.id

    if user_id not in user_signs:
        bot.send_message(
            message.chat.id,
            "Je dois d'abord connaître ton signe astrologique. ✨",
            reply_markup=signs_menu()
        )
        return

    sign = user_signs[user_id]

    bot.send_message(
        message.chat.id,
        f"🔮 Horoscope du jour\n\n"
        f"{sign}\n\n"
        "✨ Ton horoscope personnalisé arrive bientôt.\n"
        "Nous allons construire cette partie à l'étape suivante."
    )


@bot.message_handler(commands=["points"])
def points_command(message):
    bot.send_message(
        message.chat.id,
        "⭐ Le système de points arrive très bientôt."
    )


@bot.message_handler(func=lambda message: True)
def menu(message):

    if message.text == "🔮 Horoscope du jour":
        show_horoscope(message)

    elif message.text == "❤️ Compatibilité amoureuse":
        bot.send_message(
            message.chat.id,
            "❤️ Compatibilité amoureuse\n\n"
            "Cette fonctionnalité arrive bientôt."
        )

    elif message.text == "⭐ Bonus quotidien":
        bot.send_message(
            message.chat.id,
            "⭐ Bonus quotidien\n\n"
            "Tu gagnes +5 points aujourd'hui !"
        )

    elif message.text == "💎 Mode Premium":
        bot.send_message(
            message.chat.id,
            "💎 AstroVibe Premium\n\n"
            "Les fonctionnalités Premium arrivent bientôt."
        )


# Lancement du bot Telegram
threading.Thread(
    target=bot.infinity_polling,
    daemon=True
).start()


# Petit serveur web nécessaire pour Render
app = Flask(__name__)


@app.route("/")
def home():
    return "AstroVibe is running ✨"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
