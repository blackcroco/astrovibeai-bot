import hashlib
import random
from datetime import datetime, timezone


SIGN_DATA_EN = {
    "♈ Bélier": {
        "name": "Aries",
        "emoji": "♈",
        "tone": [
            "Your natural drive may open an unexpected door today.",
            "Your determination is valuable, provided that speed does not become haste.",
            "A bold energy supports thoughtful initiatives and decisive action."
        ]
    },
    "♉ Taureau": {
        "name": "Taurus",
        "emoji": "♉",
        "tone": [
            "Your inner stability helps you separate what matters from what does not.",
            "Time works in your favor when you move with patience and confidence.",
            "A calm and practical approach can turn uncertainty into clarity."
        ]
    },
    "♊ Gémeaux": {
        "name": "Gemini",
        "emoji": "♊",
        "tone": [
            "Your curiosity reveals possibilities that others may overlook.",
            "Conversations can help you clarify an important intention today.",
            "Your mental agility is an advantage when you maintain a clear direction."
        ]
    },
    "♋ Cancer": {
        "name": "Cancer",
        "emoji": "♋",
        "tone": [
            "Your intuition notices what has not yet been openly expressed.",
            "Sensitivity becomes a strength when it guides rather than overwhelms you.",
            "Taking care of your inner balance will improve your interactions today."
        ]
    },
    "♌ Lion": {
        "name": "Leo",
        "emoji": "♌",
        "tone": [
            "Your confidence attracts attention, but your ability to listen makes the difference.",
            "An opportunity to demonstrate your strengths may arise naturally.",
            "Your presence is most powerful when it inspires rather than demands."
        ]
    },
    "♍ Vierge": {
        "name": "Virgo",
        "emoji": "♍",
        "tone": [
            "Your attention to detail can resolve a situation that has remained unclear.",
            "Simple organization will create more room for calm and concentration.",
            "You can make meaningful progress without trying to control every detail."
        ]
    },
    "♎ Balance": {
        "name": "Libra",
        "emoji": "♎",
        "tone": [
            "A decision becomes easier when your own needs are included in the balance.",
            "Your diplomatic nature supports an important conversation today.",
            "Harmony matters, but it should not prevent you from stating your position."
        ]
    },
    "♏ Scorpion": {
        "name": "Scorpio",
        "emoji": "♏",
        "tone": [
            "Your depth of perception helps you recognize the real issue beneath the surface.",
            "A quiet transformation is taking place and deserves your trust.",
            "Your insight is valuable, but simple explanations may be enough today."
        ]
    },
    "♐ Sagittaire": {
        "name": "Sagittarius",
        "emoji": "♐",
        "tone": [
            "Your desire to move forward is finding a clearer direction.",
            "A new idea may broaden your understanding of a project or relationship.",
            "Your enthusiasm is contagious when it is supported by a practical plan."
        ]
    },
    "♑ Capricorne": {
        "name": "Capricorn",
        "emoji": "♑",
        "tone": [
            "Your steady efforts are beginning to produce more visible results.",
            "A responsible decision can strengthen an important long-term project.",
            "Your reliability inspires trust, but remember to acknowledge your progress."
        ]
    },
    "♒ Verseau": {
        "name": "Aquarius",
        "emoji": "♒",
        "tone": [
            "An original idea may find a surprisingly practical application today.",
            "Independent thinking helps you move beyond an outdated pattern.",
            "An unexpected conversation could inspire a promising new direction."
        ]
    },
    "♓ Poissons": {
        "name": "Pisces",
        "emoji": "♓",
        "tone": [
            "Your imagination and intuition work especially well together today.",
            "A subtle impression deserves attention before you make a decision.",
            "Your empathy strengthens connections when your own boundaries remain clear."
        ]
    }
}


LOVE_TEXTS_EN = [
    (
        "An honest conversation can bring two people closer than a dramatic gesture. "
        "If you are in a relationship, choose simple and direct words. If you are single, "
        "an interesting connection may begin with an ordinary conversation."
    ),
    (
        "The atmosphere supports mutual understanding. An unspoken expectation can be "
        "clarified with kindness. Avoid assumptions and allow the other person to explain "
        "their perspective fully."
    ),
    (
        "You may feel a stronger need for emotional closeness. Offer attention without "
        "forgetting your own pace. A relationship grows through patience, balance and "
        "genuine listening."
    ),
    (
        "Emotions are present, but they do not require an immediate reaction. A reassuring "
        "message may calm a small tension. If you are single, notice someone who has remained "
        "quietly in the background."
    ),
    (
        "A warm energy surrounds your relationships. This is a good moment to reconnect, "
        "create a pleasant memory or show your interest naturally. Sincerity will work better "
        "than a complicated strategy."
    ),
    (
        "Greater clarity may be needed in an important relationship. Ask meaningful questions "
        "with care. An honest answer, even an imperfect one, can help build something stronger."
    ),
    (
        "Affection is expressed through small, thoughtful actions today. A message, a detail "
        "or genuine availability may carry more meaning than a grand declaration."
    ),
    (
        "An old hesitation may begin to lose its power. Look at a relationship with fresh eyes "
        "and avoid forcing a conclusion. Trust can develop gradually."
    )
]


WORK_TEXTS_EN = [
    (
        "One priority deserves to be separated from everything else. Moving step by step will "
        "improve both efficiency and visibility. Financially, check the details before making "
        "a commitment."
    ),
    (
        "An idea or proposal may develop favorably when presented with precision. Focus on "
        "practical benefits. Regarding money, caution is wiser than promises of quick returns."
    ),
    (
        "Cooperation may be more productive than working alone. Someone else can provide the "
        "missing perspective. A small financial adjustment could create lasting benefits."
    ),
    (
        "A postponed task finally requires your attention. Once started, it may be easier than "
        "expected. Do not let a minor expense distract you from a more important objective."
    ),
    (
        "Your work may be noticed even if recognition is not immediate. Continue consistently. "
        "A financial decision deserves reflection rather than an impulsive response."
    ),
    (
        "The day favors adjustments, corrections and negotiations. You do not need to begin "
        "again from zero. A few focused improvements may be enough."
    ),
    (
        "An interesting opportunity could be hidden inside an ordinary request. Stay available "
        "while protecting your schedule. Spend on what offers genuine long-term value."
    ),
    (
        "Separate what is urgent from what is truly important. Better organization will free "
        "energy for projects with greater potential."
    )
]


ENERGY_TEXTS_EN = [
    (
        "Your energy is steady, but it may decline if your attention becomes too scattered. "
        "Choose a sustainable pace and allow yourself a genuine break."
    ),
    (
        "Your vitality may arrive in waves. Use the more dynamic moments to move forward, then "
        "give yourself time to recover. Gentle movement can restore balance."
    ),
    (
        "Your mind may be more active than your body today. Reducing distractions will improve "
        "your concentration. A short walk or a few calm breaths may clear your thoughts."
    ),
    (
        "Pay attention to subtle signs of fatigue. You do not need to stop completely, but your "
        "energy will benefit from better distribution throughout the day."
    ),
    (
        "A constructive energy supports you. Use it to complete a manageable task or bring order "
        "to your surroundings, while respecting your limits."
    ),
    (
        "Your balance will depend on the quality of your transitions. Avoid moving from one task "
        "to another without a pause. A few quiet minutes can restore your focus."
    ),
    (
        "Enthusiasm may encourage you to take on too much. Choose one main direction and keep "
        "some energy available for the end of the day."
    ),
    (
        "A calmer atmosphere supports emotional recovery. Step away from unnecessary demands "
        "for a moment. Your effectiveness will return when your mind feels less crowded."
    )
]


ADVICE_TEXTS_EN = [
    "Choose clarity over haste.",
    "One small, consistent action is worth more than a large intention repeatedly postponed.",
    "Listen to your intuition, then support it with practical facts.",
    "Protect your energy without closing the door to communication.",
    "You do not need to solve everything today. Focus on what is genuinely within your control.",
    "Express what you need instead of expecting others to guess.",
    "Take a moment to recognize the progress you have already made.",
    "Flexibility may be more effective than control today."
]


COLORS_EN = [
    "Gold",
    "Midnight blue",
    "Deep violet",
    "Emerald green",
    "Pearl white",
    "Garnet red",
    "Sky blue",
    "Soft pink",
    "Copper",
    "Indigo"
]


KEYWORDS_EN = [
    "Clarity",
    "Balance",
    "Confidence",
    "Momentum",
    "Renewal",
    "Patience",
    "Intuition",
    "Harmony",
    "Courage",
    "Openness"
]


def build_seed(sign, date_string):
    raw_value = f"astrovibe-en|{sign}|{date_string}"

    digest = hashlib.sha256(
        raw_value.encode("utf-8")
    ).hexdigest()

    return int(digest[:16], 16)


def generate_daily_horoscope_en(sign):
    today = datetime.now(timezone.utc).date()
    date_string = today.isoformat()

    sign_data = SIGN_DATA_EN.get(sign)

    if not sign_data:
        return None

    randomizer = random.Random(
        build_seed(sign, date_string)
    )

    introduction = randomizer.choice(
        sign_data["tone"]
    )

    love = randomizer.choice(
        LOVE_TEXTS_EN
    )

    work = randomizer.choice(
        WORK_TEXTS_EN
    )

    energy = randomizer.choice(
        ENERGY_TEXTS_EN
    )

    advice = randomizer.choice(
        ADVICE_TEXTS_EN
    )

    color = randomizer.choice(
        COLORS_EN
    )

    keyword = randomizer.choice(
        KEYWORDS_EN
    )

    lucky_number = randomizer.randint(
        1,
        22
    )

    love_score = randomizer.randint(
        6,
        9
    )

    work_score = randomizer.randint(
        6,
        9
    )

    energy_score = randomizer.randint(
        5,
        9
    )

    luck_score = randomizer.randint(
        5,
        9
    )

    date_display = today.strftime(
        "%d/%m/%Y"
    )

    horoscope = (
        f"🌌 ASTROVIBE • {date_display}\n"
        f"{sign_data['emoji']} "
        f"{sign_data['name'].upper()}\n\n"

        f"✨ DAILY OUTLOOK\n"
        f"{introduction}\n\n"

        f"❤️ LOVE • {love_score}/10\n"
        f"{love}\n\n"

        f"💼 WORK & FINANCES • "
        f"{work_score}/10\n"
        f"{work}\n\n"

        f"🌿 ENERGY & WELL-BEING • "
        f"{energy_score}/10\n"
        f"{energy}\n\n"

        f"🍀 LUCK • {luck_score}/10\n"
        f"🎨 Color of the day: {color}\n"
        f"🔢 Lucky number: {lucky_number}\n"
        f"💫 Keyword: {keyword}\n\n"

        f"🌙 ASTROVIBE ADVICE\n"
        f"{advice}\n\n"

        f"──────────────\n"
        f"Content intended for entertainment "
        f"and personal reflection."
    )

    return horoscope
