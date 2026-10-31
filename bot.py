import os
import threading
from datetime import datetime, timedelta, timezone

import psycopg2
import telebot
from flask import Flask
from telebot import types
from horoscope_engine import generate_daily_horoscope
from compatibility_engine import generate_compatibility
from translations import get_text



# ==================================================
# CONFIGURATION
# ==================================================

TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

if not TOKEN:
    raise RuntimeError(
        "BOT_TOKEN manquant dans les variables Render."
    )

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL manquant dans les variables Render."
    )

bot = telebot.TeleBot(TOKEN)


# ==================================================
# BASE DE DONNEES NEON
# ==================================================

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)


def init_database():
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    telegram_id BIGINT PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    sign TEXT,
                    points INTEGER NOT NULL DEFAULT 0,
                    level INTEGER NOT NULL DEFAULT 1,
                    streak INTEGER NOT NULL DEFAULT 0,
                    last_bonus DATE,
                    premium BOOLEAN NOT NULL DEFAULT FALSE,
                    language TEXT NOT NULL DEFAULT 'fr',
                    created_at TIMESTAMP
                        NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Ces commandes sécurisent aussi une ancienne table.
            cursor.execute("""
                ALTER TABLE users
                ADD COLUMN IF NOT EXISTS points
                INTEGER NOT NULL DEFAULT 0
            """)

            cursor.execute("""
                ALTER TABLE users
                ADD COLUMN IF NOT EXISTS level
                INTEGER NOT NULL DEFAULT 1
            """)

            cursor.execute("""
                ALTER TABLE users
                ADD COLUMN IF NOT EXISTS streak
                INTEGER NOT NULL DEFAULT 0
            """)

            cursor.execute("""
                ALTER TABLE users
                ADD COLUMN IF NOT EXISTS last_bonus
                DATE
            """)

            cursor.execute("""
                ALTER TABLE users
                ADD COLUMN IF NOT EXISTS premium
                BOOLEAN NOT NULL DEFAULT FALSE
            """)

    print("Base de donnees AstroVibe initialisee.")


def create_or_update_user(message):
    user = message.from_user

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
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


def get_user_sign(user_id):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT sign
                FROM users
                WHERE telegram_id = %s
                """,
                (user_id,)
            )

            result = cursor.fetchone()

    if result:
        return result[0]

    return None


def save_user_sign(user_id, sign):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE users
                SET sign = %s
                WHERE telegram_id = %s
            """, (
                sign,
                user_id
            ))

def get_user_language(user_id):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT language
                FROM users
                WHERE telegram_id = %s
                """,
                (user_id,)
            )

            result = cursor.fetchone()

if result:
    return result[0]

return "fr"



def save_user_language(user_id, language):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE users
                SET language = %s
                WHERE telegram_id = %s
                """,
                (
                    language,
                    user_id
                )
            )

def calculate_level(points):
    if points >= 1000:
        return 6
    if points >= 500:
        return 5
    if points >= 250:
        return 4
    if points >= 100:
        return 3
    if points >= 40:
        return 2

    return 1


def get_level_name(level):
    level_names = {
        1: "Observateur céleste",
        2: "Explorateur du Zodiaque",
        3: "Gardien des étoiles",
        4: "Oracle cosmique",
        5: "Maître du Zodiaque",
        6: "Légende astrale"
    }

    return level_names.get(
        level,
        "Observateur céleste"
    )


def get_next_level_target(level):
    targets = {
        1: 40,
        2: 100,
        3: 250,
        4: 500,
        5: 1000
    }

    return targets.get(level)


def get_user_profile(user_id):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                    sign,
                    points,
                    level,
                    streak,
                    last_bonus,
                    premium
                FROM users
                WHERE telegram_id = %s
            """, (
                user_id,
            ))

            result = cursor.fetchone()

    return result


# ==================================================
# BONUS QUOTIDIEN
# ==================================================

def claim_daily_bonus(user_id):
    today = datetime.now(timezone.utc).date()
    yesterday = today - timedelta(days=1)

    with get_db_connection() as conn:
        with conn.cursor() as cursor:

            # Verrouille la ligne durant la transaction.
            cursor.execute("""
                SELECT
                    points,
                    level,
                    streak,
                    last_bonus
                FROM users
                WHERE telegram_id = %s
                FOR UPDATE
            """, (
                user_id,
            ))

            result = cursor.fetchone()

            if not result:
                return {
                    "status": "user_not_found"
                }

            current_points = result[0] or 0
            old_level = result[1] or 1
            current_streak = result[2] or 0
            last_bonus = result[3]

            if last_bonus == today:
                return {
                    "status": "already_claimed",
                    "points": current_points,
                    "level": old_level,
                    "streak": current_streak
                }

            if last_bonus == yesterday:
                new_streak = current_streak + 1
            else:
                new_streak = 1

            base_reward = 10

            # +2 par jour consécutif après le premier,
            # avec un maximum de +10.
            streak_reward = min(
                max(new_streak - 1, 0) * 2,
                10
            )

            total_reward = base_reward + streak_reward
            new_points = current_points + total_reward
            new_level = calculate_level(new_points)

            cursor.execute("""
                UPDATE users
                SET
                    points = %s,
                    level = %s,
                    streak = %s,
                    last_bonus = %s
                WHERE telegram_id = %s
            """, (
                new_points,
                new_level,
                new_streak,
                today,
                user_id
            ))

            return {
                "status": "claimed",
                "base_reward": base_reward,
                "streak_reward": streak_reward,
                "total_reward": total_reward,
                "points": new_points,
                "streak": new_streak,
                "old_level": old_level,
                "level": new_level,
                "level_up": new_level > old_level
            }


# ==================================================
# SIGNES ASTROLOGIQUES
# ==================================================

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
compatibility_requests = set()


# ==================================================
# MENUS
# ==================================================

def main_menu():
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True
    )

    markup.row(
        types.KeyboardButton(
            "🔮 Horoscope du jour"
        ),
        types.KeyboardButton(
            "❤️ Compatibilité amoureuse"
        )
    )

    markup.row(
        types.KeyboardButton(
            "⭐ Bonus quotidien"
        ),
        types.KeyboardButton(
            "💎 Mode Premium"
        )
    )

    return markup


def signs_menu():
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
    )

    for index in range(0, len(SIGNS), 2):
        markup.row(
            types.KeyboardButton(
                SIGNS[index]
            ),
            types.KeyboardButton(
                SIGNS[index + 1]
            )
        )

    return markup


# ==================================================
# START
# ==================================================

@bot.message_handler(commands=["start"])
def start(message):
    create_or_update_user(message)

    user_id = message.from_user.id
    sign = get_user_sign(user_id)

    if not sign:
        bot.send_message(
            message.chat.id,
            "✨ Bienvenue dans AstroVibe ✨\n\n"
            "Pour commencer, quel est ton signe "
            "astrologique ?",
            reply_markup=signs_menu()
        )
        return

    bot.send_message(
        message.chat.id,
        "✨ Bienvenue dans AstroVibe ✨\n\n"
        f"Ton signe : {sign}\n\n"
        "Que souhaites-tu découvrir aujourd'hui ?",
        reply_markup=main_menu()
    )


# ==================================================
# CHOIX DU SIGNE
# ==================================================


@bot.message_handler(
    func=lambda message: message.text in SIGNS
)
def choose_sign(message):
    create_or_update_user(message)

    user_id = message.from_user.id

    if user_id in compatibility_requests:
        compatibility_requests.discard(user_id)

        first_sign = get_user_sign(user_id)
        second_sign = message.text

        if not first_sign:
            bot.send_message(
                message.chat.id,
                "✨ Je dois d'abord connaître ton signe astrologique.",
                reply_markup=signs_menu()
            )
            return

        compatibility = generate_compatibility(
            first_sign,
            second_sign
        )

        if not compatibility:
            bot.send_message(
                message.chat.id,
                "Une erreur est survenue pendant la préparation "
                "de ta compatibilité."
            )
            return

        bot.send_message(
            message.chat.id,
            compatibility,
            reply_markup=main_menu()
        )
        return

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



# ==================================================
# HOROSCOPE
# ==================================================

def show_horoscope(message):
    create_or_update_user(message)

    sign = get_user_sign(
        message.from_user.id
    )

    if not sign:
        bot.send_message(
            message.chat.id,
            "✨ Je dois d'abord connaître ton signe "
            "astrologique.",
            reply_markup=signs_menu()
        )
        return

    horoscope = generate_daily_horoscope(sign)

    if not horoscope:
        bot.send_message(
            message.chat.id,
            "Une erreur est survenue pendant la "
            "préparation de ton horoscope."
        )
        return

    bot.send_message(
        message.chat.id,
        horoscope,
        reply_markup=main_menu()
    )


@bot.message_handler(commands=["horoscope"])
def horoscope_command(message):
    show_horoscope(message)


# ==================================================
# PROFIL ET POINTS
# ==================================================

def show_points(message):
    create_or_update_user(message)

    profile = get_user_profile(
        message.from_user.id
    )

    if not profile:
        bot.send_message(
            message.chat.id,
            "Impossible de charger ton profil."
        )
        return

    sign, points, level, streak, last_bonus, premium = profile

    level_name = get_level_name(level)
    next_target = get_next_level_target(level)

    if next_target:
        remaining = max(
            next_target - points,
            0
        )

        progression_text = (
            f"📈 Prochain niveau dans "
            f"{remaining} point(s)"
        )
    else:
        progression_text = (
            "👑 Niveau maximal atteint"
        )

    premium_text = (
        "Actif 💎"
        if premium
        else "Gratuit"
    )

    bot.send_message(
        message.chat.id,
        "🌌 Ton profil AstroVibe\n\n"
        f"🔮 Signe : {sign or 'Non renseigné'}\n"
        f"⭐ Points : {points}\n"
        f"🏆 Niveau {level} : {level_name}\n"
        f"🔥 Série actuelle : {streak} jour(s)\n"
        f"💎 Statut : {premium_text}\n\n"
        f"{progression_text}",
        reply_markup=main_menu()
    )


@bot.message_handler(commands=["points"])
def points_command(message):
    show_points(message)


# ==================================================
# BONUS QUOTIDIEN
# ==================================================

def show_daily_bonus(message):
    create_or_update_user(message)

    result = claim_daily_bonus(
        message.from_user.id
    )

    if result["status"] == "user_not_found":
        bot.send_message(
            message.chat.id,
            "Impossible de charger ton profil. "
            "Envoie /start puis réessaie."
        )
        return

    if result["status"] == "already_claimed":
        bot.send_message(
            message.chat.id,
            "⏳ Bonus déjà récupéré\n\n"
            "Tu as déjà reçu ta récompense "
            "quotidienne aujourd'hui.\n\n"
            f"⭐ Solde : {result['points']} points\n"
            f"🔥 Série : {result['streak']} jour(s)\n\n"
            "Reviens demain pour prolonger "
            "ta série cosmique ✨",
            reply_markup=main_menu()
        )
        return

    message_text = (
        "🎁 Bonus quotidien récupéré !\n\n"
        f"⭐ Bonus de base : "
        f"+{result['base_reward']} points\n"
    )

    if result["streak_reward"] > 0:
        message_text += (
            f"🔥 Bonus de série : "
            f"+{result['streak_reward']} points\n"
        )

    message_text += (
        f"\n✨ Récompense totale : "
        f"+{result['total_reward']} points\n"
        f"🏆 Nouveau solde : "
        f"{result['points']} points\n"
        f"🔥 Série actuelle : "
        f"{result['streak']} jour(s)"
    )

    if result["level_up"]:
        level_name = get_level_name(
            result["level"]
        )

        message_text += (
            "\n\n🌟 NOUVEAU NIVEAU !\n"
            f"Tu atteins le niveau "
            f"{result['level']} : {level_name}"
        )

    message_text += (
        "\n\nReviens demain pour poursuivre "
        "ton ascension parmi les étoiles ✨"
    )

    bot.send_message(
        message.chat.id,
        message_text,
        reply_markup=main_menu()
    )


@bot.message_handler(commands=["bonus"])
def bonus_command(message):
    show_daily_bonus(message)


# ==================================================
# MENU PRINCIPAL
# ==================================================

@bot.message_handler(func=lambda message: True)
def menu(message):

    if message.text == "🔮 Horoscope du jour":
        show_horoscope(message)

    elif message.text == "❤️ Compatibilité amoureuse":
        create_or_update_user(message)

        user_id = message.from_user.id
        first_sign = get_user_sign(user_id)

        if not first_sign:
            bot.send_message(
                message.chat.id,
                "✨ Je dois d'abord connaître ton signe astrologique.",
                reply_markup=signs_menu()
            )
            return

        compatibility_requests.add(user_id)

        bot.send_message(
            message.chat.id,
            "❤️ Compatibilité amoureuse\n\n"
            f"Ton signe : {first_sign}\n\n"
            "Choisis maintenant le signe de l'autre personne :",
            reply_markup=signs_menu()
        )


    elif message.text == "⭐ Bonus quotidien":
        show_daily_bonus(message)

    elif message.text == "💎 Mode Premium":
        bot.send_message(
            message.chat.id,
            "💎 AstroVibe Premium\n\n"
            "Les fonctionnalités Premium "
            "arrivent bientôt."
        )

    else:
        bot.send_message(
            message.chat.id,
            "Je n'ai pas reconnu cette demande.\n\n"
            "Choisis une option dans le menu ✨",
            reply_markup=main_menu()
        )


# ==================================================
# INITIALISATION
# ==================================================

init_database()


# ==================================================
# TELEGRAM
# ==================================================

def run_telegram_bot():
    bot.infinity_polling(
        skip_pending=True,
        timeout=30,
        long_polling_timeout=30
    )


threading.Thread(
    target=run_telegram_bot,
    daemon=True
).start()


# ==================================================
# SERVEUR WEB RENDER
# ==================================================

app = Flask(__name__)


@app.route("/")
def home():
    return "AstroVibe is running ✨"


@app.route("/health")
def health():
    return {
        "status": "ok",
        "service": "AstroVibe"
    }


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
