from datetime import datetime, timezone

from premium_stars_payment import (
    validate_premium_pre_checkout,
    validate_premium_successful_payment,
)

from premium_subscription_engine import (
    activate_premium_subscription,
)


# ==================================================
# OUTILS
# ==================================================

def _normalize_expiration_date(value):
    if value is None:
        return None

    if isinstance(value, datetime):
        if value.tzinfo is None:
            return value.replace(
                tzinfo=timezone.utc
            )

        return value.astimezone(
            timezone.utc
        )

    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(
            value,
            tz=timezone.utc,
        )

    return None


# ==================================================
# PRE-CHECKOUT PREMIUM
# ==================================================

def process_premium_pre_checkout(
    payload,
    currency,
    total_amount,
    telegram_user_id,
):
    validation = validate_premium_pre_checkout(
        payload=payload,
        currency=currency,
        total_amount=total_amount,
        telegram_user_id=telegram_user_id,
    )

    if not validation["valid"]:
        return {
            "success": False,
            "reason": validation["reason"],
            "validation": validation,
        }

    return {
        "success": True,
        "reason": "valid",
        "validation": validation,
    }


# ==================================================
# SUCCESSFUL PAYMENT PREMIUM
# ==================================================

def process_successful_premium_payment(
    get_db_connection,
    payload,
    currency,
    total_amount,
    telegram_payment_charge_id,
    telegram_user_id,
    telegram_subscription_id=None,
    subscription_expiration_date=None,
    is_recurring=None,
    is_first_recurring=None,
):
    validation = (
        validate_premium_successful_payment(
            payload=payload,
            currency=currency,
            total_amount=total_amount,
            telegram_payment_charge_id=(
                telegram_payment_charge_id
            ),
            telegram_user_id=telegram_user_id,
            subscription_expiration_date=(
                subscription_expiration_date
            ),
            is_recurring=is_recurring,
            is_first_recurring=(
                is_first_recurring
            ),
        )
    )

    if not validation["valid"]:
        return {
            "success": False,
            "reason": validation["reason"],
            "validation": validation,
        }

    expires_at = _normalize_expiration_date(
        validation[
            "subscription_expiration_date"
        ]
    )

    activation = (
        activate_premium_subscription(
            get_db_connection=(
                get_db_connection
            ),
            user_id=validation["user_id"],
            telegram_payment_charge_id=(
                validation[
                    "telegram_payment_charge_id"
                ]
            ),
            telegram_subscription_id=(
                telegram_subscription_id
            ),
            expires_at=expires_at,
        )
    )

    if not activation["success"]:
        return {
            "success": False,
            "reason": activation["reason"],
            "validation": validation,
            "activation": activation,
        }

    return {
        "success": True,
        "reason": "premium_activated",
        "user_id": validation["user_id"],
        "amount": validation["amount"],
        "currency": validation["currency"],
        "telegram_payment_charge_id": (
            validation[
                "telegram_payment_charge_id"
            ]
        ),
        "telegram_subscription_id": (
            telegram_subscription_id
        ),
        "subscription_expiration_date": (
            expires_at
        ),
        "is_recurring": (
            validation["is_recurring"]
        ),
        "is_first_recurring": (
            validation[
                "is_first_recurring"
            ]
        ),
        "activation": activation,
    }
