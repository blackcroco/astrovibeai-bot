# ============================================
# ASTROVIBE - TELEGRAM STARS PAYMENT ENGINE
# ============================================

PROFILE_PRODUCT_ID = "astrovibe_personal_profile_v2"

PROFILE_PRICE_STARS = 390

PROFILE_CURRENCY = "XTR"

PROFILE_PROVIDER_TOKEN = ""

PROFILE_PAYLOAD_PREFIX = (
    "astrovibe_profile_v2"
)


# ============================================
# PRODUCT TEXTS
# ============================================

PROFILE_INVOICE_TEXTS = {
    "fr": {
        "title": (
            "Profil AstroVibe Personnel"
        ),
        "description": (
            "Débloque ton Profil AstroVibe Personnel "
            "basé sur tes informations de naissance "
            "et ton thème natal."
        ),
        "price_label": (
            "Profil AstroVibe Personnel"
        ),
    },

    "en": {
        "title": (
            "AstroVibe Personal Profile"
        ),
        "description": (
            "Unlock your AstroVibe Personal Profile "
            "based on your birth information "
            "and natal chart."
        ),
        "price_label": (
            "AstroVibe Personal Profile"
        ),
    },
}


# ============================================
# LANGUAGE
# ============================================

def normalize_payment_language(
    language,
):
    if language == "en":
        return "en"

    return "fr"


# ============================================
# PAYMENT PAYLOAD
# ============================================

def build_profile_payment_payload(
    user_id,
):
    if user_id is None:
        raise ValueError(
            "user_id is required"
        )

    try:
        normalized_user_id = int(
            user_id
        )

    except (TypeError, ValueError) as error:
        raise ValueError(
            "Invalid user_id"
        ) from error

    if normalized_user_id <= 0:
        raise ValueError(
            "Invalid user_id"
        )

    return (
        f"{PROFILE_PAYLOAD_PREFIX}:"
        f"{normalized_user_id}"
    )


def parse_profile_payment_payload(
    payload,
):
    if not isinstance(
        payload,
        str
    ):
        return None

    prefix = (
        PROFILE_PAYLOAD_PREFIX
        + ":"
    )

    if not payload.startswith(
        prefix
    ):
        return None

    user_id_text = payload[
        len(prefix):
    ]

    try:
        user_id = int(
            user_id_text
        )

    except (TypeError, ValueError):
        return None

    if user_id <= 0:
        return None

    return {
        "product_id": PROFILE_PRODUCT_ID,
        "user_id": user_id,
    }


# ============================================
# INVOICE DATA
# ============================================

def build_profile_invoice(
    user_id,
    language="fr",
):
    language = normalize_payment_language(
        language
    )

    texts = PROFILE_INVOICE_TEXTS[
        language
    ]

    payload = build_profile_payment_payload(
        user_id
    )

    return {
        "title": texts[
            "title"
        ],
        "description": texts[
            "description"
        ],
        "payload": payload,
        "provider_token": (
            PROFILE_PROVIDER_TOKEN
        ),
        "currency": PROFILE_CURRENCY,
        "prices": [
            {
                "label": texts[
                    "price_label"
                ],
                "amount": (
                    PROFILE_PRICE_STARS
                ),
            }
        ],
    }


# ============================================
# PRE-CHECKOUT VALIDATION
# ============================================

def validate_profile_pre_checkout(
    payload,
    currency,
    total_amount,
    telegram_user_id=None,
):
    parsed = parse_profile_payment_payload(
        payload
    )

    if parsed is None:
        return {
            "valid": False,
            "reason": "invalid_payload",
        }

    if currency != PROFILE_CURRENCY:
        return {
            "valid": False,
            "reason": "invalid_currency",
        }

    try:
        amount = int(
            total_amount
        )

    except (TypeError, ValueError):
        return {
            "valid": False,
            "reason": "invalid_amount",
        }

    if amount != PROFILE_PRICE_STARS:
        return {
            "valid": False,
            "reason": "invalid_amount",
        }

    if telegram_user_id is not None:
        try:
            telegram_user_id = int(
                telegram_user_id
            )

        except (TypeError, ValueError):
            return {
                "valid": False,
                "reason": "invalid_user",
            }

        if (
            parsed["user_id"]
            != telegram_user_id
        ):
            return {
                "valid": False,
                "reason": "user_mismatch",
            }

    return {
        "valid": True,
        "reason": None,
        "product_id": parsed[
            "product_id"
        ],
        "user_id": parsed[
            "user_id"
        ],
        "currency": PROFILE_CURRENCY,
        "amount": PROFILE_PRICE_STARS,
    }


# ============================================
# SUCCESSFUL PAYMENT VALIDATION
# ============================================

def validate_profile_successful_payment(
    payload,
    currency,
    total_amount,
    telegram_payment_charge_id,
    telegram_user_id=None,
):
    pre_checkout = (
        validate_profile_pre_checkout(
            payload=payload,
            currency=currency,
            total_amount=total_amount,
            telegram_user_id=telegram_user_id,
        )
    )

    if not pre_checkout[
        "valid"
    ]:
        return pre_checkout

    if not telegram_payment_charge_id:
        return {
            "valid": False,
            "reason": (
                "missing_payment_charge_id"
            ),
        }

    return {
        "valid": True,
        "reason": None,
        "product_id": PROFILE_PRODUCT_ID,
        "user_id": pre_checkout[
            "user_id"
        ],
        "currency": PROFILE_CURRENCY,
        "amount": PROFILE_PRICE_STARS,
        "telegram_payment_charge_id": (
            str(
                telegram_payment_charge_id
            )
        ),
    }


# ============================================
# USER-FACING PAYMENT MESSAGES
# ============================================

def get_payment_success_text(
    language="fr",
):
    language = normalize_payment_language(
        language
    )

    if language == "en":
        return (
            "✅ Payment confirmed!\n\n"
            "Your AstroVibe Personal Profile "
            "has been unlocked. ✨"
        )

    return (
        "✅ Paiement confirmé !\n\n"
        "Ton Profil AstroVibe Personnel "
        "est maintenant débloqué. ✨"
    )


def get_payment_error_text(
    language="fr",
):
    language = normalize_payment_language(
        language
    )

    if language == "en":
        return (
            "❌ The payment could not be "
            "validated.\n\n"
            "No profile was unlocked."
        )

    return (
        "❌ Le paiement n'a pas pu être "
        "validé.\n\n"
        "Aucun profil n'a été débloqué."
    )


# ============================================
# SELF-CHECK
# ============================================

def validate_payment_configuration():
    errors = []

    if PROFILE_PRICE_STARS != 390:
        errors.append(
            "Incorrect profile price"
        )

    if PROFILE_CURRENCY != "XTR":
        errors.append(
            "Incorrect Telegram Stars currency"
        )

    if not PROFILE_PRODUCT_ID:
        errors.append(
            "Missing product ID"
        )

    if not PROFILE_PAYLOAD_PREFIX:
        errors.append(
            "Missing payload prefix"
        )

    for language in (
        "fr",
        "en",
    ):
        texts = PROFILE_INVOICE_TEXTS.get(
            language
        )

        if not texts:
            errors.append(
                f"Missing invoice language: "
                f"{language}"
            )
            continue

        for key in (
            "title",
            "description",
            "price_label",
        ):
            if not texts.get(
                key
            ):
                errors.append(
                    f"Missing {language} "
                    f"invoice field: {key}"
                )

    return {
        "valid": not errors,
        "errors": errors,
    }
