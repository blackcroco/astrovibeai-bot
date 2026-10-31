import os
import threading
import telebot
import psycopg2

from telebot import types
from flask import Flask


# =========================
# CONFIGURATION
# =========================

TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

if not TOKEN:
    raise RuntimeError("BOT_TOKEN manquant dans les variables Render.")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL manquant dans les variables Render.")

bot = telebot.TeleBot(TOKEN)


# =========================
# BASE DE DONNEES NEON
# =========================

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)


def init_database():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            telegram_id BIGINT PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            sign TEXT,
            points INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1,
            streak INTEGER DEFAULT 0,
            last_bonus DATE,
            premium BOOLEAN DEFAULT FALSE,
            language TEXT DEFAULT 'fr',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()

    print("Base de donnees AstroVibe initialisee.")


def create_or_update_user(message):
    conn = get_db_connection()
    cursor = conn.cursor()

    user = message.from_user

    cursor.execute("""
        INSERT INTO users (
            telegram_id,
            username,
            first_name
        )
        VALUES (%s, %s, %s)

        ON CONFLICT (telegram_id)
        DO UPDATE SET
            username = EXCLUDED.username,
            first_name = EXCLUDED.first_name
    """, (
        user.id,
        user.username,
        user.first_name
    ))

    conn.commit()
    cursor.close()
    conn.close()


def get_user_sign(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT sign FROM users WHERE telegram_id = %s",
        (user_id,)
    )

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        return result[0]

    return None


def save_user_sign(user_id, sign):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET sign = %s
        WHERE telegram_id = %s
    """, (
        sign,
        user_id
    ))

    conn.commit()
    cursor.close()
    conn.close()


# =========================
# SIGNES ASTROLOGIQUES
# =========================

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


# =========================
# MENUS
# =========================

def main_menu():

    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True
    )

    btn1 = types.KeyboardButton(
        "🔮 Horoscope du jour"
    )

    btn2 = types.KeyboardButton(
        "❤️ Compatibilité amoureuse"
    )

    btn3 = types.KeyboardButton(
        "⭐ Bonus quotidien"
    )

    btn4 = types.KeyboardButton(
        "💎 Mode Premium"
    )

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


# =========================
# /START
# =========================

@bot.message_handler(commands=["start"])
def start(message):

    create_or_update_user(message)

    user_id = message.from_user.id

    sign = get_user_sign(user_id)

    if not sign:

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
            f"Ton signe : {sign}\n\n"
            "Que souhaites-tu découvrir aujourd'hui ?",

            reply_markup=main_menu()
        )


# =========================
# ENREGISTRER LE SIGNE
# =========================

@bot.message_handler(
    func=lambda message: message.text in SIGNS
)
def choose_sign(message):

    create_or_update_user(message)

    user_id = message.from_user.id

    save_user_sign(
        user_id,
        message.text
    )

    bot.send_message(
        message.chat.id,

        f"✅ Ton signe est enregistré : {message.text}\n\n"
        "Bienvenue dans ton univers AstroVibe ✨",

        reply_markup=main_menu()
    )


# =========================
# HOROSCOPE
# =========================

def show_horoscope(message):

    create_or_update_user(message)

    user_id = message.from_user.id

    sign = get_user_sign(user_id)

    if not sign:

        bot.send_message(
            message.chat.id,

            "✨ Je dois d'abord connaître ton signe astrologique.",

            reply_markup=signs_menu()
        )

        return

    bot.send_message(
        message.chat.id,

        "🔮 Horoscope du jour\n\n"
        f"{sign}\n\n"
        "✨ Ton horoscope personnalisé arrive bientôt.\n\n"
        "Nous allons construire cette partie à l'étape suivante."
    )


@bot.message_handler(commands=["horoscope"])
def horoscope_command(message):

    show_horoscope(message)


# =========================
# POINTS
# =========================

@bot.message_handler(commands=["points"])
def points_command(message):

    create_or_update_user(message)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT points, level, streak
        FROM users
        WHERE telegram_id = %s
        """,
        (message.from_user.id,)
    )

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:

        points, level, streak = result

        bot.send_message(
            message.chat.id,

            "⭐ Ton profil AstroVibe\n\n"
            f"🏆 Points : {points}\n"
            f"🌟 Niveau : {level}\n"
            f"🔥 Série : {streak} jour(s)"
        )


# =========================
# MENU PRINCIPAL
# =========================

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
            "Le système de bonus permanent arrive à la prochaine étape."
        )

    elif message.text == "💎 Mode Premium":

        bot.send_message(
            message.chat.id,

            "💎 AstroVibe Premium\n\n"
            "Les fonctionnalités Premium arrivent bientôt."
        )


# =========================
# INITIALISATION DATABASE
# =========================

init_database()


# =========================
# TELEGRAM
# =========================

threading.Thread(
    target=bot.infinity_polling,
    daemon=True
).start()


# =========================
# SERVEUR WEB RENDER
# =========================

app = Flask(__name__)


@app.route("/")
def home():

    return "AstroVibe is running ✨"


if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            10000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port
    )
