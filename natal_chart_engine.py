# ============================================
# ASTROVIBE - NATAL CHART ENGINE
# Base du moteur astrologique natal
# ============================================

from datetime import date, datetime, time


# ============================================
# ZODIAQUE
# ============================================

ZODIAC_SIGNS = (
    "aries",
    "taurus",
    "gemini",
    "cancer",
    "leo",
    "virgo",
    "libra",
    "scorpio",
    "sagittarius",
    "capricorn",
    "aquarius",
    "pisces",
)


ZODIAC_SYMBOLS = {
    "aries": "♈",
    "taurus": "♉",
    "gemini": "♊",
    "cancer": "♋",
    "leo": "♌",
    "virgo": "♍",
    "libra": "♎",
    "scorpio": "♏",
    "sagittarius": "♐",
    "capricorn": "♑",
    "aquarius": "♒",
    "pisces": "♓",
}


ZODIAC_NAMES = {
    "fr": {
        "aries": "Bélier",
        "taurus": "Taureau",
        "gemini": "Gémeaux",
        "cancer": "Cancer",
        "leo": "Lion",
        "virgo": "Vierge",
        "libra": "Balance",
        "scorpio": "Scorpion",
        "sagittarius": "Sagittaire",
        "capricorn": "Capricorne",
        "aquarius": "Verseau",
        "pisces": "Poissons",
    },
    "en": {
        "aries": "Aries",
        "taurus": "Taurus",
        "gemini": "Gemini",
        "cancer": "Cancer",
        "leo": "Leo",
        "virgo": "Virgo",
        "libra": "Libra",
        "scorpio": "Scorpio",
        "sagittarius": "Sagittarius",
        "capricorn": "Capricorn",
        "aquarius": "Aquarius",
        "pisces": "Pisces",
    },
}


# ============================================
# PLANÈTES / POINTS DU THÈME
# ============================================

NATAL_OBJECTS = (
    "sun",
    "moon",
    "mercury",
    "venus",
    "mars",
    "jupiter",
    "saturn",
    "uranus",
    "neptune",
    "pluto",
)


NATAL_OBJECT_LABELS = {
    "fr": {
        "sun": "☀️ Soleil",
        "moon": "🌙 Lune",
        "mercury": "☿ Mercure",
        "venus": "♀ Vénus",
        "mars": "♂ Mars",
        "jupiter": "♃ Jupiter",
        "saturn": "♄ Saturne",
        "uranus": "♅ Uranus",
        "neptune": "♆ Neptune",
        "pluto": "♇ Pluton",
        "ascendant": "⬆️ Ascendant",
        "midheaven": "🔝 Milieu du Ciel",
    },
    "en": {
        "sun": "☀️ Sun",
        "moon": "🌙 Moon",
        "mercury": "☿ Mercury",
        "venus": "♀ Venus",
        "mars": "♂ Mars",
        "jupiter": "♃ Jupiter",
        "saturn": "♄ Saturn",
        "uranus": "♅ Uranus",
        "neptune": "♆ Neptune",
        "pluto": "♇ Pluto",
        "ascendant": "⬆️ Ascendant",
        "midheaven": "🔝 Midheaven",
    },
}


# ============================================
# VALIDATION DES DONNÉES DE NAISSANCE
# ============================================

def validate_birth_data(
    birth_date,
    birth_time=None,
    birth_time_known=None,
    birth_place=None,
    birth_timezone=None,
    birth_latitude=None,
    birth_longitude=None,
):
    errors = []

    if not birth_date:
        errors.append("missing_birth_date")

    if birth_time_known is True and not birth_time:
        errors.append("missing_birth_time")

    if not birth_place:
        errors.append("missing_birth_place")

    if birth_latitude is not None:
        if not -90 <= float(birth_latitude) <= 90:
            errors.append("invalid_birth_latitude")

    if birth_longitude is not None:
        if not -180 <= float(birth_longitude) <= 180:
            errors.append("invalid_birth_longitude")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
    }


# ============================================
# NIVEAU DE PRÉCISION DISPONIBLE
# ============================================

def get_natal_precision_level(
    birth_date,
    birth_time=None,
    birth_time_known=None,
    birth_place=None,
    birth_timezone=None,
    birth_latitude=None,
    birth_longitude=None,
):
    if not birth_date:
        return "none"

    has_location = (
        birth_place
        and birth_timezone
        and birth_latitude is not None
        and birth_longitude is not None
    )

    has_exact_time = (
        birth_time_known is True
        and birth_time is not None
    )

    if has_exact_time and has_location:
        return "full"

    if has_location:
        return "planetary"

    return "basic"


# ============================================
# STRUCTURE STANDARD D'UNE POSITION ASTRALE
# ============================================

def create_position(
    object_name,
    sign=None,
    degree=None,
    longitude=None,
    house=None,
    retrograde=False,
):
    return {
        "object": object_name,
        "sign": sign,
        "degree": degree,
        "longitude": longitude,
        "house": house,
        "retrograde": retrograde,
    }


# ============================================
# STRUCTURE VIDE D'UN THÈME NATAL
# ============================================

def create_empty_natal_chart(
    birth_date,
    birth_time=None,
    birth_time_known=None,
    birth_place=None,
    birth_timezone=None,
    birth_latitude=None,
    birth_longitude=None,
):
    precision = get_natal_precision_level(
        birth_date=birth_date,
        birth_time=birth_time,
        birth_time_known=birth_time_known,
        birth_place=birth_place,
        birth_timezone=birth_timezone,
        birth_latitude=birth_latitude,
        birth_longitude=birth_longitude,
    )

    positions = {
        object_name: create_position(
            object_name
        )
        for object_name in NATAL_OBJECTS
    }

    return {
        "birth": {
            "date": birth_date,
            "time": birth_time,
            "time_known": birth_time_known,
            "place": birth_place,
            "timezone": birth_timezone,
            "latitude": birth_latitude,
            "longitude": birth_longitude,
        },
        "precision_level": precision,
        "positions": positions,
        "ascendant": None,
        "midheaven": None,
        "houses": None,
        "aspects": [],
        "calculation_engine": None,
        "calculated": False,
    }


# ============================================
# INFORMATIONS DISPONIBLES POUR L'UTILISATEUR
# ============================================

def describe_natal_precision(chart, language="fr"):
    language = language if language in ("fr", "en") else "fr"
    precision = chart.get(
        "precision_level",
        "none"
    )

    if language == "en":
        messages = {
            "none": (
                "Not enough birth information is available "
                "for a personalised calculation."
            ),
            "basic": (
                "Your birth date is available, but the birth location "
                "has not yet been resolved precisely."
            ),
            "planetary": (
                "Your birth location is available. Planetary information "
                "can be calculated, but an exact birth time is required "
                "before time-sensitive chart points are treated as reliable."
            ),
            "full": (
                "Your date, exact birth time, and resolved birth location "
                "are available for the most detailed calculation."
            ),
        }

    else:
        messages = {
            "none": (
                "Les informations disponibles ne permettent pas encore "
                "un calcul astrologique personnalisé."
            ),
            "basic": (
                "Ta date de naissance est disponible, mais ton lieu "
                "de naissance n'est pas encore résolu avec précision."
            ),
            "planetary": (
                "Ton lieu de naissance est disponible. Les informations "
                "planétaires pourront être calculées, mais une heure exacte "
                "est nécessaire avant de considérer comme fiables les points "
                "du thème dépendant fortement de l'heure."
            ),
            "full": (
                "Ta date, ton heure exacte et ton lieu de naissance résolu "
                "sont disponibles pour le niveau de calcul le plus détaillé."
            ),
        }

    return messages.get(
        precision,
        messages["none"]
    )
