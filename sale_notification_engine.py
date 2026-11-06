# ==========================================
# ASTROVIBE SALE ADMIN NOTIFICATIONS
# ==========================================
#
# Operational notification only.
#
# This module:
# - sends one private Telegram notification;
# - performs no database write;
# - changes no Profile or Premium rights;
# - changes no Stars or points;
# - exposes no payment charge identifier.
# ==========================================

import os


ADMIN_ENV_NAMES = (
    "SUPPORT_ADMIN_TELEGRAM_ID",
    "ADMIN_TELEGRAM_ID",
    "ADMIN_CHAT_ID",
)


PRODUCTS = {
    "profile": {
        "emoji": "✨",
        "name": "Profil AstroVibe Personnel",
        "stars": 390,
        "access": "Achat unique",
    },
    "premium": {
        "emoji": "💎",
        "name": "AstroVibe Premium",
        "stars": 199,
        "access": "30 jours",
    },
}


def get_admin_chat_id():
    for variable_name in ADMIN_ENV_NAMES:
        raw_value = os.getenv(
            variable_name,
            "",
        ).strip()

        if not raw_value:
            continue

        try:
            return int(raw_value)
        except (TypeError, ValueError):
            continue

    return None


def build_sale_message(product):
    config = PRODUCTS.get(product)

    if config is None:
        raise ValueError(
            "Unsupported AstroVibe product"
        )

    return "\n".join(
        [
            "🎉 NOUVELLE VENTE ASTROVIBE",
            "",
            (
                f"{config['emoji']} "
                f"{config['name']}"
            ),
            (
                f"⭐ {config['stars']} Stars"
            ),
            (
                f"📅 {config['access']}"
            ),
            "",
            "✅ Paiement Telegram reçu",
            "⚙️ Traitement automatique lancé",
        ]
    )


def notify_sale_admin(
    bot,
    product,
):
    admin_chat_id = get_admin_chat_id()

    if admin_chat_id is None:
        print(
            "SALE ADMIN NOTIFICATION SKIPPED: "
            "admin chat id unavailable",
            flush=True,
        )

        return False

    message_text = build_sale_message(
        product
    )

    try:
        bot.send_message(
            admin_chat_id,
            message_text,
            disable_web_page_preview=True,
        )

        print(
            "SALE ADMIN NOTIFICATION SENT:",
            product,
            flush=True,
        )

        return True

    except Exception as error:
        print(
            "SALE ADMIN NOTIFICATION ERROR:",
            product,
            repr(error),
            flush=True,
        )

        return False
