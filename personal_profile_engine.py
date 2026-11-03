# ============================================
# ASTROVIBE - PROFIL PERSONNEL
# Moteur central du Profil AstroVibe Personnel
# ============================================


SIGN_ALIASES = {
    "♈ Bélier": "aries",
    "♉ Taureau": "taurus",
    "♊ Gémeaux": "gemini",
    "♋ Cancer": "cancer",
    "♌ Lion": "leo",
    "♍ Vierge": "virgo",
    "♎ Balance": "libra",
    "♏ Scorpion": "scorpio",
    "♐ Sagittaire": "sagittarius",
    "♑ Capricorne": "capricorn",
    "♒ Verseau": "aquarius",
    "♓ Poissons": "pisces",
}


SIGN_NAMES = {
    "fr": {
        "aries": "♈ Bélier",
        "taurus": "♉ Taureau",
        "gemini": "♊ Gémeaux",
        "cancer": "♋ Cancer",
        "leo": "♌ Lion",
        "virgo": "♍ Vierge",
        "libra": "♎ Balance",
        "scorpio": "♏ Scorpion",
        "sagittarius": "♐ Sagittaire",
        "capricorn": "♑ Capricorne",
        "aquarius": "♒ Verseau",
        "pisces": "♓ Poissons",
    },
    "en": {
        "aries": "♈ Aries",
        "taurus": "♉ Taurus",
        "gemini": "♊ Gemini",
        "cancer": "♋ Cancer",
        "leo": "♌ Leo",
        "virgo": "♍ Virgo",
        "libra": "♎ Libra",
        "scorpio": "♏ Scorpio",
        "sagittarius": "♐ Sagittarius",
        "capricorn": "♑ Capricorn",
        "aquarius": "♒ Aquarius",
        "pisces": "♓ Pisces",
    }
}


SIGN_META = {
    "aries": {
        "element": "fire",
        "modality": "cardinal",
    },
    "taurus": {
        "element": "earth",
        "modality": "fixed",
    },
    "gemini": {
        "element": "air",
        "modality": "mutable",
    },
    "cancer": {
        "element": "water",
        "modality": "cardinal",
    },
    "leo": {
        "element": "fire",
        "modality": "fixed",
    },
    "virgo": {
        "element": "earth",
        "modality": "mutable",
    },
    "libra": {
        "element": "air",
        "modality": "cardinal",
    },
    "scorpio": {
        "element": "water",
        "modality": "fixed",
    },
    "sagittarius": {
        "element": "fire",
        "modality": "mutable",
    },
    "capricorn": {
        "element": "earth",
        "modality": "cardinal",
    },
    "aquarius": {
        "element": "air",
        "modality": "fixed",
    },
    "pisces": {
        "element": "water",
        "modality": "mutable",
    },
}


ELEMENT_LABELS = {
    "fr": {
        "fire": "Feu",
        "earth": "Terre",
        "air": "Air",
        "water": "Eau",
    },
    "en": {
        "fire": "Fire",
        "earth": "Earth",
        "air": "Air",
        "water": "Water",
    }
}


MODALITY_LABELS = {
    "fr": {
        "cardinal": "Cardinal",
        "fixed": "Fixe",
        "mutable": "Mutable",
    },
    "en": {
        "cardinal": "Cardinal",
        "fixed": "Fixed",
        "mutable": "Mutable",
    }
}


PROFILE_SECTIONS = {
    "fr": (
        "identity",
        "personality",
        "emotional_world",
        "communication",
        "love",
        "relationship_needs",
        "motivation",
        "work",
        "ambition",
        "finances",
        "strengths",
        "watchpoints",
        "balance",
        "growth",
        "summary",
    ),
    "en": (
        "identity",
        "personality",
        "emotional_world",
        "communication",
        "love",
        "relationship_needs",
        "motivation",
        "work",
        "ambition",
        "finances",
        "strengths",
        "watchpoints",
        "balance",
        "growth",
        "summary",
    ),
}


SECTION_TITLES = {
    "fr": {
        "identity": "🌌 Ton identité astrologique",
        "personality": "☀️ Ta personnalité profonde",
        "emotional_world": "🌙 Ton monde émotionnel",
        "communication": "🗣️ Ta manière de communiquer",
        "love": "❤️ Ta manière d'aimer",
        "relationship_needs": "💞 Tes besoins relationnels",
        "motivation": "🔥 Tes moteurs intérieurs",
        "work": "💼 Travail et talents",
        "ambition": "🚀 Tes ambitions",
        "finances": "💰 Ton rapport aux finances",
        "strengths": "💪 Tes forces naturelles",
        "watchpoints": "⚠️ Tes points de vigilance",
        "balance": "☯️ Ton équilibre personnel",
        "growth": "✨ Ton potentiel d'évolution",
        "summary": "🌟 Synthèse AstroVibe",
    },
    "en": {
        "identity": "🌌 Your astrological identity",
        "personality": "☀️ Your deeper personality",
        "emotional_world": "🌙 Your emotional world",
        "communication": "🗣️ Your communication style",
        "love": "❤️ Your way of loving",
        "relationship_needs": "💞 Your relationship needs",
        "motivation": "🔥 Your inner motivation",
        "work": "💼 Work and talents",
        "ambition": "🚀 Your ambitions",
        "finances": "💰 Your relationship with money",
        "strengths": "💪 Your natural strengths",
        "watchpoints": "⚠️ Your watchpoints",
        "balance": "☯️ Your personal balance",
        "growth": "✨ Your growth potential",
        "summary": "🌟 AstroVibe summary",
    }
}


def normalize_sign(sign):
    if not sign:
        return None

    if sign in SIGN_ALIASES:
        return SIGN_ALIASES[sign]

    normalized = str(sign).strip().lower()

    english_aliases = {
        "aries": "aries",
        "taurus": "taurus",
        "gemini": "gemini",
        "cancer": "cancer",
        "leo": "leo",
        "virgo": "virgo",
        "libra": "libra",
        "scorpio": "scorpio",
        "sagittarius": "sagittarius",
        "capricorn": "capricorn",
        "aquarius": "aquarius",
        "pisces": "pisces",
    }

    return english_aliases.get(normalized)


def get_sign_name(sign_key, language="fr"):
    language = language if language in ("fr", "en") else "fr"

    return SIGN_NAMES.get(
        language,
        SIGN_NAMES["fr"]
    ).get(sign_key, sign_key)


def get_sign_meta(sign_key, language="fr"):
    language = language if language in ("fr", "en") else "fr"

    meta = SIGN_META.get(sign_key)

    if not meta:
        return None

    return {
        "element": meta["element"],
        "element_label": ELEMENT_LABELS[language][
            meta["element"]
        ],
        "modality": meta["modality"],
        "modality_label": MODALITY_LABELS[language][
            meta["modality"]
        ],
    }


def build_profile_context(
    sign,
    language="fr",
    birth_date=None,
    birth_time=None,
    birth_time_known=None,
    birth_place=None,
):
    language = language if language in ("fr", "en") else "fr"

    sign_key = normalize_sign(sign)

    if not sign_key:
        raise ValueError(
            "Unsupported zodiac sign"
        )

    return {
        "language": language,
        "sign_key": sign_key,
        "sign_name": get_sign_name(
            sign_key,
            language
        ),
        "sign_meta": get_sign_meta(
            sign_key,
            language
        ),
        "birth_date": birth_date,
        "birth_time": birth_time,
        "birth_time_known": birth_time_known,
        "birth_place": birth_place,
    }
