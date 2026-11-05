
from datetime import datetime, timedelta, timezone


# ==================================================
# CONFIGURATION PREMIUM
# ==================================================

PREMIUM_PRICE_STARS = 199
PREMIUM_CURRENCY = "XTR"
PREMIUM_PERIOD_DAYS = 30

PREMIUM_STATUS_INACTIVE = "inactive"
PREMIUM_STATUS_ACTIVE = "active"
PREMIUM_STATUS_EXPIRED = "expired"
PREMIUM_STATUS_CANCELLED = "cancelled"


# ==================================================
# OUTILS DATE / UTC
# ==================================================

def _utc_now():
    return datetime.now(timezone.utc)


def _normalize_datetime(value):
    if value is None:
        return None

    if value.tzinfo is None:
        return value.replace(
            tzinfo=timezone.utc
        )

    return value.astimezone(
        timezone.utc
    )


# ==================================================
# LECTURE ABONNEMENT
# ==================================================

def get_premium_subscription(
    get_db_connection,
    user_id,
):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    user_id,
                    status,
                    amount_stars,
                    currency,
                    telegram_payment_charge_id,
                    telegram_subscription_id,
                    started_at,
                    expires_at,
                    created_at,
                    updated_at
                FROM premium_subscriptions
                WHERE user_id = %s
                ORDER BY updated_at DESC, id DESC
                LIMIT 1
                """,
                (user_id,),
            )

            row = cursor.fetchone()

    if not row:
        return None

    return {
        "user_id": row[0],
        "status": row[1],
        "amount_stars": row[2],
        "currency": row[3],
        "telegram_payment_charge_id": row[4],
        "telegram_subscription_id": row[5],
        "started_at": row[6],
        "expires_at": row[7],
        "created_at": row[8],
        "updated_at": row[9],
    }


# ==================================================
# CONTROLE ABONNEMENT ACTIF
# ==================================================

def is_premium_subscription_active(
    get_db_connection,
    user_id,
    now=None,
):
    now = _normalize_datetime(
        now or _utc_now()
    )

    subscription = get_premium_subscription(
        get_db_connection,
        user_id,
    )

    if not subscription:
        return False

    if (
        subscription["status"]
        != PREMIUM_STATUS_ACTIVE
    ):
        return False

    expires_at = _normalize_datetime(
        subscription["expires_at"]
    )

    if expires_at is None:
        return False

    return expires_at > now


# ==================================================
# ANTI-DOUBLE TRANSACTION
# ==================================================

def has_premium_charge(
    get_db_connection,
    telegram_payment_charge_id,
):
    if not telegram_payment_charge_id:
        return False

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT 1
                FROM premium_subscriptions
                WHERE telegram_payment_charge_id = %s
                LIMIT 1
                """,
                (
                    telegram_payment_charge_id,
                ),
            )

            return (
                cursor.fetchone()
                is not None
            )


# ==================================================
# ACTIVATION PREMIUM
# ==================================================

def activate_premium_subscription(
    get_db_connection,
    user_id,
    telegram_payment_charge_id,
    telegram_subscription_id=None,
    expires_at=None,
):
    if not telegram_payment_charge_id:
        raise ValueError(
            "telegram_payment_charge_id is required"
        )

    if has_premium_charge(
        get_db_connection,
        telegram_payment_charge_id,
    ):
        return {
            "success": False,
            "reason": "duplicate_charge",
        }

    now = _utc_now()

    expires_at = _normalize_datetime(
        expires_at
    )

    if expires_at is None:
        expires_at = (
            now
            + timedelta(
                days=PREMIUM_PERIOD_DAYS
            )
        )

    if expires_at <= now:
        return {
            "success": False,
            "reason": "invalid_expiration",
        }

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO premium_subscriptions (
                    user_id,
                    status,
                    amount_stars,
                    currency,
                    telegram_payment_charge_id,
                    telegram_subscription_id,
                    started_at,
                    expires_at,
                    created_at,
                    updated_at
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
                """,
                (
                    user_id,
                    PREMIUM_STATUS_ACTIVE,
                    PREMIUM_PRICE_STARS,
                    PREMIUM_CURRENCY,
                    telegram_payment_charge_id,
                    telegram_subscription_id,
                    now,
                    expires_at,
                    now,
                    now,
                ),
            )

            cursor.execute(
                """
                UPDATE users
                SET premium = TRUE
                WHERE telegram_id = %s
                """,
                (user_id,),
            )

            if cursor.rowcount != 1:
                raise RuntimeError(
                    "Premium user not found"
                )

        conn.commit()

    return {
        "success": True,
        "reason": "activated",
        "user_id": user_id,
        "status": PREMIUM_STATUS_ACTIVE,
        "amount_stars": PREMIUM_PRICE_STARS,
        "currency": PREMIUM_CURRENCY,
        "expires_at": expires_at,
    }


# ==================================================
# EXPIRATION PREMIUM
# ==================================================

def expire_premium_subscription(
    get_db_connection,
    user_id,
    now=None,
):
    now = _normalize_datetime(
        now or _utc_now()
    )

    subscription = get_premium_subscription(
        get_db_connection,
        user_id,
    )

    if not subscription:
        return False

    expires_at = _normalize_datetime(
        subscription["expires_at"]
    )

    if expires_at is None:
        return False

    if expires_at > now:
        return False

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE premium_subscriptions
                SET
                    status = %s,
                    updated_at = %s
                WHERE user_id = %s
                AND status = %s
                """,
                (
                    PREMIUM_STATUS_EXPIRED,
                    now,
                    user_id,
                    PREMIUM_STATUS_ACTIVE,
                ),
            )

            cursor.execute(
                """
                UPDATE users
                SET premium = FALSE
                WHERE telegram_id = %s
                """,
                (user_id,),
            )

        conn.commit()

    return True
