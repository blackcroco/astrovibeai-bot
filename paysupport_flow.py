SUPPORT_CATEGORIES = {
    "profile": (
        "✨ Profil Personnel",
        "✨ Personal Profile",
    ),
    "premium": (
        "💎 Premium",
        "💎 Premium",
    ),
    "payment": (
        "⭐ Paiement / Stars",
        "⭐ Payment / Stars",
    ),
    "subscription": (
        "🔄 Abonnement",
        "🔄 Subscription",
    ),
    "refund": (
        "↩️ Remboursement",
        "↩️ Refund",
    ),
    "other": (
        "❓ Autre",
        "❓ Other",
    ),
}


def get_support_intro(language):
    if language == "en":
        return (
            "🆘 AstroVibe Payment Support\n\n"
            "Choose the category that best "
            "matches your problem."
        )

    return (
        "🆘 Support paiement AstroVibe\n\n"
        "Choisis la catégorie qui correspond "
        "le mieux à ton problème."
    )


def get_category_label(
    category,
    language,
):
    labels = SUPPORT_CATEGORIES.get(
        category
    )

    if not labels:
        return None

    if language == "en":
        return labels[1]

    return labels[0]


def parse_category(data):
    prefix = "paysupport:"

    if not isinstance(data, str):
        return None

    if not data.startswith(prefix):
        return None

    category = data[len(prefix):]

    if category not in SUPPORT_CATEGORIES:
        return None

    return category


def get_prompt(
    category,
    language,
):
    label = get_category_label(
        category,
        language,
    )

    if language == "en":
        return (
            f"{label}\n\n"
            "Describe your problem in one "
            "message.\n\n"
            "Never send passwords or Telegram "
            "login codes."
        )

    return (
        f"{label}\n\n"
        "Décris ton problème en un seul "
        "message.\n\n"
        "Ne transmets jamais de mot de passe "
        "ou de code de connexion Telegram."
    )


def get_product(category):
    if category == "profile":
        return "profile"

    if category in (
        "premium",
        "subscription",
    ):
        return "premium"

    return None


def get_amount(category):
    if category == "profile":
        return 390

    if category in (
        "premium",
        "subscription",
    ):
        return 199

    return None
