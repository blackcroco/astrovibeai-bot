import hashlib
import random
from datetime import datetime, timezone


SIGN_DATA = {
    "♈ Bélier": {
        "name": "Bélier",
        "emoji": "♈",
        "tone": [
            "Ton élan naturel peut aujourd’hui ouvrir une porte inattendue.",
            "Ta détermination est précieuse, à condition de ne pas confondre vitesse et précipitation.",
            "Une énergie franche t’accompagne et favorise les initiatives réfléchies."
        ]
    },
    "♉ Taureau": {
        "name": "Taureau",
        "emoji": "♉",
        "tone": [
            "Ta stabilité intérieure t’aide à distinguer l’essentiel du superflu.",
            "Le temps joue en ta faveur si tu avances avec méthode et confiance.",
            "Une approche calme et concrète peut transformer une hésitation en certitude."
        ]
    },
    "♊ Gémeaux": {
        "name": "Gémeaux",
        "emoji": "♊",
        "tone": [
            "Ta curiosité révèle aujourd’hui des possibilités que d’autres ne remarquent pas.",
            "Les échanges seront particulièrement importants pour clarifier tes intentions.",
            "Ton agilité d’esprit est un avantage, à condition de garder un fil conducteur."
        ]
    },
    "♋ Cancer": {
        "name": "Cancer",
        "emoji": "♋",
        "tone": [
            "Ton intuition perçoit aujourd’hui ce qui n’est pas encore clairement exprimé.",
            "Une sensibilité bien canalisée peut devenir une véritable force de décision.",
            "Prendre soin de ton équilibre intérieur facilitera tes relations avec les autres."
        ]
    },
    "♌ Lion": {
        "name": "Lion",
        "emoji": "♌",
        "tone": [
            "Ton assurance attire l’attention, mais ton écoute fera aujourd’hui la différence.",
            "Une occasion de montrer ta valeur pourrait apparaître de façon naturelle.",
            "Ton rayonnement est puissant lorsque tu l’utilises pour inspirer plutôt que convaincre."
        ]
    },
    "♍ Vierge": {
        "name": "Vierge",
        "emoji": "♍",
        "tone": [
            "Ton sens du détail permet de résoudre une situation restée floue.",
            "Une organisation simple t’aidera à retrouver de l’espace mental.",
            "Tu peux progresser efficacement sans chercher à tout contrôler."
        ]
    },
    "♎ Balance": {
        "name": "Balance",
        "emoji": "♎",
        "tone": [
            "Une décision devient plus simple lorsque tu écoutes aussi tes propres besoins.",
            "Ton sens de l’équilibre facilite aujourd’hui une discussion importante.",
            "L’harmonie recherchée ne doit pas t’empêcher d’exprimer clairement ta position."
        ]
    },
    "♏ Scorpion": {
        "name": "Scorpion",
        "emoji": "♏",
        "tone": [
            "Ton intuition profonde t’aide à comprendre les véritables enjeux d’une situation.",
            "Une transformation discrète est en cours et mérite ta confiance.",
            "Ta lucidité est précieuse, mais laisse aussi une place aux explications simples."
        ]
    },
    "♐ Sagittaire": {
        "name": "Sagittaire",
        "emoji": "♐",
        "tone": [
            "Ton besoin d’avancer retrouve aujourd’hui une direction plus claire.",
            "Une idée nouvelle peut élargir ta vision d’un projet ou d’une relation.",
            "Ton enthousiasme est communicatif lorsqu’il reste associé à un plan concret."
        ]
    },
    "♑ Capricorne": {
        "name": "Capricorne",
        "emoji": "♑",
        "tone": [
            "Tes efforts réguliers commencent à produire des résultats plus visibles.",
            "Une décision responsable peut consolider un projet important.",
            "Ton sérieux inspire confiance, mais n’oublie pas de reconnaître tes progrès."
        ]
    },
    "♒ Verseau": {
        "name": "Verseau",
        "emoji": "♒",
        "tone": [
            "Une idée originale peut aujourd’hui trouver une application très concrète.",
            "Ta liberté de pensée t’aide à sortir d’un schéma devenu trop étroit.",
            "Un échange inattendu pourrait nourrir une réflexion prometteuse."
        ]
    },
    "♓ Poissons": {
        "name": "Poissons",
        "emoji": "♓",
        "tone": [
            "Ton imagination et ton intuition se complètent particulièrement bien aujourd’hui.",
            "Une impression subtile mérite d’être écoutée avant de prendre une décision.",
            "Ton empathie crée des liens, à condition de préserver aussi tes propres limites."
        ]
    }
}


LOVE_TEXTS = [
    "Une conversation sincère peut rapprocher deux personnes davantage qu’un grand geste. Si tu es en couple, privilégie les mots simples et directs. Si tu es célibataire, une rencontre intéressante pourrait commencer par un échange sans prétention.",
    "La journée favorise la compréhension mutuelle. Une attente non exprimée pourrait être clarifiée avec douceur. En amour, évite les suppositions et laisse à l’autre la possibilité d’expliquer son point de vue.",
    "Un besoin de proximité se fait sentir, mais il doit rester équilibré. Offre de l’attention sans oublier ton propre rythme. Une relation gagne aujourd’hui en qualité grâce à la patience et à l’écoute.",
    "Les émotions sont présentes, mais elles demandent à être accueillies sans réaction précipitée. Une parole rassurante peut apaiser une tension. Les célibataires pourraient remarquer une personne jusque-là restée en retrait.",
    "Une énergie chaleureuse accompagne les relations. C’est un bon moment pour créer un souvenir agréable, reprendre contact ou montrer ton intérêt avec naturel. La spontanéité sera plus efficace que les stratégies compliquées.",
    "Tu pourrais avoir besoin de davantage de clarté dans une relation. Pose les questions importantes avec bienveillance. Une réponse honnête, même imparfaite, contribuera à construire quelque chose de plus solide.",
    "L’affection passe aujourd’hui par les petites attentions. Un détail, un message ou une disponibilité réelle peut avoir plus de valeur qu’une grande déclaration. Reste attentif aux signes de réciprocité.",
    "Une ancienne hésitation peut perdre de son importance. L’ambiance encourage à regarder une relation avec un regard neuf. Ne cherche pas à forcer une conclusion, laisse la confiance se construire progressivement."
]


WORK_TEXTS = [
    "Une priorité mérite d’être isolée du reste. En avançant étape par étape, tu gagneras en efficacité et en visibilité. Côté finances, évite les décisions impulsives et vérifie les détails avant de t’engager.",
    "Une proposition ou une idée peut évoluer favorablement si elle est présentée avec précision. Concentre-toi sur les bénéfices concrets. Pour l’argent, la prudence reste préférable aux promesses de gains rapides.",
    "La coopération sera plus productive que le travail solitaire. Une personne peut apporter le complément qui manquait à ton raisonnement. Sur le plan financier, une petite optimisation peut avoir un effet durable.",
    "Une tâche repoussée demande enfin ton attention. Une fois commencée, elle devrait être moins difficile que prévu. Ne laisse pas une dépense secondaire détourner tes ressources d’un objectif plus important.",
    "Ton travail peut être remarqué, même si les résultats ne sont pas immédiatement annoncés. Continue avec régularité. Une décision financière mérite une nuit de réflexion plutôt qu’une réponse immédiate.",
    "La journée convient aux ajustements, aux corrections et aux négociations. Tu n’as pas besoin de tout recommencer : quelques changements ciblés suffiront. Garde une vision réaliste de ton budget.",
    "Une opportunité intéressante peut se cacher dans une demande ordinaire. Reste disponible tout en protégeant ton emploi du temps. Concernant les finances, privilégie ce qui apporte une valeur réelle et durable.",
    "Il est temps de distinguer l’urgent de l’important. Une meilleure organisation libérera de l’énergie pour les projets à fort potentiel. Évite de dépenser pour compenser une frustration passagère."
]


ENERGY_TEXTS = [
    "Ton énergie est régulière, mais elle peut diminuer si tu disperses trop ton attention. Prévois une vraie pause et privilégie un rythme soutenable plutôt qu’un effort excessif.",
    "La vitalité est présente par vagues. Utilise les moments dynamiques pour avancer, puis accorde-toi un temps de récupération. Une activité douce peut t’aider à retrouver ton équilibre.",
    "Ton mental pourrait être plus sollicité que ton corps. Réduire les distractions améliorera ta concentration. Une respiration lente ou une courte marche peut clarifier tes idées.",
    "La journée invite à écouter les signaux subtils de fatigue. Il ne s’agit pas de ralentir complètement, mais de mieux répartir ton énergie. La qualité du repos aura son importance.",
    "Une énergie constructive t’accompagne. Elle sera particulièrement utile pour terminer une tâche courte ou remettre de l’ordre dans ton environnement. Attention cependant à ne pas dépasser tes limites.",
    "Ton équilibre dépendra de la qualité de tes transitions. Évite d’enchaîner toutes les activités sans pause. Quelques minutes de calme peuvent suffire à retrouver une meilleure présence.",
    "Ton enthousiasme peut te pousser à en faire beaucoup. Choisis une direction principale et conserve une réserve d’énergie pour la fin de journée. L’hydratation et le sommeil restent essentiels.",
    "Une ambiance plus calme favorise la récupération émotionnelle. Éloigne-toi momentanément des sollicitations inutiles. Ton efficacité reviendra naturellement lorsque ton esprit sera moins encombré."
]


ADVICE_TEXTS = [
    "Choisis la clarté plutôt que la précipitation.",
    "Une petite action cohérente vaut mieux qu’une grande intention repoussée.",
    "Écoute ton intuition, puis vérifie-la avec des faits concrets.",
    "Protège ton énergie sans fermer la porte au dialogue.",
    "Ne cherche pas à tout résoudre aujourd’hui : avance sur ce qui dépend réellement de toi.",
    "Exprime ce que tu souhaites sans attendre que les autres le devinent.",
    "Prends le temps de reconnaître le chemin déjà parcouru.",
    "La souplesse peut aujourd’hui être plus efficace que le contrôle."
]


COLORS = [
    "Or",
    "Bleu nuit",
    "Violet profond",
    "Vert émeraude",
    "Blanc perlé",
    "Rouge grenat",
    "Bleu céleste",
    "Rose poudré",
    "Cuivre",
    "Indigo"
]


KEYWORDS = [
    "Clarté",
    "Équilibre",
    "Confiance",
    "Élan",
    "Renouveau",
    "Patience",
    "Intuition",
    "Harmonie",
    "Courage",
    "Ouverture"
]


def build_seed(sign, date_string):
    raw_value = f"astrovibe|{sign}|{date_string}"

    digest = hashlib.sha256(
        raw_value.encode("utf-8")
    ).hexdigest()

    return int(digest[:16], 16)


def generate_daily_horoscope(sign):
    today = datetime.now(timezone.utc).date()
    date_string = today.isoformat()

    sign_data = SIGN_DATA.get(sign)

    if not sign_data:
        return None

    randomizer = random.Random(
        build_seed(sign, date_string)
    )

    introduction = randomizer.choice(
        sign_data["tone"]
    )

    love = randomizer.choice(
        LOVE_TEXTS
    )

    work = randomizer.choice(
        WORK_TEXTS
    )

    energy = randomizer.choice(
        ENERGY_TEXTS
    )

    advice = randomizer.choice(
        ADVICE_TEXTS
    )

    color = randomizer.choice(
        COLORS
    )

    keyword = randomizer.choice(
        KEYWORDS
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

        f"✨ TENDANCE GÉNÉRALE\n"
        f"{introduction}\n\n"

        f"❤️ AMOUR • {love_score}/10\n"
        f"{love}\n\n"

        f"💼 TRAVAIL & FINANCES • "
        f"{work_score}/10\n"
        f"{work}\n\n"

        f"🌿 ÉNERGIE & BIEN-ÊTRE • "
        f"{energy_score}/10\n"
        f"{energy}\n\n"

        f"🍀 CHANCE • {luck_score}/10\n"
        f"🎨 Couleur du jour : {color}\n"
        f"🔢 Nombre du jour : {lucky_number}\n"
        f"💫 Mot-clé : {keyword}\n\n"

        f"🌙 CONSEIL ASTROVIBE\n"
        f"{advice}\n\n"

        f"──────────────\n"
        f"Contenu de divertissement et de "
        f"réflexion personnelle."
    )

    return horoscope
