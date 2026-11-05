# ==================================================
# ASTROVIBE PREMIUM - TELEGRAM STARS PAYMENT
# ==================================================

PREMIUM_PRICE_STARS = 199
PREMIUM_CURRENCY = "XTR"
PREMIUM_PERIOD_SECONDS = 30 * 24 * 60 * 60

PREMIUM_PAYLOAD_PREFIX = "astrovibe_premium"


# ==================================================
# PAYLOAD
# ==================================================

def build_premium_payload(user_id):
    return (
        f"{PREMIUM_PAYLOAD_PREFIX}:"
        f"{int(user_id)}"
    )


def parse_premium_payload(payload):
    if not isinstance(payload, str):
        return None

    prefix = PREMIUM_PAYLOAD_PREFIX + ":"

    if not payload.startswith(prefix):
        return None

    raw_user_id = payload[len(prefix):]

    if not raw_user_id:
        return None

    try:
        user_id = int(raw_user_id)
    except (TypeError, ValueError):
        return None

    if user_id <= 0:
        return None

    return user_id


# ==================================================
# FACTURE PREMIUM
# ==================================================

def build_premium_invoice(
    user_id,
    language="fr",
):
    if language == "en":
        title = "AstroVibe Premium"
        description = (
            "Unlock AstroVibe Premium "
            "for 199 Stars every 30 days."
        )
        price_label = "AstroVibe Premium"

    else:
        title = "AstroVibe Premium"
        description = (
            "Débloque AstroVibe Premium "
            "pour 199 Stars tous les 30 jours."
        )
        price_label = "AstroVibe Premium"

    return {
        "title": title,
        "description": description,
        "payload": build_premium_payload(
            user_id
        ),
        "currency": PREMIUM_CURRENCY,
        "prices": [
            {
                "label": price_label,
                "amount": PREMIUM_PRICE_STARS,
            }
        ],
        "subscription_period": (
            PREMIUM_PERIOD_SECONDS
        ),
    }


# ==================================================
# VALIDATION COMMUNE
# ==================================================

def validate_premium_payment_data(
    payload,
    currency,
    total_amount,
    telegram_user_id,
):
    payload_user_id = parse_premium_payload(
        payload
    )

    if payload_user_id is None:
        return {
            "valid": False,
            "reason": "invalid_payload",
        }

    try:
        current_user_id = int(
            telegram_user_id
        )
    except (TypeError, ValueError):
        return {
            "valid": False,
            "reason": "invalid_user",
        }

    if payload_user_id != current_user_id:
        return {
            "valid": False,
            "reason": "invalid_user",
        }

    if currency != PREMIUM_CURRENCY:
        return {
            "valid": False,
            "reason": "invalid_currency",
        }

    if total_amount != PREMIUM_PRICE_STARS:
        return {
            "valid": False,
            "reason": "invalid_amount",
        }

    return {
        "valid": True,
        "reason": "valid",
        "user_id": payload_user_id,
        "amount": PREMIUM_PRICE_STARS,
        "currency": PREMIUM_CURRENCY,
    }


# ==================================================
# PRE-CHECKOUT
# ==================================================

def validate_premium_pre_checkout(
    payload,
    currency,
    total_amount,
    telegram_user_id,
):
    return validate_premium_payment_data(
        payload=payload,
        currency=currency,
        total_amount=total_amount,
        telegram_user_id=telegram_user_id,
    )


# ==================================================
# SUCCESSFUL PAYMENT
# ==================================================

def validate_premium_successful_payment(
    payload,
    currency,
    total_amount,
    telegram_payment_charge_id,
    telegram_user_id,
    subscription_expiration_date=None,
    is_recurring=None,
    is_first_recurring=None,
):
    validation = validate_premium_payment_data(
        payload=payload,
        currency=currency,
        total_amount=total_amount,
        telegram_user_id=telegram_user_id,
    )

    if not validation["valid"]:
        return validation

    if not telegram_payment_charge_id:
        return {
            "valid": False,
            "reason": "missing_charge_id",
        }

    return {
        "valid": True,
        "reason": "valid",
        "user_id": validation["user_id"],
        "amount": PREMIUM_PRICE_STARS,
        "currency": PREMIUM_CURRENCY,
        "telegram_payment_charge_id": (
            telegram_payment_charge_id
        ),
        "subscription_expiration_date": (
            subscription_expiration_date
        ),
        "is_recurring": is_recurring,
        "is_first_recurring": (
            is_first_recurring
        ),
    }
