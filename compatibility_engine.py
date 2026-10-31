import hashlib
import random


SIGN_DATA = {
    "♈ Bélier": {
        "name": "Bélier",
        "emoji": "♈",
        "element": "Feu",
        "quality": "Cardinal"
    },
    "♉ Taureau": {
        "name": "Taureau",
        "emoji": "♉",
        "element": "Terre",
        "quality": "Fixe"
    },
    "♊ Gémeaux": {
        "name": "Gémeaux",
        "emoji": "♊",
        "element": "Air",
        "quality": "Mutable"
    },
    "♋ Cancer": {
        "name": "Cancer",
        "emoji": "♋",
        "element": "Eau",
        "quality": "Cardinal"
    },
    "♌ Lion": {
        "name": "Lion",
        "emoji": "♌",
        "element": "Feu",
        "quality": "Fixe"
    },
    "♍ Vierge": {
        "name": "Vierge",
        "emoji": "♍",
        "element": "Terre",
        "quality": "Mutable"
    },
    "♎ Balance": {
        "name": "Balance",
        "emoji": "♎",
        "element": "Air",
        "quality": "Cardinal"
    },
    "♏ Scorpion": {
        "name": "Scorpion",
        "emoji": "♏",
        "element": "Eau",
        "quality": "Fixe"
    },
    "♐ Sagittaire": {
        "name": "Sagittaire",
        "emoji": "♐",
        "element": "Feu",
        "quality": "Mutable"
    },
    "♑ Capricorne": {
        "name": "Capricorne",
        "emoji": "♑",
        "element": "Terre",
        "quality": "Cardinal"
    },
    "♒ Verseau": {
        "name": "Verseau",
        "emoji": "♒",
        "element": "Air",
        "quality": "Fixe"
    },
    "♓ Poissons": {
        "name": "Poissons",
        "emoji": "♓",
        "element": "Eau",
        "quality": "Mutable"
    }
}


ELEMENT_RELATIONS = {
    frozenset(["Feu", "Air"]): {
        "base": 82,
        "dynamic": (
            "Cette association réunit l’élan et les idées. "
            "Le premier mouvement inspire le second, tandis que "
            "la communication nourrit l’enthousiasme du duo."
        ),
        "strength": (
            "La spontanéité, la curiosité et la capacité à créer "
            "ensemble constituent les principales forces de cette relation."
        ),
        "challenge": (
            "Le rythme peut toutefois devenir irrégulier. Le couple doit "
            "veiller à transformer les projets et les promesses en actions concrètes."
        )
    },

    frozenset(["Terre", "Eau"]): {
        "base": 84,
        "dynamic": (
            "Cette association combine sécurité et sensibilité. "
            "La Terre apporte une structure rassurante, tandis que "
            "l’Eau enrichit la relation par son intuition et sa profondeur."
        ),
        "strength": (
            "La loyauté, l’écoute et le désir de construire progressivement "
            "peuvent créer un lien solide et protecteur."
        ),
        "challenge": (
            "La prudence peut parfois ralentir les échanges. Il est important "
            "d’exprimer les émotions avant qu’elles ne deviennent trop lourdes."
        )
    },

    frozenset(["Feu", "Eau"]): {
        "base": 64,
        "dynamic": (
            "Cette relation réunit intensité et sensibilité. L’attirance peut "
            "être forte, mais les réactions émotionnelles ne suivent pas "
            "toujours le même rythme."
        ),
        "strength": (
            "Le Feu encourage l’action tandis que l’Eau développe l’intuition. "
            "Ensemble, ces signes peuvent apprendre à conjuguer courage et profondeur."
        ),
        "challenge": (
            "Les paroles trop directes peuvent heurter la sensibilité, tandis "
            "que les silences peuvent déstabiliser le partenaire le plus spontané."
        )
    },

    frozenset(["Terre", "Air"]): {
        "base": 66,
        "dynamic": (
            "Cette association confronte le besoin de concret au désir de liberté "
            "intellectuelle. Elle peut devenir enrichissante lorsque chacun respecte "
            "la manière de penser de l’autre."
        ),
        "strength": (
            "L’Air apporte des perspectives nouvelles et la Terre aide à donner "
            "une forme durable aux idées."
        ),
        "challenge": (
            "L’un peut trouver l’autre trop prudent, tandis que l’autre peut "
            "percevoir un manque de constance. Des attentes clairement exprimées "
            "sont essentielles."
        )
    },

    frozenset(["Feu", "Terre"]): {
        "base": 71,
        "dynamic": (
            "L’ambition du Feu rencontre ici le réalisme de la Terre. "
            "Cette combinaison peut être très productive lorsqu’elle évite "
            "la compétition et les jugements trop rapides."
        ),
        "strength": (
            "L’un apporte l’impulsion, l’autre la méthode. Ensemble, ils peuvent "
            "transformer une inspiration en projet concret."
        ),
        "challenge": (
            "Le rythme représente le principal défi. Le Feu veut avancer vite, "
            "alors que la Terre préfère vérifier la solidité de chaque étape."
        )
    },

    frozenset(["Air", "Eau"]): {
        "base": 69,
        "dynamic": (
            "Cette relation associe réflexion et ressenti. L’Air cherche à comprendre "
            "par les mots, tandis que l’Eau interprète d’abord par l’intuition."
        ),
        "strength": (
            "La compréhension peut devenir très fine lorsque les idées et "
            "les émotions sont partagées sans jugement."
        ),
        "challenge": (
            "Le risque principal est de parler sans vraiment ressentir, ou de "
            "ressentir sans parvenir à expliquer. La patience facilite le dialogue."
        )
    }
}


SAME_ELEMENT_TEXTS = {
    "Feu": {
        "base": 80,
        "dynamic": (
            "Deux tempéraments passionnés se rencontrent. L’enthousiasme, "
            "l’audace et le désir de vivre pleinement peuvent créer une relation intense."
        ),
        "strength": (
            "La motivation et l’admiration mutuelle nourrissent naturellement le lien."
        ),
        "challenge": (
            "Les ego et l’impatience peuvent provoquer des affrontements. "
            "Il faut apprendre à partager l’espace et les initiatives."
        )
    },

    "Terre": {
        "base": 86,
        "dynamic": (
            "Cette relation repose sur la stabilité, la confiance et le désir "
            "de construire quelque chose de durable."
        ),
        "strength": (
            "La fidélité, le réalisme et la constance offrent une base très rassurante."
        ),
        "challenge": (
            "La routine peut prendre trop de place. Le duo gagne à introduire "
            "régulièrement de la nouveauté et de la spontanéité."
        )
    },

    "Air": {
        "base": 81,
        "dynamic": (
            "Les idées circulent facilement et la relation se nourrit de discussions, "
            "de découvertes et d’une grande liberté intellectuelle."
        ),
        "strength": (
            "La communication, l’humour et la curiosité créent une vraie complicité."
        ),
        "challenge": (
            "Le lien peut parfois rester trop cérébral. Les émotions doivent aussi "
            "trouver une place claire dans la relation."
        )
    },

    "Eau": {
        "base": 85,
        "dynamic": (
            "La connexion émotionnelle peut être profonde, intuitive et protectrice. "
            "Chacun perçoit facilement les nuances de l’autre."
        ),
        "strength": (
            "L’empathie et la tendresse favorisent un sentiment de compréhension rare."
        ),
        "challenge": (
            "Une grande sensibilité peut amplifier les non-dits. Les limites et les "
            "besoins personnels doivent rester clairement exprimés."
        )
    }
}


QUALITY_TEXTS = {
    "Cardinal": (
        "Les deux partenaires aiment initier et orienter les situations. "
        "La relation avance vite, mais les décisions doivent rester partagées."
    ),
    "Fixe": (
        "Les deux partenaires recherchent la loyauté et la continuité. "
        "Cette solidité est précieuse, à condition de ne pas transformer "
        "la détermination en rigidité."
    ),
    "Mutable": (
        "Les deux partenaires savent s’adapter et évoluer. La relation reste "
        "vivante, mais elle gagne à s’appuyer sur quelques repères stables."
    )
}


GENERAL_ADVICE = [
    (
        "Exprimez vos attentes avant qu’elles ne deviennent des frustrations. "
        "La transparence renforce cette relation."
    ),
    (
        "Préservez les qualités qui vous différencient au lieu de chercher "
        "à fonctionner exactement de la même manière."
    ),
    (
        "Créez des projets communs tout en conservant un espace personnel. "
        "Cet équilibre nourrit la complicité."
    ),
    (
        "Pendant un désaccord, cherchez d’abord à comprendre le besoin caché "
        "derrière la réaction de l’autre."
    ),
    (
        "Les petites attentions régulières auront davantage d’effet que "
        "les promesses spectaculaires mais occasionnelles."
    ),
    (
        "Votre relation se renforce lorsque chacun peut parler sans craindre "
        "d’être immédiatement jugé ou corrigé."
    )
]


def stable_randomizer(first_sign, second_sign):
    ordered_pair = sorted([first_sign, second_sign])
    raw_value = "astrovibe-compatibility|" + "|".join(ordered_pair)

    digest = hashlib.sha256(
        raw_value.encode("utf-8")
    ).hexdigest()

    seed = int(digest[:16], 16)

    return random.Random(seed)


def clamp_score(value):
    return max(4, min(10, value))


def generate_compatibility(first_sign, second_sign):
    first = SIGN_DATA.get(first_sign)
    second = SIGN_DATA.get(second_sign)

    if not first or not second:
        return None

    randomizer = stable_randomizer(
        first_sign,
        second_sign
    )

    same_sign = first_sign == second_sign
    same_element = first["element"] == second["element"]

    if same_element:
        relation = SAME_ELEMENT_TEXTS[
            first["element"]
        ]
    else:
        relation = ELEMENT_RELATIONS[
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
            base_percentage + randomizer.randint(-3, 3)
        )
    )

    base_score = round(overall_percentage / 10)

    attraction = clamp_score(
        base_score + randomizer.randint(-1, 1)
    )

    communication = clamp_score(
        base_score + randomizer.randint(-2, 1)
    )

    passion = clamp_score(
        base_score + randomizer.randint(-1, 2)
    )

    stability = clamp_score(
        base_score + randomizer.randint(-2, 1)
    )

    emotional = clamp_score(
        base_score + randomizer.randint(-1, 1)
    )

    if first["quality"] == second["quality"]:
        quality_analysis = QUALITY_TEXTS[
            first["quality"]
        ]
    else:
        quality_analysis = (
            f"Le tempérament {first['quality'].lower()} du "
            f"{first['name']} rencontre le rythme "
            f"{second['quality'].lower()} du {second['name']}. "
            "Cette différence peut devenir complémentaire si chacun "
            "respecte la façon d’avancer de l’autre."
        )

    advice = randomizer.choice(
        GENERAL_ADVICE
    )

    if overall_percentage >= 85:
        verdict = (
            "Une compatibilité naturellement forte, avec un potentiel "
            "de complicité et de construction durable."
        )
    elif overall_percentage >= 75:
        verdict = (
            "Une belle compatibilité qui peut s’épanouir grâce à "
            "une communication sincère et régulière."
        )
    elif overall_percentage >= 65:
        verdict = (
            "Une relation complémentaire qui demande quelques ajustements, "
            "mais qui peut devenir très enrichissante."
        )
    else:
        verdict = (
            "Une relation contrastée qui peut fonctionner lorsque les différences "
            "sont comprises plutôt que combattues."
        )

    result = (
        "🌌 ASTROVIBE • COMPATIBILITÉ\n\n"
        f"{first['emoji']} {first['name'].upper()}\n"
        f"×\n"
        f"{second['emoji']} {second['name'].upper()}\n\n"

        f"💞 COMPATIBILITÉ GLOBALE : "
        f"{overall_percentage} %\n"
        f"{verdict}\n\n"

        f"❤️ Attraction : {attraction}/10\n"
        f"💬 Communication : {communication}/10\n"
        f"🔥 Passion : {passion}/10\n"
        f"🤝 Stabilité : {stability}/10\n"
        f"🌙 Connexion émotionnelle : {emotional}/10\n\n"

        f"✨ VOTRE DYNAMIQUE\n"
        f"{relation['dynamic']}\n\n"

        f"💖 VOS FORCES\n"
        f"{relation['strength']}\n\n"

        f"⚡ VOS DÉFIS\n"
        f"{relation['challenge']}\n\n"

        f"🔭 VOTRE RYTHME RELATIONNEL\n"
        f"{quality_analysis}\n\n"

        f"🌙 CONSEIL ASTROVIBE\n"
        f"{advice}\n\n"

        f"──────────────\n"
        f"Contenu de divertissement et de réflexion personnelle."
    )

    return result
