# ============================================
# ASTROVIBE - PROFILE PURCHASE ENGINE
# Permanent purchase persistence in Neon
# ============================================

from datetime import datetime, timezone


PROFILE_PRODUCT_ID = (
    "astrovibe_personal_profile_v2"
)

PROFILE_PRICE_STARS = 390

PROFILE_CURRENCY = "XTR"


# ============================================
# VALIDATION
# ============================================

def normalize_purchase_user_id(
    user_id,
):
    try:
        normalized_user_id = int(
            user_id
        )

    except (TypeError, ValueError) as error:
        raise ValueError(
            "Invalid purchase user_id"
        ) from error

    if normalized_user_id <= 0:
        raise ValueError(
            "Invalid purchase user_id"
        )

    return normalized_user_id


def normalize_charge_id(
    telegram_payment_charge_id,
):
    if telegram_payment_charge_id is None:
        raise ValueError(
            "Missing Telegram payment charge ID"
        )

    charge_id = str(
        telegram_payment_charge_id
    ).strip()

    if not charge_id:
        raise ValueError(
            "Missing Telegram payment charge ID"
        )

    return charge_id


# ============================================
# TABLE INITIALIZATION
# ============================================

def init_profile_purchase_table(
    connection_factory,
):
    if not callable(
        connection_factory
    ):
        raise ValueError(
            "connection_factory must be callable"
        )

    with connection_factory() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS
                profile_purchases (
                    id BIGSERIAL PRIMARY KEY,

                    user_id BIGINT NOT NULL,

                    product_id TEXT NOT NULL,

                    amount INTEGER NOT NULL,

                    currency VARCHAR(8) NOT NULL,

                    telegram_payment_charge_id
                        TEXT NOT NULL,

                    purchased_at
                        TIMESTAMPTZ NOT NULL
                        DEFAULT CURRENT_TIMESTAMP,

                    CONSTRAINT
                        profile_purchases_charge_unique
                        UNIQUE (
                            telegram_payment_charge_id
                        ),

                    CONSTRAINT
                        profile_purchases_owner_unique
                        UNIQUE (
                            user_id,
                            product_id
                        ),

                    CONSTRAINT
                        profile_purchases_amount_positive
                        CHECK (
                            amount > 0
                        ),

                    CONSTRAINT
                        profile_purchases_currency_check
                        CHECK (
                            currency = 'XTR'
                        )
                )
                """
            )

        connection.commit()

    return True


# ============================================
# OWNERSHIP CHECK
# ============================================

def has_purchased_profile(
    connection_factory,
    user_id,
):
    normalized_user_id = (
        normalize_purchase_user_id(
            user_id
        )
    )

    with connection_factory() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT EXISTS (
                    SELECT 1
                    FROM profile_purchases
                    WHERE user_id = %s
                      AND product_id = %s
                )
                """,
                (
                    normalized_user_id,
                    PROFILE_PRODUCT_ID,
                ),
            )

            result = cursor.fetchone()

    return bool(
        result
        and result[0]
    )


# ============================================
# CHARGE CHECK
# ============================================

def payment_charge_exists(
    connection_factory,
    telegram_payment_charge_id,
):
    charge_id = normalize_charge_id(
        telegram_payment_charge_id
    )

    with connection_factory() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT EXISTS (
                    SELECT 1
                    FROM profile_purchases
                    WHERE telegram_payment_charge_id
                        = %s
                )
                """,
                (
                    charge_id,
                ),
            )

            result = cursor.fetchone()

    return bool(
        result
        and result[0]
    )


# ============================================
# RECORD PURCHASE
# ============================================

def record_profile_purchase(
    connection_factory,
    user_id,
    telegram_payment_charge_id,
    amount=PROFILE_PRICE_STARS,
    currency=PROFILE_CURRENCY,
):
    normalized_user_id = (
        normalize_purchase_user_id(
            user_id
        )
    )

    charge_id = normalize_charge_id(
        telegram_payment_charge_id
    )

    try:
        normalized_amount = int(
            amount
        )

    except (TypeError, ValueError) as error:
        raise ValueError(
            "Invalid purchase amount"
        ) from error

    if normalized_amount != PROFILE_PRICE_STARS:
        raise ValueError(
            "Unexpected purchase amount"
        )

    if currency != PROFILE_CURRENCY:
        raise ValueError(
            "Unexpected purchase currency"
        )

    purchased_at = datetime.now(
        timezone.utc
    )

    with connection_factory() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO profile_purchases (
                    user_id,
                    product_id,
                    amount,
                    currency,
                    telegram_payment_charge_id,
                    purchased_at
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
                ON CONFLICT DO NOTHING
                RETURNING
                    id,
                    user_id,
                    product_id,
                    amount,
                    currency,
                    telegram_payment_charge_id,
                    purchased_at
                """,
                (
                    normalized_user_id,
                    PROFILE_PRODUCT_ID,
                    normalized_amount,
                    PROFILE_CURRENCY,
                    charge_id,
                    purchased_at,
                ),
            )

            inserted = cursor.fetchone()

        connection.commit()

    if inserted:
        return {
            "recorded": True,
            "already_owned": False,
            "duplicate_charge": False,
            "purchase": {
                "id": inserted[0],
                "user_id": inserted[1],
                "product_id": inserted[2],
                "amount": inserted[3],
                "currency": inserted[4],
                "telegram_payment_charge_id": (
                    inserted[5]
                ),
                "purchased_at": inserted[6],
            },
        }

    already_owned = has_purchased_profile(
        connection_factory,
        normalized_user_id,
    )

    duplicate_charge = payment_charge_exists(
        connection_factory,
        charge_id,
    )

    return {
        "recorded": False,
        "already_owned": already_owned,
        "duplicate_charge": duplicate_charge,
        "purchase": None,
    }


# ============================================
# GET USER PURCHASE
# ============================================

def get_profile_purchase(
    connection_factory,
    user_id,
):
    normalized_user_id = (
        normalize_purchase_user_id(
            user_id
        )
    )

    with connection_factory() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    user_id,
                    product_id,
                    amount,
                    currency,
                    telegram_payment_charge_id,
                    purchased_at
                FROM profile_purchases
                WHERE user_id = %s
                  AND product_id = %s
                LIMIT 1
                """,
                (
                    normalized_user_id,
                    PROFILE_PRODUCT_ID,
                ),
            )

            result = cursor.fetchone()

    if not result:
        return None

    return {
        "id": result[0],
        "user_id": result[1],
        "product_id": result[2],
        "amount": result[3],
        "currency": result[4],
        "telegram_payment_charge_id": (
            result[5]
        ),
        "purchased_at": result[6],
    }


# ============================================
# GET PURCHASE BY TELEGRAM CHARGE
# ============================================

def get_purchase_by_charge_id(
    connection_factory,
    telegram_payment_charge_id,
):
    charge_id = normalize_charge_id(
        telegram_payment_charge_id
    )

    with connection_factory() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    user_id,
                    product_id,
                    amount,
                    currency,
                    telegram_payment_charge_id,
                    purchased_at
                FROM profile_purchases
                WHERE telegram_payment_charge_id
                    = %s
                LIMIT 1
                """,
                (
                    charge_id,
                ),
            )

            result = cursor.fetchone()

    if not result:
        return None

    return {
        "id": result[0],
        "user_id": result[1],
        "product_id": result[2],
        "amount": result[3],
        "currency": result[4],
        "telegram_payment_charge_id": (
            result[5]
        ),
        "purchased_at": result[6],
    }


# ============================================
# CONFIGURATION CHECK
# ============================================

def validate_purchase_configuration():
    errors = []

    if (
        PROFILE_PRODUCT_ID
        != "astrovibe_personal_profile_v2"
    ):
        errors.append(
            "Invalid profile product ID"
        )

    if PROFILE_PRICE_STARS != 390:
        errors.append(
            "Invalid profile Stars price"
        )

    if PROFILE_CURRENCY != "XTR":
        errors.append(
            "Invalid profile currency"
        )

    return {
        "valid": not errors,
        "errors": errors,
    }
