
import os


# ==================================================
# ASTROVIBE PAYMENT SUPPORT - ADMIN
# ==================================================

ADMIN_ENV_NAME = "SUPPORT_ADMIN_TELEGRAM_ID"

ADMIN_REPLY_PREFIX = "/supportreply"


# ==================================================
# ADMIN CONFIGURATION
# ==================================================

def get_support_admin_id():
    raw_value = os.getenv(
        ADMIN_ENV_NAME
    )

    if not raw_value:
        return None

    try:
        admin_id = int(
            raw_value
        )
    except (
        TypeError,
        ValueError,
    ):
        return None

    if admin_id <= 0:
        return None

    return admin_id


def is_support_admin(
    telegram_user_id,
):
    admin_id = get_support_admin_id()

    if admin_id is None:
        return False

    try:
        user_id = int(
            telegram_user_id
        )
    except (
        TypeError,
        ValueError,
    ):
        return False

    return user_id == admin_id


# ==================================================
# TICKET DISPLAY HELPERS
# ==================================================

def _safe_text(
    value,
    fallback="-",
):
    if value is None:
        return fallback

    text = str(value).strip()

    if not text:
        return fallback

    return text


def get_product_label(
    product,
    language="fr",
):
    if product == "profile":
        if language == "en":
            return "Personal Profile"

        return "Profil Personnel"

    if product == "premium":
        return "Premium"

    if language == "en":
        return "Not specified"

    return "Non précisé"


def get_category_label(
    category,
    language="fr",
):
    labels = {
        "profile": {
            "fr": "Profil Personnel",
            "en": "Personal Profile",
        },
        "premium": {
            "fr": "Premium",
            "en": "Premium",
        },
        "payment": {
            "fr": "Paiement / Stars",
            "en": "Payment / Stars",
        },
        "subscription": {
            "fr": "Abonnement",
            "en": "Subscription",
        },
        "refund": {
            "fr": "Remboursement",
            "en": "Refund",
        },
        "other": {
            "fr": "Autre",
            "en": "Other",
        },
    }

    category_data = labels.get(
        category
    )

    if not category_data:
        return _safe_text(
            category
        )

    if language == "en":
        return category_data["en"]

    return category_data["fr"]


# ==================================================
# ADMIN NOTIFICATION
# ==================================================

def build_admin_ticket_message(
    ticket,
):
    if not isinstance(
        ticket,
        dict,
    ):
        raise ValueError(
            "Ticket must be a dictionary"
        )

    ticket_code = _safe_text(
        ticket.get(
            "ticket_code"
        )
    )

    user_id = _safe_text(
        ticket.get(
            "user_id"
        )
    )

    language = _safe_text(
        ticket.get(
            "language"
        )
    )

    category = get_category_label(
        ticket.get(
            "category"
        ),
        "fr",
    )

    product = get_product_label(
        ticket.get(
            "product"
        ),
        "fr",
    )

    message = _safe_text(
        ticket.get(
            "user_message"
        )
    )

    amount = ticket.get(
        "payment_amount_stars"
    )

    if amount is None:
        amount_text = (
            "Non précisé"
        )
    else:
        amount_text = (
            f"{amount} ⭐"
        )

    charge_id = _safe_text(
        ticket.get(
            "telegram_payment_charge_id"
        ),
        "Non fourni",
    )

    ai_summary = _safe_text(
        ticket.get(
            "ai_summary"
        ),
        "Pas encore disponible",
    )

    return (
        "🆘 ASTROVIBE — TICKET SUPPORT\n\n"
        f"🎫 Ticket : {ticket_code}\n"
        f"👤 User ID : {user_id}\n"
        f"🌍 Langue : {language}\n"
        f"📂 Catégorie : {category}\n"
        f"📦 Produit : {product}\n"
        f"⭐ Montant : {amount_text}\n\n"
        "💬 Message utilisateur :\n"
        f"{message}\n\n"
        "🤖 Résumé support :\n"
        f"{ai_summary}\n\n"
        "🔐 Transaction Telegram :\n"
        f"{charge_id}\n\n"
        "Pour répondre :\n"
        f"{ADMIN_REPLY_PREFIX} "
        f"{ticket_code} "
        "<ta réponse>"
    )


def send_ticket_to_admin(
    bot,
    ticket,
):
    admin_id = get_support_admin_id()

    if admin_id is None:
        return {
            "success": False,
            "reason": (
                "admin_not_configured"
            ),
        }

    try:
        message = build_admin_ticket_message(
            ticket
        )

        sent_message = bot.send_message(
            admin_id,
            message,
        )

    except Exception as error:
        print(
            "PAYSUPPORT ADMIN SEND ERROR:",
            repr(error),
            flush=True,
        )

        return {
            "success": False,
            "reason": "send_failed",
        }

    return {
        "success": True,
        "reason": "sent",
        "admin_id": admin_id,
        "message": sent_message,
    }


# ==================================================
# ADMIN REPLY PARSING
# ==================================================

def parse_admin_reply_command(
    text,
):
    if not isinstance(
        text,
        str,
    ):
        return None

    normalized = text.strip()

    if not normalized:
        return None

    parts = normalized.split(
        maxsplit=2
    )

    if len(parts) != 3:
        return None

    command = parts[0]

    command = command.split(
        "@"
    )[0]

    if command.lower() != (
        ADMIN_REPLY_PREFIX
    ):
        return None

    ticket_code = (
        parts[1]
        .strip()
        .upper()
    )

    reply = parts[2].strip()

    if not ticket_code.startswith(
        "AV-"
    ):
        return None

    if not reply:
        return None

    return {
        "ticket_code": ticket_code,
        "reply": reply,
    }


# ==================================================
# USER REPLY TEXT
# ==================================================

def build_user_admin_reply(
    ticket,
    admin_reply,
):
    language = ticket.get(
        "language",
        "fr",
    )

    ticket_code = ticket.get(
        "ticket_code",
        "",
    )

    reply = _safe_text(
        admin_reply
    )

    if language == "en":
        return (
            "🆘 AstroVibe Support\n\n"
            f"Ticket: {ticket_code}\n\n"
            "Our support team replied:\n\n"
            f"{reply}\n\n"
            "This response was delivered through "
            "AstroVibe. You do not need to contact "
            "a personal Telegram account."
        )

    return (
        "🆘 Support AstroVibe\n\n"
        f"Ticket : {ticket_code}\n\n"
        "Le support t’a répondu :\n\n"
        f"{reply}\n\n"
        "Cette réponse t’est transmise directement "
        "par AstroVibe. Tu n’as pas besoin de "
        "contacter un compte Telegram personnel."
    )


# ==================================================
# COMPLETE ADMIN RESPONSE FLOW
# ==================================================

def process_admin_reply(
    bot,
    get_db_connection,
    admin_user_id,
    command_text,
):
    if not is_support_admin(
        admin_user_id
    ):
        return {
            "success": False,
            "reason": "unauthorized",
        }

    parsed = parse_admin_reply_command(
        command_text
    )

    if parsed is None:
        return {
            "success": False,
            "reason": (
                "invalid_command"
            ),
        }

    from paysupport_engine import (
        get_support_ticket,
        save_admin_reply,
    )

    ticket = get_support_ticket(
        get_db_connection,
        parsed["ticket_code"],
    )

    if ticket is None:
        return {
            "success": False,
            "reason": "ticket_not_found",
        }

    user_id = ticket.get(
        "user_id"
    )

    if not user_id:
        return {
            "success": False,
            "reason": "missing_user",
        }

    user_message = build_user_admin_reply(
        ticket,
        parsed["reply"],
    )

    try:
        bot.send_message(
            user_id,
            user_message,
        )

    except Exception as error:
        print(
            "PAYSUPPORT USER REPLY ERROR:",
            repr(error),
            flush=True,
        )

        return {
            "success": False,
            "reason": (
                "user_delivery_failed"
            ),
        }

    saved = save_admin_reply(
        get_db_connection,
        parsed["ticket_code"],
        parsed["reply"],
        resolve=True,
    )

    if not saved:
        return {
            "success": False,
            "reason": (
                "ticket_update_failed"
            ),
        }

    return {
        "success": True,
        "reason": "resolved",
        "ticket_code": (
            parsed["ticket_code"]
        ),
        "user_id": user_id,
    }


# ==================================================
# ADMIN CONFIRMATION TEXT
# ==================================================

def get_admin_resolution_text(
    result,
):
    if not result.get(
        "success"
    ):
        reason = result.get(
            "reason",
            "unknown_error",
        )

        return (
            "⚠️ Support AstroVibe\n\n"
            f"Échec : {reason}"
        )

    return (
        "✅ Ticket résolu\n\n"
        "Ticket : "
        + result["ticket_code"]
        + "\n\n"
        "La réponse a été transmise "
        "à l’utilisateur via AstroVibe."
    )
