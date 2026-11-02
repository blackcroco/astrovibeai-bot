from weekly_engine import generate_weekly_horoscope


# ==================================================
# IDENTIFIANTS DES FONCTIONNALITES PREMIUM
# ==================================================

PREMIUM_DAILY = "daily"
PREMIUM_WEEKLY = "weekly"
PREMIUM_MONTHLY = "monthly"
PREMIUM_YEARLY = "yearly"
PREMIUM_COMPATIBILITY = "compatibility"
PREMIUM_NOTIFICATIONS = "notifications"
PREMIUM_SUBSCRIPTION = "subscription"


# ==================================================
# RESULTATS STANDARDISES
# ==================================================

def premium_result(
    status,
    content=None,
    feature=None
):
    return {
        "status": status,
        "content": content,
        "feature": feature
    }


# ==================================================
# ASTRO HEBDOMADAIRE
# ==================================================

def generate_weekly(sign, language):
    content = generate_weekly_horoscope(
        sign,
        language
    )

    if not content:
        return premium_result(
            status="error",
            feature=PREMIUM_WEEKLY
        )

    return premium_result(
        status="success",
        content=content,
        feature=PREMIUM_WEEKLY
    )


# ==================================================
# ASTRO DU JOUR +
# ==================================================

def generate_daily_plus(sign, language):
    # Le moteur complet sera ajouté ici.
    return premium_result(
        status="coming_soon",
        feature=PREMIUM_DAILY
    )


# ==================================================
# ASTRO MENSUEL
# ==================================================

def generate_monthly(sign, language):
    # Le moteur complet sera ajouté ici.
    return premium_result(
        status="coming_soon",
        feature=PREMIUM_MONTHLY
    )


# ==================================================
# ASTRO ANNUEL
# ==================================================

def generate_yearly(sign, language):
    # Le moteur complet sera ajouté ici.
    return premium_result(
        status="coming_soon",
        feature=PREMIUM_YEARLY
    )


# ==================================================
# COMPATIBILITE PREMIUM
# ==================================================

def generate_premium_compatibility(
    first_sign,
    second_sign,
    language
):
    # Le moteur complet sera ajouté ici.
    return premium_result(
        status="coming_soon",
        feature=PREMIUM_COMPATIBILITY
    )


# ==================================================
# NOTIFICATIONS
# ==================================================

def get_notifications_settings(
    user_id,
    language
):
    # La gestion des notifications sera ajoutée ici.
    return premium_result(
        status="coming_soon",
        feature=PREMIUM_NOTIFICATIONS
    )


# ==================================================
# ABONNEMENT
# ==================================================

def get_subscription_info(
    user_id,
    language
):
    # La gestion de l'abonnement sera ajoutée ici.
    return premium_result(
        status="coming_soon",
        feature=PREMIUM_SUBSCRIPTION
    )


# ==================================================
# ROUTEUR PREMIUM CENTRAL
# ==================================================

def generate_premium_feature(
    feature,
    sign=None,
    language="fr",
    user_id=None,
    second_sign=None
):
    if language not in (
        "fr",
        "en"
    ):
        language = "fr"

    if feature == PREMIUM_WEEKLY:
        if not sign:
            return premium_result(
                status="missing_sign",
                feature=feature
            )

        return generate_weekly(
            sign,
            language
        )

    if feature == PREMIUM_DAILY:
        if not sign:
            return premium_result(
                status="missing_sign",
                feature=feature
            )

        return generate_daily_plus(
            sign,
            language
        )

    if feature == PREMIUM_MONTHLY:
        if not sign:
            return premium_result(
                status="missing_sign",
                feature=feature
            )

        return generate_monthly(
            sign,
            language
        )

    if feature == PREMIUM_YEARLY:
        if not sign:
            return premium_result(
                status="missing_sign",
                feature=feature
            )

        return generate_yearly(
            sign,
            language
        )

    if feature == PREMIUM_COMPATIBILITY:
        if not sign:
            return premium_result(
                status="missing_sign",
                feature=feature
            )

        if not second_sign:
            return premium_result(
                status="missing_second_sign",
                feature=feature
            )

        return generate_premium_compatibility(
            sign,
            second_sign,
            language
        )

    if feature == PREMIUM_NOTIFICATIONS:
        if not user_id:
            return premium_result(
                status="missing_user",
                feature=feature
            )

        return get_notifications_settings(
            user_id,
            language
        )

    if feature == PREMIUM_SUBSCRIPTION:
        if not user_id:
            return premium_result(
                status="missing_user",
                feature=feature
            )

        return get_subscription_info(
            user_id,
            language
        )

    return premium_result(
        status="unknown_feature",
        feature=feature
    )
