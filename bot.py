import os
import threading
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

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
from personal_profile_engine import generate_personal_profile
from birth_location_engine import resolve_birth_location, format_location_label

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
def get_birth_info(user_id):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    birth_date,
                    birth_time,
                    birth_time_known,
                    birth_place,
                    birth_timezone,
                    birth_latitude,
                    birth_longitude
                FROM users
                WHERE telegram_id = %s
                """,
                (user_id,)
            )

            result = cursor.fetchone()

    if not result:
        return None

    return {
        "birth_date": result[0],
        "birth_time": result[1],
        "birth_time_known": result[2],
        "birth_place": result[3],
        "birth_timezone": result[4],
        "birth_latitude": result[5],
        "birth_longitude": result[6],
    }


def has_birth_info(user_id):
    birth_info = get_birth_info(user_id)

    if not birth_info:
        return False

    return bool(
        birth_info["birth_date"]
        and birth_info["birth_place"]
        and birth_info["birth_time_known"] is not None
    )


def save_birth_info(
    user_id,
    birth_date,
    birth_time,
    birth_time_known,
    birth_place,
    birth_timezone=None,
    birth_latitude=None,
    birth_longitude=None
):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE users
                SET
                    birth_date = %s,
                    birth_time = %s,
                    birth_time_known = %s,
                    birth_place = %s,
                    birth_timezone = %s,
                    birth_latitude = %s,
                    birth_longitude = %s
                WHERE telegram_id = %s
                """,
                (
                    birth_date,
                    birth_time,
                    birth_time_known,
                    birth_place,
                    birth_timezone,
                    birth_latitude,
                    birth_longitude,
                    user_id
                )
            )
def send_personal_profile(chat_id, user_id):
    language = get_user_language(user_id)
    sign = get_user_sign(user_id)
    birth_info = get_birth_info(user_id)

    if not sign:
        bot.send_message(
            chat_id,
            "❌ Aucun signe astrologique enregistré."
            if language == "fr"
            else "❌ No zodiac sign is currently saved."
        )
        return

    if not birth_info or not has_birth_info(user_id):
        bot.send_message(
            chat_id,
            (
                "🎂 Tes informations de naissance sont nécessaires "
                "pour générer ton Profil AstroVibe Personnel.\n\n"
                "Va dans ⚙️ Paramètres → "
                "🎂 Mes informations de naissance."
            )
            if language == "fr"
            else (
                "🎂 Your birth information is required "
                "to generate your AstroVibe Personal Profile.\n\n"
                "Go to ⚙️ Settings → 🎂 My Birth Information."
            )
        )
        return

    try:
        profile = generate_personal_profile(
            sign=sign,
            language=language,
            birth_date=birth_info["birth_date"],
            birth_time=birth_info["birth_time"],
            birth_time_known=birth_info["birth_time_known"],
            birth_place=birth_info["birth_place"],
        )

    except ValueError as error:
        bot.send_message(
            chat_id,
            (
                "❌ Le Profil AstroVibe Personnel n'est pas encore "
                f"disponible : {error}"
            )
            if language == "fr"
            else (
                "❌ The AstroVibe Personal Profile is not available "
                f"yet: {error}"
            )
        )
        return

    profile_sections = profile.split("\n\n")

    current_message = ""

    for section in profile_sections:
        candidate = (
            section
            if not current_message
            else current_message + "\n\n" + section
        )

        if len(candidate) > 3500:
            if current_message:
                bot.send_message(
                    chat_id,
                    current_message
                )

            current_message = section

        else:
            current_message = candidate

    if current_message:
        bot.send_message(
            chat_id,
            current_message
        )

    bot.send_message(
        chat_id,
        (
            "✨ Fin de ton Profil AstroVibe Personnel."
            if language == "fr"
            else "✨ End of your AstroVibe Personal Profile."
        ),
        reply_markup=settings_menu(language)
    )

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
def get_notification_settings(user_id):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    notifications_enabled,
                    notification_time,
                    timezone,
                    last_notification_date
                FROM users
                WHERE telegram_id = %s
                """,
                (user_id,)
            )

            result = cursor.fetchone()

    if result:
        return {
            "enabled": result[0],
            "time": result[1],
            "timezone": result[2],
            "last_notification_date": result[3]
        }

    return {
        "enabled": False,
        "time": None,
        "timezone": None,
        "last_notification_date": None
    }


def set_notifications_enabled(user_id, enabled):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE users
                SET notifications_enabled = %s
                WHERE telegram_id = %s
                """,
                (
                    enabled,
                    user_id
                )
            )
def set_notification_time(user_id, notification_time):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE users
                SET notification_time = %s
                WHERE telegram_id = %s
                """,
                (
                    notification_time,
                    user_id
                )
            )
def set_notification_timezone(user_id, timezone_name):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE users
                SET timezone = %s
                WHERE telegram_id = %s
                """,
                (
                    timezone_name,
                    user_id
                )
            )
def get_notification_candidates():
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    telegram_id,
                    sign,
                    language,
                    notification_time,
                    timezone,
                    last_notification_date
                FROM users
                WHERE premium = TRUE
                  AND notifications_enabled = TRUE
                  AND notification_time IS NOT NULL
                  AND timezone IS NOT NULL
                """
            )

            return cursor.fetchall()


def mark_notification_sent(
    user_id,
    local_date
):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE users
                SET last_notification_date = %s
                WHERE telegram_id = %s
                """,
                (
                    local_date,
                    user_id
                )
            )


def build_morning_notification(
    sign,
    language
):
    if language == "en":
        display_sign = next(
            (
                english_sign
                for english_sign, french_sign in SIGNS_EN.items()
                if french_sign == sign
            ),
            sign
        )

        return (
            "☀️ GOOD MORNING\n\n"
            f"{display_sign}\n\n"
            "Your Premium cosmic forecast is ready ✨\n\n"
            "Discover today's dominant energy, love insights, "
            "career guidance, opportunities and points of attention.\n\n"
            "☀️ Open My Daily Astro+ in AstroVibe."
        )

    return (
        "☀️ BONJOUR\n\n"
        f"{sign}\n\n"
        "Tes prévisions cosmiques Premium sont prêtes ✨\n\n"
        "Découvre l'énergie dominante de ta journée, "
        "tes tendances en amour, tes ambitions, "
        "tes opportunités et tes points de vigilance.\n\n"
        "☀️ Ouvre Mon Astro du jour + dans AstroVibe."
    )


def run_due_notifications():
    utc_now = datetime.now(
        timezone.utc
    )

    candidates = get_notification_candidates()

    sent_count = 0
    skipped_count = 0
    error_count = 0

    for candidate in candidates:
        (
            user_id,
            sign,
            language,
            notification_time,
            timezone_name,
            last_notification_date
        ) = candidate

        try:
            user_timezone = ZoneInfo(
                timezone_name
            )

            local_now = utc_now.astimezone(
                user_timezone
            )

            local_date = local_now.date()

            local_time = local_now.time().replace(
                second=0,
                microsecond=0,
                tzinfo=None
            )

            configured_time = notification_time.replace(
                second=0,
                microsecond=0
            )

            if last_notification_date == local_date:
                skipped_count += 1
                continue

            if local_time < configured_time:
                skipped_count += 1
                continue

            if not sign:
                skipped_count += 1
                continue

            if language not in ("fr", "en"):
                language = "fr"

            message_text = build_morning_notification(
                sign,
                language
            )

            bot.send_message(
                user_id,
                message_text,
                reply_markup=premium_menu(
                    language
                )
            )

            mark_notification_sent(
                user_id,
                local_date
            )

            sent_count += 1

        except ZoneInfoNotFoundError:
            print(
                "Invalid notification timezone:",
                user_id,
                timezone_name
            )
            error_count += 1

        except Exception as error:
            print(
                "Notification error:",
                user_id,
                str(error)
            )
            error_count += 1

    return {
        "status": "ok",
        "candidates": len(candidates),
        "sent": sent_count,
        "skipped": skipped_count,
        "errors": error_count
    }

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
premium_compatibility_requests = set()
birth_info_requests = {}


# ==================================================
# MENUS
# ==================================================
def birth_time_choice_menu(language="fr"):
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
    )

    markup.row(
        types.KeyboardButton(
            get_text(language, "birth_time_known_button")
        )
    )

    markup.row(
        types.KeyboardButton(
            get_text(language, "birth_time_unknown_button")
        )
    )

    markup.row(
        types.KeyboardButton(
            get_text(language, "back_button")
        )
    )

    return markup


def birth_info_confirmation_menu(language="fr"):
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
    )

    markup.row(
        types.KeyboardButton(
            get_text(language, "birth_info_confirm_button")
        ),
        types.KeyboardButton(
            get_text(language, "birth_info_edit_button")
        )
    )

    markup.row(
        types.KeyboardButton(
            get_text(language, "back_button")
        )
    )

    return markup


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
            get_text(language, "settings_sign_button")
        )
    )

    markup.row(
        types.KeyboardButton(
            get_text(language, "language_button")
        )
    )

    markup.row(
        types.KeyboardButton(
            get_text(language, "birth_info_button")
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
def notifications_menu(language="fr", enabled=False):
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True
    )

    if enabled:
        toggle_button = get_text(
            language,
            "notifications_disable_button"
        )
    else:
        toggle_button = get_text(
            language,
            "notifications_enable_button"
        )

    markup.row(
        types.KeyboardButton(
            toggle_button
        )
    )

    markup.row(
        types.KeyboardButton(
            get_text(
                language,
                "notifications_time_button"
            )
        ),
        types.KeyboardButton(
            get_text(
                language,
                "notifications_timezone_button"
            )
        )
    )

    markup.row(
        types.KeyboardButton(
            get_text(
                language,
                "back_button"
            )
        )
    )

    return markup
def notification_time_menu(language="fr"):
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True
    )

    markup.row(
        types.KeyboardButton("07:00"),
        types.KeyboardButton("08:00")
    )

    markup.row(
        types.KeyboardButton("09:00"),
        types.KeyboardButton("10:00")
    )

    markup.row(
        types.KeyboardButton(
            get_text(language, "back_button")
        )
    )

    return markup
def notification_timezone_menu(language="fr"):
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True
    )

    markup.row(
        types.KeyboardButton(
            "🇮🇸 Atlantic/Reykjavik"
        ),
        types.KeyboardButton(
            "🇫🇷 Europe/Paris"
        )
    )

    markup.row(
        types.KeyboardButton(
            "🇬🇧 Europe/London"
        ),
        types.KeyboardButton(
            "🇺🇸 America/New_York"
        )
    )

    markup.row(
        types.KeyboardButton(
            get_text(
                language,
                "back_button"
            )
        )
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

# ============================================
# TEST TEMPORAIRE DU PROFIL ASTROVIBE
# ============================================


@bot.message_handler(commands=["profile_test"])
def profile_test(message):
    create_or_update_user(message)

    user_id = message.from_user.id
    language = get_user_language(user_id)

    if language == "en":
        loading_message = (
            "✨ Generating your AstroVibe Personal Profile..."
        )
    else:
        loading_message = (
            "✨ Génération de ton Profil AstroVibe Personnel..."
        )

    bot.send_message(
        message.chat.id,
        loading_message
    )

    send_personal_profile(
        message.chat.id,
        user_id
    )
# ============================================
# TEST TEMPORAIRE DE LOCALISATION
# ============================================

@bot.message_handler(commands=["location_test"])
def location_test(message):
    create_or_update_user(message)

    user_id = message.from_user.id
    language = get_user_language(user_id)

    parts = message.text.split(
        maxsplit=1
    )

    if len(parts) < 2:
        bot.send_message(
            message.chat.id,
            (
                "📍 Utilisation : /location_test Paris"
                if language == "fr"
                else "📍 Usage: /location_test Paris"
            )
        )
        return

    city_query = parts[1].strip()

    bot.send_message(
        message.chat.id,
        (
            f"🔎 Recherche du lieu : {city_query}..."
            if language == "fr"
            else f"🔎 Searching for location: {city_query}..."
        )
    )

    result = resolve_birth_location(
        city_query
    )

    status = result.get(
        "status"
    )

    if status == "resolved":
        location = result[
            "location"
        ]

        bot.send_message(
            message.chat.id,
            (
                "✅ Lieu trouvé\n\n"
                f"📍 {format_location_label(location, language)}\n"
                f"🌐 Latitude : {location['latitude']}\n"
                f"🌐 Longitude : {location['longitude']}\n"
                f"🕐 Fuseau : {location['timezone']}"
            )
            if language == "fr"
            else (
                "✅ Location found\n\n"
                f"📍 {format_location_label(location, language)}\n"
                f"🌐 Latitude: {location['latitude']}\n"
                f"🌐 Longitude: {location['longitude']}\n"
                f"🕐 Time zone: {location['timezone']}"
            )
        )
        return

    if status == "ambiguous":
        choices = result.get(
            "choices",
            []
        )

        lines = []

        for index, location in enumerate(
            choices,
            start=1
        ):
            lines.append(
                f"{index}. "
                f"{format_location_label(location, language)}"
            )

        choices_text = "\n".join(
            lines
        )

        bot.send_message(
            message.chat.id,
            (
                "⚠️ Plusieurs lieux correspondent à ta recherche.\n\n"
                f"{choices_text}\n\n"
                "Aucun lieu n'a été sélectionné automatiquement."
            )
            if language == "fr"
            else (
                "⚠️ Several locations match your search.\n\n"
                f"{choices_text}\n\n"
                "No location was selected automatically."
            )
        )
        return

    if status == "not_found":
        bot.send_message(
            message.chat.id,
            (
                "❌ Aucun lieu correspondant n'a été trouvé."
                if language == "fr"
                else "❌ No matching location was found."
            )
        )
        return

    bot.send_message(
        message.chat.id,
        (
            "❌ La recherche du lieu est temporairement indisponible.\n\n"
            f"Diagnostic : {status}"
        )
        if language == "fr"
        else (
            "❌ Location search is temporarily unavailable.\n\n"
            f"Diagnostic: {status}"
        )
    )

# ============================================
# START
# ============================================




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
    if user_id in premium_compatibility_requests:
        premium_compatibility_requests.discard(user_id)

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

        result = generate_premium_feature(
            feature="compatibility",
            sign=first_sign,
            second_sign=second_sign,
            language=language,
            user_id=user_id
        )

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
                "your Premium compatibility."
            )
        else:
            error_text = (
                "Une erreur est survenue pendant la préparation "
                "de ta compatibilité Premium."
            )

        bot.send_message(
            message.chat.id,
            error_text,
            reply_markup=premium_menu(language)
        )
        return

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

    premium_daily_buttons = (
        "☀️ Mon Astro du jour +",
        "☀️ My Daily Astro+"
    )

    premium_month_buttons = (
        "🌙 Mon mois",
        "🌙 My Month"
    )

    premium_year_buttons = (
        "🌟 Mon année",
        "🌟 My Year"
    )
    premium_compatibility_buttons = (
        "❤️ Compatibilité Premium",
        "❤️ Premium Compatibility"
    )
    premium_notifications_buttons = (
        "🔔 Notifications",
    )

    premium_subscription_buttons = (
        "💎 Mon abonnement",
        "💎 My Subscription"
    )

    notifications_enable_buttons = (
        "🔔 Activer",
        "🔔 Enable"
    )

    notifications_disable_buttons = (
        "🔕 Désactiver",
        "🔕 Disable"
    )
    notifications_time_buttons = (
        "⏰ Modifier l'heure",
        "⏰ Change time"
    )

    notification_time_choices = (
        "07:00",
        "08:00",
        "09:00",
        "10:00"
    )
    notifications_timezone_buttons = (
        "🌐 Fuseau horaire",
        "🌐 Time zone"
    )

    notification_timezone_choices = {
        "🇮🇸 Atlantic/Reykjavik": "Atlantic/Reykjavik",
        "🇫🇷 Europe/Paris": "Europe/Paris",
        "🇬🇧 Europe/London": "Europe/London",
        "🇺🇸 America/New_York": "America/New_York"
    }



    language_buttons = (
        "🌍 Langue",
        "🌍 Language"
    )
    settings_sign_buttons = (
        "♈ Mon signe",
        "♈ My Zodiac Sign"
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
    elif message.text in premium_daily_buttons:
        if not is_premium(user_id):
            show_premium_locked(message)
            return

        sign = get_user_sign(user_id)

        result = generate_premium_feature(
            feature="daily",
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

        error_text = (
            "Une erreur est survenue pendant la préparation "
            "de ton Astro du jour +."
            if language == "fr"
            else
            "An error occurred while preparing your Daily Astro+."
        )

        bot.send_message(
            message.chat.id,
            error_text,
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

    elif message.text in premium_month_buttons:
        if not is_premium(user_id):
            show_premium_locked(message)
            return

        sign = get_user_sign(user_id)

        result = generate_premium_feature(
            feature="monthly",
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

        error_text = (
            "Une erreur est survenue pendant la préparation "
            "de tes prévisions du mois."
            if language == "fr"
            else
            "An error occurred while preparing "
            "your monthly forecast."
        )

        bot.send_message(
            message.chat.id,
            error_text,
            reply_markup=premium_menu(language)
        )

    elif message.text in premium_year_buttons:
        if not is_premium(user_id):
            show_premium_locked(message)
            return

        sign = get_user_sign(user_id)

        result = generate_premium_feature(
            feature="yearly",
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

        error_text = (
            "Une erreur est survenue pendant la préparation "
            "de tes prévisions annuelles."
            if language == "fr"
            else
            "An error occurred while preparing "
            "your yearly forecast."
        )

        bot.send_message(
            message.chat.id,
            error_text,
            reply_markup=premium_menu(language)
        )

    elif message.text in premium_compatibility_buttons:
        if not is_premium(user_id):
            show_premium_locked(message)
            return

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

        premium_compatibility_requests.add(user_id)

        if language == "en":
            display_first_sign = next(
                (
                    english_sign
                    for english_sign, french_sign in SIGNS_EN.items()
                    if french_sign == first_sign
                ),
                first_sign
            )

            message_text = (
                "💎 Premium Compatibility\n\n"
                f"Your sign: {display_first_sign}\n\n"
                "Choose the other person's zodiac sign:"
            )
        else:
            message_text = (
                "💎 Compatibilité Premium\n\n"
                f"Ton signe : {first_sign}\n\n"
                "Choisis le signe de l'autre personne :"
            )

        bot.send_message(
            message.chat.id,
            message_text,
            reply_markup=signs_menu(language)
        )
    elif message.text in premium_notifications_buttons:
        if not is_premium(user_id):
            show_premium_locked(message)
            return

        notification_settings = get_notification_settings(
            user_id
        )

        enabled = notification_settings["enabled"]
        notification_time = notification_settings["time"]
        user_timezone = notification_settings["timezone"]

        if enabled:
            status_text = get_text(
                language,
                "notifications_on"
            )
        else:
            status_text = get_text(
                language,
                "notifications_off"
            )

        if notification_time:
            time_text = notification_time.strftime("%H:%M")
        else:
            time_text = "08:00"

        if user_timezone:
            timezone_text = user_timezone
        else:
            timezone_text = get_text(
                language,
                "notifications_no_timezone"
            )

        message_text = (
            get_text(
                language,
                "notifications_title"
            )
            + "\n\n"
            + get_text(
                language,
                "notifications_morning"
            )
            + "\n\n"
            + get_text(
                language,
                "notifications_status",
                status=status_text
            )
            + "\n"
            + get_text(
                language,
                "notifications_time",
                time=time_text
            )
            + "\n"
            + get_text(
                language,
                "notifications_timezone",
                timezone=timezone_text
            )
        )

        bot.send_message(
            message.chat.id,
            message_text,
            reply_markup=notifications_menu(
                language,
                enabled
            )
        )
    elif message.text in notifications_enable_buttons:
        if not is_premium(user_id):
            show_premium_locked(message)
            return

        set_notifications_enabled(
            user_id,
            True
        )

        notification_settings = get_notification_settings(
            user_id
        )

        bot.send_message(
            message.chat.id,
            (
                "✅ Notifications activées."
                if language == "fr"
                else "✅ Notifications enabled."
            ),
            reply_markup=notifications_menu(
                language,
                notification_settings["enabled"]
            )
        )

    elif message.text in notifications_disable_buttons:
        if not is_premium(user_id):
            show_premium_locked(message)
            return

        set_notifications_enabled(
            user_id,
            False
        )

        notification_settings = get_notification_settings(
            user_id
        )

        bot.send_message(
            message.chat.id,
            (
                "🔕 Notifications désactivées."
                if language == "fr"
                else "🔕 Notifications disabled."
            ),
            reply_markup=notifications_menu(
                language,
                notification_settings["enabled"]
            )
        )
    elif message.text in notifications_time_buttons:
        if not is_premium(user_id):
            show_premium_locked(message)
            return

        bot.send_message(
            message.chat.id,
            get_text(
                language,
                "notifications_choose_time"
            ),
            reply_markup=notification_time_menu(language)
        )
    elif message.text in notifications_timezone_buttons:
        if not is_premium(user_id):
            show_premium_locked(message)
            return

        bot.send_message(
            message.chat.id,
            get_text(
                language,
                "notifications_choose_timezone"
            ),
            reply_markup=notification_timezone_menu(language)
        )

    elif message.text in notification_timezone_choices:
        if not is_premium(user_id):
            show_premium_locked(message)
            return

        timezone_name = notification_timezone_choices[
            message.text
        ]

        set_notification_timezone(
            user_id,
            timezone_name
        )

        notification_settings = get_notification_settings(
            user_id
        )

        bot.send_message(
            message.chat.id,
            get_text(
                language,
                "notifications_timezone_saved",
                timezone=timezone_name
            ),
            reply_markup=notifications_menu(
                language,
                notification_settings["enabled"]
            )
        )

    elif message.text in notification_time_choices:
        if not is_premium(user_id):
            show_premium_locked(message)
            return

        set_notification_time(
            user_id,
            message.text
        )

        notification_settings = get_notification_settings(
            user_id
        )

        bot.send_message(
            message.chat.id,
            get_text(
                language,
                "notifications_time_saved",
                time=message.text
            ),
            reply_markup=notifications_menu(
                language,
                notification_settings["enabled"]
            )
        )
    elif message.text in premium_subscription_buttons:
        premium_active = is_premium(user_id)

        if premium_active:
            status_text = get_text(
                language,
                "subscription_premium"
            )

            message_text = (
                get_text(
                    language,
                    "subscription_title"
                )
                + "\n\n"
                + get_text(
                    language,
                    "subscription_status",
                    status=status_text
                )
                + "\n\n"
                + get_text(
                    language,
                    "subscription_features"
                )
                + "\n\n"
                + get_text(
                    language,
                    "subscription_active"
                )
            )

        else:
            status_text = get_text(
                language,
                "subscription_free"
            )

            message_text = (
                get_text(
                    language,
                    "subscription_title"
                )
                + "\n\n"
                + get_text(
                    language,
                    "subscription_status",
                    status=status_text
                )
                + "\n\n"
                + get_text(
                    language,
                    "subscription_features"
                )
            )

        bot.send_message(
            message.chat.id,
            message_text,
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
    elif message.text == get_text(language, "birth_info_button"):
        birth_info_requests[user_id] = {
            "step": "birth_date",
            "birth_date": None,
            "birth_time": None,
            "birth_time_known": None,
            "birth_place": None,
        }

        bot.send_message(
            message.chat.id,
            get_text(language, "birth_info_intro")
            + "\n\n"
            + get_text(language, "birth_date_question")
        )

    elif user_id in birth_info_requests:
        birth_request = birth_info_requests[user_id]
        step = birth_request.get("step")

        if message.text == get_text(language, "back_button"):
            birth_info_requests.pop(user_id, None)

            bot.send_message(
                message.chat.id,
                get_text(language, "settings_title"),
                reply_markup=settings_menu(language)
            )

        elif step == "birth_date":
            try:
                parsed_date = datetime.strptime(
                    message.text.strip(),
                    "%d/%m/%Y"
                ).date()

                if parsed_date > datetime.now().date():
                    raise ValueError

                birth_request["birth_date"] = parsed_date
                birth_request["step"] = "birth_time_choice"

                bot.send_message(
                    message.chat.id,
                    get_text(language, "birth_time_question"),
                    reply_markup=birth_time_choice_menu(language)
                )

            except ValueError:
                bot.send_message(
                    message.chat.id,
                    get_text(language, "birth_date_invalid")
                )

        elif step == "birth_time_choice":
            if message.text == get_text(
                language,
                "birth_time_known_button"
            ):
                birth_request["birth_time_known"] = True
                birth_request["step"] = "birth_time"

                bot.send_message(
                    message.chat.id,
                    get_text(language, "birth_time_enter")
                )

            elif message.text == get_text(
                language,
                "birth_time_unknown_button"
            ):
                birth_request["birth_time_known"] = False
                birth_request["birth_time"] = None
                birth_request["step"] = "birth_place"

                bot.send_message(
                    message.chat.id,
                    get_text(language, "birth_place_question")
                )

            else:
                bot.send_message(
                    message.chat.id,
                    get_text(language, "birth_time_question"),
                    reply_markup=birth_time_choice_menu(language)
                )

        elif step == "birth_time":
            try:
                parsed_time = datetime.strptime(
                    message.text.strip(),
                    "%H:%M"
                ).time()

                birth_request["birth_time"] = parsed_time
                birth_request["step"] = "birth_place"

                bot.send_message(
                    message.chat.id,
                    get_text(language, "birth_place_question")
                )

            except ValueError:
                bot.send_message(
                    message.chat.id,
                    get_text(language, "birth_time_invalid")
                )

        elif step == "birth_place":
            birth_place = message.text.strip()

            if len(birth_place) < 2:
                bot.send_message(
                    message.chat.id,
                    get_text(
                        language,
                        "birth_place_invalid"
                    )
                )

            else:
                location_result = resolve_birth_location(
                    birth_place
                )

                if location_result["status"] == "resolved":
                    location = location_result["location"]

                    birth_request["birth_place"] = (
                        f"{location['name']}, "
                        f"{location['country_code']}"
                    )
                    birth_request["birth_timezone"] = (
                        location["timezone"]
                    )
                    birth_request["birth_latitude"] = (
                        location["latitude"]
                    )
                    birth_request["birth_longitude"] = (
                        location["longitude"]
                    )
                    birth_request["step"] = "confirmation"

                    birth_date_text = birth_request[
                        "birth_date"
                    ].strftime("%d/%m/%Y")

                    if birth_request["birth_time_known"]:
                        birth_time_text = birth_request[
                            "birth_time"
                        ].strftime("%H:%M")
                    else:
                        birth_time_text = (
                            "Unknown"
                            if language == "en"
                            else "Inconnue"
                        )

                    summary = get_text(
                        language,
                        "birth_info_summary",
                        birth_date=birth_date_text,
                        birth_time=birth_time_text,
                        birth_place=birth_request[
                            "birth_place"
                        ]
                    )

                    bot.send_message(
                        message.chat.id,
                        summary,
                        reply_markup=birth_info_confirmation_menu(
                            language
                        )
                    )

                elif location_result["status"] == "ambiguous":
                    choices = location_result.get(
                        "choices",
                        []
                    )

                    choice_lines = []

                    for index, location in enumerate(
                        choices,
                        start=1
                    ):
                        choice_lines.append(
                            f"{index}. "
                            f"{format_location_label(
                                location,
                                language
                            )}"
                        )

                    choices_text = "\n".join(
                        choice_lines
                    )

                    if language == "fr":
                        location_message = (
                            "⚠️ Plusieurs lieux correspondent à ce nom.\n\n"
                            f"{choices_text}\n\n"
                            "Précise la ville et le pays."
                        )
                    else:
                        location_message = (
                            "⚠️ Several locations match that name.\n\n"
                            f"{choices_text}\n\n"
                            "Please enter the city and country."
                        )

                    bot.send_message(
                        message.chat.id,
                        location_message
                    )

                elif location_result["status"] == "not_found":
                    bot.send_message(
                        message.chat.id,
                        (
                            "❌ Je n'ai pas trouvé ce lieu. "
                            "Essaie avec la ville et le pays."
                        )
                        if language == "fr"
                        else (
                            "❌ I couldn't find that location. "
                            "Try entering the city and country."
                        )
                    )

                else:
                    bot.send_message(
                        message.chat.id,
                        (
                            "❌ La recherche du lieu est temporairement "
                            "indisponible."
                        )
                        if language == "fr"
                        else (
                            "❌ Location search is temporarily unavailable."
                        )
                    )

        elif step == "confirmation":
            if message.text == get_text(
                language,
                "birth_info_confirm_button"
            ):
                save_birth_info(
                    user_id=user_id,
                    birth_date=birth_request["birth_date"],
                    birth_time=birth_request["birth_time"],
                    birth_time_known=birth_request[
                        "birth_time_known"
                    ],
                    birth_place=birth_request["birth_place"],
                    birth_timezone=birth_request[
                        "birth_timezone"
                    ],
                    birth_latitude=birth_request[
                        "birth_latitude"
                    ],
                    birth_longitude=birth_request[
                        "birth_longitude"
                    ]
                )

                birth_info_requests.pop(user_id, None)

                bot.send_message(
                    message.chat.id,
                    get_text(language, "birth_info_saved"),
                    reply_markup=settings_menu(language)
                )

            elif message.text == get_text(
                language,
                "birth_info_edit_button"
            ):
                birth_info_requests[user_id] = {
                    "step": "birth_date",
                    "birth_date": None,
                    "birth_time": None,
                    "birth_time_known": None,
                    "birth_place": None,
                }

                bot.send_message(
                    message.chat.id,
                    get_text(language, "birth_date_question")
                )

            else:
                birth_date_text = birth_request[
                    "birth_date"
                ].strftime("%d/%m/%Y")

                if birth_request["birth_time_known"]:

                    birth_time_text = birth_request[
                        "birth_time"
                    ].strftime("%H:%M")
                else:
                    birth_time_text = (
                        "Unknown"
                        if language == "en"
                        else "Inconnue"
                    )

                summary = get_text(
                    language,
                    "birth_info_summary",
                    birth_date=birth_date_text,
                    birth_time=birth_time_text,
                    birth_place=birth_request["birth_place"]
                )

                bot.send_message(
                    message.chat.id,
                    summary,
                    reply_markup=birth_info_confirmation_menu(
                        language
                    )
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
    elif message.text in settings_sign_buttons:
        current_sign = get_user_sign(user_id)

        if current_sign:
            if language == "en":
                display_sign = next(
                    (
                        english_sign
                        for english_sign, french_sign in SIGNS_EN.items()
                        if french_sign == current_sign
                    ),
                    current_sign
                )
                message_text = f"♈ Your current zodiac sign: {display_sign}\n\nChoose your new zodiac sign:"
            else:
                message_text = f"♈ Ton signe actuel : {current_sign}\n\nChoisis ton nouveau signe :"
        else:
            if language == "en":
                message_text = "♈ Choose your zodiac sign:"
            else:
                message_text = "♈ Choisis ton signe astrologique :"

        bot.send_message(
            message.chat.id,
            message_text,
            reply_markup=signs_menu(language)
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
@app.route(
    "/notifications/run",
    methods=["GET", "POST"]
)
def run_notifications_route():
    configured_secret = os.getenv(
        "NOTIFICATION_SECRET"
    )

    provided_secret = request.headers.get(
        "X-Notification-Secret"
    )

    if not configured_secret:
        return {
            "status": "error",
            "message": "Notification secret is not configured",
            "configured_present": False,
            "provided_present": bool(provided_secret),
            "provided_length": len(provided_secret) if provided_secret else 0,
        }, 500

    if provided_secret != configured_secret:
        return {
            "status": "forbidden",
            "configured_present": True,
            "provided_present": bool(provided_secret),
            "configured_length": len(configured_secret),
            "provided_length": len(provided_secret) if provided_secret else 0,
        }, 403

    result = run_due_notifications()

    return result, 200


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


