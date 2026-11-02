import os
import threading
from datetime import datetime, timedelta, timezone

import psycopg2
import telebot
from flask import Flask, request

from telebot import types
from horoscope_engine import generate_daily_horoscope
from horoscope_engine_en import generate_daily_horoscope_en

from compatibility_engine import generate_compatibility
from compatibility_engine_en import generate_compatibility_en
from weekly_engine import generate_weekly_horoscope
from premium_engine import generate_premium_feature

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
def is_premium(user_id):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT premium
                FROM users
                WHERE telegram_id = %s
                """,
                (user_id,)
            )

            result = cursor.fetchone()

    if result:
        return bool(result[0])

    return False

def show_premium_locked(message):
    user_id = message.from_user.id
    language = get_user_language(user_id)

    message_text = (
        get_text(
            language,
            "premium_locked_title"
        )
        + "\n\n"
        + get_text(
            language,
            "premium_locked_text"
        )
    )

    bot.send_message(
        message.chat.id,
        message_text,
        reply_markup=premium_menu(language)
    )

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
SIGNS_EN = {
    "♈ Aries": "♈ Bélier",
    "♉ Taurus": "♉ Taureau",
    "♊ Gemini": "♊ Gémeaux",
    "♋ Cancer": "♋ Cancer",
    "♌ Leo": "♌ Lion",
    "♍ Virgo": "♍ Vierge",
    "♎ Libra": "♎ Balance",
    "♏ Scorpio": "♏ Scorpion",
    "♐ Sagittarius": "♐ Sagittaire",
    "♑ Capricorn": "♑ Capricorne",
    "♒ Aquarius": "♒ Verseau",
    "♓ Pisces": "♓ Poissons"
}

compatibility_requests = set()


# ==================================================
# MENUS
# ==================================================


def main_menu(language="fr"):
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True
    )

    markup.row(
        types.KeyboardButton(
            get_text(language, "horoscope_button")
        ),
        types.KeyboardButton(
            get_text(language, "compatibility_button")
        )
    )

    markup.row(
        types.KeyboardButton(
            get_text(language, "bonus_button")
        ),
        types.KeyboardButton(
            get_text(language, "points_button")
        )
    )

    markup.row(
        types.KeyboardButton(
            get_text(language, "premium_button")
        ),
        types.KeyboardButton(
            get_text(language, "settings_button")
        )
    )

    return markup

def settings_menu(language="fr"):
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True
    )

    markup.row(
        types.KeyboardButton(
            get_text(language, "language_button")
        )
    )

    markup.row(
        types.KeyboardButton(
            get_text(language, "back_button")
        )
    )

    return markup
def premium_menu(language="fr"):
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True
    )

    markup.row(
        types.KeyboardButton(
            get_text(language, "premium_daily_button")
        ),
        types.KeyboardButton(
            get_text(language, "premium_week_button")
        )
    )

    markup.row(
        types.KeyboardButton(
            get_text(language, "premium_month_button")
        ),
        types.KeyboardButton(
            get_text(language, "premium_year_button")
        )
    )

    markup.row(
        types.KeyboardButton(
            get_text(language, "premium_compatibility_button")
        ),
        types.KeyboardButton(
            get_text(language, "premium_morning_button")
        )
    )

    markup.row(
        types.KeyboardButton(
            get_text(language, "premium_subscription_button")
        )
    )

    markup.row(
        types.KeyboardButton(
            get_text(language, "back_button")
        )
    )

    return markup

def language_menu():
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
    )

    markup.row(
        types.KeyboardButton("🇫🇷 Français"),
        types.KeyboardButton("🇬🇧 English")
    )

    return markup

def signs_menu(language="fr"):
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
    )

    if language == "en":
        signs = list(SIGNS_EN.keys())
    else:
        signs = SIGNS

    for index in range(0, len(signs), 2):
        markup.row(
            types.KeyboardButton(
                signs[index]
            ),
            types.KeyboardButton(
                signs[index + 1]
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
    language = get_user_language(user_id)

    if language == "en" and sign:
        display_sign = next(
            (
                english_sign
                for english_sign, french_sign in SIGNS_EN.items()
                if french_sign == sign
            ),
            sign
        )
    else:
        display_sign = sign

    if not sign:
        bot.send_message(
            message.chat.id,
            get_text(
                language,
                "choose_sign"
            ),
            reply_markup=signs_menu(language)
        )
        return

    bot.send_message(
        message.chat.id,
        (
            get_text(language, "welcome")
            + "\n\n"
            + get_text(
                language,
                "your_sign",
                sign=display_sign
            )
            + "\n\n"
            + get_text(
                language,
                "what_today"
            )
        ),
        reply_markup=main_menu(language)
    )




# ==================================================
# CHOIX DU SIGNE
# ==================================================

@bot.message_handler(
    func=lambda message: (
        message.text in SIGNS
        or message.text in SIGNS_EN
    )
)
def choose_sign(message):
    create_or_update_user(message)

    user_id = message.from_user.id
    language = get_user_language(user_id)

    if message.text in SIGNS_EN:
        selected_sign = SIGNS_EN[message.text]
    else:
        selected_sign = message.text

    if user_id in compatibility_requests:
        compatibility_requests.discard(user_id)

        first_sign = get_user_sign(user_id)
        second_sign = selected_sign

        if not first_sign:
            bot.send_message(
                message.chat.id,
                get_text(
                    language,
                    "need_sign"
                ),
                reply_markup=signs_menu(language)
            )
            return

        if language == "en":
            compatibility = generate_compatibility_en(
                first_sign,
                second_sign
            )
        else:
            compatibility = generate_compatibility(
                first_sign,
                second_sign
            )

        if not compatibility:
            bot.send_message(
                message.chat.id,
                get_text(
                    language,
                    "compatibility_error"
                )
            )
            return

        bot.send_message(
            message.chat.id,
            compatibility,
            reply_markup=main_menu(language)
        )
        return

    save_user_sign(
        user_id,
        selected_sign
    )

    if language == "en":
        display_sign = message.text
    else:
        display_sign = selected_sign

    bot.send_message(
        message.chat.id,
        get_text(
            language,
            "sign_saved",
            sign=display_sign
        ),
        reply_markup=main_menu(language)
    )

    



# ==================================================
# HOROSCOPE
# ==================================================

def show_horoscope(message):
    create_or_update_user(message)

    sign = get_user_sign(
        message.from_user.id
    )

    language = get_user_language(
        message.from_user.id
    )

    if not sign:
        bot.send_message(
            message.chat.id,
            get_text(
                language,
                "need_sign"
            ),
            reply_markup=signs_menu(language)

        )
        return

    if language == "en":
        horoscope = generate_daily_horoscope_en(sign)
    else:
        horoscope = generate_daily_horoscope(sign)

    if not horoscope:
        bot.send_message(
            message.chat.id,
            get_text(
                language,
                "horoscope_error"
            )
        )
        return

    bot.send_message(
        message.chat.id,
        horoscope,
        reply_markup=main_menu(language)
    )



# ==================================================
# PROFIL ET POINTS
# ==================================================

def show_points(message):
    create_or_update_user(message)

    user_id = message.from_user.id
    language = get_user_language(user_id)

    profile = get_user_profile(user_id)

    if not profile:
        bot.send_message(
            message.chat.id,
            get_text(
                language,
                "user_not_found"
            ),
            reply_markup=main_menu(language)
        )
        return

    sign, points, level, streak, last_bonus, premium = profile

    level_names_en = {
        1: "Celestial Observer",
        2: "Zodiac Explorer",
        3: "Guardian of the Stars",
        4: "Cosmic Oracle",
        5: "Zodiac Master",
        6: "Astral Legend"
    }

    sign_names_en = {
        "♈ Bélier": "♈ Aries",
        "♉ Taureau": "♉ Taurus",
        "♊ Gémeaux": "♊ Gemini",
        "♋ Cancer": "♋ Cancer",
        "♌ Lion": "♌ Leo",
        "♍ Vierge": "♍ Virgo",
        "♎ Balance": "♎ Libra",
        "♏ Scorpion": "♏ Scorpio",
        "♐ Sagittaire": "♐ Sagittarius",
        "♑ Capricorne": "♑ Capricorn",
        "♒ Verseau": "♒ Aquarius",
        "♓ Poissons": "♓ Pisces"
    }

    if language == "en":
        display_sign = sign_names_en.get(
            sign,
            sign or "Not specified"
        )

        level_name = level_names_en.get(
            level,
            "Celestial Observer"
        )

        premium_text = (
            "Active 💎"
            if premium
            else "Free"
        )
    else:
        display_sign = sign or "Non renseigné"
        level_name = get_level_name(level)

        premium_text = (
            "Actif 💎"
            if premium
            else "Gratuit"
        )

    next_target = get_next_level_target(level)

    if next_target:
        remaining = max(
            next_target - points,
            0
        )

        if language == "en":
            progression_text = (
                f"📈 Next level in {remaining} point(s)"
            )
        else:
            progression_text = (
                f"📈 Prochain niveau dans "
                f"{remaining} point(s)"
            )
    else:
        if language == "en":
            progression_text = "👑 Maximum level reached"
        else:
            progression_text = "👑 Niveau maximal atteint"

    if language == "en":
        message_text = (
            "🌌 Your AstroVibe Profile\n\n"
            f"🔮 Sign: {display_sign}\n"
            f"⭐ Points: {points}\n"
            f"🏆 Level {level}: {level_name}\n"
            f"🔥 Current streak: {streak} day(s)\n"
            f"💎 Status: {premium_text}\n\n"
            f"{progression_text}"
        )
    else:
        message_text = (
            "🌌 Ton profil AstroVibe\n\n"
            f"🔮 Signe : {display_sign}\n"
            f"⭐ Points : {points}\n"
            f"🏆 Niveau {level} : {level_name}\n"
            f"🔥 Série actuelle : {streak} jour(s)\n"
            f"💎 Statut : {premium_text}\n\n"
            f"{progression_text}"
        )

    bot.send_message(
        message.chat.id,
        message_text,
        reply_markup=main_menu(language)
    )



@bot.message_handler(commands=["points"])
def points_command(message):
    show_points(message)


# ==================================================
# BONUS QUOTIDIEN
# ==================================================
def show_daily_bonus(message):
    create_or_update_user(message)

    user_id = message.from_user.id
    language = get_user_language(user_id)

    result = claim_daily_bonus(user_id)

    if result["status"] == "user_not_found":
        bot.send_message(
            message.chat.id,
            get_text(
                language,
                "user_not_found"
            ),
            reply_markup=main_menu(language)
        )
        return

    if result["status"] == "already_claimed":
        message_text = (
            get_text(
                language,
                "bonus_already"
            )
            + "\n\n"
            + get_text(
                language,
                "balance",
                points=result["points"]
            )
            + "\n"
            + get_text(
                language,
                "bonus_streak",
                streak=result["streak"]
            )
            + "\n\n"
            + get_text(
                language,
                "bonus_return"
            )
        )

        bot.send_message(
            message.chat.id,
            message_text,
            reply_markup=main_menu(language)
        )
        return

    message_text = (
        get_text(
            language,
            "bonus_claimed_title"
        )
        + "\n\n"
        + get_text(
            language,
            "base_bonus",
            points=result["base_reward"]
        )
    )

    if result["streak_reward"] > 0:
        message_text += (
            "\n"
            + get_text(
                language,
                "streak_bonus",
                points=result["streak_reward"]
            )
        )

    message_text += (
        "\n\n"
        + get_text(
            language,
            "total_reward",
            points=result["total_reward"]
        )
        + "\n"
        + get_text(
            language,
            "new_balance",
            points=result["points"]
        )
        + "\n"
        + get_text(
            language,
            "current_streak",
            streak=result["streak"]
        )
    )

    if result["level_up"]:
        level_name = get_level_name(
            result["level"]
        )

        message_text += (
            "\n\n"
            + get_text(
                language,
                "level_up",
                level=result["level"],
                name=level_name
            )
        )

    message_text += (
        "\n\n"
        + get_text(
            language,
            "come_back_tomorrow"
        )
    )

    bot.send_message(
        message.chat.id,
        message_text,
        reply_markup=main_menu(language)
    )



@bot.message_handler(commands=["bonus"])
def bonus_command(message):
    show_daily_bonus(message)
@bot.message_handler(
    func=lambda message: message.text in (
        "🇫🇷 Français",
        "🇬🇧 English"
    )
)
def choose_language(message):
    create_or_update_user(message)

    user_id = message.from_user.id

    if message.text == "🇬🇧 English":
        language = "en"
    else:
        language = "fr"

    save_user_language(
        user_id,
        language
    )

    bot.send_message(
        message.chat.id,
        get_text(
            language,
            "language_saved"
        ),
        reply_markup=main_menu(language)
    )


# ==================================================
# MENU PRINCIPAL
# ==================================================

@bot.message_handler(func=lambda message: True)
def menu(message):
    create_or_update_user(message)

    user_id = message.from_user.id
    language = get_user_language(user_id)

    horoscope_buttons = (
        "🔮 Horoscope du jour",
        "🔮 Daily Horoscope"
    )

    compatibility_buttons = (
        "❤️ Compatibilité amoureuse",
        "❤️ Love Compatibility"
    )

    bonus_buttons = (
        "⭐ Bonus quotidien",
        "⭐ Daily Bonus"
    )


    points_buttons = (
        "🏆 Mes points",
        "🏆 My Points"
    )

    premium_buttons = (
        "💎 Mode Premium",
        "💎 Premium"
    )
    premium_week_buttons = (
        "📆 Ma semaine",
        "📆 My Week"
    )


    language_buttons = (
        "🌍 Langue",
        "🌍 Language"
    )
    settings_buttons = (
        "⚙️ Paramètres",
        "⚙️ Settings"
    )

    back_buttons = (
        "↩️ Retour",
        "↩️ Back"
    )


    if message.text in horoscope_buttons:
        show_horoscope(message)

    elif message.text in compatibility_buttons:
        first_sign = get_user_sign(user_id)

        if not first_sign:
            bot.send_message(
                message.chat.id,
                get_text(
                    language,
                    "need_sign"
                ),
                reply_markup=signs_menu(language)

            )
            return
        if language == "en":
            display_first_sign = next(
                (
                    english_sign
                    for english_sign, french_sign in SIGNS_EN.items()
                    if french_sign == first_sign
                ),
                first_sign
            )
        else:
            display_first_sign = first_sign

        compatibility_requests.add(user_id)

        bot.send_message(
            message.chat.id,
            get_text(
                language,
                "choose_partner_sign",
                sign=display_first_sign
            ),
            reply_markup=signs_menu(language)
        )


    elif message.text in bonus_buttons:
        show_daily_bonus(message)
    elif message.text in points_buttons:
        show_points(message)

    elif message.text in premium_buttons:
        bot.send_message(
            message.chat.id,
            (
                get_text(
                    language,
                    "premium_menu_title"
                )
                + "\n\n"
                + get_text(
                    language,
                    "premium_menu_intro"
                )
            ),
            reply_markup=premium_menu(language)
        )

        elif message.text in premium_week_buttons:
        if not is_premium(user_id):
            show_premium_locked(message)
            return

        sign = get_user_sign(user_id)

        result = generate_premium_feature(
            feature="weekly",
            sign=sign,
            language=language,
            user_id=user_id
        )

        if result["status"] == "missing_sign":
            bot.send_message(
                message.chat.id,
                get_text(
                    language,
                    "need_sign"
                ),
                reply_markup=signs_menu(language)
            )
            return

        if result["status"] == "success":
            bot.send_message(
                message.chat.id,
                result["content"],
                reply_markup=premium_menu(language)
            )
            return

        if language == "en":
            error_text = (
                "An error occurred while preparing "
                "your weekly forecast."
            )
        else:
            error_text = (
                "Une erreur est survenue pendant la préparation "
                "de tes prévisions de la semaine."
            )

        bot.send_message(
            message.chat.id,
            error_text,
            reply_markup=premium_menu(language)
        )



    elif message.text in settings_buttons:
        bot.send_message(
            message.chat.id,
            get_text(
                language,
                "settings_title"
            ),
            reply_markup=settings_menu(language)
        )

    elif message.text in back_buttons:
        bot.send_message(
            message.chat.id,
            get_text(
                language,
                "what_today"
            ),
            reply_markup=main_menu(language)
        )

    elif message.text in language_buttons:
        bot.send_message(
            message.chat.id,
            get_text(
                language,
                "language_title"
            ),
            reply_markup=language_menu()
        )

    else:
        bot.send_message(
            message.chat.id,
            get_text(
                language,
                "unknown_request"
            ),
            reply_markup=main_menu(language)
        )



# ==================================================
# INITIALISATION
# ==================================================

init_database()


# ==================================================
# TELEGRAM
# ==================================================




# ==================================================
# SERVEUR WEB RENDER
# ==================================================

app = Flask(__name__)
WEBHOOK_URL = "https://astrovibeai-bot.onrender.com/webhook"


@app.route("/webhook", methods=["POST"])
def telegram_webhook():
    if request.headers.get("content-type") == "application/json":
        json_string = request.get_data().decode("utf-8")

        update = telebot.types.Update.de_json(
            json_string
        )

        bot.process_new_updates(
            [update]
        )

        return "OK", 200

    return "Invalid content type", 403


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
    bot.set_webhook(
        url=WEBHOOK_URL,
        drop_pending_updates=True
    )

    print(
        f"Webhook Telegram actif : {WEBHOOK_URL}"
    )

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


