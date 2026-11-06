import re


REFERRER_REWARD = 50
REFERRED_REWARD = 20

REFERRAL_PREFIX = "ref_"

REFERRAL_STATUS_PENDING = "pending"
REFERRAL_STATUS_REWARDED = "rewarded"
REFERRAL_STATUS_REJECTED = "rejected"

BOT_USERNAME = "AstrovibeAIbot"


def normalize_user_id(value):
    try:
        user_id = int(value)
    except (TypeError, ValueError):
        return None

    if user_id <= 0:
        return None

    return user_id


def parse_referral_payload(text):
    if not isinstance(text, str):
        return None

    normalized = text.strip()

    if not normalized:
        return None

    parts = normalized.split(maxsplit=1)

    if len(parts) != 2:
        return None

    command = parts[0].split(
        "@",
        1,
    )[0].lower()

    if command != "/start":
        return None

    payload = parts[1].strip()

    match = re.fullmatch(
        r"ref_([1-9][0-9]*)",
        payload,
    )

    if match is None:
        return None

    return normalize_user_id(
        match.group(1)
    )


def build_referral_link(user_id):
    normalized = normalize_user_id(
        user_id
    )

    if normalized is None:
        raise ValueError(
            "Invalid referral user ID"
        )

    return (
        "https://t.me/"
        f"{BOT_USERNAME}"
        "?start="
        f"{REFERRAL_PREFIX}"
        f"{normalized}"
    )


def build_invite_message(
    user_id,
    language="fr",
):
    link = build_referral_link(
        user_id
    )

    if language == "en":
        return (
            "🤝 Invite your friends to AstroVibe\n\n"
            "Share your personal link:\n\n"
            f"{link}\n\n"
            "🎁 Your friend receives "
            f"{REFERRED_REWARD} welcome points.\n"
            "⭐ You receive "
            f"{REFERRER_REWARD} points when their "
            "AstroVibe registration is completed.\n\n"
            "Only genuine new AstroVibe users "
            "are eligible."
        )

    return (
        "🤝 Invite tes amis sur AstroVibe\n\n"
        "Partage ton lien personnel :\n\n"
        f"{link}\n\n"
        "🎁 Ton ami reçoit "
        f"{REFERRED_REWARD} points de bienvenue.\n"
        "⭐ Tu reçois "
        f"{REFERRER_REWARD} points lorsque son "
        "inscription AstroVibe est terminée.\n\n"
        "Seuls les nouveaux utilisateurs "
        "AstroVibe réels sont éligibles."
    )


def build_referral_reward_message(
    role,
    points,
    language="fr",
):
    if language == "en":
        if role == "referrer":
            return (
                "🎉 AstroVibe referral validated!\n\n"
                f"You earned {points} points because "
                "your friend completed their "
                "registration."
            )

        return (
            "🎁 Welcome to AstroVibe!\n\n"
            f"You received {points} welcome points "
            "through a valid referral."
        )

    if role == "referrer":
        return (
            "🎉 Parrainage AstroVibe validé !\n\n"
            f"Tu as gagné {points} points car ton ami "
            "a terminé son inscription."
        )

    return (
        "🎁 Bienvenue sur AstroVibe !\n\n"
        f"Tu as reçu {points} points de bienvenue "
        "grâce à un parrainage valide."
    )


def _rollback_quietly(connection):
    try:
        connection.rollback()
    except Exception:
        pass


def _commit(connection):
    commit = getattr(
        connection,
        "commit",
        None,
    )

    if callable(commit):
        commit()


def _close_quietly(resource):
    close = getattr(
        resource,
        "close",
        None,
    )

    if callable(close):
        try:
            close()
        except Exception:
            pass


def capture_referral_start(
    get_db_connection,
    referred_user_id,
    command_text,
):
    referred_id = normalize_user_id(
        referred_user_id
    )

    referrer_id = parse_referral_payload(
        command_text
    )

    if referred_id is None:
        return {
            "success": False,
            "reason": "invalid_referred_user",
        }

    if referrer_id is None:
        return {
            "success": False,
            "reason": "no_referral_payload",
        }

    if referrer_id == referred_id:
        return {
            "success": False,
            "reason": "self_referral",
        }

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT 1
            FROM users
            WHERE telegram_id = %s
            LIMIT 1
            """,
            (
                referred_id,
            ),
        )

        if cursor.fetchone():
            _rollback_quietly(
                connection
            )

            return {
                "success": False,
                "reason": "existing_user",
            }

        cursor.execute(
            """
            SELECT 1
            FROM users
            WHERE telegram_id = %s
            LIMIT 1
            """,
            (
                referrer_id,
            ),
        )

        if not cursor.fetchone():
            _rollback_quietly(
                connection
            )

            return {
                "success": False,
                "reason": "referrer_not_found",
            }

        cursor.execute(
            """
            INSERT INTO referrals (
                referrer_user_id,
                referred_user_id,
                referrer_reward,
                referred_reward,
                status
            )
            VALUES (
                %s,
                %s,
                %s,
                %s,
                'pending'
            )
            ON CONFLICT (
                referred_user_id
            )
            DO NOTHING
            RETURNING id
            """,
            (
                referrer_id,
                referred_id,
                REFERRER_REWARD,
                REFERRED_REWARD,
            ),
        )

        inserted = cursor.fetchone()

        if not inserted:
            _rollback_quietly(
                connection
            )

            return {
                "success": False,
                "reason": "already_referred",
            }

        _commit(connection)

        return {
            "success": True,
            "reason": "pending_created",
            "referral_id": inserted[0],
            "referrer_user_id": referrer_id,
            "referred_user_id": referred_id,
        }

    except Exception as error:
        if connection is not None:
            _rollback_quietly(
                connection
            )

        print(
            "REFERRAL CAPTURE ERROR:",
            repr(error),
            flush=True,
        )

        return {
            "success": False,
            "reason": "database_error",
        }

    finally:
        if cursor is not None:
            _close_quietly(cursor)

        if connection is not None:
            _close_quietly(connection)


def finalize_pending_referral(
    get_db_connection,
    referred_user_id,
    calculate_level,
):
    referred_id = normalize_user_id(
        referred_user_id
    )

    if referred_id is None:
        return {
            "success": False,
            "reason": "invalid_referred_user",
        }

    if not callable(calculate_level):
        return {
            "success": False,
            "reason": "invalid_level_calculator",
        }

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                referrer_user_id,
                referred_user_id,
                referrer_reward,
                referred_reward,
                status
            FROM referrals
            WHERE referred_user_id = %s
            FOR UPDATE
            """,
            (
                referred_id,
            ),
        )

        referral = cursor.fetchone()

        if referral is None:
            _rollback_quietly(
                connection
            )

            return {
                "success": False,
                "reason": "no_pending_referral",
            }

        (
            referral_id,
            referrer_id,
            stored_referred_id,
            referrer_reward,
            referred_reward,
            status,
        ) = referral

        if status != REFERRAL_STATUS_PENDING:
            _rollback_quietly(
                connection
            )

            return {
                "success": False,
                "reason": "already_processed",
            }

        if referrer_id == stored_referred_id:
            cursor.execute(
                """
                UPDATE referrals
                SET status = 'rejected'
                WHERE id = %s
                """,
                (
                    referral_id,
                ),
            )

            _commit(connection)

            return {
                "success": False,
                "reason": "self_referral",
            }

        locked_ids = sorted(
            [
                int(referrer_id),
                int(stored_referred_id),
            ]
        )

        cursor.execute(
            """
            SELECT
                telegram_id,
                points,
                level,
                sign
            FROM users
            WHERE telegram_id IN (
                %s,
                %s
            )
            ORDER BY telegram_id
            FOR UPDATE
            """,
            (
                locked_ids[0],
                locked_ids[1],
            ),
        )

        users = cursor.fetchall()

        user_map = {
            int(row[0]): row
            for row in users
        }

        referrer = user_map.get(
            int(referrer_id)
        )

        referred = user_map.get(
            int(stored_referred_id)
        )

        if referrer is None:
            _rollback_quietly(
                connection
            )

            return {
                "success": False,
                "reason": "referrer_not_found",
            }

        if referred is None:
            _rollback_quietly(
                connection
            )

            return {
                "success": False,
                "reason": "referred_not_registered",
            }

        referred_sign = referred[3]

        if (
            referred_sign is None
            or not str(
                referred_sign
            ).strip()
        ):
            _rollback_quietly(
                connection
            )

            return {
                "success": False,
                "reason": "registration_incomplete",
            }

        referrer_points = (
            int(referrer[1] or 0)
            + int(referrer_reward)
        )

        referred_points = (
            int(referred[1] or 0)
            + int(referred_reward)
        )

        referrer_level = calculate_level(
            referrer_points
        )

        referred_level = calculate_level(
            referred_points
        )

        cursor.execute(
            """
            UPDATE users
            SET
                points = %s,
                level = %s
            WHERE telegram_id = %s
            """,
            (
                referrer_points,
                referrer_level,
                referrer_id,
            ),
        )

        cursor.execute(
            """
            UPDATE users
            SET
                points = %s,
                level = %s
            WHERE telegram_id = %s
            """,
            (
                referred_points,
                referred_level,
                stored_referred_id,
            ),
        )

        cursor.execute(
            """
            UPDATE referrals
            SET
                status = 'rewarded',
                rewarded_at = NOW()
            WHERE
                id = %s
                AND status = 'pending'
            """,
            (
                referral_id,
            ),
        )

        if cursor.rowcount != 1:
            raise RuntimeError(
                "Referral status update failed"
            )

        _commit(connection)

        return {
            "success": True,
            "reason": "rewarded",
            "referral_id": referral_id,
            "referrer_user_id": int(
                referrer_id
            ),
            "referred_user_id": int(
                stored_referred_id
            ),
            "referrer_reward": int(
                referrer_reward
            ),
            "referred_reward": int(
                referred_reward
            ),
            "referrer_points": (
                referrer_points
            ),
            "referred_points": (
                referred_points
            ),
        }

    except Exception as error:
        if connection is not None:
            _rollback_quietly(
                connection
            )

        print(
            "REFERRAL FINALIZE ERROR:",
            repr(error),
            flush=True,
        )

        return {
            "success": False,
            "reason": "database_error",
        }

    finally:
        if cursor is not None:
            _close_quietly(cursor)

        if connection is not None:
            _close_quietly(connection)


def get_referral_stats(
    get_db_connection,
    referrer_user_id,
):
    referrer_id = normalize_user_id(
        referrer_user_id
    )

    if referrer_id is None:
        return {
            "successful_referrals": 0,
            "points_earned": 0,
        }

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                COUNT(*),
                COALESCE(
                    SUM(referrer_reward),
                    0
                )
            FROM referrals
            WHERE
                referrer_user_id = %s
                AND status = 'rewarded'
            """,
            (
                referrer_id,
            ),
        )

        row = cursor.fetchone()

        return {
            "successful_referrals": int(
                row[0] or 0
            ),
            "points_earned": int(
                row[1] or 0
            ),
        }

    except Exception as error:
        print(
            "REFERRAL STATS ERROR:",
            repr(error),
            flush=True,
        )

        return {
            "successful_referrals": 0,
            "points_earned": 0,
        }

    finally:
        if cursor is not None:
            _close_quietly(cursor)

        if connection is not None:
            _close_quietly(connection)
