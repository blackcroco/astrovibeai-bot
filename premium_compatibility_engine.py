import hashlib
import random


# ==================================================
# SIGNES
# Les clés restent en français pour rester
# compatibles avec les valeurs enregistrées dans Neon.
# ==================================================

SIGN_DATA = {
    "♈ Bélier": {
        "emoji": "♈",
        "fr": "Bélier",
        "en": "Aries",
        "element": "fire"
    },
    "♉ Taureau": {
        "emoji": "♉",
        "fr": "Taureau",
        "en": "Taurus",
        "element": "earth"
    },
    "♊ Gémeaux": {
        "emoji": "♊",
        "fr": "Gémeaux",
        "en": "Gemini",
        "element": "air"
    },
    "♋ Cancer": {
        "emoji": "♋",
        "fr": "Cancer",
        "en": "Cancer",
        "element": "water"
    },
    "♌ Lion": {
        "emoji": "♌",
        "fr": "Lion",
        "en": "Leo",
        "element": "fire"
    },
    "♍ Vierge": {
        "emoji": "♍",
        "fr": "Vierge",
        "en": "Virgo",
        "element": "earth"
    },
    "♎ Balance": {
        "emoji": "♎",
        "fr": "Balance",
        "en": "Libra",
        "element": "air"
    },
    "♏ Scorpion": {
        "emoji": "♏",
        "fr": "Scorpion",
        "en": "Scorpio",
        "element": "water"
    },
    "♐ Sagittaire": {
        "emoji": "♐",
        "fr": "Sagittaire",
        "en": "Sagittarius",
        "element": "fire"
    },
    "♑ Capricorne": {
        "emoji": "♑",
        "fr": "Capricorne",
        "en": "Capricorn",
        "element": "earth"
    },
    "♒ Verseau": {
        "emoji": "♒",
        "fr": "Verseau",
        "en": "Aquarius",
        "element": "air"
    },
    "♓ Poissons": {
        "emoji": "♓",
        "fr": "Poissons",
        "en": "Pisces",
        "element": "water"
    }
}


# ==================================================
# DYNAMIQUE DES ELEMENTS
# ==================================================

ELEMENT_BASE = {
    frozenset(["fire"]): 82,
    frozenset(["earth"]): 84,
    frozenset(["air"]): 81,
    frozenset(["water"]): 85,

    frozenset(["fire", "air"]): 84,
    frozenset(["earth", "water"]): 86,
    frozenset(["fire", "earth"]): 72,
    frozenset(["fire", "water"]): 66,
    frozenset(["earth", "air"]): 68,
    frozenset(["air", "water"]): 70
}


TEXTS = {
    "fr": {
        "dynamic": [
            (
                "Votre relation possède une énergie capable de créer "
                "une vraie complémentarité. Les différences peuvent "
                "devenir une force lorsque chacun respecte le rythme "
                "et la sensibilité de l'autre."
            ),
            (
                "Cette combinaison crée une dynamique riche, parfois "
                "intense. Votre connexion devient plus solide lorsque "
                "les attentes sont exprimées clairement."
            ),
            (
                "Votre duo peut évoluer de manière très constructive. "
                "La clé consiste à préserver vos individualités tout "
                "en développant des objectifs communs."
            )
        ],

        "trust": [
            (
                "La confiance se construit surtout par la cohérence "
                "entre les paroles et les actes. Les petites preuves "
                "régulières auront plus de poids que les grandes promesses."
            ),
            (
                "Votre confiance mutuelle peut devenir solide lorsqu'aucun "
                "des deux ne transforme les inquiétudes en suppositions."
            ),
            (
                "La transparence renforcera fortement cette connexion. "
                "Dire les choses tôt évitera que de petites incertitudes "
                "deviennent des tensions."
            )
        ],

        "emotional": [
            (
                "L'intimité émotionnelle gagne en profondeur lorsque "
                "chacun peut exprimer ses fragilités sans se sentir jugé."
            ),
            (
                "Vos émotions ne suivent pas toujours le même rythme. "
                "Créer un espace calme pour parler renforcera le sentiment "
                "de sécurité dans la relation."
            ),
            (
                "Une vraie proximité est possible si chacun apprend à "
                "reconnaître la manière dont l'autre manifeste son affection."
            )
        ],

        "needs": [
            (
                "L'un peut rechercher davantage d'intensité tandis que "
                "l'autre a besoin de stabilité ou d'espace. Trouver un "
                "équilibre entre proximité et autonomie sera essentiel."
            ),
            (
                "Vos besoins affectifs peuvent être différents sans être "
                "incompatibles. Les comprendre explicitement évitera de "
                "nombreuses frustrations."
            ),
            (
                "La relation s'épanouit lorsque chacun se sent à la fois "
                "considéré, respecté et libre d'exprimer ses attentes."
            )
        ],

        "conflict": [
            (
                "Pendant un désaccord, évitez de chercher immédiatement "
                "qui a raison. Identifier le besoin derrière la réaction "
                "de chacun sera beaucoup plus utile."
            ),
            (
                "Les tensions risquent surtout de s'amplifier lorsque les "
                "non-dits s'accumulent. Une discussion précoce et calme "
                "évite souvent les conflits plus importants."
            ),
            (
                "Votre principal défi consiste à ne pas transformer une "
                "différence de fonctionnement en jugement sur l'autre."
            )
        ],

        "strength": [
            (
                "Votre force réside dans votre capacité à vous apporter "
                "des perspectives différentes tout en poursuivant un "
                "objectif commun."
            ),
            (
                "La complicité peut devenir particulièrement forte lorsque "
                "vous encouragez les ambitions et les projets de l'autre."
            ),
            (
                "Vous pouvez créer une relation stimulante lorsque chacun "
                "utilise ses qualités pour compléter celles de l'autre."
            )
        ],

        "risk": [
            (
                "Le principal risque serait de supposer que l'autre doit "
                "comprendre vos besoins sans qu'ils soient exprimés."
            ),
            (
                "La routine ou les attentes implicites peuvent progressivement "
                "réduire la qualité des échanges."
            ),
            (
                "Une compétition silencieuse ou un besoin excessif de contrôle "
                "pourrait déséquilibrer la relation."
            )
        ],

        "action": [
            (
                "Planifiez régulièrement un moment où chacun peut parler "
                "librement de ses attentes sans chercher immédiatement "
                "une solution."
            ),
            (
                "Créez un projet commun qui vous permette d'avancer ensemble "
                "tout en conservant vos espaces personnels."
            ),
            (
                "Valorisez davantage les efforts quotidiens de l'autre. "
                "La reconnaissance renforce naturellement la confiance."
            ),
            (
                "Apprenez à poser une question avant d'interpréter un silence "
                "ou une réaction."
            )
        ],

        "summary": [
            (
                "Cette relation possède un potentiel réel lorsqu'elle "
                "associe sincérité, respect et capacité d'adaptation. "
                "Les différences ne sont pas nécessairement des obstacles : "
                "elles peuvent devenir le moteur de votre évolution commune."
            ),
            (
                "Votre compatibilité peut évoluer favorablement si la "
                "communication reste ouverte et si chacun conserve une "
                "place pour les besoins de l'autre."
            ),
            (
                "Ce duo fonctionne particulièrement bien lorsque la relation "
                "reste vivante, honnête et construite sur des actions "
                "concrètes plutôt que sur des suppositions."
            )
        ]
    },

    "en": {
        "dynamic": [
            (
                "This relationship carries an energy capable of creating "
                "genuine complementarity. Differences can become a strength "
                "when both partners respect each other's rhythm and sensitivity."
            ),
            (
                "This combination creates a rich and sometimes intense "
                "dynamic. The connection becomes stronger when expectations "
                "are expressed clearly."
            ),
            (
                "This partnership can develop in a highly constructive way. "
                "The key is to preserve individuality while building shared goals."
            )
        ],

        "trust": [
            (
                "Trust grows mainly through consistency between words and "
                "actions. Small and regular signs of reliability will matter "
                "more than dramatic promises."
            ),
            (
                "Mutual trust can become strong when neither partner turns "
                "concerns into assumptions."
            ),
            (
                "Transparency will strengthen this connection considerably. "
                "Speaking early prevents small uncertainties from becoming tensions."
            )
        ],

        "emotional": [
            (
                "Emotional intimacy deepens when both partners can express "
                "vulnerability without feeling judged."
            ),
            (
                "Emotions may not always move at the same pace. Creating a "
                "calm space for conversation will strengthen emotional security."
            ),
            (
                "Genuine closeness is possible when both partners recognize "
                "the different ways affection can be expressed."
            )
        ],

        "needs": [
            (
                "One partner may seek greater intensity while the other needs "
                "stability or personal space. Balancing closeness and independence "
                "will be essential."
            ),
            (
                "Emotional needs may be different without being incompatible. "
                "Understanding them explicitly will prevent many frustrations."
            ),
            (
                "The relationship thrives when both partners feel respected, "
                "valued and free to express their expectations."
            )
        ],

        "conflict": [
            (
                "During disagreements, avoid focusing immediately on who is "
                "right. Understanding the need behind each reaction will be "
                "far more useful."
            ),
            (
                "Tension is most likely to grow when unspoken concerns accumulate. "
                "An early and calm conversation can prevent larger conflicts."
            ),
            (
                "The main challenge is to avoid turning different ways of "
                "functioning into judgments about each other."
            )
        ],

        "strength": [
            (
                "A major strength lies in your ability to bring different "
                "perspectives while still pursuing shared goals."
            ),
            (
                "Companionship can become especially strong when both partners "
                "support each other's ambitions and projects."
            ),
            (
                "You can create a stimulating relationship when each person's "
                "qualities complement the strengths of the other."
            )
        ],

        "risk": [
            (
                "The main risk would be assuming that the other person should "
                "understand your needs without them being expressed."
            ),
            (
                "Routine or unspoken expectations may gradually reduce the "
                "quality of communication."
            ),
            (
                "Silent competition or an excessive need for control could "
                "create imbalance in the relationship."
            )
        ],

        "action": [
            (
                "Regularly create a moment where both partners can speak freely "
                "about expectations without immediately trying to solve everything."
            ),
            (
                "Create a shared project that allows you to move forward together "
                "while preserving personal space."
            ),
            (
                "Acknowledge each other's everyday efforts more often. "
                "Recognition naturally strengthens trust."
            ),
            (
                "Learn to ask a question before interpreting silence or a reaction."
            )
        ],

        "summary": [
            (
                "This relationship has genuine potential when sincerity, respect "
                "and adaptability work together. Differences do not have to be "
                "obstacles; they can become part of your shared growth."
            ),
            (
                "Your compatibility can develop positively when communication "
                "remains open and both partners make room for each other's needs."
            ),
            (
                "This partnership works especially well when the relationship "
                "remains alive, honest and built on consistent actions rather "
                "than assumptions."
            )
        ]
    }
}


def build_seed(first_sign, second_sign):
    pair = sorted([
        first_sign,
        second_sign
    ])

    raw_value = (
        "astrovibe-premium-compatibility|"
        + "|".join(pair)
    )

    digest = hashlib.sha256(
        raw_value.encode("utf-8")
    ).hexdigest()

    return int(
        digest[:16],
        16
    )


def clamp(value):
    return max(
        4,
        min(10, value)
    )


def get_base_score(first, second):
    first_element = first["element"]
    second_element = second["element"]

    elements = frozenset([
        first_element,
        second_element
    ])

    return ELEMENT_BASE.get(
        elements,
        72
    )


def generate_premium_compatibility(
    first_sign,
    second_sign,
    language="fr"
):
    if language not in (
        "fr",
        "en"
    ):
        language = "fr"

    first = SIGN_DATA.get(
        first_sign
    )

    second = SIGN_DATA.get(
        second_sign
    )

    if not first or not second:
        return None

    randomizer = random.Random(
        build_seed(
            first_sign,
            second_sign
        )
    )

    base = get_base_score(
        first,
        second
    )

    if first_sign == second_sign:
        base += 3

    overall = max(
        52,
        min(
            95,
            base + randomizer.randint(-4, 4)
        )
    )

    score_base = round(
        overall / 10
    )

    scores = {
        "attraction": clamp(
            score_base
            + randomizer.randint(-1, 1)
        ),
        "communication": clamp(
            score_base
            + randomizer.randint(-2, 1)
        ),
        "trust": clamp(
            score_base
            + randomizer.randint(-1, 1)
        ),
        "emotional": clamp(
            score_base
            + randomizer.randint(-1, 1)
        ),
        "passion": clamp(
            score_base
            + randomizer.randint(-1, 2)
        ),
        "stability": clamp(
            score_base
            + randomizer.randint(-2, 1)
        ),
        "conflict": clamp(
            score_base
            + randomizer.randint(-2, 1)
        ),
        "long_term": clamp(
            score_base
            + randomizer.randint(-1, 1)
        )
    }

    texts = TEXTS[
        language
    ]

    dynamic = randomizer.choice(
        texts["dynamic"]
    )

    trust_text = randomizer.choice(
        texts["trust"]
    )

    emotional_text = randomizer.choice(
        texts["emotional"]
    )

    needs_text = randomizer.choice(
        texts["needs"]
    )

    conflict_text = randomizer.choice(
        texts["conflict"]
    )

    strength_text = randomizer.choice(
        texts["strength"]
    )

    risk_text = randomizer.choice(
        texts["risk"]
    )

    action_text = randomizer.choice(
        texts["action"]
    )

    summary_text = randomizer.choice(
        texts["summary"]
    )

    first_name = first[
        language
    ].upper()

    second_name = second[
        language
    ].upper()

    if language == "en":
        return (
            f"💎 ASTROVIBE PREMIUM\n"
            f"❤️ DEEP COMPATIBILITY\n\n"

            f"{first['emoji']} {first_name}\n"
            f"×\n"
            f"{second['emoji']} {second_name}\n\n"

            f"💞 OVERALL COMPATIBILITY: "
            f"{overall}%\n\n"

            f"❤️ Attraction: "
            f"{scores['attraction']}/10\n"

            f"💬 Communication: "
            f"{scores['communication']}/10\n"

            f"🔐 Trust: "
            f"{scores['trust']}/10\n"

            f"🌙 Emotional intimacy: "
            f"{scores['emotional']}/10\n"

            f"🔥 Passion: "
            f"{scores['passion']}/10\n"

            f"🤝 Stability: "
            f"{scores['stability']}/10\n"

            f"⚡ Conflict management: "
            f"{scores['conflict']}/10\n"

            f"🔭 Long-term potential: "
            f"{scores['long_term']}/10\n\n"

            f"✨ YOUR DEEP DYNAMIC\n"
            f"{dynamic}\n\n"

            f"🔐 TRUST\n"
            f"{trust_text}\n\n"

            f"🌙 EMOTIONAL INTIMACY\n"
            f"{emotional_text}\n\n"

            f"💖 EMOTIONAL NEEDS\n"
            f"{needs_text}\n\n"

            f"⚡ CONFLICT MANAGEMENT\n"
            f"{conflict_text}\n\n"

            f"✨ WHAT BRINGS YOU TOGETHER\n"
            f"{strength_text}\n\n"

            f"⚠️ WHAT MAY PULL YOU APART\n"
            f"{risk_text}\n\n"

            f"🎯 HOW TO STRENGTHEN THE RELATIONSHIP\n"
            f"{action_text}\n\n"

            f"🌙 ASTROVIBE PREMIUM SUMMARY\n"
            f"{summary_text}\n\n"

            f"──────────────\n"
            f"Premium content intended for "
            f"entertainment and personal reflection."
        )

    return (
        f"💎 ASTROVIBE PREMIUM\n"
        f"❤️ COMPATIBILITÉ APPROFONDIE\n\n"

        f"{first['emoji']} {first_name}\n"
        f"×\n"
        f"{second['emoji']} {second_name}\n\n"

        f"💞 COMPATIBILITÉ GLOBALE : "
        f"{overall}%\n\n"

        f"❤️ Attraction : "
        f"{scores['attraction']}/10\n"

        f"💬 Communication : "
        f"{scores['communication']}/10\n"

        f"🔐 Confiance : "
        f"{scores['trust']}/10\n"

        f"🌙 Intimité émotionnelle : "
        f"{scores['emotional']}/10\n"

        f"🔥 Passion : "
        f"{scores['passion']}/10\n"

        f"🤝 Stabilité : "
        f"{scores['stability']}/10\n"

        f"⚡ Gestion des conflits : "
        f"{scores['conflict']}/10\n"

        f"🔭 Potentiel à long terme : "
        f"{scores['long_term']}/10\n\n"

        f"✨ VOTRE DYNAMIQUE PROFONDE\n"
        f"{dynamic}\n\n"

        f"🔐 CONFIANCE\n"
        f"{trust_text}\n\n"

        f"🌙 INTIMITÉ ÉMOTIONNELLE\n"
        f"{emotional_text}\n\n"

        f"💖 BESOINS AFFECTIFS\n"
        f"{needs_text}\n\n"

        f"⚡ GESTION DES CONFLITS\n"
        f"{conflict_text}\n\n"

        f"✨ CE QUI VOUS RAPPROCHE\n"
        f"{strength_text}\n\n"

        f"⚠️ CE QUI PEUT VOUS ÉLOIGNER\n"
        f"{risk_text}\n\n"

        f"🎯 COMMENT RENFORCER LA RELATION\n"
        f"{action_text}\n\n"

        f"🌙 SYNTHÈSE ASTROVIBE PREMIUM\n"
        f"{summary_text}\n\n"

        f"──────────────\n"
        f"Contenu Premium destiné au divertissement "
        f"et à la réflexion personnelle."
    )
