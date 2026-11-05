from datetime import datetime, timezone
import secrets


# ==================================================
# ASTROVIBE PAYMENT SUPPORT ENGINE
# ==================================================

SUPPORTED_LANGUAGES = {
    "fr",
    "en",
}

SUPPORTED_CATEGORIES = {
    "profile",
    "premium",
    "payment",
    "subscription",
    "refund",
    "other",
}

SUPPORTED_PRODUCTS = {
    "profile",
    "premium",
}

SUPPORTED_STATUSES = {
    "open",
    "ai_processing",
    "waiting_user",
    "escalated",
    "resolved",
    "closed",
}


# ==================================================
# HELPERS
# ==================================================

def _utc_now():
    return datetime.now(
        timezone.utc
    )


def _validate_language(language):
    if language not in SUPPORTED_LANGUAGES:
        raise ValueError(
            "Unsupported support language"
        )


def _validate_category(category):
    if category not in SUPPORTED_CATEGORIES:
        raise ValueError(
            "Unsupported support category"
        )


def _validate_product(product):
    if (
        product is not None
        and product not in SUPPORTED_PRODUCTS
    ):
        raise ValueError(
            "Unsupported support product"
        )


def _validate_status(status):
    if status not in SUPPORTED_STATUSES:
        raise ValueError(
            "Unsupported support status"
        )


def _normalize_message(message):
    if not isinstance(message, str):
        raise ValueError(
            "Support message must be text"
        )

    normalized = message.strip()

    if not normalized:
        raise ValueError(
            "Support message cannot be empty"
        )

    return normalized


def generate_ticket_code():
    random_part = secrets.token_hex(
        3
    ).upper()

    return f"AV-{random_part}"


def _row_to_ticket(row):
    if not row:
        return None

    return {
        "id": row[0],
        "ticket_code": row[1],
        "user_id": row[2],
        "language": row[3],
        "category": row[4],
        "product": row[5],
        "status": row[6],
        "user_message": row[7],
        "ai_summary": row[8],
        "ai_resolution": row[9],
        "escalated_to_human": row[10],
        "admin_reply": row[11],
        "payment_amount_stars": row[12],
        "telegram_payment_charge_id": row[13],
        "created_at": row[14],
        "updated_at": row[15],
        "resolved_at": row[16],
    }


# ==================================================
# CREATE TICKET
# ==================================================

def create_support_ticket(
    get_db_connection,
    user_id,
    user_message,
    language="fr",
    category="other",
    product=None,
    payment_amount_stars=None,
    telegram_payment_charge_id=None,
):
    _validate_language(language)
    _validate_category(category)
    _validate_product(product)

    message = _normalize_message(
        user_message
    )

    try:
        normalized_user_id = int(
            user_id
        )
    except (TypeError, ValueError):
        raise ValueError(
            "Invalid support user ID"
        )

    if normalized_user_id <= 0:
        raise ValueError(
            "Invalid support user ID"
        )

    if payment_amount_stars is not None:
        try:
            payment_amount_stars = int(
                payment_amount_stars
            )
        except (TypeError, ValueError):
            raise ValueError(
                "Invalid Stars amount"
            )

        if payment_amount_stars < 0:
            raise ValueError(
                "Invalid Stars amount"
            )

    now = _utc_now()

    for _ in range(5):
        ticket_code = generate_ticket_code()

        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO support_tickets (
                            ticket_code,
                            user_id,
                            language,
                            category,
                            product,
                            status,
                            user_message,
                            escalated_to_human,
                            payment_amount_stars,
                            telegram_payment_charge_id,
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
                            %s,
                            %s,
                            %s
                        )
                        RETURNING
                            id,
                            ticket_code,
                            user_id,
                            language,
                            category,
                            product,
                            status,
                            user_message,
                            ai_summary,
                            ai_resolution,
                            escalated_to_human,
                            admin_reply,
                            payment_amount_stars,
                            telegram_payment_charge_id,
                            created_at,
                            updated_at,
                            resolved_at
                        """,
                        (
                            ticket_code,
                            normalized_user_id,
                            language,
                            category,
                            product,
                            "open",
                            message,
                            False,
                            payment_amount_stars,
                            telegram_payment_charge_id,
                            now,
                            now,
                        ),
                    )

                    row = cursor.fetchone()

                conn.commit()

            return _row_to_ticket(row)

        except Exception as error:
            error_text = str(
                error
            ).lower()

            collision = (
                "ticket_code"
                in error_text
                and (
                    "unique"
                    in error_text
                    or "duplicate"
                    in error_text
                )
            )

            if collision:
                continue

            raise

    raise RuntimeError(
        "Unable to generate a unique ticket code"
    )


# ==================================================
# READ TICKETS
# ==================================================

def get_support_ticket(
    get_db_connection,
    ticket_code,
):
    if not isinstance(
        ticket_code,
        str,
    ):
        return None

    normalized_code = (
        ticket_code.strip().upper()
    )

    if not normalized_code:
        return None

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    ticket_code,
                    user_id,
                    language,
                    category,
                    product,
                    status,
                    user_message,
                    ai_summary,
                    ai_resolution,
                    escalated_to_human,
                    admin_reply,
                    payment_amount_stars,
                    telegram_payment_charge_id,
                    created_at,
                    updated_at,
                    resolved_at
                FROM support_tickets
                WHERE ticket_code = %s
                LIMIT 1
                """,
                (
                    normalized_code,
                ),
            )

            row = cursor.fetchone()

    return _row_to_ticket(row)


def get_latest_user_ticket(
    get_db_connection,
    user_id,
):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    ticket_code,
                    user_id,
                    language,
                    category,
                    product,
                    status,
                    user_message,
                    ai_summary,
                    ai_resolution,
                    escalated_to_human,
                    admin_reply,
                    payment_amount_stars,
                    telegram_payment_charge_id,
                    created_at,
                    updated_at,
                    resolved_at
                FROM support_tickets
                WHERE user_id = %s
                ORDER BY created_at DESC, id DESC
                LIMIT 1
                """,
                (
                    int(user_id),
                ),
            )

            row = cursor.fetchone()

    return _row_to_ticket(row)


def get_open_user_ticket(
    get_db_connection,
    user_id,
):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    ticket_code,
                    user_id,
                    language,
                    category,
                    product,
                    status,
                    user_message,
                    ai_summary,
                    ai_resolution,
                    escalated_to_human,
                    admin_reply,
                    payment_amount_stars,
                    telegram_payment_charge_id,
                    created_at,
                    updated_at,
                    resolved_at
                FROM support_tickets
                WHERE user_id = %s
                AND status IN (
                    'open',
                    'ai_processing',
                    'waiting_user',
                    'escalated'
                )
                ORDER BY created_at DESC, id DESC
                LIMIT 1
                """,
                (
                    int(user_id),
                ),
            )

            row = cursor.fetchone()

    return _row_to_ticket(row)


# ==================================================
# GENERIC UPDATE
# ==================================================

def update_ticket_status(
    get_db_connection,
    ticket_code,
    status,
):
    _validate_status(status)

    normalized_code = (
        ticket_code.strip().upper()
    )

    now = _utc_now()

    resolved_at = (
        now
        if status in {
            "resolved",
            "closed",
        }
        else None
    )

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE support_tickets
                SET
                    status = %s,
                    updated_at = %s,
                    resolved_at = %s
                WHERE ticket_code = %s
                """,
                (
                    status,
                    now,
                    resolved_at,
                    normalized_code,
                ),
            )

            updated = (
                cursor.rowcount == 1
            )

        conn.commit()

    return updated


# ==================================================
# AI SUPPORT DATA
# ==================================================

def save_ai_analysis(
    get_db_connection,
    ticket_code,
    ai_summary,
    ai_resolution=None,
    status="waiting_user",
):
    _validate_status(status)

    if status not in {
        "ai_processing",
        "waiting_user",
        "resolved",
        "escalated",
    }:
        raise ValueError(
            "Invalid AI support status"
        )

    summary = _normalize_message(
        ai_summary
    )

    resolution = None

    if ai_resolution is not None:
        resolution = _normalize_message(
            ai_resolution
        )

    normalized_code = (
        ticket_code.strip().upper()
    )

    now = _utc_now()

    resolved_at = (
        now
        if status == "resolved"
        else None
    )

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE support_tickets
                SET
                    ai_summary = %s,
                    ai_resolution = %s,
                    status = %s,
                    updated_at = %s,
                    resolved_at = %s
                WHERE ticket_code = %s
                """,
                (
                    summary,
                    resolution,
                    status,
                    now,
                    resolved_at,
                    normalized_code,
                ),
            )

            updated = (
                cursor.rowcount == 1
            )

        conn.commit()

    return updated


# ==================================================
# HUMAN ESCALATION
# ==================================================

def escalate_ticket(
    get_db_connection,
    ticket_code,
    ai_summary=None,
):
    normalized_code = (
        ticket_code.strip().upper()
    )

    now = _utc_now()

    summary = None

    if ai_summary is not None:
        summary = _normalize_message(
            ai_summary
        )

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE support_tickets
                SET
                    status = 'escalated',
                    escalated_to_human = TRUE,
                    ai_summary = COALESCE(
                        %s,
                        ai_summary
                    ),
                    updated_at = %s
                WHERE ticket_code = %s
                """,
                (
                    summary,
                    now,
                    normalized_code,
                ),
            )

            updated = (
                cursor.rowcount == 1
            )

        conn.commit()

    return updated


def save_admin_reply(
    get_db_connection,
    ticket_code,
    admin_reply,
    resolve=True,
):
    reply = _normalize_message(
        admin_reply
    )

    normalized_code = (
        ticket_code.strip().upper()
    )

    now = _utc_now()

    status = (
        "resolved"
        if resolve
        else "waiting_user"
    )

    resolved_at = (
        now
        if resolve
        else None
    )

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE support_tickets
                SET
                    admin_reply = %s,
                    status = %s,
                    updated_at = %s,
                    resolved_at = %s
                WHERE ticket_code = %s
                """,
                (
                    reply,
                    status,
                    now,
                    resolved_at,
                    normalized_code,
                ),
            )

            updated = (
                cursor.rowcount == 1
            )

        conn.commit()

    return updated


# ==================================================
# USER-FACING TEXT HELPERS
# ==================================================

def get_ticket_created_text(
    ticket,
):
    language = ticket.get(
        "language",
        "fr",
    )

    ticket_code = ticket[
        "ticket_code"
    ]

    if language == "en":
        return (
            "🎫 Your support request has been "
            "created.\n\n"
            f"Ticket: {ticket_code}\n\n"
            "AstroVibe will first try to help "
            "automatically. If needed, the request "
            "will be privately escalated to human "
            "support.\n\n"
            "You will receive the response directly "
            "in AstroVibe."
        )

    return (
        "🎫 Ta demande de support a été créée.\n\n"
        f"Ticket : {ticket_code}\n\n"
        "AstroVibe va d’abord tenter de t’aider "
        "automatiquement. Si nécessaire, la demande "
        "sera transmise de façon privée au support "
        "humain.\n\n"
        "Tu recevras la réponse directement dans "
        "AstroVibe."
    )


def get_ticket_escalated_text(
    ticket,
):
    language = ticket.get(
        "language",
        "fr",
    )

    ticket_code = ticket[
        "ticket_code"
    ]

    if language == "en":
        return (
            "👤 Your request has been escalated "
            "to AstroVibe support.\n\n"
            f"Ticket: {ticket_code}\n\n"
            "You will receive the response directly "
            "in this conversation. You do not need "
            "to contact a personal Telegram account."
        )

    return (
        "👤 Ta demande a été transmise au support "
        "AstroVibe.\n\n"
        f"Ticket : {ticket_code}\n\n"
        "Tu recevras la réponse directement dans "
        "cette conversation. Tu n’as pas besoin de "
        "contacter un compte Telegram personnel."
    )
