import hashlib
import random


# ==================================================
# ZODIAC SIGN DATA
# Internal keys remain in French to match Neon data.
# ==================================================

SIGN_DATA_EN = {
    "♈ Bélier": {
        "name": "Aries",
        "emoji": "♈",
        "element": "Fire",
        "quality": "Cardinal"
    },
    "♉ Taureau": {
        "name": "Taurus",
        "emoji": "♉",
        "element": "Earth",
        "quality": "Fixed"
    },
    "♊ Gémeaux": {
        "name": "Gemini",
        "emoji": "♊",
        "element": "Air",
        "quality": "Mutable"
    },
    "♋ Cancer": {
        "name": "Cancer",
        "emoji": "♋",
        "element": "Water",
        "quality": "Cardinal"
    },
    "♌ Lion": {
        "name": "Leo",
        "emoji": "♌",
        "element": "Fire",
        "quality": "Fixed"
    },
    "♍ Vierge": {
        "name": "Virgo",
        "emoji": "♍",
        "element": "Earth",
        "quality": "Mutable"
    },
    "♎ Balance": {
        "name": "Libra",
        "emoji": "♎",
        "element": "Air",
        "quality": "Cardinal"
    },
    "♏ Scorpion": {
        "name": "Scorpio",
        "emoji": "♏",
        "element": "Water",
        "quality": "Fixed"
    },
    "♐ Sagittaire": {
        "name": "Sagittarius",
        "emoji": "♐",
        "element": "Fire",
        "quality": "Mutable"
    },
    "♑ Capricorne": {
        "name": "Capricorn",
        "emoji": "♑",
        "element": "Earth",
        "quality": "Cardinal"
    },
    "♒ Verseau": {
        "name": "Aquarius",
        "emoji": "♒",
        "element": "Air",
        "quality": "Fixed"
    },
    "♓ Poissons": {
        "name": "Pisces",
        "emoji": "♓",
        "element": "Water",
        "quality": "Mutable"
    }
}


# ==================================================
# RELATIONSHIPS BETWEEN DIFFERENT ELEMENTS
# ==================================================

ELEMENT_RELATIONS_EN = {
    frozenset(["Fire", "Air"]): {
        "base": 82,
        "dynamic": (
            "This connection brings together inspiration and momentum. "
            "Fire provides courage and enthusiasm, while Air brings ideas, "
            "curiosity and communication. Together, these signs can create "
            "a lively relationship that rarely feels predictable."
        ),
        "strength": (
            "Spontaneity, creativity and mutual encouragement are among "
            "the greatest strengths of this pairing. Each person can help "
            "the other explore new possibilities."
        ),
        "challenge": (
            "The relationship may sometimes lack consistency. Promises and "
            "exciting ideas need to be supported by practical action if the "
            "connection is to remain strong over time."
        )
    },

    frozenset(["Earth", "Water"]): {
        "base": 84,
        "dynamic": (
            "This pairing combines emotional sensitivity with stability. "
            "Earth offers structure and reassurance, while Water brings "
            "intuition, empathy and emotional depth."
        ),
        "strength": (
            "Loyalty, patience and the desire to build something meaningful "
            "can create a deeply supportive and lasting relationship."
        ),
        "challenge": (
            "Both partners may become overly cautious or hold back difficult "
            "feelings. Honest communication is essential before unspoken "
            "emotions become too heavy."
        )
    },

    frozenset(["Fire", "Water"]): {
        "base": 64,
        "dynamic": (
            "This relationship combines passion with sensitivity. Attraction "
            "can be powerful, but the two partners may process emotions at "
            "very different speeds."
        ),
        "strength": (
            "Fire encourages courage and action, while Water brings intuition "
            "and emotional awareness. When balanced, these differences can "
            "create genuine personal growth."
        ),
        "challenge": (
            "Direct words may hurt the more sensitive partner, while silence "
            "or emotional withdrawal may confuse the more spontaneous one. "
            "Gentleness and clarity are especially important."
        )
    },

    frozenset(["Earth", "Air"]): {
        "base": 66,
        "dynamic": (
            "This pairing brings practical thinking together with intellectual "
            "freedom. The relationship can become rewarding when both partners "
            "respect their different ways of understanding life."
        ),
        "strength": (
            "Air introduces new perspectives and possibilities, while Earth "
            "helps turn ideas into realistic and lasting plans."
        ),
        "challenge": (
            "One partner may appear too cautious, while the other may seem "
            "inconsistent or detached. Clear expectations will prevent many "
            "avoidable misunderstandings."
        )
    },

    frozenset(["Fire", "Earth"]): {
        "base": 71,
        "dynamic": (
            "The ambition of Fire meets the realism of Earth. This connection "
            "can be highly productive when determination is used to cooperate "
            "rather than compete."
        ),
        "strength": (
            "One partner brings initiative and enthusiasm, while the other "
            "provides patience, structure and practical judgment. Together, "
            "they can turn inspiration into results."
        ),
        "challenge": (
            "Their different pace may create frustration. Fire wants immediate "
            "movement, while Earth prefers to verify that every step is secure "
            "before moving forward."
        )
    },

    frozenset(["Air", "Water"]): {
        "base": 69,
        "dynamic": (
            "This relationship combines thought with feeling. Air seeks clarity "
            "through conversation, while Water understands situations through "
            "intuition and emotional perception."
        ),
        "strength": (
            "The connection can become remarkably insightful when thoughts and "
            "emotions are shared openly and without judgment."
        ),
        "challenge": (
            "One partner may talk about emotions without fully experiencing "
            "them, while the other may feel deeply without finding the right "
            "words. Patience will improve mutual understanding."
        )
    }
}


# ==================================================
# RELATIONSHIPS WITHIN THE SAME ELEMENT
# ==================================================

SAME_ELEMENT_TEXTS_EN = {
    "Fire": {
        "base": 80,
        "dynamic": (
            "Two passionate temperaments meet in this relationship. "
            "Enthusiasm, confidence and the desire to experience life fully "
            "can create a powerful and exciting connection."
        ),
        "strength": (
            "Mutual motivation, admiration and shared energy naturally "
            "strengthen the bond."
        ),
        "challenge": (
            "Impatience and strong personalities may lead to conflict. "
            "Both partners need room to express themselves and take initiative."
        )
    },

    "Earth": {
        "base": 86,
        "dynamic": (
            "This relationship is based on stability, trust and the desire "
            "to build something reliable and lasting."
        ),
        "strength": (
            "Loyalty, realism and consistency create a reassuring foundation "
            "for both partners."
        ),
        "challenge": (
            "Routine may gradually take up too much space. The relationship "
            "benefits from regular moments of novelty and spontaneity."
        )
    },

    "Air": {
        "base": 81,
        "dynamic": (
            "Ideas flow easily between these partners. The relationship thrives "
            "on conversation, discovery, humor and intellectual freedom."
        ),
        "strength": (
            "Communication, curiosity and a shared openness to new experiences "
            "create genuine companionship."
        ),
        "challenge": (
            "The connection may sometimes remain too intellectual. Both partners "
            "need to create space for vulnerability and emotional depth."
        )
    },

    "Water": {
        "base": 85,
        "dynamic": (
            "The emotional connection between these partners may be deep, "
            "intuitive and protective. Each person can perceive the other's "
            "feelings with remarkable sensitivity."
        ),
        "strength": (
            "Empathy, tenderness and emotional understanding can create a rare "
            "sense of closeness."
        ),
        "challenge": (
            "Strong sensitivity may amplify silence and misunderstanding. "
            "Personal boundaries and emotional needs should remain clearly stated."
        )
    }
}


# ==================================================
# RELATIONSHIP QUALITIES
# ==================================================

QUALITY_TEXTS_EN = {
    "Cardinal": (
        "Both partners naturally like to initiate, decide and move situations "
        "forward. This creates momentum, but important decisions must remain "
        "shared rather than becoming a competition for control."
    ),

    "Fixed": (
        "Both partners value loyalty, continuity and commitment. This stability "
        "can be a major strength, provided that determination does not turn "
        "into stubbornness or emotional rigidity."
    ),

    "Mutable": (
        "Both partners are capable of adapting, learning and evolving. "
        "The relationship remains flexible and alive, but it benefits from "
        "a few clear agreements and shared long-term goals."
    )
}


# ==================================================
# GENERAL ADVICE
# ==================================================

GENERAL_ADVICE_EN = [
    (
        "Express your expectations before they become frustrations. "
        "Transparency will strengthen this relationship."
    ),
    (
        "Respect the qualities that make each partner different instead of "
        "trying to approach every situation in exactly the same way."
    ),
    (
        "Create shared projects while preserving enough personal space. "
        "That balance will support both closeness and individuality."
    ),
    (
        "During disagreements, try to understand the need behind the other "
        "person's reaction before defending your own position."
    ),
    (
        "Small and consistent gestures of care will have more impact than "
        "occasional promises or dramatic declarations."
    ),
    (
        "The connection becomes stronger when both partners can speak honestly "
        "without immediately feeling judged, corrected or dismissed."
    )
]


# ==================================================
# STABLE RANDOM GENERATION
# ==================================================

def stable_randomizer(first_sign, second_sign):
    ordered_pair = sorted([
        first_sign,
        second_sign
    ])

    raw_value = (
        "astrovibe-compatibility|"
        + "|".join(ordered_pair)
    )

    digest = hashlib.sha256(
        raw_value.encode("utf-8")
    ).hexdigest()

    seed = int(
        digest[:16],
        16
    )

    return random.Random(seed)


def clamp_score(value):
    return max(
        4,
        min(
            10,
            value
        )
    )


# ==================================================
# ENGLISH COMPATIBILITY GENERATOR
# ==================================================

def generate_compatibility_en(
    first_sign,
    second_sign
):
    first = SIGN_DATA_EN.get(
        first_sign
    )

    second = SIGN_DATA_EN.get(
        second_sign
    )

    if not first or not second:
        return None

    randomizer = stable_randomizer(
        first_sign,
        second_sign
    )

    same_sign = (
        first_sign == second_sign
    )

    same_element = (
        first["element"]
        == second["element"]
    )

    if same_element:
        relation = SAME_ELEMENT_TEXTS_EN[
            first["element"]
        ]
    else:
        relation = ELEMENT_RELATIONS_EN[
            frozenset([
                first["element"],
                second["element"]
            ])
        ]

    base_percentage = relation["base"]

    if same_sign:
        base_percentage += 2

    if first["quality"] == second["quality"]:
        base_percentage += 2

    overall_percentage = max(
        50,
        min(
            95,
            base_percentage
            + randomizer.randint(-3, 3)
        )
    )

    base_score = round(
        overall_percentage / 10
    )

    attraction = clamp_score(
        base_score
        + randomizer.randint(-1, 1)
    )

    communication = clamp_score(
        base_score
        + randomizer.randint(-2, 1)
    )

    passion = clamp_score(
        base_score
        + randomizer.randint(-1, 2)
    )

    stability = clamp_score(
        base_score
        + randomizer.randint(-2, 1)
    )

    emotional = clamp_score(
        base_score
        + randomizer.randint(-1, 1)
    )

    if first["quality"] == second["quality"]:
        quality_analysis = QUALITY_TEXTS_EN[
            first["quality"]
        ]
    else:
        quality_analysis = (
            f"The {first['quality'].lower()} nature of "
            f"{first['name']} meets the "
            f"{second['quality'].lower()} rhythm of "
            f"{second['name']}. This difference can become "
            f"complementary when both partners respect the "
            f"other person's natural way of moving forward."
        )

    advice = randomizer.choice(
        GENERAL_ADVICE_EN
    )

    if overall_percentage >= 85:
        verdict = (
            "A naturally strong match with excellent potential "
            "for emotional closeness, mutual support and lasting commitment."
        )

    elif overall_percentage >= 75:
        verdict = (
            "A promising compatibility that can grow through "
            "honest communication, trust and consistent attention."
        )

    elif overall_percentage >= 65:
        verdict = (
            "A complementary relationship that requires a few adjustments, "
            "but can become deeply rewarding for both partners."
        )

    else:
        verdict = (
            "A relationship built on strong contrasts. It can work when "
            "differences are understood, respected and used as opportunities "
            "for growth."
        )

    result = (
        "🌌 ASTROVIBE • COMPATIBILITY\n\n"

        f"{first['emoji']} "
        f"{first['name'].upper()}\n"

        f"×\n"

        f"{second['emoji']} "
        f"{second['name'].upper()}\n\n"

        f"💞 OVERALL COMPATIBILITY: "
        f"{overall_percentage}%\n"

        f"{verdict}\n\n"

        f"❤️ Attraction: {attraction}/10\n"
        f"💬 Communication: {communication}/10\n"
        f"🔥 Passion: {passion}/10\n"
        f"🤝 Stability: {stability}/10\n"
        f"🌙 Emotional Connection: "
        f"{emotional}/10\n\n"

        f"✨ YOUR DYNAMIC\n"
        f"{relation['dynamic']}\n\n"

        f"💖 YOUR STRENGTHS\n"
        f"{relation['strength']}\n\n"

        f"⚡ YOUR CHALLENGES\n"
        f"{relation['challenge']}\n\n"

        f"🔭 YOUR RELATIONSHIP RHYTHM\n"
        f"{quality_analysis}\n\n"

        f"🌙 ASTROVIBE ADVICE\n"
        f"{advice}\n\n"

        f"──────────────\n"
        f"Content intended for entertainment "
        f"and personal reflection."
    )

    return result
