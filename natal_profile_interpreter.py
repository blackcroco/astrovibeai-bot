# ============================================
# ASTROVIBE - NATAL PROFILE INTERPRETER
# Interprétation symbolique du thème natal
# FR / EN
# ============================================


# ============================================
# NOMS DES SIGNES
# ============================================

SIGN_NAMES = {
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


SIGN_SYMBOLS = {
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


# ============================================
# STYLE SYMBOLIQUE DES 12 SIGNES
# ============================================

SIGN_STYLE = {
    "fr": {
        "aries": (
            "de manière directe, spontanée et volontaire, "
            "avec un besoin d'agir et d'ouvrir la voie"
        ),
        "taurus": (
            "avec constance, patience et réalisme, "
            "en recherchant stabilité et sécurité"
        ),
        "gemini": (
            "avec curiosité, mobilité et souplesse, "
            "en privilégiant les idées et les échanges"
        ),
        "cancer": (
            "avec sensibilité, intuition et protection, "
            "en accordant une grande importance à la sécurité émotionnelle"
        ),
        "leo": (
            "avec chaleur, créativité et assurance, "
            "en cherchant à exprimer une identité personnelle forte"
        ),
        "virgo": (
            "avec précision, analyse et sens pratique, "
            "en cherchant à comprendre, améliorer et organiser"
        ),
        "libra": (
            "avec diplomatie, recherche d'équilibre et sens relationnel, "
            "en tenant compte des différents points de vue"
        ),
        "scorpio": (
            "avec intensité, profondeur et détermination, "
            "en cherchant ce qui se cache derrière les apparences"
        ),
        "sagittarius": (
            "avec enthousiasme, franchise et besoin d'expansion, "
            "en recherchant sens, découverte et liberté"
        ),
        "capricorn": (
            "avec discipline, réalisme et persévérance, "
            "en privilégiant la maîtrise et la construction à long terme"
        ),
        "aquarius": (
            "avec indépendance, originalité et recul intellectuel, "
            "en remettant volontiers en question les habitudes établies"
        ),
        "pisces": (
            "avec sensibilité, imagination et intuition, "
            "en restant particulièrement réceptif aux ambiances et aux autres"
        ),
    },

    "en": {
        "aries": (
            "in a direct, spontaneous and determined way, "
            "with a strong impulse to act and initiate"
        ),
        "taurus": (
            "with patience, consistency and realism, "
            "seeking stability and security"
        ),
        "gemini": (
            "with curiosity, flexibility and mental mobility, "
            "favouring ideas, exchange and discovery"
        ),
        "cancer": (
            "with sensitivity, intuition and protectiveness, "
            "placing strong value on emotional security"
        ),
        "leo": (
            "with warmth, creativity and confidence, "
            "seeking a strong and personal form of self-expression"
        ),
        "virgo": (
            "with precision, analysis and practicality, "
            "seeking to understand, improve and organise"
        ),
        "libra": (
            "with diplomacy, balance and relational awareness, "
            "naturally considering several perspectives"
        ),
        "scorpio": (
            "with intensity, depth and determination, "
            "seeking what lies beneath appearances"
        ),
        "sagittarius": (
            "with enthusiasm, honesty and a desire for expansion, "
            "seeking meaning, discovery and freedom"
        ),
        "capricorn": (
            "with discipline, realism and perseverance, "
            "favouring mastery and long-term construction"
        ),
        "aquarius": (
            "with independence, originality and intellectual distance, "
            "readily questioning established patterns"
        ),
        "pisces": (
            "with sensitivity, imagination and intuition, "
            "remaining particularly receptive to atmosphere and other people"
        ),
    },
}


# ============================================
# DOMAINES DES 12 MAISONS
# ============================================

HOUSE_THEMES = {
    "fr": {
        1: "l'identité, l'affirmation de soi et la manière d'aborder le monde",
        2: "les ressources, les valeurs personnelles et la sécurité matérielle",
        3: "la communication, l'apprentissage et les échanges quotidiens",
        4: "les racines, le foyer, l'intimité et les fondations émotionnelles",
        5: "la créativité, le plaisir, l'expression personnelle et les élans du cœur",
        6: "le quotidien, le travail concret, les habitudes et le sens du service",
        7: "les relations, les associations et la manière de rencontrer l'autre",
        8: "la transformation, l'intimité profonde et les ressources partagées",
        9: "les convictions, l'exploration, les études et la recherche de sens",
        10: "la vocation, l'ambition, la réputation et la contribution sociale",
        11: "les amitiés, les projets collectifs et les aspirations futures",
        12: "la vie intérieure, l'inconscient, le retrait et les dimensions invisibles",
    },

    "en": {
        1: "identity, self-expression and the way you approach the world",
        2: "resources, personal values and material security",
        3: "communication, learning and everyday exchanges",
        4: "roots, home, privacy and emotional foundations",
        5: "creativity, pleasure, self-expression and matters of the heart",
        6: "daily life, practical work, habits and service",
        7: "relationships, partnership and the way you meet others",
        8: "transformation, deep intimacy and shared resources",
        9: "beliefs, exploration, education and the search for meaning",
        10: "vocation, ambition, reputation and social contribution",
        11: "friendship, collective projects and future aspirations",
        12: "inner life, the unconscious, withdrawal and invisible dimensions",
    },
}


# ============================================
# FONCTIONS SYMBOLIQUES DES PLANETES
# ============================================

PLANET_FUNCTIONS = {
    "fr": {
        "sun": {
            "title": "☀️ Soleil — Identité profonde",
            "function": (
                "Le Soleil représente symboliquement l'identité consciente, "
                "la vitalité et la manière de développer un sentiment de direction personnelle."
            ),
        },
        "moon": {
            "title": "🌙 Lune — Monde émotionnel",
            "function": (
                "La Lune représente symboliquement les besoins émotionnels, "
                "les réactions instinctives, les habitudes et ce qui procure un sentiment de sécurité."
            ),
        },
        "mercury": {
            "title": "☿ Mercure — Pensée et communication",
            "function": (
                "Mercure représente symboliquement la manière de penser, "
                "d'apprendre, de communiquer et de traiter l'information."
            ),
        },
        "venus": {
            "title": "♀ Vénus — Amour et valeurs",
            "function": (
                "Vénus représente symboliquement l'attachement, l'attraction, "
                "les valeurs, les plaisirs et la manière d'entrer en relation."
            ),
        },
        "mars": {
            "title": "♂ Mars — Action et désir",
            "function": (
                "Mars représente symboliquement l'action, l'affirmation, "
                "le désir, l'énergie combative et la manière de poursuivre ce que l'on veut."
            ),
        },
        "jupiter": {
            "title": "♃ Jupiter — Expansion",
            "function": (
                "Jupiter représente symboliquement l'expansion, la confiance, "
                "l'apprentissage, les convictions et les possibilités de développement."
            ),
        },
        "saturn": {
            "title": "♄ Saturne — Structure et maîtrise",
            "function": (
                "Saturne représente symboliquement les limites, les responsabilités, "
                "la discipline et les domaines où la maîtrise se construit progressivement."
            ),
        },
        "uranus": {
            "title": "♅ Uranus — Liberté et changement",
            "function": (
                "Uranus représente symboliquement l'indépendance, l'innovation, "
                "la rupture avec les habitudes et le besoin de fonctionner autrement."
            ),
        },
        "neptune": {
            "title": "♆ Neptune — Imagination et intuition",
            "function": (
                "Neptune représente symboliquement l'imagination, l'idéalisation, "
                "la sensibilité aux ambiances et la recherche d'une réalité plus vaste."
            ),
        },
        "pluto": {
            "title": "♇ Pluton — Transformation",
            "function": (
                "Pluton représente symboliquement la transformation profonde, "
                "les rapports au pouvoir, l'intensité et la capacité de renouvellement."
            ),
        },
    },

    "en": {
        "sun": {
            "title": "☀️ Sun — Core identity",
            "function": (
                "The Sun symbolically represents conscious identity, vitality "
                "and the development of a personal sense of direction."
            ),
        },
        "moon": {
            "title": "🌙 Moon — Emotional world",
            "function": (
                "The Moon symbolically represents emotional needs, instinctive "
                "responses, habits and what creates a sense of security."
            ),
        },
        "mercury": {
            "title": "☿ Mercury — Mind and communication",
            "function": (
                "Mercury symbolically represents thinking, learning, communication "
                "and the way information is processed."
            ),
        },
        "venus": {
            "title": "♀ Venus — Love and values",
            "function": (
                "Venus symbolically represents attraction, attachment, values, "
                "pleasure and the way relationships are approached."
            ),
        },
        "mars": {
            "title": "♂ Mars — Action and desire",
            "function": (
                "Mars symbolically represents action, assertion, desire, "
                "competitive energy and the pursuit of what is wanted."
            ),
        },
        "jupiter": {
            "title": "♃ Jupiter — Expansion",
            "function": (
                "Jupiter symbolically represents expansion, confidence, learning, "
                "belief and opportunities for development."
            ),
        },
        "saturn": {
            "title": "♄ Saturn — Structure and mastery",
            "function": (
                "Saturn symbolically represents limits, responsibility, discipline "
                "and the areas where mastery develops gradually."
            ),
        },
        "uranus": {
            "title": "♅ Uranus — Freedom and change",
            "function": (
                "Uranus symbolically represents independence, innovation, disruption "
                "and the desire to operate beyond established patterns."
            ),
        },
        "neptune": {
            "title": "♆ Neptune — Imagination and intuition",
            "function": (
                "Neptune symbolically represents imagination, idealisation, "
                "sensitivity to atmosphere and the search for something beyond the ordinary."
            ),
        },
        "pluto": {
            "title": "♇ Pluto — Transformation",
            "function": (
                "Pluto symbolically represents deep transformation, power dynamics, "
                "intensity and the capacity for renewal."
            ),
        },
    },
}


# ============================================
# INTERPRETATION D'UN PLACEMENT
# ============================================

def interpret_placement(
    planet_name,
    position,
    language="fr",
):
    language = (
        language
        if language in ("fr", "en")
        else "fr"
    )

    if not position:
        return None

    planet_data = PLANET_FUNCTIONS[
        language
    ].get(
        planet_name
    )

    if not planet_data:
        return None

    sign_key = position.get(
        "sign"
    )

    if sign_key not in SIGN_STYLE[
        language
]:

        return None

    sign_name = SIGN_NAMES[
        language
    ][
        sign_key
    ]

    sign_symbol = SIGN_SYMBOLS[
        sign_key
    ]

    sign_style = SIGN_STYLE[
        language
    ][
        sign_key
    ]

    degree = position.get(
        "degree"
    )

    house_number = position.get(
        "house"
    )

    if degree is not None:
        placement_label = (
            f"{sign_symbol} {sign_name} "
            f"{degree:.2f}°"
        )
    else:
        placement_label = (
            f"{sign_symbol} {sign_name}"
        )

    if language == "fr":
        text = (
            f"{planet_data['function']}\n\n"
            f"Dans ton thème, {planet_name_label(planet_name, language)} "
            f"se trouve en {placement_label}. "
            f"Cette fonction tend donc à s'exprimer {sign_style}."
        )

        if house_number:
            house_theme = HOUSE_THEMES[
                language
            ].get(
                house_number
            )

            if house_theme:
                text += (
                    f"\n\nSa présence en Maison {house_number} "
                    f"met particulièrement l'accent sur {house_theme}."
                )

    else:
        text = (
            f"{planet_data['function']}\n\n"
            f"In your chart, {planet_name_label(planet_name, language)} "
            f"is placed in {placement_label}. "
            f"This function therefore tends to express itself {sign_style}."
        )

        if house_number:
            house_theme = HOUSE_THEMES[
                language
            ].get(
                house_number
            )

            if house_theme:
                text += (
                    f"\n\nIts placement in House {house_number} "
                    f"places particular emphasis on {house_theme}."
                )

    return {
        "title": planet_data[
            "title"
        ],
        "text": text,
        "planet": planet_name,
        "sign": sign_key,
        "degree": degree,
        "house": house_number,
    }


# ============================================
# LABEL COURT D'UNE PLANETE
# ============================================

def planet_name_label(
    planet_name,
    language="fr",
):
    labels = {
        "fr": {
            "sun": "le Soleil",
            "moon": "la Lune",
            "mercury": "Mercure",
            "venus": "Vénus",
            "mars": "Mars",
            "jupiter": "Jupiter",
            "saturn": "Saturne",
            "uranus": "Uranus",
            "neptune": "Neptune",
            "pluto": "Pluton",
        },
        "en": {
            "sun": "the Sun",
            "moon": "the Moon",
            "mercury": "Mercury",
            "venus": "Venus",
            "mars": "Mars",
            "jupiter": "Jupiter",
            "saturn": "Saturn",
            "uranus": "Uranus",
            "neptune": "Neptune",
            "pluto": "Pluto",
        },
    }

    return labels[
        language
    ].get(
        planet_name,
        planet_name
    )


# ============================================
# ASCENDANT
# ============================================

def interpret_ascendant(
    chart,
    language="fr",
):
    language = (
        language
        if language in ("fr", "en")
        else "fr"
    )

    ascendant = chart.get(
        "ascendant"
    )

    if not ascendant:
        return None

    sign_key = ascendant.get(
        "sign"
    )

    if sign_key not in SIGN_STYLE[
        language
    ]:


        return None

    sign_name = SIGN_NAMES[
        language
    ][
        sign_key
    ]

    symbol = SIGN_SYMBOLS[
        sign_key
    ]

    degree = ascendant.get(
        "degree"
    )

    style = SIGN_STYLE[
        language
    ][
        sign_key
    ]

    if language == "fr":
        return {
            "title": "⬆️ Ascendant — Expression extérieure",
            "text": (
                f"Ton Ascendant est {symbol} {sign_name} "
                f"{degree:.2f}°.\n\n"
                "Dans la tradition astrologique, l'Ascendant décrit "
                "la manière d'aborder spontanément le monde et la première "
                "façon dont l'énergie personnelle se manifeste. "
                f"Cette expression tend ici à fonctionner {style}."
            ),
            "sign": sign_key,
            "degree": degree,
        }

    return {
        "title": "⬆️ Ascendant — Outer expression",
        "text": (
            f"Your Ascendant is {symbol} {sign_name} "
            f"{degree:.2f}°.\n\n"
            "In astrological tradition, the Ascendant describes "
            "the spontaneous approach to the world and the first "
            "way personal energy tends to express itself. "
            f"Here, that expression tends to operate {style}."
        ),
        "sign": sign_key,
        "degree": degree,
    }


# ============================================
# GENERATION DU PROFIL NATAL INTERPRETE
# ============================================

def interpret_natal_chart(
    chart,
    language="fr",
):
    language = (
        language
        if language in ("fr", "en")
        else "fr"
    )

    if not chart:
        return {
            "available": False,
            "reason": "missing_chart",
            "sections": [],
        }

    if not chart.get(
        "calculated"
    ):
        return {
            "available": False,
            "reason": "chart_not_calculated",
            "sections": [],
        }

    sections = []

    ascendant_section = interpret_ascendant(
        chart,
        language
    )

    if ascendant_section:
        sections.append(
            ascendant_section
        )

    positions = chart.get(
        "positions",
        {}
    )

    planet_order = (
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

    for planet_name in planet_order:
        section = interpret_placement(
            planet_name=planet_name,
            position=positions.get(
                planet_name
            ),
            language=language,
        )

        if section:
            sections.append(
                section
            )

    return {
        "available": bool(
            sections
        ),
        "reason": None,
        "language": language,
        "sections": sections,
        "houses_available": chart.get(
            "houses_available",
            False
        ),
        "time_precision": chart.get(
            "time_precision"
        ),
    }


# ============================================
# FORMAT TEXTE POUR TESTS
# ============================================

def format_natal_interpretation(
    interpretation,
    language="fr",
):
    language = (
        language
        if language in ("fr", "en")
        else "fr"
    )

    if not interpretation.get(
        "available"
    ):
        if language == "en":
            return (
                "❌ Natal interpretation "
                "is not available."
            )

        return (
            "❌ L'interprétation natale "
            "n'est pas disponible."
        )

    if language == "en":
        title = (
            "✨ YOUR ASTROVIBE NATAL PROFILE"
        )
    else:
        title = (
            "✨ TON PROFIL NATAL ASTROVIBE"
        )

    parts = [
        title
    ]

    for section in interpretation[
        "sections"
    ]:
        parts.append(
            section[
                "title"
            ]
            + "\n\n"
            + section[
                "text"
            ]
        )

    return "\n\n".join(
        parts
    )
