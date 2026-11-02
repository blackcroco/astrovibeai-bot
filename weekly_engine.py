import hashlib
import random
from datetime import datetime, timedelta, timezone


# ==================================================
# SIGNES
# Les clés restent en français pour correspondre
# aux valeurs déjà enregistrées dans Neon.
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
# TENDANCES PAR ÉLÉMENT
# ==================================================

ELEMENT_OUTLOOKS = {
    "fr": {
        "fire": [
            (
                "Cette semaine t'invite à transformer ton enthousiasme "
                "en actions concrètes. Ton élan peut ouvrir une porte, "
                "à condition de choisir une direction claire."
            ),
            (
                "Une énergie volontaire t'accompagne. Tu peux accélérer "
                "un projet important, mais les meilleurs résultats "
                "viendront d'une initiative réfléchie."
            ),
            (
                "Ton courage sera l'un de tes meilleurs atouts. Une "
                "décision assumée pourrait faire évoluer une situation "
                "restée trop longtemps immobile."
            )
        ],
        "earth": [
            (
                "La semaine favorise la stabilité et la construction. "
                "En avançant avec méthode, tu peux consolider quelque "
                "chose qui compte réellement pour toi."
            ),
            (
                "Tes efforts réguliers commencent à produire des effets "
                "plus visibles. Ne sous-estime pas la valeur d'un progrès "
                "lent mais durable."
            ),
            (
                "Une approche pragmatique t'aidera à faire la différence "
                "entre une priorité réelle et une distraction passagère."
            )
        ],
        "air": [
            (
                "Les échanges et les idées occupent une place importante "
                "cette semaine. Une conversation pourrait modifier ta "
                "manière de voir une situation."
            ),
            (
                "Ta curiosité t'ouvre de nouvelles perspectives. Garde "
                "cependant un fil conducteur afin de ne pas disperser "
                "ton énergie."
            ),
            (
                "Une information, une rencontre ou une intuition rapide "
                "peut déclencher une réflexion utile. Prends le temps "
                "d'approfondir avant de décider."
            )
        ],
        "water": [
            (
                "Ton intuition sera particulièrement présente cette "
                "semaine. Elle peut t'aider à percevoir ce qui ne se dit "
                "pas encore clairement."
            ),
            (
                "La semaine encourage un recentrage émotionnel. Écouter "
                "tes besoins te permettra d'aborder les autres avec "
                "davantage de sérénité."
            ),
            (
                "Une évolution intérieure discrète peut modifier ta façon "
                "de réagir à une situation ancienne. Fais confiance à "
                "ce processus."
            )
        ]
    },
    "en": {
        "fire": [
            (
                "This week invites you to turn enthusiasm into practical "
                "action. Your momentum can open a door, provided that "
                "you choose a clear direction."
            ),
            (
                "A determined energy supports you. An important project "
                "can move forward when initiative is combined with good "
                "judgment."
            ),
            (
                "Courage is one of your greatest assets this week. "
                "A confident decision may revive a situation that has "
                "remained still for too long."
            )
        ],
        "earth": [
            (
                "The week favors stability and careful construction. "
                "A methodical approach can strengthen something that "
                "genuinely matters to you."
            ),
            (
                "Your consistent efforts are beginning to show more "
                "visible results. Do not underestimate slow but lasting "
                "progress."
            ),
            (
                "A practical perspective will help you separate a real "
                "priority from a temporary distraction."
            )
        ],
        "air": [
            (
                "Ideas and conversations play an important role this "
                "week. One exchange may change the way you understand "
                "a situation."
            ),
            (
                "Curiosity opens new perspectives. Keep a clear thread "
                "running through your plans so that your energy does not "
                "become scattered."
            ),
            (
                "Information, an encounter or a quick insight may inspire "
                "a useful reflection. Explore it fully before deciding."
            )
        ],
        "water": [
            (
                "Your intuition is especially present this week. It may "
                "help you notice what has not yet been expressed clearly."
            ),
            (
                "The week encourages emotional balance. Listening to your "
                "needs will help you approach others with greater calm."
            ),
            (
                "A quiet inner change may transform the way you respond "
                "to an old situation. Trust the process."
            )
        ]
    }
}


# ==================================================
# TEXTES HEBDOMADAIRES
# ==================================================

WEEKLY_TEXTS = {
    "fr": {
        "love": [
            (
                "Une conversation sincère peut renforcer une relation. "
                "Exprime ce que tu ressens sans attendre que l'autre "
                "personne devine tes besoins."
            ),
            (
                "Les liens affectifs gagnent en profondeur lorsque tu "
                "acceptes de ralentir et d'écouter réellement. Si tu es "
                "célibataire, une rencontre peut commencer simplement."
            ),
            (
                "Un ancien malentendu peut perdre de son importance. "
                "La tendresse et la clarté permettront de rétablir un "
                "équilibre plus naturel."
            ),
            (
                "Cette semaine favorise les gestes authentiques. Une "
                "attention discrète peut avoir davantage d'effet qu'une "
                "grande déclaration."
            ),
            (
                "Tes émotions méritent d'être reconnues sans être "
                "transformées immédiatement en décision. Laisse la "
                "relation évoluer à un rythme naturel."
            )
        ],
        "work": [
            (
                "Une priorité professionnelle mérite toute ton attention. "
                "En évitant la dispersion, tu peux obtenir un résultat "
                "plus important que prévu."
            ),
            (
                "Une idée peut être bien accueillie si elle est présentée "
                "avec précision. Mets en avant les bénéfices concrets "
                "plutôt que de vouloir tout expliquer."
            ),
            (
                "La coopération sera particulièrement utile. Une autre "
                "personne peut apporter la perspective qui manquait à ton "
                "projet."
            ),
            (
                "Une tâche repoussée réclame désormais une décision. "
                "Une fois le premier pas accompli, la suite semblera "
                "beaucoup moins compliquée."
            ),
            (
                "Ton sérieux peut être remarqué, même si la reconnaissance "
                "n'est pas immédiate. Continue avec régularité."
            )
        ],
        "finance": [
            (
                "La prudence reste ta meilleure alliée. Vérifie les détails "
                "avant un achat ou un engagement financier important."
            ),
            (
                "Une petite correction dans tes dépenses peut apporter "
                "davantage de liberté dans les semaines à venir."
            ),
            (
                "La semaine favorise la planification plutôt que les "
                "décisions impulsives. Privilégie ce qui possède une "
                "valeur durable."
            ),
            (
                "Une opportunité mérite d'être étudiée, mais pas acceptée "
                "dans l'urgence. Demande les informations qui te manquent."
            ),
            (
                "Tes finances gagnent à être observées avec simplicité. "
                "Un objectif clair sera plus efficace qu'une multitude "
                "de restrictions."
            )
        ],
        "energy": [
            (
                "Ton énergie sera plus stable si tu respectes de vraies "
                "pauses. Évite d'enchaîner les obligations sans transition."
            ),
            (
                "Ta vitalité peut évoluer par vagues. Profite des périodes "
                "dynamiques pour avancer, puis autorise-toi à récupérer."
            ),
            (
                "Ton esprit risque d'être plus actif que ton corps. Une "
                "marche ou quelques minutes au calme peuvent rétablir "
                "ton équilibre."
            ),
            (
                "Écoute les premiers signes de fatigue. Répartir ton énergie "
                "sera plus utile que vouloir tout terminer immédiatement."
            ),
            (
                "Un rythme plus régulier améliorera ta concentration. "
                "Protège aussi ton sommeil et tes moments de déconnexion."
            )
        ],
        "opportunity": [
            "Une conversation apparemment ordinaire peut ouvrir une nouvelle piste.",
            "Une initiative personnelle peut recevoir un soutien inattendu.",
            "Une occasion de montrer tes compétences pourrait se présenter.",
            "Un changement de méthode peut produire un résultat rapide.",
            "Une rencontre peut apporter une information précieuse.",
            "Un projet laissé de côté mérite peut-être une seconde chance."
        ],
        "warning": [
            "Ne confonds pas vitesse et précipitation.",
            "Évite de promettre davantage que ce que tu peux réellement offrir.",
            "Ne laisse pas une inquiétude passagère diriger toute ta semaine.",
            "Protège ton temps face aux demandes qui ne sont pas prioritaires.",
            "Vérifie les faits avant de tirer une conclusion.",
            "Ne cherche pas à contrôler ce qui demande simplement de la patience."
        ],
        "advice": [
            "Choisis une priorité forte et avance avec constance.",
            "Fais confiance à ton intuition, puis vérifie-la avec des faits.",
            "Dis clairement ce dont tu as besoin.",
            "Préserve ton énergie pour ce qui possède une vraie valeur.",
            "Accepte d'ajuster ton plan sans abandonner ton objectif.",
            "Reconnais le chemin déjà parcouru avant d'exiger davantage de toi."
        ],
        "days": [
            "Lundi",
            "Mardi",
            "Mercredi",
            "Jeudi",
            "Vendredi",
            "Samedi",
            "Dimanche"
        ]
    },

    "en": {
        "love": [
            (
                "An honest conversation can strengthen an important bond. "
                "Express your feelings instead of expecting the other "
                "person to guess your needs."
            ),
            (
                "Relationships gain depth when you slow down and genuinely "
                "listen. If you are single, a meaningful connection may "
                "begin in a simple way."
            ),
            (
                "An old misunderstanding may lose its importance. "
                "Tenderness and clarity can restore a more natural balance."
            ),
            (
                "The week favors authentic gestures. A thoughtful detail "
                "may have more impact than a dramatic declaration."
            ),
            (
                "Your emotions deserve recognition without immediately "
                "becoming decisions. Allow the relationship to develop "
                "at a natural pace."
            )
        ],
        "work": [
            (
                "One professional priority deserves your full attention. "
                "By avoiding distractions, you may achieve more than "
                "originally expected."
            ),
            (
                "An idea may be well received when presented clearly. "
                "Focus on practical benefits instead of explaining every "
                "single detail."
            ),
            (
                "Cooperation will be especially valuable. Another person "
                "may provide the perspective your project was missing."
            ),
            (
                "A postponed task now requires a decision. Once the first "
                "step is taken, the rest may feel much easier."
            ),
            (
                "Your reliability may be noticed even if recognition is "
                "not immediate. Continue with consistency."
            )
        ],
        "finance": [
            (
                "Caution remains your best ally. Check the details before "
                "making an important purchase or financial commitment."
            ),
            (
                "A small adjustment to your spending may create more "
                "freedom in the weeks ahead."
            ),
            (
                "The week favors planning rather than impulsive decisions. "
                "Prioritize what offers lasting value."
            ),
            (
                "An opportunity deserves consideration, but not an urgent "
                "answer. Ask for any information that is still missing."
            ),
            (
                "Your finances benefit from simplicity. One clear goal "
                "will be more effective than many restrictions."
            )
        ],
        "energy": [
            (
                "Your energy will remain steadier if you take genuine "
                "breaks. Avoid moving from one obligation directly into "
                "the next."
            ),
            (
                "Your vitality may arrive in waves. Use dynamic periods "
                "to make progress, then give yourself time to recover."
            ),
            (
                "Your mind may be more active than your body. A walk or "
                "a few quiet minutes can restore balance."
            ),
            (
                "Notice the first signs of fatigue. Distributing your "
                "energy wisely will be more helpful than rushing."
            ),
            (
                "A more regular rhythm will improve concentration. Protect "
                "your sleep and your moments away from distractions."
            )
        ],
        "opportunity": [
            "An ordinary conversation may open an unexpected path.",
            "A personal initiative could receive surprising support.",
            "An opportunity to demonstrate your abilities may arise.",
            "A change of method could produce a quick improvement.",
            "An encounter may bring valuable information.",
            "A forgotten project may deserve a second chance."
        ],
        "warning": [
            "Do not confuse speed with haste.",
            "Avoid promising more than you can realistically deliver.",
            "Do not let a temporary worry control the entire week.",
            "Protect your time from requests that are not priorities.",
            "Check the facts before reaching a conclusion.",
            "Do not try to control what simply requires patience."
        ],
        "advice": [
            "Choose one strong priority and move forward consistently.",
            "Trust your intuition, then support it with facts.",
            "State clearly what you need.",
            "Protect your energy for what offers genuine value.",
            "Adjust your plan without abandoning your objective.",
            "Recognize the progress already made before demanding more of yourself."
        ],
        "days": [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
        ]
    }
}


# ==================================================
# OUTILS DE GÉNÉRATION
# ==================================================

def get_week_dates():
    today = datetime.now(timezone.utc).date()

    start_date = today - timedelta(
        days=today.weekday()
    )

    end_date = start_date + timedelta(
        days=6
    )

    return start_date, end_date


def build_week_seed(sign, year, week_number):
    raw_value = (
        f"astrovibe-weekly|{sign}|"
        f"{year}|{week_number}"
    )

    digest = hashlib.sha256(
        raw_value.encode("utf-8")
    ).hexdigest()

    return int(
        digest[:16],
        16
    )


def format_period(start_date, end_date, language):
    if language == "en":
        return (
            f"{start_date.strftime('%d/%m/%Y')} "
            f"to {end_date.strftime('%d/%m/%Y')}"
        )

    return (
        f"Du {start_date.strftime('%d/%m/%Y')} "
        f"au {end_date.strftime('%d/%m/%Y')}"
    )


# ==================================================
# GÉNÉRATEUR HEBDOMADAIRE PREMIUM
# ==================================================

def generate_weekly_horoscope(sign, language="fr"):
    if language not in ("fr", "en"):
        language = "fr"

    sign_data = SIGN_DATA.get(sign)

    if not sign_data:
        return None

    start_date, end_date = get_week_dates()

    iso_calendar = start_date.isocalendar()
    year = iso_calendar.year
    week_number = iso_calendar.week

    randomizer = random.Random(
        build_week_seed(
            sign,
            year,
            week_number
        )
    )

    texts = WEEKLY_TEXTS[language]

    outlook = randomizer.choice(
        ELEMENT_OUTLOOKS[language][
            sign_data["element"]
        ]
    )

    love = randomizer.choice(
        texts["love"]
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

    advice = randomizer.choice(
        texts["advice"]
    )

    strong_day = randomizer.choice(
        texts["days"]
    )

    love_score = randomizer.randint(6, 9)
    work_score = randomizer.randint(6, 9)
    finance_score = randomizer.randint(5, 9)
    energy_score = randomizer.randint(5, 9)

    period = format_period(
        start_date,
        end_date,
        language
    )

    sign_name = sign_data[language].upper()
    emoji = sign_data["emoji"]

    if language == "en":
        result = (
            f"💎 ASTROVIBE PREMIUM\n"
            f"📆 WEEKLY FORECAST\n\n"

            f"{emoji} {sign_name}\n"
            f"{period}\n\n"

            f"✨ WEEKLY OUTLOOK\n"
            f"{outlook}\n\n"

            f"❤️ LOVE & RELATIONSHIPS • "
            f"{love_score}/10\n"
            f"{love}\n\n"

            f"💼 WORK & AMBITIONS • "
            f"{work_score}/10\n"
            f"{work}\n\n"

            f"💰 FINANCES • "
            f"{finance_score}/10\n"
            f"{finance}\n\n"

            f"🌿 ENERGY & WELL-BEING • "
            f"{energy_score}/10\n"
            f"{energy}\n\n"

            f"🍀 OPPORTUNITY OF THE WEEK\n"
            f"{opportunity}\n\n"

            f"⚠️ POINT OF ATTENTION\n"
            f"{warning}\n\n"

            f"⭐ STRONG DAY: {strong_day}\n\n"

            f"🌙 ASTROVIBE ADVICE\n"
            f"{advice}\n\n"

            f"──────────────\n"
            f"Premium content intended for "
            f"entertainment and personal reflection."
        )

    else:
        result = (
            f"💎 ASTROVIBE PREMIUM\n"
            f"📆 PRÉVISIONS DE LA SEMAINE\n\n"

            f"{emoji} {sign_name}\n"
            f"{period}\n\n"

            f"✨ TENDANCE GÉNÉRALE\n"
            f"{outlook}\n\n"

            f"❤️ AMOUR & RELATIONS • "
            f"{love_score}/10\n"
            f"{love}\n\n"

            f"💼 TRAVAIL & AMBITIONS • "
            f"{work_score}/10\n"
            f"{work}\n\n"

            f"💰 FINANCES • "
            f"{finance_score}/10\n"
            f"{finance}\n\n"

            f"🌿 ÉNERGIE & BIEN-ÊTRE • "
            f"{energy_score}/10\n"
            f"{energy}\n\n"

            f"🍀 OPPORTUNITÉ DE LA SEMAINE\n"
            f"{opportunity}\n\n"

            f"⚠️ POINT DE VIGILANCE\n"
            f"{warning}\n\n"

            f"⭐ JOURNÉE FORTE : {strong_day}\n\n"

            f"🌙 CONSEIL ASTROVIBE\n"
            f"{advice}\n\n"

            f"──────────────\n"
            f"Contenu Premium destiné au "
            f"divertissement et à la réflexion personnelle."
        )

    return result
