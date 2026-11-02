import hashlib
import random
from datetime import datetime, timezone


# ==================================================
# SIGNES
# Les valeurs internes restent en français
# pour rester compatibles avec Neon.
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


ELEMENT_OUTLOOKS = {
    "fr": {
        "fire": [
            "Ton énergie d'initiative est particulièrement forte aujourd'hui. Choisis une direction précise et transforme ton enthousiasme en action concrète.",
            "Une journée dynamique se dessine. Ton courage peut faire avancer une situation, à condition d'éviter la précipitation.",
            "Ton envie d'agir peut devenir un véritable moteur. Utilise cette énergie pour une priorité qui mérite réellement ton attention."
        ],
        "earth": [
            "La journée favorise le concret, la stabilité et les décisions réfléchies. Les petits progrès auront davantage de valeur qu'un changement spectaculaire.",
            "Ton sens pratique est particulièrement utile aujourd'hui. Une approche calme peut résoudre une situation devenue inutilement compliquée.",
            "La constance sera ton meilleur atout. Avance avec méthode et évite de modifier un plan simplement par impatience."
        ],
        "air": [
            "Les idées circulent rapidement aujourd'hui. Une conversation ou une information peut modifier ta manière d'aborder une situation.",
            "Ta curiosité est stimulée. Profite-en pour explorer une nouvelle piste sans disperser ton attention.",
            "La communication joue un rôle central. Les bons mots peuvent ouvrir une porte qui semblait jusque-là fermée."
        ],
        "water": [
            "Ton intuition est particulièrement fine aujourd'hui. Prends en compte ce que tu ressens, tout en vérifiant les faits avant une décision importante.",
            "Une énergie plus intérieure accompagne cette journée. Comprendre tes propres besoins facilitera aussi tes relations avec les autres.",
            "Ta sensibilité peut devenir une force de compréhension. Préserve néanmoins des limites claires pour ne pas absorber les tensions environnantes."
        ]
    },

    "en": {
        "fire": [
            "Your drive is especially strong today. Choose one clear direction and turn enthusiasm into practical action.",
            "A dynamic day is taking shape. Courage can move an important situation forward, provided that you avoid unnecessary haste.",
            "Your desire to act can become a powerful advantage. Direct that energy toward a priority that genuinely deserves your attention."
        ],
        "earth": [
            "The day favors practical decisions, stability and thoughtful progress. Small improvements may matter more than dramatic change.",
            "Your practical judgment is especially useful today. A calm approach may simplify a situation that has become unnecessarily complicated.",
            "Consistency is your greatest advantage today. Move methodically and avoid changing a solid plan simply because of impatience."
        ],
        "air": [
            "Ideas are moving quickly today. A conversation or piece of information may change the way you approach an important situation.",
            "Your curiosity is stimulated. Explore a new possibility without allowing your attention to become scattered.",
            "Communication plays a central role today. The right words may open a door that previously appeared closed."
        ],
        "water": [
            "Your intuition is especially sharp today. Listen to what you feel while checking the facts before making an important decision.",
            "A more reflective energy surrounds the day. Understanding your own needs will also improve your relationships with others.",
            "Sensitivity can become a powerful source of understanding. Maintain clear boundaries so that other people's tensions do not become your own."
        ]
    }
}


TEXTS = {
    "fr": {
        "love": [
            "Une relation peut gagner en profondeur grâce à une conversation plus sincère. Si tu es célibataire, reste attentif aux échanges spontanés.",
            "Les émotions demandent de la clarté plutôt que des suppositions. Une petite attention peut avoir beaucoup plus d'impact qu'une grande déclaration.",
            "Aujourd'hui favorise l'écoute et les gestes authentiques. Une tension peut s'apaiser si chacun exprime ses attentes simplement.",
            "L'amour gagne en qualité lorsque tu ralentis le rythme. Ne cherche pas à définir trop vite une situation encore en évolution."
        ],
        "communication": [
            "Choisis des mots simples et directs. Une conversation importante sera plus productive si tu écoutes autant que tu parles.",
            "Une information pourrait être mal interprétée si elle reste incomplète. Pose les bonnes questions avant de tirer une conclusion.",
            "Ton message passera mieux avec calme et précision. Évite de répondre à chaud à une remarque secondaire.",
            "Une discussion peut débloquer une situation. Cherche d'abord à comprendre le besoin derrière les paroles de l'autre."
        ],
        "work": [
            "Une priorité professionnelle mérite ton énergie. En réduisant les distractions, tu peux avancer beaucoup plus vite que prévu.",
            "Une idée intéressante peut être remarquée si tu la présentes de manière claire et concrète.",
            "La coopération peut accélérer un projet. Accepte une aide ou un point de vue extérieur lorsqu'il apporte une vraie valeur.",
            "Une tâche repoussée mérite enfin d'être traitée. Le plus difficile sera probablement simplement de commencer."
        ],
        "finance": [
            "Évite les décisions financières impulsives. Une vérification supplémentaire pourrait t'éviter une dépense inutile.",
            "Une petite économie ou un ajustement budgétaire peut créer davantage de liberté dans les prochains jours.",
            "Privilégie aujourd'hui la valeur durable plutôt que la satisfaction immédiate.",
            "Une opportunité peut sembler intéressante, mais mérite d'être examinée avant tout engagement."
        ],
        "energy": [
            "Ton énergie est correcte mais demande une bonne gestion. Préserve des moments sans sollicitations.",
            "Ton rythme peut varier au fil de la journée. Utilise les périodes dynamiques sans négliger la récupération.",
            "Ton mental est très actif. Une marche ou quelques minutes de calme peuvent améliorer ta concentration.",
            "Une meilleure répartition de ton énergie sera plus efficace qu'un effort intense et continu."
        ],
        "opportunity": [
            "Une conversation peut ouvrir une piste inattendue.",
            "Une initiative personnelle pourrait être remarquée.",
            "Une information nouvelle peut t'aider à prendre une meilleure décision.",
            "Une occasion de montrer une compétence peut apparaître.",
            "Un projet laissé de côté mérite peut-être une seconde attention."
        ],
        "warning": [
            "Ne prends pas une décision simplement pour aller plus vite.",
            "Évite de confondre intuition et inquiétude.",
            "Protège ton temps face aux demandes inutiles.",
            "Ne promets pas davantage que ce que tu peux réellement offrir.",
            "Vérifie les faits avant de réagir."
        ],
        "action": [
            "Termine une tâche importante avant d'en commencer une nouvelle.",
            "Prends contact avec une personne que tu repousses depuis quelque temps.",
            "Accorde trente minutes à une priorité sans aucune distraction.",
            "Clarifie une décision que tu évites depuis plusieurs jours.",
            "Fais aujourd'hui une petite action qui facilitera ta semaine."
        ],
        "advice": [
            "Choisis la clarté plutôt que la précipitation.",
            "Fais confiance à ton intuition tout en restant attentif aux faits.",
            "Ton énergie mérite d'être investie dans ce qui a réellement de la valeur.",
            "Une petite décision cohérente peut avoir plus d'impact qu'un grand changement.",
            "Ne sous-estime pas le pouvoir d'une conversation honnête."
        ],
        "periods": [
            "07:00 - 09:00",
            "09:00 - 11:00",
            "11:00 - 13:00",
            "14:00 - 16:00",
            "16:00 - 18:00",
            "19:00 - 21:00"
        ]
    },

    "en": {
        "love": [
            "A relationship may gain depth through a more honest conversation. If you are single, pay attention to spontaneous interactions.",
            "Emotions require clarity rather than assumptions. A small thoughtful gesture may have more impact than a dramatic declaration.",
            "Today favors listening and authentic gestures. A tension may ease when expectations are expressed simply.",
            "Love benefits from a slower pace today. Avoid defining too quickly a situation that is still evolving."
        ],
        "communication": [
            "Choose simple and direct words. An important conversation will be more productive when you listen as much as you speak.",
            "Information may be misunderstood if it remains incomplete. Ask the right questions before reaching a conclusion.",
            "Your message will be stronger when delivered calmly and precisely. Avoid reacting immediately to a secondary remark.",
            "A discussion may unlock a situation. First try to understand the need behind the other person's words."
        ],
        "work": [
            "One professional priority deserves your energy. Reducing distractions may help you progress much faster than expected.",
            "An interesting idea may attract attention when presented clearly and practically.",
            "Cooperation can accelerate a project. Accept help or an outside perspective when it brings genuine value.",
            "A postponed task deserves attention today. The hardest part may simply be getting started."
        ],
        "finance": [
            "Avoid impulsive financial decisions. One additional check could prevent an unnecessary expense.",
            "A small saving or budget adjustment may create greater freedom over the coming days.",
            "Prioritize lasting value rather than immediate satisfaction today.",
            "An opportunity may appear attractive but deserves careful consideration before any commitment."
        ],
        "energy": [
            "Your energy is steady but requires good management. Protect a few moments without constant demands.",
            "Your rhythm may change throughout the day. Use your dynamic periods while allowing enough recovery.",
            "Your mind is highly active. A walk or a few quiet minutes may improve concentration.",
            "Distributing your energy wisely will be more effective than maintaining constant intensity."
        ],
        "opportunity": [
            "A conversation may open an unexpected path.",
            "A personal initiative could attract positive attention.",
            "New information may help you make a better decision.",
            "An opportunity to demonstrate a skill may arise.",
            "A project left aside may deserve another look."
        ],
        "warning": [
            "Do not make a decision simply to move faster.",
            "Avoid confusing intuition with anxiety.",
            "Protect your time from unnecessary demands.",
            "Do not promise more than you can realistically deliver.",
            "Check the facts before reacting."
        ],
        "action": [
            "Finish one important task before starting another.",
            "Contact someone you have been meaning to reach.",
            "Give one priority thirty minutes of completely focused attention.",
            "Clarify a decision you have been avoiding.",
            "Take one small action today that will make the rest of your week easier."
        ],
        "advice": [
            "Choose clarity over haste.",
            "Trust your intuition while staying attentive to the facts.",
            "Invest your energy in what genuinely offers value.",
            "One small consistent decision may matter more than a dramatic change.",
            "Do not underestimate the power of an honest conversation."
        ],
        "periods": [
            "7:00 AM - 9:00 AM",
            "9:00 AM - 11:00 AM",
            "11:00 AM - 1:00 PM",
            "2:00 PM - 4:00 PM",
            "4:00 PM - 6:00 PM",
            "7:00 PM - 9:00 PM"
        ]
    }
}


def build_seed(sign, date_string):
    value = f"astrovibe-premium-daily|{sign}|{date_string}"

    digest = hashlib.sha256(
        value.encode("utf-8")
    ).hexdigest()

    return int(
        digest[:16],
        16
    )


def generate_premium_daily(sign, language="fr"):
    if language not in ("fr", "en"):
        language = "fr"

    sign_data = SIGN_DATA.get(sign)

    if not sign_data:
        return None

    today = datetime.now(
        timezone.utc
    ).date()

    date_string = today.isoformat()

    randomizer = random.Random(
        build_seed(
            sign,
            date_string
        )
    )

    texts = TEXTS[language]

    outlook = randomizer.choice(
        ELEMENT_OUTLOOKS[
            language
        ][
            sign_data["element"]
        ]
    )

    love = randomizer.choice(
        texts["love"]
    )
    communication = randomizer.choice(
        texts["communication"]
    )
    work = randomizer.choice(
        texts["work"]
    )
    finance = randomizer.choice(
        texts["finance"]
    )
    energy = randomizer.choice(
        texts["energy"]
    )
    opportunity = randomizer.choice(
        texts["opportunity"]
    )
    warning = randomizer.choice(
        texts["warning"]
    )
    action = randomizer.choice(
        texts["action"]
    )
    advice = randomizer.choice(
        texts["advice"]
    )
    favorable_period = randomizer.choice(
        texts["periods"]
    )

    love_score = randomizer.randint(6, 9)
    communication_score = randomizer.randint(5, 9)
    work_score = randomizer.randint(6, 9)
    finance_score = randomizer.randint(5, 9)
    energy_score = randomizer.randint(5, 9)

    sign_name = sign_data[
        language
    ].upper()

    emoji = sign_data["emoji"]

    date_display = today.strftime(
        "%d/%m/%Y"
    )

    if language == "en":
        result = (
            f"💎 ASTROVIBE PREMIUM\n"
            f"☀️ DAILY ASTRO+\n\n"

            f"{emoji} {sign_name}\n"
            f"{date_display}\n\n"

            f"✨ DOMINANT ENERGY\n"
            f"{outlook}\n\n"

            f"❤️ LOVE • {love_score}/10\n"
            f"{love}\n\n"

            f"💬 RELATIONSHIPS & COMMUNICATION • "
            f"{communication_score}/10\n"
            f"{communication}\n\n"

            f"💼 WORK & AMBITIONS • "
            f"{work_score}/10\n"
            f"{work}\n\n"

            f"💰 FINANCES • "
            f"{finance_score}/10\n"
            f"{finance}\n\n"

            f"🌿 ENERGY & WELL-BEING • "
            f"{energy_score}/10\n"
            f"{energy}\n\n"

            f"🍀 OPPORTUNITY OF THE DAY\n"
            f"{opportunity}\n\n"

            f"⚠️ POINT OF ATTENTION\n"
            f"{warning}\n\n"

            f"🕐 FAVORABLE PERIOD\n"
            f"{favorable_period}\n\n"

            f"🎯 RECOMMENDED ACTION\n"
            f"{action}\n\n"

            f"🌙 ASTROVIBE MESSAGE\n"
            f"{advice}\n\n"

            f"──────────────\n"
            f"Premium content intended for "
            f"entertainment and personal reflection."
        )

    else:
        result = (
            f"💎 ASTROVIBE PREMIUM\n"
            f"☀️ MON ASTRO DU JOUR +\n\n"

            f"{emoji} {sign_name}\n"
            f"{date_display}\n\n"

            f"✨ ÉNERGIE DOMINANTE\n"
            f"{outlook}\n\n"

            f"❤️ AMOUR • {love_score}/10\n"
            f"{love}\n\n"

            f"💬 RELATIONS & COMMUNICATION • "
            f"{communication_score}/10\n"
            f"{communication}\n\n"

            f"💼 TRAVAIL & AMBITIONS • "
            f"{work_score}/10\n"
            f"{work}\n\n"

            f"💰 FINANCES • "
            f"{finance_score}/10\n"
            f"{finance}\n\n"

            f"🌿 ÉNERGIE & BIEN-ÊTRE • "
            f"{energy_score}/10\n"
            f"{energy}\n\n"

            f"🍀 OPPORTUNITÉ DU JOUR\n"
            f"{opportunity}\n\n"

            f"⚠️ POINT DE VIGILANCE\n"
            f"{warning}\n\n"

            f"🕐 MOMENT FAVORABLE\n"
            f"{favorable_period}\n\n"

            f"🎯 ACTION CONSEILLÉE\n"
            f"{action}\n\n"

            f"🌙 MESSAGE ASTROVIBE\n"
            f"{advice}\n\n"

            f"──────────────\n"
            f"Contenu Premium destiné au "
            f"divertissement et à la réflexion personnelle."
        )

    return result
