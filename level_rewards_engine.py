# ==========================================
# ASTROVIBE LEVEL REWARDS V1
# ==========================================
#
# Points remain cumulative experience.
# This engine never writes to the database,
# never removes points and never grants
# Premium, Profile access or Telegram Stars.
# ==========================================


LEVEL_THRESHOLDS = {
    1: 0,
    2: 40,
    3: 100,
    4: 250,
    5: 500,
    6: 1000,
}


LEVEL_NAMES_FR = {
    1: "Observateur céleste",
    2: "Explorateur du Zodiaque",
    3: "Gardien des étoiles",
    4: "Oracle cosmique",
    5: "Maître du Zodiaque",
    6: "Légende astrale",
}


LEVEL_NAMES_EN = {
    1: "Celestial Observer",
    2: "Zodiac Explorer",
    3: "Guardian of the Stars",
    4: "Cosmic Oracle",
    5: "Zodiac Master",
    6: "Astral Legend",
}


REWARD_NAMES_FR = {
    2: "🔭 Insight céleste",
    3: "⭐ Message des astres",
    4: "🔮 Focus cosmique",
    5: "🌌 Guidance astrale",
    6: "🏆 Lecture Légende",
}


REWARD_NAMES_EN = {
    2: "🔭 Celestial Insight",
    3: "⭐ Message from the Stars",
    4: "🔮 Cosmic Focus",
    5: "🌌 Astral Guidance",
    6: "🏆 Legend Reading",
}


SIGN_GUIDANCE_FR = {
    "Bélier": (
        "Ton énergie avance vite. Choisis "
        "aujourd'hui une action claire et "
        "termine-la avant d'en commencer une autre."
    ),
    "Taureau": (
        "Ta stabilité est une force. Protège ce "
        "qui compte tout en laissant une petite "
        "place au changement."
    ),
    "Gémeaux": (
        "Tes idées ont besoin d'un fil conducteur. "
        "Note l'essentiel avant de te disperser."
    ),
    "Cancer": (
        "Ton intuition capte les nuances. Écoute-la "
        "sans porter les émotions des autres."
    ),
    "Lion": (
        "Ton rayonnement grandit lorsque ta "
        "confiance sert une intention sincère."
    ),
    "Vierge": (
        "Ton sens du détail peut transformer une "
        "petite amélioration en vrai progrès."
    ),
    "Balance": (
        "Cherche l'équilibre sans repousser une "
        "décision qui mérite d'être prise."
    ),
    "Scorpion": (
        "Ta profondeur révèle ce qui doit évoluer. "
        "Concentre ton énergie sur l'essentiel."
    ),
    "Sagittaire": (
        "Ton élan ouvre des horizons. Donne-lui "
        "une direction concrète aujourd'hui."
    ),
    "Capricorne": (
        "Ta constance construit loin. Avance par "
        "une étape simple mais solide."
    ),
    "Verseau": (
        "Ton regard original éclaire une solution "
        "que les habitudes ne montrent pas."
    ),
    "Poissons": (
        "Ta sensibilité nourrit l'inspiration. "
        "Ancre une intuition dans une action réelle."
    ),
}


SIGN_GUIDANCE_EN = {
    "Aries": (
        "Your energy moves quickly. Choose one "
        "clear action today and finish it before "
        "starting another."
    ),
    "Taurus": (
        "Your stability is a strength. Protect "
        "what matters while leaving some room "
        "for change."
    ),
    "Gemini": (
        "Your ideas need a guiding thread. Write "
        "down the essential before spreading "
        "your attention too widely."
    ),
    "Cancer": (
        "Your intuition notices subtle details. "
        "Listen to it without carrying everyone "
        "else's emotions."
    ),
    "Leo": (
        "Your presence grows when confidence "
        "serves a sincere intention."
    ),
    "Virgo": (
        "Your attention to detail can turn one "
        "small improvement into real progress."
    ),
    "Libra": (
        "Seek balance without postponing a "
        "decision that deserves to be made."
    ),
    "Scorpio": (
        "Your depth reveals what needs to evolve. "
        "Focus your energy on what truly matters."
    ),
    "Sagittarius": (
        "Your momentum opens new horizons. Give "
        "it one concrete direction today."
    ),
    "Capricorn": (
        "Your consistency builds for the long "
        "term. Take one simple but solid step."
    ),
    "Aquarius": (
        "Your original perspective reveals a "
        "solution that habit cannot see."
    ),
    "Pisces": (
        "Your sensitivity feeds inspiration. "
        "Ground one intuition in a real action."
    ),
}


def normalize_points(value):
    try:
        points = int(value)
    except (TypeError, ValueError):
        return 0

    return max(points, 0)


def calculate_reward_level(points):
    normalized = normalize_points(points)

    if normalized >= 1000:
        return 6

    if normalized >= 500:
        return 5

    if normalized >= 250:
        return 4

    if normalized >= 100:
        return 3

    if normalized >= 40:
        return 2

    return 1


def get_level_name(level, language="fr"):
    names = (
        LEVEL_NAMES_EN
        if language == "en"
        else LEVEL_NAMES_FR
    )

    return names.get(
        int(level or 1),
        names[1],
    )


def get_unlocked_rewards(points):
    level = calculate_reward_level(
        points
    )

    return [
        reward_level
        for reward_level
        in range(2, 7)
        if reward_level <= level
    ]


def get_next_reward(points):
    normalized = normalize_points(points)

    for level in range(2, 7):
        threshold = LEVEL_THRESHOLDS[
            level
        ]

        if normalized < threshold:
            return {
                "level": level,
                "threshold": threshold,
                "remaining": (
                    threshold
                    - normalized
                ),
            }

    return None


def build_rewards_summary(
    points,
    language="fr",
):
    normalized = normalize_points(
        points
    )

    level = calculate_reward_level(
        normalized
    )

    names = (
        REWARD_NAMES_EN
        if language == "en"
        else REWARD_NAMES_FR
    )

    output = []

    if language == "en":
        output.extend(
            [
                "🎁 Your AstroVibe rewards",
                "",
                (
                    f"⭐ Points: {normalized}"
                ),
                (
                    "🏆 Level "
                    f"{level}: "
                    f"{get_level_name(level, language)}"
                ),
                "",
            ]
        )
    else:
        output.extend(
            [
                "🎁 Tes récompenses AstroVibe",
                "",
                (
                    f"⭐ Points : {normalized}"
                ),
                (
                    "🏆 Niveau "
                    f"{level} : "
                    f"{get_level_name(level, language)}"
                ),
                "",
            ]
        )

    for reward_level in range(2, 7):
        threshold = LEVEL_THRESHOLDS[
            reward_level
        ]

        reward_name = names[
            reward_level
        ]

        if level >= reward_level:
            output.append(
                f"✅ {reward_name}"
            )
        else:
            output.append(
                (
                    f"🔒 {reward_name} "
                    f"— {threshold} points"
                )
            )

    next_reward = get_next_reward(
        normalized
    )

    output.append("")

    if next_reward is None:
        if language == "en":
            output.append(
                "🏆 All level rewards unlocked."
            )
        else:
            output.append(
                "🏆 Toutes les récompenses "
                "de niveau sont débloquées."
            )
    else:
        if language == "en":
            output.append(
                "📈 "
                f"{next_reward['remaining']} "
                "points until the next reward."
            )
        else:
            output.append(
                "📈 Plus que "
                f"{next_reward['remaining']} "
                "points avant la prochaine "
                "récompense."
            )

    if level >= 2:
        output.append("")

        if language == "en":
            output.append(
                "Use /rewards to read your "
                "unlocked celestial guidance."
            )
        else:
            output.append(
                "Utilise /rewards pour lire "
                "tes guidances célestes "
                "débloquées."
            )

    return "\n".join(output)


def _normalize_sign(
    sign,
    language,
):
    if not isinstance(sign, str):
        return "Aries" if language == "en" else "Bélier"

    normalized = sign.strip()

    if not normalized:
        return "Aries" if language == "en" else "Bélier"

    return normalized


def _base_guidance(
    sign,
    language,
):
    normalized_sign = _normalize_sign(
        sign,
        language,
    )

    mapping = (
        SIGN_GUIDANCE_EN
        if language == "en"
        else SIGN_GUIDANCE_FR
    )

    fallback = (
        "Your celestial rhythm invites you to "
        "observe, choose and act with intention."
        if language == "en"
        else
        "Ton rythme céleste t'invite à observer, "
        "choisir et agir avec intention."
    )

    return mapping.get(
        normalized_sign,
        fallback,
    )


def build_unlocked_content(
    points,
    sign=None,
    language="fr",
):
    normalized = normalize_points(
        points
    )

    level = calculate_reward_level(
        normalized
    )

    sign_text = _normalize_sign(
        sign,
        language,
    )

    guidance = _base_guidance(
        sign_text,
        language,
    )

    output = []

    if language == "en":
        output.extend(
            [
                "🌟 AstroVibe Level Rewards",
                "",
                (
                    f"🏆 Level {level}: "
                    f"{get_level_name(level, language)}"
                ),
                (
                    f"🔮 Sign: {sign_text}"
                ),
            ]
        )
    else:
        output.extend(
            [
                "🌟 Récompenses de niveau AstroVibe",
                "",
                (
                    f"🏆 Niveau {level} : "
                    f"{get_level_name(level, language)}"
                ),
                (
                    f"🔮 Signe : {sign_text}"
                ),
            ]
        )

    if level == 1:
        output.append("")

        if language == "en":
            output.append(
                "🔒 Your first celestial reward "
                "unlocks at 40 points."
            )
        else:
            output.append(
                "🔒 Ta première récompense "
                "céleste se débloque à 40 points."
            )

        return "\n".join(output)

    output.extend(
        [
            "",
            (
                "🔭 Celestial Insight"
                if language == "en"
                else
                "🔭 Insight céleste"
            ),
            guidance,
        ]
    )

    if level >= 3:
        output.extend(
            [
                "",
                (
                    "⭐ Message from the Stars"
                    if language == "en"
                    else
                    "⭐ Message des astres"
                ),
                (
                    "Turn one recurring thought "
                    "into one useful decision. "
                    "Clarity grows through action."
                    if language == "en"
                    else
                    "Transforme une pensée récurrente "
                    "en une décision utile. La clarté "
                    "grandit dans l'action."
                ),
            ]
        )

    if level >= 4:
        output.extend(
            [
                "",
                (
                    "🔮 Cosmic Focus"
                    if language == "en"
                    else
                    "🔮 Focus cosmique"
                ),
                (
                    "Choose one priority for the "
                    "next seven days. Protect time "
                    "for it and observe the result."
                    if language == "en"
                    else
                    "Choisis une priorité pour les "
                    "sept prochains jours. Protège "
                    "du temps pour elle et observe "
                    "le résultat."
                ),
            ]
        )

    if level >= 5:
        output.extend(
            [
                "",
                (
                    "🌌 Astral Guidance"
                    if language == "en"
                    else
                    "🌌 Guidance astrale"
                ),
                (
                    "Your progress now comes from "
                    "alignment rather than speed. "
                    "Keep what supports your path "
                    "and release one distraction."
                    if language == "en"
                    else
                    "Ta progression vient maintenant "
                    "de l'alignement plutôt que de la "
                    "vitesse. Garde ce qui soutient "
                    "ton chemin et libère-toi d'une "
                    "distraction."
                ),
            ]
        )

    if level >= 6:
        output.extend(
            [
                "",
                (
                    "🏆 Legend Reading"
                    if language == "en"
                    else
                    "🏆 Lecture Légende"
                ),
                (
                    "You have reached AstroVibe's "
                    "highest loyalty level. Your "
                    "consistency, curiosity and "
                    "sharing form your astral legacy."
                    if language == "en"
                    else
                    "Tu as atteint le plus haut "
                    "niveau de fidélité AstroVibe. "
                    "Ta constance, ta curiosité et "
                    "tes partages forment désormais "
                    "ton héritage astral."
                ),
            ]
        )

    output.append("")

    if language == "en":
        output.append(
            "These rewards complement but do not "
            "replace the Personal Profile or Premium."
        )
    else:
        output.append(
            "Ces récompenses complètent, sans les "
            "remplacer, le Profil Personnel et Premium."
        )

    return "\n".join(output)
