import hashlib
import random
from datetime import datetime, timezone


# ==================================================
# SIGNES
# Les clés internes restent en français pour
# correspondre aux valeurs enregistrées dans Neon.
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


MONTH_NAMES = {
    "fr": [
        "Janvier",
        "Février",
        "Mars",
        "Avril",
        "Mai",
        "Juin",
        "Juillet",
        "Août",
        "Septembre",
        "Octobre",
        "Novembre",
        "Décembre"
    ],
    "en": [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
    ]
}


# ==================================================
# TENDANCES SELON L'ÉLÉMENT
# ==================================================

ELEMENT_OUTLOOKS = {
    "fr": {
        "fire": [
            (
                "Ce mois encourage l'initiative et le mouvement. "
                "Ton énergie peut accélérer un projet important, "
                "à condition de choisir une direction précise."
            ),
            (
                "Une phase dynamique s'ouvre devant toi. Ton courage "
                "peut créer une évolution concrète si tu évites de "
                "confondre enthousiasme et précipitation."
            ),
            (
                "Le mois met en valeur ta capacité à agir et à entraîner "
                "les autres. Une décision assumée pourrait transformer "
                "une situation jusque-là immobile."
            )
        ],
        "earth": [
            (
                "Ce mois favorise la construction et la stabilité. "
                "Tes efforts réguliers peuvent produire un résultat "
                "durable, même si les progrès restent progressifs."
            ),
            (
                "Une période constructive se présente. Ton pragmatisme "
                "t'aidera à consolider une situation qui mérite ton "
                "attention sur le long terme."
            ),
            (
                "Le mois t'invite à avancer avec patience et méthode. "
                "Une base solide sera plus utile qu'une réussite rapide "
                "mais fragile."
            )
        ],
        "air": [
            (
                "Les idées, les échanges et les nouvelles perspectives "
                "occupent une place importante ce mois-ci. Une rencontre "
                "ou une conversation peut modifier tes projets."
            ),
            (
                "Ta curiosité peut t'ouvrir des portes intéressantes. "
                "Garde toutefois une direction claire pour ne pas "
                "disperser ton énergie."
            ),
            (
                "Ce mois met la communication au premier plan. "
                "Les bons mots et les bonnes alliances peuvent faciliter "
                "une évolution importante."
            )
        ],
        "water": [
            (
                "Ce mois favorise l'intuition, la sensibilité et le "
                "recentrage émotionnel. Une évolution intérieure peut "
                "influencer positivement tes décisions."
            ),
            (
                "Une période de compréhension plus profonde commence. "
                "Tes ressentis apportent des informations utiles, à "
                "condition de conserver des limites claires."
            ),
            (
                "Le mois t'invite à écouter ce qui se passe sous la "
                "surface. Une situation ancienne peut être comprise "
                "différemment et perdre une partie de son poids."
            )
        ]
    },

    "en": {
        "fire": [
            (
                "This month encourages initiative and movement. "
                "Your energy may accelerate an important project when "
                "you choose one clear direction."
            ),
            (
                "A dynamic phase is opening. Courage may create practical "
                "progress when enthusiasm is balanced with good judgment."
            ),
            (
                "The month highlights your ability to act and inspire "
                "others. A confident decision may transform a situation "
                "that has remained still."
            )
        ],
        "earth": [
            (
                "This month favors stability and careful construction. "
                "Consistent efforts may create lasting results even when "
                "progress feels gradual."
            ),
            (
                "A constructive period is beginning. Practical thinking "
                "will help you strengthen a situation that deserves "
                "long-term attention."
            ),
            (
                "The month invites patience and method. A solid foundation "
                "will be more valuable than fast but fragile success."
            )
        ],
        "air": [
            (
                "Ideas, conversations and new perspectives play an "
                "important role this month. An encounter may influence "
                "the direction of your plans."
            ),
            (
                "Curiosity may open interesting doors. Maintain a clear "
                "direction so that your energy does not become scattered."
            ),
            (
                "Communication comes to the foreground. The right words "
                "and alliances may support an important development."
            )
        ],
        "water": [
            (
                "This month favors intuition, sensitivity and emotional "
                "balance. An inner change may positively influence your "
                "decisions."
            ),
            (
                "A period of deeper understanding is beginning. Feelings "
                "offer useful information when supported by clear boundaries."
            ),
            (
                "The month invites you to notice what lies beneath the "
                "surface. An old situation may be understood differently "
                "and lose some of its weight."
            )
        ]
    }
}


# ==================================================
# TEXTES MENSUELS
# ==================================================

MONTHLY_TEXTS = {
    "fr": {
        "love": [
            (
                "Le mois favorise une communication plus sincère. "
                "Une relation peut évoluer lorsque les attentes sont "
                "exprimées clairement et sans reproche."
            ),
            (
                "Les liens affectifs demandent à la fois proximité et "
                "liberté. Un meilleur équilibre peut renforcer une "
                "relation existante."
            ),
            (
                "Une ancienne hésitation peut perdre de son importance. "
                "Si tu es célibataire, une rencontre peut se développer "
                "progressivement."
            ),
            (
                "La tendresse et les petites attentions auront davantage "
                "d'impact que les grandes promesses."
            )
        ],
        "work": [
            (
                "Une priorité professionnelle mérite une organisation "
                "plus claire. Le mois peut apporter une avancée concrète "
                "si tu évites de disperser tes efforts."
            ),
            (
                "Un projet peut bénéficier d'un regard extérieur. "
                "La coopération et la communication renforceront tes "
                "chances de réussite."
            ),
            (
                "Ta régularité commence à être remarquée. Continue à "
                "développer tes compétences sans attendre une validation "
                "immédiate."
            ),
            (
                "Une décision repoussée doit désormais être clarifiée. "
                "Une fois le premier pas accompli, la suite deviendra "
                "plus simple."
            )
        ],
        "finance": [
            (
                "Le mois encourage une gestion prudente et structurée. "
                "Un petit ajustement peut améliorer durablement ton équilibre."
            ),
            (
                "Évite les engagements financiers pris dans l'urgence. "
                "Demande toutes les informations nécessaires avant de décider."
            ),
            (
                "Une occasion intéressante peut se présenter, mais sa "
                "valeur doit être étudiée sur le long terme."
            ),
            (
                "Fixer un objectif financier précis sera plus efficace "
                "que multiplier les restrictions."
            )
        ],
        "energy": [
            (
                "Ton énergie sera plus régulière si tu respectes des temps "
                "de récupération. Évite de remplir chaque espace disponible."
            ),
            (
                "Le mois peut alterner périodes dynamiques et moments plus "
                "calmes. Adapte ton rythme au lieu de lutter contre lui."
            ),
            (
                "Une meilleure qualité de sommeil et quelques pauses "
                "réelles amélioreront ta concentration."
            ),
            (
                "Ton équilibre dépendra de ta capacité à protéger ton temps "
                "et à diminuer les sollicitations inutiles."
            )
        ],
        "opportunity": [
            "Une rencontre peut ouvrir une perspective professionnelle.",
            "Un projet ancien peut recevoir une nouvelle impulsion.",
            "Une conversation peut apporter l'information qui te manquait.",
            "Une compétence personnelle peut être davantage remarquée.",
            "Un changement d'organisation peut libérer du temps et de l'énergie."
        ],
        "warning": [
            "Évite de vouloir tout accélérer en même temps.",
            "Ne néglige pas les détails d'un engagement important.",
            "Protège tes priorités face aux demandes secondaires.",
            "Ne transforme pas une inquiétude passagère en certitude.",
            "Évite de repousser une discussion devenue nécessaire."
        ],
        "advice": [
            "Construis ce mois autour d'une priorité claire.",
            "Accepte de modifier la méthode sans abandonner l'objectif.",
            "Préserve ton énergie pour ce qui possède une valeur durable.",
            "Exprime tes besoins avant qu'ils deviennent des frustrations.",
            "Reconnais tes progrès avant de te fixer un nouvel objectif."
        ],
        "keywords": [
            "Expansion",
            "Stabilité",
            "Clarté",
            "Évolution",
            "Confiance",
            "Renouveau",
            "Patience",
            "Équilibre"
        ]
    },

    "en": {
        "love": [
            (
                "The month favors more honest communication. A relationship "
                "may evolve when expectations are expressed clearly and "
                "without blame."
            ),
            (
                "Relationships require both closeness and personal freedom. "
                "A better balance may strengthen an existing bond."
            ),
            (
                "An old hesitation may lose its importance. If you are "
                "single, a connection may develop gradually."
            ),
            (
                "Tenderness and thoughtful gestures will have more impact "
                "than dramatic promises."
            )
        ],
        "work": [
            (
                "One professional priority requires clearer organization. "
                "The month may bring practical progress when efforts remain focused."
            ),
            (
                "A project may benefit from an outside perspective. "
                "Cooperation and communication will improve your chances."
            ),
            (
                "Your consistency is beginning to attract attention. "
                "Continue improving your abilities without waiting for "
                "immediate recognition."
            ),
            (
                "A postponed decision now requires clarity. Once the first "
                "step is taken, the rest may become easier."
            )
        ],
        "finance": [
            (
                "The month encourages careful and structured financial "
                "management. A small adjustment may create lasting balance."
            ),
            (
                "Avoid financial commitments made under pressure. Ask for "
                "all necessary information before deciding."
            ),
            (
                "An interesting opportunity may appear, but its long-term "
                "value needs careful consideration."
            ),
            (
                "One clear financial objective will be more effective than "
                "many restrictions."
            )
        ],
        "energy": [
            (
                "Your energy will remain steadier when genuine recovery "
                "time is protected. Avoid filling every available moment."
            ),
            (
                "The month may alternate between dynamic and quieter periods. "
                "Adapt your rhythm instead of resisting it."
            ),
            (
                "Better sleep and a few genuine pauses will improve concentration."
            ),
            (
                "Balance depends on protecting your time and reducing "
                "unnecessary demands."
            )
        ],
        "opportunity": [
            "An encounter may open a professional perspective.",
            "An older project may receive new momentum.",
            "A conversation may provide the information you were missing.",
            "A personal ability may attract greater recognition.",
            "A change in organization may free time and energy."
        ],
        "warning": [
            "Avoid trying to accelerate everything at once.",
            "Do not overlook the details of an important commitment.",
            "Protect your priorities from secondary demands.",
            "Do not turn a temporary concern into a certainty.",
            "Avoid postponing a conversation that has become necessary."
        ],
        "advice": [
            "Build the month around one clear priority.",
            "Change the method when necessary without abandoning the objective.",
            "Protect your energy for what offers lasting value.",
            "Express your needs before they become frustrations.",
            "Recognize your progress before setting a new objective."
        ],
        "keywords": [
            "Expansion",
            "Stability",
            "Clarity",
            "Growth",
            "Confidence",
            "Renewal",
            "Patience",
            "Balance"
        ]
    }
}


# ==================================================
# TEXTES ANNUELS
# ==================================================

YEARLY_TEXTS = {
    "fr": {
        "love": [
            (
                "L'année encourage une évolution plus consciente de ta vie "
                "affective. Les relations solides gagneront en profondeur, "
                "tandis que les liens fragiles demanderont davantage de clarté."
            ),
            (
                "Une nouvelle maturité émotionnelle peut transformer tes "
                "relations. Tu apprendras à différencier le besoin d'attention "
                "d'une véritable connexion."
            ),
            (
                "Cette année favorise les choix affectifs plus authentiques. "
                "Une relation importante peut se construire ou évoluer grâce "
                "à une communication honnête."
            )
        ],
        "work": [
            (
                "L'année peut marquer une étape importante dans ton évolution "
                "professionnelle. Les résultats dépendront surtout de ta "
                "régularité et de ta capacité à saisir les bonnes occasions."
            ),
            (
                "Un projet ambitieux peut gagner en importance. Développer "
                "une compétence précise ou créer une nouvelle alliance "
                "professionnelle sera particulièrement utile."
            ),
            (
                "Ta progression se construira par étapes. Le succès viendra "
                "moins d'un coup de chance que de décisions cohérentes et répétées."
            )
        ],
        "finance": [
            (
                "L'année favorise une relation plus structurée à l'argent. "
                "Un objectif précis peut t'aider à renforcer ta sécurité "
                "et ta liberté."
            ),
            (
                "Une évolution financière reste possible, mais elle demandera "
                "d'éviter les décisions impulsives et les promesses trop rapides."
            ),
            (
                "La planification et la patience seront tes meilleures alliées. "
                "Privilégie les choix soutenables sur le long terme."
            )
        ],
        "growth": [
            (
                "Cette année t'invite à mieux connaître tes priorités et à "
                "cesser d'investir ton énergie dans ce qui ne correspond plus "
                "à tes objectifs."
            ),
            (
                "Une transformation personnelle peut s'installer progressivement. "
                "Tu gagneras en confiance en assumant davantage tes choix."
            ),
            (
                "L'année favorise la simplification. En réduisant les distractions, "
                "tu pourras consacrer plus de temps à ce qui possède un vrai sens."
            )
        ],
        "energy": [
            (
                "Ton énergie dépendra de ta capacité à équilibrer ambition et "
                "récupération. Un rythme durable sera plus efficace qu'une "
                "succession d'efforts excessifs."
            ),
            (
                "Le bien-être deviendra une priorité plus importante. "
                "Le sommeil, les pauses et les limites personnelles auront "
                "un impact direct sur tes résultats."
            ),
            (
                "Cette année t'encourage à écouter plus tôt les signaux de "
                "fatigue. Prévenir l'épuisement sera essentiel pour maintenir "
                "ta concentration."
            )
        ],
        "opportunity": [
            "Une nouvelle responsabilité peut soutenir ton évolution.",
            "Un déplacement ou une rencontre peut ouvrir une perspective inattendue.",
            "Une compétence personnelle peut devenir une véritable opportunité.",
            "Un projet indépendant peut gagner en importance.",
            "Une collaboration peut accélérer un objectif de long terme."
        ],
        "warning": [
            "Ne poursuis pas un objectif uniquement pour prouver ta valeur.",
            "Évite de négliger ton équilibre au profit de résultats immédiats.",
            "Ne laisse pas la peur du changement maintenir une situation devenue limitée.",
            "Vérifie la solidité des engagements avant de t'investir pleinement.",
            "Évite de multiplier les projets au point de perdre ta direction."
        ],
        "advice": [
            "Construis l'année autour de ce qui possède une valeur durable.",
            "Fais de la régularité ton principal avantage.",
            "Choisis les engagements qui respectent réellement tes priorités.",
            "Accepte l'évolution sans abandonner tes valeurs essentielles.",
            "Mesure ta progression sur plusieurs mois, pas sur une seule journée."
        ],
        "themes": [
            "Construction",
            "Transformation",
            "Expansion",
            "Clarté",
            "Renouveau",
            "Confiance",
            "Équilibre",
            "Accomplissement"
        ],
        "favorable_periods": [
            "Janvier à mars",
            "Février à avril",
            "Avril à juin",
            "Juin à août",
            "Septembre à novembre",
            "Octobre à décembre"
        ],
        "vigilance_periods": [
            "Mars et avril",
            "Mai et juin",
            "Juillet et août",
            "Septembre et octobre",
            "Novembre et décembre"
        ]
    },

    "en": {
        "love": [
            (
                "The year encourages a more conscious evolution in your "
                "relationships. Strong bonds may deepen, while fragile "
                "connections will require greater clarity."
            ),
            (
                "Greater emotional maturity may transform your relationships. "
                "You may learn to distinguish the need for attention from "
                "a genuine connection."
            ),
            (
                "The year favors more authentic emotional decisions. "
                "An important relationship may grow through honest communication."
            )
        ],
        "work": [
            (
                "The year may mark an important stage in your professional "
                "development. Results will depend mainly on consistency and "
                "your ability to recognize the right opportunities."
            ),
            (
                "An ambitious project may gain importance. Developing one "
                "specific ability or forming a new professional alliance "
                "will be especially useful."
            ),
            (
                "Progress will develop step by step. Success will come less "
                "from luck than from repeated and consistent decisions."
            )
        ],
        "finance": [
            (
                "The year favors a more structured relationship with money. "
                "One precise objective may strengthen both security and freedom."
            ),
            (
                "Financial progress is possible, but impulsive decisions and "
                "promises of immediate results should be avoided."
            ),
            (
                "Planning and patience will be your strongest allies. "
                "Prioritize choices that remain sustainable over time."
            )
        ],
        "growth": [
            (
                "The year invites you to understand your priorities more "
                "clearly and stop investing energy in what no longer supports them."
            ),
            (
                "A personal transformation may develop gradually. Confidence "
                "will grow as you take greater ownership of your decisions."
            ),
            (
                "The year favors simplification. Reducing distractions will "
                "create more space for what genuinely matters."
            )
        ],
        "energy": [
            (
                "Your energy will depend on balancing ambition with recovery. "
                "A sustainable pace will be more effective than repeated excess."
            ),
            (
                "Well-being may become a stronger priority. Sleep, pauses and "
                "personal limits will directly influence your results."
            ),
            (
                "The year encourages you to notice fatigue earlier. Preventing "
                "exhaustion will be essential for maintaining concentration."
            )
        ],
        "opportunity": [
            "A new responsibility may support your development.",
            "Travel or an encounter may open an unexpected perspective.",
            "A personal ability may become a genuine opportunity.",
            "An independent project may gain importance.",
            "A collaboration may accelerate a long-term objective."
        ],
        "warning": [
            "Do not pursue an objective only to prove your value.",
            "Avoid sacrificing balance for immediate results.",
            "Do not allow fear of change to preserve a limiting situation.",
            "Check the strength of commitments before investing fully.",
            "Avoid multiplying projects until your direction becomes unclear."
        ],
        "advice": [
            "Build the year around what offers lasting value.",
            "Make consistency your strongest advantage.",
            "Choose commitments that genuinely respect your priorities.",
            "Accept evolution without abandoning your essential values.",
            "Measure progress over several months, not one day."
        ],
        "themes": [
            "Construction",
            "Transformation",
            "Expansion",
            "Clarity",
            "Renewal",
            "Confidence",
            "Balance",
            "Achievement"
        ],
        "favorable_periods": [
            "January to March",
            "February to April",
            "April to June",
            "June to August",
            "September to November",
            "October to December"
        ],
        "vigilance_periods": [
            "March and April",
            "May and June",
            "July and August",
            "September and October",
            "November and December"
        ]
    }
}


# ==================================================
# OUTILS
# ==================================================

def build_seed(prefix, sign, period):
    raw_value = (
        f"astrovibe-{prefix}|{sign}|{period}"
    )

    digest = hashlib.sha256(
        raw_value.encode("utf-8")
    ).hexdigest()

    return int(
        digest[:16],
        16
    )


def choose_scores(randomizer):
    return {
        "love": randomizer.randint(6, 9),
        "work": randomizer.randint(6, 9),
        "finance": randomizer.randint(5, 9),
        "energy": randomizer.randint(5, 9)
    }


# ==================================================
# HOROSCOPE MENSUEL PREMIUM
# ==================================================

def generate_monthly_horoscope(sign, language="fr"):
    if language not in ("fr", "en"):
        language = "fr"

    sign_data = SIGN_DATA.get(sign)

    if not sign_data:
        return None

    today = datetime.now(timezone.utc).date()

    randomizer = random.Random(
        build_seed(
            "monthly",
            sign,
            f"{today.year}-{today.month}"
        )
    )

    texts = MONTHLY_TEXTS[language]
    scores = choose_scores(randomizer)

    outlook = randomizer.choice(
        ELEMENT_OUTLOOKS[
            language
        ][
            sign_data["element"]
        ]
    )

    love = randomizer.choice(texts["love"])
    work = randomizer.choice(texts["work"])
    finance = randomizer.choice(texts["finance"])
    energy = randomizer.choice(texts["energy"])
    opportunity = randomizer.choice(texts["opportunity"])
    warning = randomizer.choice(texts["warning"])
    advice = randomizer.choice(texts["advice"])
    keyword = randomizer.choice(texts["keywords"])

    strong_week = randomizer.randint(1, 4)

    month_name = MONTH_NAMES[
        language
    ][
        today.month - 1
    ]

    sign_name = sign_data[language].upper()
    emoji = sign_data["emoji"]

    if language == "en":
        return (
            f"💎 ASTROVIBE PREMIUM\n"
            f"🌙 MONTHLY FORECAST\n\n"
            f"{emoji} {sign_name}\n"
            f"{month_name} {today.year}\n\n"

            f"✨ MONTHLY OUTLOOK\n"
            f"{outlook}\n\n"

            f"❤️ LOVE & RELATIONSHIPS • "
            f"{scores['love']}/10\n"
            f"{love}\n\n"

            f"💼 WORK & AMBITIONS • "
            f"{scores['work']}/10\n"
            f"{work}\n\n"

            f"💰 FINANCES • "
            f"{scores['finance']}/10\n"
            f"{finance}\n\n"

            f"🌿 ENERGY & WELL-BEING • "
            f"{scores['energy']}/10\n"
            f"{energy}\n\n"

            f"🍀 OPPORTUNITY OF THE MONTH\n"
            f"{opportunity}\n\n"

            f"⚠️ POINT OF ATTENTION\n"
            f"{warning}\n\n"

            f"⭐ STRONGEST PERIOD\n"
            f"Week {strong_week}\n\n"

            f"💫 KEYWORD\n"
            f"{keyword}\n\n"

            f"🌙 ASTROVIBE ADVICE\n"
            f"{advice}\n\n"

            f"──────────────\n"
            f"Premium content intended for "
            f"entertainment and personal reflection."
        )

    return (
        f"💎 ASTROVIBE PREMIUM\n"
        f"🌙 PRÉVISIONS DU MOIS\n\n"
        f"{emoji} {sign_name}\n"
        f"{month_name} {today.year}\n\n"

        f"✨ TENDANCE DU MOIS\n"
        f"{outlook}\n\n"

        f"❤️ AMOUR & RELATIONS • "
        f"{scores['love']}/10\n"
        f"{love}\n\n"

        f"💼 TRAVAIL & AMBITIONS • "
        f"{scores['work']}/10\n"
        f"{work}\n\n"

        f"💰 FINANCES • "
        f"{scores['finance']}/10\n"
        f"{finance}\n\n"

        f"🌿 ÉNERGIE & BIEN-ÊTRE • "
        f"{scores['energy']}/10\n"
        f"{energy}\n\n"

        f"🍀 OPPORTUNITÉ DU MOIS\n"
        f"{opportunity}\n\n"

        f"⚠️ POINT DE VIGILANCE\n"
        f"{warning}\n\n"

        f"⭐ PÉRIODE FORTE\n"
        f"Semaine {strong_week}\n\n"

        f"💫 MOT-CLÉ\n"
        f"{keyword}\n\n"

        f"🌙 CONSEIL ASTROVIBE\n"
        f"{advice}\n\n"

        f"──────────────\n"
        f"Contenu Premium destiné au divertissement "
        f"et à la réflexion personnelle."
    )


# ==================================================
# HOROSCOPE ANNUEL PREMIUM
# ==================================================

def generate_yearly_horoscope(sign, language="fr"):
    if language not in ("fr", "en"):
        language = "fr"

    sign_data = SIGN_DATA.get(sign)

    if not sign_data:
        return None

    today = datetime.now(timezone.utc).date()
    year = today.year

    randomizer = random.Random(
        build_seed(
            "yearly",
            sign,
            str(year)
        )
    )

    texts = YEARLY_TEXTS[language]
    scores = choose_scores(randomizer)

    outlook = randomizer.choice(
        ELEMENT_OUTLOOKS[
            language
        ][
            sign_data["element"]
        ]
    )

    love = randomizer.choice(texts["love"])
    work = randomizer.choice(texts["work"])
    finance = randomizer.choice(texts["finance"])
    growth = randomizer.choice(texts["growth"])
    energy = randomizer.choice(texts["energy"])
    opportunity = randomizer.choice(texts["opportunity"])
    warning = randomizer.choice(texts["warning"])
    advice = randomizer.choice(texts["advice"])
    theme = randomizer.choice(texts["themes"])

    favorable_period = randomizer.choice(
        texts["favorable_periods"]
    )

    vigilance_period = randomizer.choice(
        texts["vigilance_periods"]
    )

    sign_name = sign_data[language].upper()
    emoji = sign_data["emoji"]

    if language == "en":
        return (
            f"💎 ASTROVIBE PREMIUM\n"
            f"🌟 YEARLY FORECAST {year}\n\n"
            f"{emoji} {sign_name}\n\n"

            f"✨ MAIN THEME OF THE YEAR\n"
            f"{theme}\n\n"
            f"{outlook}\n\n"

            f"❤️ LOVE & RELATIONSHIPS • "
            f"{scores['love']}/10\n"
            f"{love}\n\n"

            f"💼 CAREER & AMBITIONS • "
            f"{scores['work']}/10\n"
            f"{work}\n\n"

            f"💰 FINANCES • "
            f"{scores['finance']}/10\n"
            f"{finance}\n\n"

            f"🌱 PERSONAL GROWTH\n"
            f"{growth}\n\n"

            f"🌿 ENERGY & WELL-BEING • "
            f"{scores['energy']}/10\n"
            f"{energy}\n\n"

            f"🍀 OPPORTUNITY OF THE YEAR\n"
            f"{opportunity}\n\n"

            f"⭐ FAVORABLE PERIOD\n"
            f"{favorable_period}\n\n"

            f"⚠️ PERIOD OF ATTENTION\n"
            f"{vigilance_period}\n"
            f"{warning}\n\n"

            f"🌙 ASTROVIBE ADVICE FOR {year}\n"
            f"{advice}\n\n"

            f"──────────────\n"
            f"Premium content intended for "
            f"entertainment and personal reflection."
        )

    return (
        f"💎 ASTROVIBE PREMIUM\n"
        f"🌟 PRÉVISIONS ANNUELLES {year}\n\n"
        f"{emoji} {sign_name}\n\n"

        f"✨ GRAND THÈME DE L'ANNÉE\n"
        f"{theme}\n\n"
        f"{outlook}\n\n"

        f"❤️ AMOUR & RELATIONS • "
        f"{scores['love']}/10\n"
        f"{love}\n\n"

        f"💼 CARRIÈRE & AMBITIONS • "
        f"{scores['work']}/10\n"
        f"{work}\n\n"

        f"💰 FINANCES • "
        f"{scores['finance']}/10\n"
        f"{finance}\n\n"

        f"🌱 ÉVOLUTION PERSONNELLE\n"
        f"{growth}\n\n"

        f"🌿 ÉNERGIE & BIEN-ÊTRE • "
        f"{scores['energy']}/10\n"
        f"{energy}\n\n"

        f"🍀 OPPORTUNITÉ DE L'ANNÉE\n"
        f"{opportunity}\n\n"

        f"⭐ PÉRIODE FAVORABLE\n"
        f"{favorable_period}\n\n"

        f"⚠️ PÉRIODE DE VIGILANCE\n"
        f"{vigilance_period}\n"
        f"{warning}\n\n"

        f"🌙 CONSEIL ASTROVIBE POUR {year}\n"
        f"{advice}\n\n"

        f"──────────────\n"
        f"Contenu Premium destiné au divertissement "
        f"et à la réflexion personnelle."
    )
