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
# ============================================
# CALCUL PLANETAIRE REEL AVEC PYEPHEMERA
# ============================================

import ephemera as eph
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
PLANET_BODIES = {
    "sun": "SUN",
    "moon": "MOON",
    "mercury": "MERCURY",
    "venus": "VENUS",
    "mars": "MARS",
    "jupiter": "JUPITER",
    "saturn": "SATURN",
    "uranus": "URANUS",
    "neptune": "NEPTUNE",
    "pluto": "PLUTO",
}
# ============================================
# CONVERSION LONGITUDE -> SIGNE
# ============================================

def longitude_to_zodiac(longitude):
    longitude = float(longitude) % 360.0

    sign_index = int(
        longitude // 30
    )

    sign = ZODIAC_SIGNS[
        sign_index
    ]

    degree = longitude % 30.0

    return {
        "sign": sign,
        "degree": degree,
        "longitude": longitude,
    }


# ============================================
# EXTRACTION D'UNE POSITION PLANETAIRE
# ============================================

def extract_position_values(position_result):
    if hasattr(position_result, "longitude"):
        longitude = float(
            position_result.longitude
        )

        latitude = getattr(
            position_result,
            "latitude",
            None
        )

        distance = getattr(
            position_result,
            "distance",
            None
        )

        speed = getattr(
            position_result,
            "speed",
            None
        )

        return {
            "longitude": longitude,
            "latitude": latitude,
            "distance": distance,
            "speed": speed,
        }

    if isinstance(
        position_result,
        (tuple, list)
    ):
        if not position_result:
            raise ValueError(
                "Empty planetary position"
            )

        return {
            "longitude": float(
                position_result[0]
            ),
            "latitude": (
                position_result[1]
                if len(position_result) > 1
                else None
            ),
            "distance": (
                position_result[2]
                if len(position_result) > 2
                else None
            ),
            "speed": (
                position_result[3]
                if len(position_result) > 3
                else None
            ),
        }

    try:
        return {
            "longitude": float(
                position_result
            ),
            "latitude": None,
            "distance": None,
            "speed": None,
        }

    except (TypeError, ValueError):
        raise ValueError(
            "Unsupported planetary position format"
        )


# ============================================
# DATETIME DE NAISSANCE
# ============================================

def build_birth_datetime(
    birth_date,
    birth_time=None,
    birth_time_known=None,
    birth_timezone=None,
):
    if not birth_date:
        raise ValueError(
            "Birth date is required"
        )

    if not birth_timezone:
        raise ValueError(
            "Birth timezone is required"
        )

    try:
        timezone = ZoneInfo(
            birth_timezone
        )

    except ZoneInfoNotFoundError as error:
        raise ValueError(
            "Invalid birth timezone"
        ) from error

    if (
        birth_time_known is True
        and birth_time is not None
    ):
        calculation_time = birth_time
        time_precision = "exact"

    else:
        calculation_time = time(
            12,
            0
        )
        time_precision = "unknown_noon_reference"

    local_datetime = datetime.combine(
        birth_date,
        calculation_time
    ).replace(
        tzinfo=timezone
    )

    return {
        "datetime": local_datetime,
        "time_precision": time_precision,
    }


# ============================================
# JOUR JULIEN
# ============================================

def calculate_birth_julian_day(
    birth_date,
    birth_time=None,
    birth_time_known=None,
    birth_timezone=None,
):
    birth_datetime_data = build_birth_datetime(
        birth_date=birth_date,
        birth_time=birth_time,
        birth_time_known=birth_time_known,
        birth_timezone=birth_timezone,
    )

    local_datetime = birth_datetime_data[
        "datetime"
    ]

    jd_tt, jd_ut = eph.utc_to_jd(
        local_datetime
    )

    return {
        "jd_tt": jd_tt,
        "jd_ut": jd_ut,
        "datetime": local_datetime,
        "time_precision": birth_datetime_data[
            "time_precision"
        ],
    }


# ============================================
# CALCUL D'UNE PLANETE
# ============================================

def calculate_planet_position(
    planet_name,
    jd_ut,
):
    body_name = PLANET_BODIES.get(
        planet_name
    )

    if not body_name:
        raise ValueError(
            f"Unsupported planet: {planet_name}"
        )

    body = getattr(
        eph.Body,
        body_name,
        None
    )

    if body is None:
        raise ValueError(
            f"Planet unavailable: {planet_name}"
        )

    raw_position = eph.position(
        body,
        jd_ut
    )

    values = extract_position_values(
        raw_position
    )

    zodiac = longitude_to_zodiac(
        values["longitude"]
    )

    speed = values.get(
        "speed"
    )

    retrograde = (
        speed is not None
        and speed < 0
    )

    return {
        "object": planet_name,
        "sign": zodiac["sign"],
        "degree": zodiac["degree"],
        "longitude": zodiac["longitude"],
        "latitude": values["latitude"],
        "distance": values["distance"],
        "speed": speed,
        "retrograde": retrograde,
        "house": None,
    }


# ============================================
# CALCUL DES PLANETES
# ============================================

def calculate_planetary_positions(
    birth_date,
    birth_time=None,
    birth_time_known=None,
    birth_timezone=None,
):
    julian_data = calculate_birth_julian_day(
        birth_date=birth_date,
        birth_time=birth_time,
        birth_time_known=birth_time_known,
        birth_timezone=birth_timezone,
    )

    jd_ut = julian_data[
        "jd_ut"
    ]

    positions = {}
    errors = {}

    for planet_name in NATAL_OBJECTS:
        try:
            positions[
                planet_name
            ] = calculate_planet_position(
                planet_name,
                jd_ut
            )

        except Exception as error:
            positions[
                planet_name
            ] = None

            errors[
                planet_name
            ] = str(error)

    return {
        "positions": positions,
        "errors": errors,
        "jd_ut": julian_data["jd_ut"],
        "jd_tt": julian_data["jd_tt"],
        "calculation_datetime": julian_data[
            "datetime"
        ],
        "time_precision": julian_data[
            "time_precision"
        ],
    }


# ============================================
# CALCUL DU THEME NATAL
# ============================================

def calculate_natal_chart(
    birth_date,
    birth_time=None,
    birth_time_known=None,
    birth_place=None,
    birth_timezone=None,
    birth_latitude=None,
    birth_longitude=None,
):
    validation = validate_birth_data(
        birth_date=birth_date,
        birth_time=birth_time,
        birth_time_known=birth_time_known,
        birth_place=birth_place,
        birth_timezone=birth_timezone,
        birth_latitude=birth_latitude,
        birth_longitude=birth_longitude,
    )

    if not validation["valid"]:

        return {
            "calculated": False,
            "errors": validation[
                "errors"
            ],
        }

    chart = create_empty_natal_chart(
        birth_date=birth_date,
        birth_time=birth_time,
        birth_time_known=birth_time_known,
        birth_place=birth_place,
        birth_timezone=birth_timezone,
        birth_latitude=birth_latitude,
        birth_longitude=birth_longitude,
    )

    planetary_data = calculate_planetary_positions(
        birth_date=birth_date,
        birth_time=birth_time,
        birth_time_known=birth_time_known,
        birth_timezone=birth_timezone,
    )

    chart["positions"] = planetary_data[
        "positions"
    ]

    chart["planetary_errors"] = planetary_data[
        "errors"
    ]

    chart["jd_ut"] = planetary_data[
        "jd_ut"
    ]

    chart["jd_tt"] = planetary_data[
        "jd_tt"
    ]

    chart["calculation_datetime"] = planetary_data[
        "calculation_datetime"
    ]

    chart["time_precision"] = planetary_data[
        "time_precision"
    ]

    chart["calculation_engine"] = "pyephemera"
    chart["calculated"] = True

    return chart


# ============================================
# AFFICHAGE POUR LES TESTS
# ============================================

def format_planetary_positions(
    chart,
    language="fr",
):
    language = (
        language
        if language in ("fr", "en")
        else "fr"
    )

    if not chart.get("calculated"):
        if language == "en":
            return (
                "❌ Natal chart calculation "
                "is not available."
            )

        return (
            "❌ Le calcul du thème natal "
            "n'est pas disponible."
        )

    lines = []

    for planet_name in NATAL_OBJECTS:
        position = chart[
            "positions"
        ].get(
            planet_name
        )

        if not position:
            continue

        label = NATAL_OBJECT_LABELS[
            language
        ][planet_name]

        sign_key = position[
            "sign"
        ]

        sign_name = ZODIAC_NAMES[
            language
        ][sign_key]

        symbol = ZODIAC_SYMBOLS[
            sign_key
        ]

        degree = position[
            "degree"
        ]

        retrograde = (
            " ℞"
            if position["retrograde"]
            else ""
        )

        lines.append(
            f"{label} : "
            f"{symbol} {sign_name} "
            f"{degree:.2f}°"
            f"{retrograde}"
        )

    if language == "en":
        title = "🌌 Planetary birth positions"
    else:
        title = (
            "🌌 Positions planétaires de naissance"
        )

    return (
        title
        + "\n\n"
        + "\n".join(lines)
    )
# ============================================
# ASCENDANT ET MAISONS PLACIDUS
# ============================================

def calculate_house_cusps(
    jd_ut,
    birth_time_known,
    birth_latitude,
    birth_longitude,
):
    if birth_time_known is not True:
        return {
            "available": False,
            "reason": "unknown_birth_time",
            "system": None,
            "ascendant": None,
            "houses": None,
        }

    if birth_latitude is None:
        return {
            "available": False,
            "reason": "missing_birth_latitude",
            "system": None,
            "ascendant": None,
            "houses": None,
        }

    if birth_longitude is None:
        return {
            "available": False,
            "reason": "missing_birth_longitude",
            "system": None,
            "ascendant": None,
            "houses": None,
        }

    latitude = float(
        birth_latitude
    )

    longitude = float(
        birth_longitude
    )

    if not -90 <= latitude <= 90:
        raise ValueError(
            "Invalid birth latitude"
        )

    if not -180 <= longitude <= 180:
        raise ValueError(
            "Invalid birth longitude"
        )

    raw_cusps = eph.houses(
        jd_ut,
        longitude,
        latitude,
        eph.HouseSystem.PLACIDUS,
    )

    if not isinstance(
        raw_cusps,
        (list, tuple)
    ):
        raise ValueError(
            "Unsupported houses result format"
        )

    if len(raw_cusps) != 12:
        raise ValueError(
            "Expected 12 house cusps"
        )

    houses = []

    for house_number, cusp_longitude in enumerate(
        raw_cusps,
        start=1,
    ):
        zodiac = longitude_to_zodiac(
            cusp_longitude
        )

        houses.append(
            {
                "house": house_number,
                "longitude": zodiac[
                    "longitude"
                ],
                "sign": zodiac[
                    "sign"
                ],
                "degree": zodiac[
                    "degree"
                ],
            }
        )

    ascendant = {
        "object": "ascendant",
        "longitude": houses[0][
            "longitude"
        ],
        "sign": houses[0][
            "sign"
        ],
        "degree": houses[0][
            "degree"
        ],
        "house": 1,
    }

    return {
        "available": True,
        "reason": None,
        "system": "placidus",
        "ascendant": ascendant,
        "houses": houses,
    }


# ============================================
# POSITION D'UNE PLANETE DANS UNE MAISON
# ============================================

def longitude_in_house(
    longitude,
    house_start,
    house_end,
):
    longitude = float(
        longitude
    ) % 360.0

    house_start = float(
        house_start
    ) % 360.0

    house_end = float(
        house_end
    ) % 360.0

    if house_start < house_end:
        return (
            house_start
            <= longitude
            < house_end
        )

    return (
        longitude >= house_start
        or longitude < house_end
    )


def find_planet_house(
    longitude,
    houses,
):
    if not houses:
        return None

    for index, house in enumerate(
        houses
    ):
        next_index = (
            index + 1
        ) % len(houses)

        next_house = houses[
            next_index
        ]

        if longitude_in_house(
            longitude=longitude,
            house_start=house[
                "longitude"
            ],
            house_end=next_house[
                "longitude"
            ],
        ):
            return house[
                "house"
            ]

    return None


def assign_planets_to_houses(
    positions,
    houses,
):
    if not positions or not houses:
        return positions

    for planet_name, position in positions.items():
        if not position:
            continue

        position["house"] = find_planet_house(
            longitude=position[
                "longitude"
            ],
            houses=houses,
        )

    return positions


# ============================================
# THEME NATAL COMPLET
# Cette définition remplace la précédente.
# ============================================

def calculate_natal_chart(
    birth_date,
    birth_time=None,
    birth_time_known=None,
    birth_place=None,
    birth_timezone=None,
    birth_latitude=None,
    birth_longitude=None,
):
    validation = validate_birth_data(
        birth_date=birth_date,
        birth_time=birth_time,
        birth_time_known=birth_time_known,
        birth_place=birth_place,
        birth_timezone=birth_timezone,
        birth_latitude=birth_latitude,
        birth_longitude=birth_longitude,
    )

    if not validation["valid"]:
        return {
            "calculated": False,
            "errors": validation[
                "errors"
            ],
        }

    chart = create_empty_natal_chart(
        birth_date=birth_date,
        birth_time=birth_time,
        birth_time_known=birth_time_known,
        birth_place=birth_place,
        birth_timezone=birth_timezone,
        birth_latitude=birth_latitude,
        birth_longitude=birth_longitude,
    )

    planetary_data = calculate_planetary_positions(
        birth_date=birth_date,
        birth_time=birth_time,
        birth_time_known=birth_time_known,
        birth_timezone=birth_timezone,
    )

    house_data = calculate_house_cusps(
        jd_ut=planetary_data[
            "jd_ut"
        ],
        birth_time_known=birth_time_known,
        birth_latitude=birth_latitude,
        birth_longitude=birth_longitude,
    )

    positions = planetary_data[
        "positions"
    ]

    if house_data["available"]:
        positions = assign_planets_to_houses(
            positions=positions,
            houses=house_data[
                "houses"
            ],
        )

    chart["positions"] = positions

    chart["planetary_errors"] = planetary_data[
        "errors"
    ]

    chart["jd_ut"] = planetary_data[
        "jd_ut"
    ]

    chart["jd_tt"] = planetary_data[
        "jd_tt"
    ]

    chart["calculation_datetime"] = planetary_data[
        "calculation_datetime"
    ]

    chart["time_precision"] = planetary_data[
        "time_precision"
    ]

    chart["ascendant"] = house_data[
        "ascendant"
    ]

    chart["houses"] = house_data[
        "houses"
    ]

    chart["house_system"] = house_data[
        "system"
    ]

    chart["houses_available"] = house_data[
        "available"
    ]

    chart["houses_unavailable_reason"] = house_data[
        "reason"
    ]

    chart["midheaven"] = None
    chart["calculation_engine"] = "pyephemera"
    chart["calculated"] = True

    return chart


# ============================================
# AFFICHAGE ASCENDANT ET MAISONS
# ============================================

def format_houses(
    chart,
    language="fr",
):
    language = (
        language
        if language in ("fr", "en")
        else "fr"
    )

    if not chart.get(
        "calculated"
    ):
        if language == "en":
            return (
                "❌ The natal chart has not "
                "been calculated."
            )

        return (
            "❌ Le thème natal n'a pas "
            "été calculé."
        )

    if not chart.get(
        "houses_available"
    ):
        if language == "en":
            return (
                "⬆️ Ascendant and houses are "
                "not displayed because the exact "
                "birth time is unknown."
            )

        return (
            "⬆️ L'Ascendant et les maisons ne "
            "sont pas affichés car l'heure exacte "
            "de naissance est inconnue."
        )

    ascendant = chart[
        "ascendant"
    ]

    ascendant_sign = ascendant[
        "sign"
    ]

    ascendant_symbol = ZODIAC_SYMBOLS[
        ascendant_sign
    ]

    ascendant_name = ZODIAC_NAMES[
        language
    ][
        ascendant_sign
    ]

    ascendant_degree = ascendant[
        "degree"
    ]

    if language == "en":
        lines = [
            "🌌 Ascendant and Placidus houses",
            "",
            (
                "⬆️ Ascendant: "
                f"{ascendant_symbol} "
                f"{ascendant_name} "
                f"{ascendant_degree:.2f}°"
            ),
            "",
        ]
    else:
        lines = [
            "🌌 Ascendant et maisons Placidus",
            "",
            (
                "⬆️ Ascendant : "
                f"{ascendant_symbol} "
                f"{ascendant_name} "
                f"{ascendant_degree:.2f}°"
            ),
            "",
        ]

    for house in chart[
        "houses"
    ]:
        sign_key = house[
            "sign"
        ]

        symbol = ZODIAC_SYMBOLS[
            sign_key
        ]

        sign_name = ZODIAC_NAMES[
            language
        ][
            sign_key
        ]

        degree = house[
            "degree"
        ]

        house_number = house[
            "house"
        ]

        if language == "en":
            label = (
                f"House {house_number}"
            )
        else:
            label = (
                f"Maison {house_number}"
            )

        lines.append(
            f"🏠 {label} : "
            f"{symbol} {sign_name} "
            f"{degree:.2f}°"
        )

    return "\n".join(
        lines
    )


# ============================================
# AFFICHAGE PLANETES + MAISONS
# ============================================

def format_planets_with_houses(
    chart,
    language="fr",
):
    language = (
        language
        if language in ("fr", "en")
        else "fr"
    )

    if not chart.get(
        "calculated"
    ):
        if language == "en":
            return (
                "❌ Planetary positions are "
                "not available."
            )

        return (
            "❌ Les positions planétaires ne "
            "sont pas disponibles."
        )

    lines = []

    for planet_name in NATAL_OBJECTS:
        position = chart[
            "positions"
        ].get(
            planet_name
        )

        if not position:
            continue

        label = NATAL_OBJECT_LABELS[
            language
        ][
            planet_name
        ]

        sign_key = position[
            "sign"
        ]

        symbol = ZODIAC_SYMBOLS[
            sign_key
        ]

        sign_name = ZODIAC_NAMES[
            language
        ][
            sign_key
        ]

        degree = position[
            "degree"
        ]

        house_number = position.get(
            "house"
        )

        if house_number:
            if language == "en":
                house_text = (
                    f" · House {house_number}"
                )
            else:
                house_text = (
                    f" · Maison {house_number}"
                )
        else:
            house_text = ""

        retrograde = (
            " ℞"
            if position.get(
                "retrograde"
            )
            else ""
        )

        lines.append(
            f"{label} : "
            f"{symbol} {sign_name} "
            f"{degree:.2f}°"
            f"{retrograde}"
            f"{house_text}"
        )

    if language == "en":
        title = (
            "🪐 Planets in signs and houses"
        )
    else:
        title = (
            "🪐 Planètes dans les signes "
            "et les maisons"
        )

    return (
        title
        + "\n\n"
        + "\n".join(
            lines
        )
    )
