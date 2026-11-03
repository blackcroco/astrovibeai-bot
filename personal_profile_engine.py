# ============================================
# ASTROVIBE - PROFIL PERSONNEL
# Moteur central du Profil AstroVibe Personnel
# ============================================


SIGN_ALIASES = {
    "♈ Bélier": "aries",
    "♉ Taureau": "taurus",
    "♊ Gémeaux": "gemini",
    "♋ Cancer": "cancer",
    "♌ Lion": "leo",
    "♍ Vierge": "virgo",
    "♎ Balance": "libra",
    "♏ Scorpion": "scorpio",
    "♐ Sagittaire": "sagittarius",
    "♑ Capricorne": "capricorn",
    "♒ Verseau": "aquarius",
    "♓ Poissons": "pisces",
}


SIGN_NAMES = {
    "fr": {
        "aries": "♈ Bélier",
        "taurus": "♉ Taureau",
        "gemini": "♊ Gémeaux",
        "cancer": "♋ Cancer",
        "leo": "♌ Lion",
        "virgo": "♍ Vierge",
        "libra": "♎ Balance",
        "scorpio": "♏ Scorpion",
        "sagittarius": "♐ Sagittaire",
        "capricorn": "♑ Capricorne",
        "aquarius": "♒ Verseau",
        "pisces": "♓ Poissons",
    },
    "en": {
        "aries": "♈ Aries",
        "taurus": "♉ Taurus",
        "gemini": "♊ Gemini",
        "cancer": "♋ Cancer",
        "leo": "♌ Leo",
        "virgo": "♍ Virgo",
        "libra": "♎ Libra",
        "scorpio": "♏ Scorpio",
        "sagittarius": "♐ Sagittarius",
        "capricorn": "♑ Capricorn",
        "aquarius": "♒ Aquarius",
        "pisces": "♓ Pisces",
    }
}


SIGN_META = {
    "aries": {
        "element": "fire",
        "modality": "cardinal",
    },
    "taurus": {
        "element": "earth",
        "modality": "fixed",
    },
    "gemini": {
        "element": "air",
        "modality": "mutable",
    },
    "cancer": {
        "element": "water",
        "modality": "cardinal",
    },
    "leo": {
        "element": "fire",
        "modality": "fixed",
    },
    "virgo": {
        "element": "earth",
        "modality": "mutable",
    },
    "libra": {
        "element": "air",
        "modality": "cardinal",
    },
    "scorpio": {
        "element": "water",
        "modality": "fixed",
    },
    "sagittarius": {
        "element": "fire",
        "modality": "mutable",
    },
    "capricorn": {
        "element": "earth",
        "modality": "cardinal",
    },
    "aquarius": {
        "element": "air",
        "modality": "fixed",
    },
    "pisces": {
        "element": "water",
        "modality": "mutable",
    },
}


ELEMENT_LABELS = {
    "fr": {
        "fire": "Feu",
        "earth": "Terre",
        "air": "Air",
        "water": "Eau",
    },
    "en": {
        "fire": "Fire",
        "earth": "Earth",
        "air": "Air",
        "water": "Water",
    }
}


MODALITY_LABELS = {
    "fr": {
        "cardinal": "Cardinal",
        "fixed": "Fixe",
        "mutable": "Mutable",
    },
    "en": {
        "cardinal": "Cardinal",
        "fixed": "Fixed",
        "mutable": "Mutable",
    }
}


PROFILE_SECTIONS = {
    "fr": (
        "identity",
        "personality",
        "emotional_world",
        "communication",
        "love",
        "relationship_needs",
        "motivation",
        "work",
        "ambition",
        "finances",
        "strengths",
        "watchpoints",
        "balance",
        "growth",
        "summary",
    ),
    "en": (
        "identity",
        "personality",
        "emotional_world",
        "communication",
        "love",
        "relationship_needs",
        "motivation",
        "work",
        "ambition",
        "finances",
        "strengths",
        "watchpoints",
        "balance",
        "growth",
        "summary",
    ),
}


SECTION_TITLES = {
    "fr": {
        "identity": "🌌 Ton identité astrologique",
        "personality": "☀️ Ta personnalité profonde",
        "emotional_world": "🌙 Ton monde émotionnel",
        "communication": "🗣️ Ta manière de communiquer",
        "love": "❤️ Ta manière d'aimer",
        "relationship_needs": "💞 Tes besoins relationnels",
        "motivation": "🔥 Tes moteurs intérieurs",
        "work": "💼 Travail et talents",
        "ambition": "🚀 Tes ambitions",
        "finances": "💰 Ton rapport aux finances",
        "strengths": "💪 Tes forces naturelles",
        "watchpoints": "⚠️ Tes points de vigilance",
        "balance": "☯️ Ton équilibre personnel",
        "growth": "✨ Ton potentiel d'évolution",
        "summary": "🌟 Synthèse AstroVibe",
    },
    "en": {
        "identity": "🌌 Your astrological identity",
        "personality": "☀️ Your deeper personality",
        "emotional_world": "🌙 Your emotional world",
        "communication": "🗣️ Your communication style",
        "love": "❤️ Your way of loving",
        "relationship_needs": "💞 Your relationship needs",
        "motivation": "🔥 Your inner motivation",
        "work": "💼 Work and talents",
        "ambition": "🚀 Your ambitions",
        "finances": "💰 Your relationship with money",
        "strengths": "💪 Your natural strengths",
        "watchpoints": "⚠️ Your watchpoints",
        "balance": "☯️ Your personal balance",
        "growth": "✨ Your growth potential",
        "summary": "🌟 AstroVibe summary",
    }
}


def normalize_sign(sign):
    if not sign:
        return None

    if sign in SIGN_ALIASES:
        return SIGN_ALIASES[sign]

    normalized = str(sign).strip().lower()

    english_aliases = {
        "aries": "aries",
        "taurus": "taurus",
        "gemini": "gemini",
        "cancer": "cancer",
        "leo": "leo",
        "virgo": "virgo",
        "libra": "libra",
        "scorpio": "scorpio",
        "sagittarius": "sagittarius",
        "capricorn": "capricorn",
        "aquarius": "aquarius",
        "pisces": "pisces",
    }

    return english_aliases.get(normalized)


def get_sign_name(sign_key, language="fr"):
    language = language if language in ("fr", "en") else "fr"

    return SIGN_NAMES.get(
        language,
        SIGN_NAMES["fr"]
    ).get(sign_key, sign_key)


def get_sign_meta(sign_key, language="fr"):
    language = language if language in ("fr", "en") else "fr"

    meta = SIGN_META.get(sign_key)

    if not meta:
        return None

    return {
        "element": meta["element"],
        "element_label": ELEMENT_LABELS[language][
            meta["element"]
        ],
        "modality": meta["modality"],
        "modality_label": MODALITY_LABELS[language][
            meta["modality"]
        ],
    }


def build_profile_context(
    sign,
    language="fr",
    birth_date=None,
    birth_time=None,
    birth_time_known=None,
    birth_place=None,
):
    language = language if language in ("fr", "en") else "fr"

    sign_key = normalize_sign(sign)

    if not sign_key:
        raise ValueError(
            "Unsupported zodiac sign"
        )

    return {
        "language": language,
        "sign_key": sign_key,
        "sign_name": get_sign_name(
            sign_key,
            language
        ),
        "sign_meta": get_sign_meta(
            sign_key,
            language
        ),
        "birth_date": birth_date,
        "birth_time": birth_time,
        "birth_time_known": birth_time_known,
        "birth_place": birth_place,
    }
# ============================================
# CONTENU FRANÇAIS DU PROFIL PERSONNEL
# BLOC 1/2 : BÉLIER À VIERGE
# ============================================


SIGN_PROFILES_FR = {
    "aries": {
        "identity": (
            "Ton énergie de Bélier repose sur l'élan, l'initiative et "
            "le besoin d'avancer. Tu te construis en relevant des défis "
            "et en ouvrant des voies que d'autres n'osent pas encore explorer."
        ),
        "personality": (
            "Tu possèdes une personnalité directe, volontaire et spontanée. "
            "Lorsque quelque chose t'inspire, tu préfères agir immédiatement "
            "plutôt que rester longtemps dans l'observation ou l'hésitation."
        ),
        "emotional_world": (
            "Tes émotions peuvent apparaître rapidement et avec intensité, "
            "mais elles ont rarement vocation à s'installer durablement. "
            "Tu retrouves ton équilibre lorsque tu peux exprimer franchement "
            "ce que tu ressens puis reprendre ton mouvement."
        ),
        "communication": (
            "Tu communiques avec franchise et efficacité. Ton discours gagne "
            "en impact lorsque ta sincérité reste accompagnée d'écoute, car "
            "ton rythme naturel peut parfois devancer celui de tes interlocuteurs."
        ),
        "love": (
            "En amour, tu recherches de la vitalité, de la présence et une "
            "relation qui continue à te stimuler. Tu apprécies la séduction "
            "vivante, les gestes spontanés et la sensation d'avancer à deux."
        ),
        "relationship_needs": (
            "Tu as besoin d'un lien qui respecte ton autonomie sans créer de "
            "distance émotionnelle. Une relation saine pour toi combine "
            "franchise, désir, liberté d'action et capacité à résoudre les "
            "tensions sans jeux indirects."
        ),
        "motivation": (
            "Tu es motivé par les commencements, les défis et les situations "
            "qui te permettent de mesurer ton courage. Ton énergie augmente "
            "lorsqu'un objectif est clair, concret et suffisamment stimulant."
        ),
        "work": (
            "Dans le travail, tu peux exceller dans les environnements où "
            "l'initiative, la réactivité et la prise de décision sont valorisées. "
            "Tu apportes volontiers l'impulsion qui transforme une idée en action."
        ),
        "ambition": (
            "Ton ambition se nourrit du besoin de progresser et de prouver que "
            "tu peux dépasser les obstacles. Pour durer, elle gagne à être "
            "soutenue par une stratégie plutôt que par le seul enthousiasme initial."
        ),
        "finances": (
            "Ton rapport à l'argent peut être instinctif et orienté vers l'action. "
            "Tu peux investir rapidement dans ce qui t'enthousiasme ; une règle "
            "simple de recul avant les dépenses importantes renforce ta sécurité."
        ),
        "strengths": (
            "Courage, spontanéité, capacité d'initiative, honnêteté et faculté "
            "à rebondir constituent tes principales forces. Tu sais remettre "
            "du mouvement là où une situation semblait bloquée."
        ),
        "watchpoints": (
            "L'impatience, la précipitation et la difficulté à supporter les "
            "rythmes plus lents peuvent parfois disperser ton énergie. Tout "
            "n'a pas besoin d'être gagné immédiatement pour avoir de la valeur."
        ),
        "balance": (
            "Ton équilibre passe par une alternance entre action intense et "
            "récupération réelle. Le mouvement physique, les objectifs courts "
            "et les espaces où tu peux décider librement t'aident à te recentrer."
        ),
        "growth": (
            "Ton potentiel grandit lorsque tu transformes l'impulsion en "
            "persévérance. Apprendre à écouter sans perdre ton courage te permet "
            "de devenir une force motrice aussi solide qu'inspirante."
        ),
    },

    "taurus": {
        "identity": (
            "Ton énergie de Taureau s'organise autour de la stabilité, des valeurs "
            "concrètes et du besoin de construire quelque chose qui résiste au temps."
        ),
        "personality": (
            "Tu avances généralement avec calme, constance et réalisme. Tu préfères "
            "comprendre ce qui est fiable avant de t'engager, puis tu peux faire "
            "preuve d'une remarquable endurance lorsque ta décision est prise."
        ),
        "emotional_world": (
            "Ton monde émotionnel recherche la sécurité, la continuité et des "
            "repères tangibles. Les gestes réguliers et la présence comptent "
            "souvent davantage pour toi que les grandes déclarations passagères."
        ),
        "communication": (
            "Tu t'exprimes de façon posée et réfléchie. Tu accordes de l'importance "
            "à la cohérence entre les paroles et les actes, et tu peux avoir besoin "
            "de temps avant d'accepter une opinion qui bouleverse tes repères."
        ),
        "love": (
            "En amour, tu recherches la fidélité, la sensualité et une confiance "
            "qui se construit progressivement. Tu aimes créer un lien rassurant "
            "où l'affection se manifeste dans la vie quotidienne."
        ),
        "relationship_needs": (
            "Tu as besoin de stabilité sans immobilité, de proximité sans pression "
            "et d'un partenaire dont les engagements sont lisibles. La douceur, "
            "la loyauté et la patience nourrissent profondément ton attachement."
        ),
        "motivation": (
            "Tu es motivé par les résultats durables, le confort gagné et la "
            "possibilité de voir concrètement le fruit de tes efforts."
        ),
        "work": (
            "Au travail, ta patience, ton sens pratique et ta fiabilité font de toi "
            "une présence stabilisante. Tu es particulièrement efficace lorsqu'un "
            "projet demande régularité, précision et gestion des ressources."
        ),
        "ambition": (
            "Ton ambition est rarement bruyante, mais elle peut être très solide. "
            "Tu préfères une progression sûre et maîtrisée à une réussite rapide "
            "qui ne disposerait pas de fondations suffisantes."
        ),
        "finances": (
            "Tu recherches naturellement la sécurité matérielle et la valeur "
            "réelle. Tu peux bien gérer sur le long terme, à condition que le "
            "besoin de confort ne devienne pas une résistance excessive au changement."
        ),
        "strengths": (
            "Persévérance, loyauté, patience, réalisme et capacité à créer de la "
            "stabilité sont tes forces majeures. Tu sais donner une forme concrète "
            "à ce qui n'était au départ qu'une intention."
        ),
        "watchpoints": (
            "L'attachement aux habitudes peut parfois te retenir dans une situation "
            "qui ne te correspond plus. Ta détermination devient plus féconde "
            "lorsqu'elle reste capable d'évoluer."
        ),
        "balance": (
            "Ton équilibre se nourrit de rythmes réguliers, de plaisirs simples, "
            "d'un environnement apaisant et d'un rapport sain au corps."
        ),
        "growth": (
            "Ton potentiel s'élargit lorsque tu découvres que le changement ne "
            "menace pas forcément ta stabilité. Tu peux évoluer tout en conservant "
            "tes valeurs essentielles."
        ),
    },

    "gemini": {
        "identity": (
            "Ton énergie de Gémeaux repose sur la curiosité, l'échange et le besoin "
            "de relier les idées. Tu te développes en découvrant, en questionnant "
            "et en partageant ce que tu comprends."
        ),
        "personality": (
            "Tu possèdes un esprit mobile, adaptable et souvent très réactif. "
            "La diversité stimule ton intelligence et t'empêche de te sentir enfermé."
        ),
        "emotional_world": (
            "Tu cherches souvent à comprendre tes émotions en les nommant ou en "
            "les racontant. Le dialogue t'aide à prendre du recul, mais certaines "
            "émotions demandent d'être ressenties avant d'être analysées."
        ),
        "communication": (
            "La communication est l'une de tes grandes ressources. Tu sais adapter "
            "ton langage, capter rapidement une information et créer des ponts "
            "entre des personnes ou des sujets différents."
        ),
        "love": (
            "En amour, tu recherches de la complicité mentale, de l'humour et une "
            "relation qui reste vivante. Une conversation stimulante peut être "
            "aussi importante pour toi qu'une démonstration romantique."
        ),
        "relationship_needs": (
            "Tu as besoin de liberté d'expression, de renouvellement et d'un lien "
            "qui ne confonde pas engagement avec enfermement."
        ),
        "motivation": (
            "Tu es motivé par les idées nouvelles, les rencontres et la possibilité "
            "d'apprendre rapidement. Ton énergie se réveille lorsque plusieurs "
            "perspectives deviennent accessibles."
        ),
        "work": (
            "Tu peux exceller dans la communication, l'écriture, l'enseignement, "
            "le commerce ou les fonctions qui demandent souplesse et circulation "
            "de l'information."
        ),
        "ambition": (
            "Ton ambition peut emprunter plusieurs directions. Elle devient plus "
            "puissante lorsque tu sélectionnes quelques priorités capables de "
            "transformer ta polyvalence en expertise."
        ),
        "finances": (
            "Ton rapport à l'argent peut varier selon tes centres d'intérêt. "
            "Une organisation simple et automatisée t'aide à préserver ta liberté "
            "sans perdre de vue les objectifs à long terme."
        ),
        "strengths": (
            "Curiosité, intelligence relationnelle, adaptabilité, humour et rapidité "
            "d'apprentissage constituent tes principales forces."
        ),
        "watchpoints": (
            "La dispersion, l'inconstance ou la tendance à rester à la surface "
            "peuvent diluer ton potentiel. Approfondir ne signifie pas renoncer "
            "à ta diversité."
        ),
        "balance": (
            "Ton équilibre demande à la fois des échanges stimulants et des moments "
            "sans bruit mental. Écrire, marcher ou limiter les sollicitations "
            "t'aide à retrouver une direction intérieure."
        ),
        "growth": (
            "Ton évolution passe par l'union de ta curiosité et de ta constance. "
            "Lorsque tu approfondis ce qui t'anime réellement, ta parole gagne "
            "en influence et en crédibilité."
        ),
    },

    "cancer": {
        "identity": (
            "Ton énergie de Cancer s'organise autour de la sensibilité, de la "
            "protection et du besoin d'appartenance. Tu te construis en créant "
            "des liens et des espaces où la confiance peut grandir."
        ),
        "personality": (
            "Tu perçois volontiers les atmosphères et les besoins implicites. "
            "Derrière une apparente réserve peut se trouver une grande force "
            "de fidélité, d'imagination et de résistance émotionnelle."
        ),
        "emotional_world": (
            "Ton monde intérieur est riche et profondément lié à la mémoire. "
            "Tu peux ressentir longtemps ce qui t'a touché, même lorsque tu n'en "
            "parles pas immédiatement."
        ),
        "communication": (
            "Tu communiques mieux lorsque le climat est sûr. Ton intuition te "
            "permet de comprendre ce qui n'est pas dit, mais exprimer directement "
            "tes besoins évite que les autres aient à les deviner."
        ),
        "love": (
            "En amour, tu recherches un attachement sincère, protecteur et intime. "
            "Tu offres beaucoup lorsque tu te sens en confiance et tu apprécies "
            "les liens capables de devenir un véritable refuge émotionnel."
        ),
        "relationship_needs": (
            "Tu as besoin de sécurité affective, de continuité et de délicatesse. "
            "Une relation saine respecte ta sensibilité sans t'enfermer dans un "
            "rôle où tu devrais prendre soin de tout le monde."
        ),
        "motivation": (
            "Tu es motivé par le besoin de protéger, de transmettre et de donner "
            "du sens humain à ce que tu construis."
        ),
        "work": (
            "Ta compréhension des besoins, ton intuition et ta persévérance peuvent "
            "être précieuses dans les métiers d'accompagnement, de création, "
            "d'accueil ou de gestion d'une communauté."
        ),
        "ambition": (
            "Ton ambition se renforce lorsqu'elle est liée à une cause ou à un "
            "sentiment d'utilité. Tu peux avancer avec détermination dès lors "
            "que ton engagement possède une valeur personnelle."
        ),
        "finances": (
            "La sécurité financière représente souvent une forme de protection. "
            "Tu peux privilégier l'épargne et les choix prudents, tout en veillant "
            "à ne pas laisser l'inquiétude décider à ta place."
        ),
        "strengths": (
            "Intuition, empathie, fidélité, imagination et capacité à protéger "
            "constituent tes forces naturelles."
        ),
        "watchpoints": (
            "La susceptibilité, le repli ou l'attachement au passé peuvent parfois "
            "te retenir. Une émotion mérite d'être entendue sans forcément devenir "
            "une définition permanente de la situation."
        ),
        "balance": (
            "Ton équilibre repose sur un espace intime rassurant, des liens fiables "
            "et des moments où tu peux accueillir tes émotions sans les subir."
        ),
        "growth": (
            "Ton potentiel s'exprime pleinement lorsque ta sensibilité devient "
            "une boussole plutôt qu'une protection. Poser des limites te permet "
            "de continuer à donner sans t'épuiser."
        ),
    },

    "leo": {
        "identity": (
            "Ton énergie de Lion repose sur la créativité, la présence et le besoin "
            "d'exprimer quelque chose d'unique. Tu te réalises lorsque tu peux "
            "mettre du cœur dans ce que tu fais."
        ),
        "personality": (
            "Tu possèdes une nature expressive, chaleureuse et généreuse. Tu peux "
            "rassembler les autres par ton enthousiasme et ta capacité à donner "
            "une dimension vivante aux projets."
        ),
        "emotional_world": (
            "Tes émotions sont liées au besoin d'être reconnu sincèrement. "
            "Tu peux paraître fort tout en étant sensible à l'indifférence ou "
            "au manque de considération."
        ),
        "communication": (
            "Tu communiques avec présence et conviction. Ton influence devient "
            "encore plus forte lorsque tu mets ton assurance au service d'un "
            "message plutôt qu'au service de ton image."
        ),
        "love": (
            "En amour, tu recherches chaleur, loyauté, admiration réciproque et "
            "expression des sentiments. Tu aimes sentir que le lien possède "
            "une place importante et clairement assumée."
        ),
        "relationship_needs": (
            "Tu as besoin d'affection visible, de fidélité et d'un partenaire "
            "capable de célébrer ta lumière sans oublier la sienne."
        ),
        "motivation": (
            "Tu es motivé par la création, la reconnaissance et la possibilité "
            "d'inspirer. Tu donnes le meilleur de toi lorsque ton implication "
            "peut laisser une empreinte personnelle."
        ),
        "work": (
            "Tu peux exceller dans les fonctions qui demandent leadership, "
            "créativité, représentation ou capacité à fédérer."
        ),
        "ambition": (
            "Ton ambition vise souvent une réalisation dont tu peux être fier. "
            "Elle devient durable lorsque la reconnaissance extérieure confirme "
            "un accomplissement réellement aligné avec tes valeurs."
        ),
        "finances": (
            "Tu peux voir l'argent comme un moyen de vivre pleinement, de créer "
            "ou de partager. Préserver une marge de sécurité t'évite que la "
            "générosité ou le goût du beau ne dépasse tes ressources."
        ),
        "strengths": (
            "Créativité, courage, loyauté, générosité et capacité à inspirer "
            "constituent tes forces essentielles."
        ),
        "watchpoints": (
            "La fierté peut parfois rendre difficile l'aveu d'une fragilité. "
            "Tu ne perds rien de ta dignité lorsque tu acceptes de ne pas tout "
            "maîtriser ou de ne pas toujours occuper le premier plan."
        ),
        "balance": (
            "Ton équilibre demande une expression créative, des relations sincères "
            "et des espaces où tu peux rayonner sans devoir constamment prouver "
            "ta valeur."
        ),
        "growth": (
            "Ton potentiel grandit lorsque ton besoin de reconnaissance devient "
            "une capacité à reconnaître aussi les autres. Ton leadership gagne "
            "alors en profondeur et en confiance."
        ),
    },

    "virgo": {
        "identity": (
            "Ton énergie de Vierge repose sur l'observation, l'amélioration et le "
            "besoin de rendre les choses plus utiles, plus claires et plus justes."
        ),
        "personality": (
            "Tu possèdes un esprit analytique, consciencieux et attentif aux détails. "
            "Tu te sens à ta place lorsque tes compétences produisent un résultat "
            "concret et fiable."
        ),
        "emotional_world": (
            "Tu peux chercher à organiser ce que tu ressens avant de l'exprimer. "
            "Cette retenue protège ton intimité, mais elle peut aussi transformer "
            "une émotion simple en réflexion prolongée."
        ),
        "communication": (
            "Tu t'exprimes avec précision et discernement. Tu repères facilement "
            "les incohérences et les pistes d'amélioration, tout en gagnant à "
            "différencier une critique utile d'une exigence excessive."
        ),
        "love": (
            "En amour, tu manifestes souvent ton attachement par l'attention, "
            "la fiabilité et les gestes qui facilitent réellement la vie de l'autre."
        ),
        "relationship_needs": (
            "Tu as besoin d'une relation claire, respectueuse et cohérente. "
            "La confiance grandit lorsque les paroles sont suivies d'actes et "
            "que chacun prend sa part de responsabilité."
        ),
        "motivation": (
            "Tu es motivé par l'utilité, la maîtrise et le sentiment de progresser. "
            "Résoudre un problème ou améliorer un système peut fortement stimuler "
            "ton énergie."
        ),
        "work": (
            "Ta méthode, ton sens du détail et ta capacité d'analyse sont précieux "
            "dans les rôles demandant organisation, expertise, service ou contrôle "
            "de la qualité."
        ),
        "ambition": (
            "Ton ambition vise souvent la compétence plus que le prestige. "
            "Tu veux être légitime par la qualité de ton travail, mais tu dois "
            "parfois reconnaître tes progrès avant que tout soit parfait."
        ),
        "finances": (
            "Tu peux gérer l'argent avec prudence et méthode. Les outils de suivi "
            "te conviennent, à condition que la recherche de contrôle ne transforme "
            "pas chaque dépense en source d'inquiétude."
        ),
        "strengths": (
            "Précision, fiabilité, sens du service, intelligence pratique et "
            "capacité d'amélioration constituent tes forces naturelles."
        ),
        "watchpoints": (
            "Le perfectionnisme, l'autocritique et l'analyse excessive peuvent "
            "te faire oublier la valeur de ce qui fonctionne déjà."
        ),
        "balance": (
            "Ton équilibre repose sur des routines souples, un environnement clair "
            "et la possibilité de te sentir utile sans porter toutes les responsabilités."
        ),
        "growth": (
            "Ton potentiel se déploie lorsque tu remplaces l'exigence de perfection "
            "par une recherche d'excellence vivante. Accepter l'imperfection te "
            "rend plus libre sans diminuer ta qualité."
        ),
    },
}
# ============================================
# CONTENU FRANÇAIS DU PROFIL PERSONNEL
# BLOC 2/2 : BALANCE À POISSONS
# ============================================


SIGN_PROFILES_FR.update({
    "libra": {
        "identity": (
            "Ton énergie de Balance s'organise autour de l'harmonie, "
            "de la relation et de la recherche d'un équilibre juste. "
            "Tu te construis en confrontant tes idées à celles des autres "
            "et en cherchant des solutions capables de réunir."
        ),
        "personality": (
            "Tu possèdes une personnalité sociable, diplomate et attentive "
            "aux nuances. Tu comprends facilement plusieurs points de vue "
            "et tu préfères généralement créer un terrain d'entente plutôt "
            "que provoquer une opposition inutile."
        ),
        "emotional_world": (
            "Ton équilibre émotionnel dépend beaucoup de la qualité de tes "
            "relations et de l'atmosphère qui t'entoure. Les conflits non "
            "résolus peuvent te peser, même lorsque tu conserves une apparence "
            "calme et maîtrisée."
        ),
        "communication": (
            "Tu communiques avec tact, élégance et sens de la mesure. "
            "Tu sais présenter une idée sans brusquer, mais ta parole gagne "
            "en force lorsque tu exprimes clairement ta position au lieu "
            "de chercher systématiquement la formulation parfaite."
        ),
        "love": (
            "En amour, tu recherches la complicité, le respect et une relation "
            "où chacun considère réellement l'autre. Tu accordes de l'importance "
            "aux attentions, au dialogue et à la sensation de former une équipe."
        ),
        "relationship_needs": (
            "Tu as besoin d'échanges équilibrés, d'affection et d'un partenaire "
            "capable de prendre des décisions avec toi. Une relation saine "
            "t'autorise à préserver l'harmonie sans renoncer à tes propres besoins."
        ),
        "motivation": (
            "Tu es motivé par la beauté, la coopération et les projets capables "
            "d'améliorer un environnement ou une relation. Tu donnes beaucoup "
            "lorsque tu crois à la qualité humaine de ce que tu construis."
        ),
        "work": (
            "Au travail, ton sens de la diplomatie, de la présentation et de "
            "la négociation peut être précieux. Tu peux exceller dans les rôles "
            "où il faut coordonner, conseiller, représenter ou créer de l'harmonie."
        ),
        "ambition": (
            "Ton ambition cherche souvent à conjuguer réussite personnelle "
            "et reconnaissance sociale. Elle devient plus solide lorsque tu "
            "choisis une direction sans attendre l'approbation unanime."
        ),
        "finances": (
            "Tu peux être sensible à la qualité, à l'esthétique et au plaisir "
            "de partager. Un cadre budgétaire simple t'aide à profiter de ces "
            "valeurs sans laisser les dépenses relationnelles ou impulsives "
            "déséquilibrer tes objectifs."
        ),
        "strengths": (
            "Diplomatie, charme, sens de la justice, intelligence relationnelle "
            "et capacité à rapprocher les points de vue constituent tes forces."
        ),
        "watchpoints": (
            "L'indécision, l'évitement du conflit ou la tendance à trop tenir "
            "compte du regard extérieur peuvent t'éloigner de ce que tu veux "
            "réellement."
        ),
        "balance": (
            "Ton équilibre passe par des relations réciproques, un environnement "
            "harmonieux et des moments où tu peux retrouver ton propre avis "
            "sans être influencé par les attentes environnantes."
        ),
        "growth": (
            "Ton potentiel s'affirme lorsque ta recherche d'harmonie inclut "
            "ta propre vérité. Dire non, choisir et assumer une préférence "
            "peuvent devenir de puissants actes d'équilibre."
        ),
    },

    "scorpio": {
        "identity": (
            "Ton énergie de Scorpion repose sur la profondeur, l'intensité "
            "et la transformation. Tu ne te satisfais pas facilement des "
            "apparences et tu cherches instinctivement ce qui se joue derrière elles."
        ),
        "personality": (
            "Tu possèdes une personnalité déterminée, intuitive et souvent "
            "magnétique. Tu observes attentivement avant d'accorder ta confiance, "
            "mais ton engagement peut devenir très puissant lorsqu'il est sincère."
        ),
        "emotional_world": (
            "Ton monde émotionnel est profond et complexe. Tu peux ressentir "
            "avec force sans toujours montrer immédiatement ce qui te traverse. "
            "La confiance est essentielle pour que tu dévoiles ta vulnérabilité."
        ),
        "communication": (
            "Tu communiques avec intensité et discernement. Tu sais détecter "
            "les incohérences et les non-dits, mais ton intuition devient plus "
            "fiable lorsqu'elle reste ouverte à la vérification et au dialogue."
        ),
        "love": (
            "En amour, tu recherches une connexion authentique, loyale et "
            "transformatrice. Les relations superficielles t'intéressent peu : "
            "tu veux pouvoir connaître l'autre en profondeur et être connu avec "
            "la même sincérité."
        ),
        "relationship_needs": (
            "Tu as besoin de confiance, d'exclusivité émotionnelle et de vérité. "
            "Une relation saine respecte ton intensité tout en préservant "
            "l'autonomie et l'espace personnel de chacun."
        ),
        "motivation": (
            "Tu es motivé par les défis profonds, les situations complexes "
            "et la possibilité de transformer une faiblesse en force."
        ),
        "work": (
            "Au travail, tu peux exceller dans la recherche, l'analyse, la stratégie, "
            "la psychologie ou les contextes qui demandent confidentialité, "
            "résistance et compréhension des enjeux cachés."
        ),
        "ambition": (
            "Ton ambition est souvent discrète mais extrêmement déterminée. "
            "Lorsque tu choisis un objectif, tu peux mobiliser d'importantes "
            "ressources intérieures pour traverser les obstacles."
        ),
        "finances": (
            "Tu peux entretenir un rapport stratégique à l'argent et chercher "
            "à comprendre les rapports de pouvoir qui l'accompagnent. La clarté "
            "et la transparence sont essentielles dans les ressources partagées."
        ),
        "strengths": (
            "Lucidité, courage émotionnel, détermination, intuition et capacité "
            "de transformation constituent tes forces majeures."
        ),
        "watchpoints": (
            "La méfiance, la volonté de contrôle ou la difficulté à lâcher une "
            "blessure peuvent prolonger des tensions qui demanderaient plutôt "
            "à être exprimées puis dépassées."
        ),
        "balance": (
            "Ton équilibre repose sur des relations fiables, des espaces de "
            "confidentialité et des activités qui transforment ton intensité "
            "en création, compréhension ou action constructive."
        ),
        "growth": (
            "Ton potentiel grandit lorsque tu découvres que la confiance n'est "
            "pas une perte de pouvoir. Partager progressivement ta vulnérabilité "
            "peut approfondir tes liens sans diminuer ta force."
        ),
    },

    "sagittarius": {
        "identity": (
            "Ton énergie de Sagittaire repose sur l'exploration, le sens et "
            "l'élargissement des horizons. Tu te construis en découvrant ce qui "
            "existe au-delà de tes habitudes et de tes certitudes."
        ),
        "personality": (
            "Tu possèdes une personnalité enthousiaste, indépendante et tournée "
            "vers les possibilités. Ton optimisme t'aide à rebondir et à remettre "
            "du mouvement là où une situation semble limitée."
        ),
        "emotional_world": (
            "Tu supportes difficilement de te sentir enfermé dans une émotion. "
            "Tu cherches souvent à retrouver rapidement de l'espoir ou une "
            "perspective plus vaste, mais certaines expériences demandent du "
            "temps avant de révéler leur sens."
        ),
        "communication": (
            "Tu communiques avec franchise, humour et conviction. Tu sais transmettre "
            "une vision, mais ta parole gagne en justesse lorsque la spontanéité "
            "reste attentive à la sensibilité des autres."
        ),
        "love": (
            "En amour, tu recherches la sincérité, l'aventure et une relation "
            "qui continue à évoluer. Tu apprécies un partenaire capable de partager "
            "des expériences tout en respectant ton besoin d'espace."
        ),
        "relationship_needs": (
            "Tu as besoin de confiance, de liberté et d'une direction commune. "
            "La relation doit pouvoir grandir sans devenir une succession "
            "d'obligations ou de contrôles."
        ),
        "motivation": (
            "Tu es motivé par les voyages, l'apprentissage, les grandes idées "
            "et les défis qui donnent une impression d'expansion."
        ),
        "work": (
            "Tu peux exceller dans l'enseignement, la communication, le conseil, "
            "l'international ou les fonctions qui demandent vision et capacité "
            "à inspirer."
        ),
        "ambition": (
            "Ton ambition vise souvent un objectif vaste et porteur de sens. "
            "Pour devenir durable, elle gagne à être accompagnée d'étapes concrètes "
            "et d'une discipline régulière."
        ),
        "finances": (
            "Tu peux considérer l'argent comme un moyen d'explorer et de vivre "
            "des expériences. Une réserve structurée t'aide à préserver cette "
            "liberté sans dépendre constamment de circonstances favorables."
        ),
        "strengths": (
            "Optimisme, franchise, vision, générosité et capacité à transmettre "
            "un enthousiasme constituent tes principales forces."
        ),
        "watchpoints": (
            "L'impatience, l'excès de confiance ou la tendance à promettre plus "
            "que tu ne peux accomplir peuvent fragiliser tes projets."
        ),
        "balance": (
            "Ton équilibre exige de l'espace, du mouvement et une direction "
            "qui nourrit ton besoin de sens, mais également quelques repères "
            "stables auxquels revenir."
        ),
        "growth": (
            "Ton potentiel se déploie lorsque tu associes ta vision à une méthode. "
            "La liberté devient alors une capacité à choisir consciemment plutôt "
            "qu'un besoin permanent d'échapper aux limites."
        ),
    },

    "capricorn": {
        "identity": (
            "Ton énergie de Capricorne repose sur la responsabilité, la maîtrise "
            "et la construction à long terme. Tu te réalises en développant une "
            "compétence solide et en gagnant progressivement ta légitimité."
        ),
        "personality": (
            "Tu possèdes une personnalité sérieuse, persévérante et pragmatique. "
            "Tu observes les contraintes avec réalisme et tu peux avancer longtemps "
            "là où d'autres abandonnent faute de résultats immédiats."
        ),
        "emotional_world": (
            "Tu peux garder tes émotions sous contrôle afin de rester efficace "
            "et digne de confiance. Derrière cette maîtrise existe pourtant un "
            "besoin profond de sécurité, de respect et de reconnaissance sincère."
        ),
        "communication": (
            "Tu communiques avec sobriété, structure et sens des responsabilités. "
            "Tu préfères les paroles utiles aux déclarations excessives et tu "
            "accordes beaucoup de valeur à la fiabilité."
        ),
        "love": (
            "En amour, tu recherches un lien stable, loyal et construit avec sérieux. "
            "Tu peux exprimer ton affection par tes engagements, ta présence et "
            "ta volonté de protéger le futur de la relation."
        ),
        "relationship_needs": (
            "Tu as besoin d'une relation mature, fiable et respectueuse de tes "
            "objectifs. La confiance se construit lorsque chacun assume ses choix "
            "et tient ses engagements."
        ),
        "motivation": (
            "Tu es motivé par la progression, la maîtrise et la possibilité de "
            "bâtir quelque chose dont la valeur sera reconnue dans le temps."
        ),
        "work": (
            "Au travail, ton organisation, ta patience et ton sens stratégique "
            "peuvent te conduire vers des responsabilités importantes. Tu sais "
            "transformer une ambition en plan réaliste."
        ),
        "ambition": (
            "L'ambition est souvent une composante centrale de ton évolution. "
            "Tu recherches moins l'effet immédiat que la solidité d'une réussite "
            "acquise par l'expérience et la constance."
        ),
        "finances": (
            "Tu peux gérer l'argent avec prudence et vision à long terme. "
            "La sécurité matérielle représente pour toi une forme d'autonomie, "
            "mais elle ne doit pas devenir l'unique mesure de ta réussite."
        ),
        "strengths": (
            "Discipline, persévérance, intégrité, réalisme et sens stratégique "
            "constituent tes forces naturelles."
        ),
        "watchpoints": (
            "L'exigence, le pessimisme ou la tendance à porter seul trop de "
            "responsabilités peuvent te faire perdre le contact avec tes besoins "
            "plus spontanés."
        ),
        "balance": (
            "Ton équilibre passe par des objectifs structurés, mais aussi par "
            "des périodes où ta valeur ne dépend ni de ta productivité ni de "
            "ta capacité à tout contrôler."
        ),
        "growth": (
            "Ton potentiel grandit lorsque tu autorises davantage de souplesse, "
            "de confiance et de plaisir dans ton parcours. La solidité ne demande "
            "pas de renoncer à la sensibilité."
        ),
    },

    "aquarius": {
        "identity": (
            "Ton énergie de Verseau repose sur l'indépendance, l'originalité "
            "et la capacité à imaginer d'autres manières de fonctionner. "
            "Tu te construis en refusant les cadres qui ne possèdent plus de sens."
        ),
        "personality": (
            "Tu possèdes une personnalité inventive, autonome et souvent tournée "
            "vers l'avenir. Tu apprécies les idées nouvelles et les personnes "
            "capables de respecter les différences."
        ),
        "emotional_world": (
            "Tu peux prendre de la distance pour comprendre ce que tu ressens. "
            "Cette capacité t'apporte de la lucidité, mais elle ne doit pas "
            "transformer l'émotion en simple question intellectuelle."
        ),
        "communication": (
            "Tu communiques de façon originale, rationnelle et libre. Tu sais "
            "remettre en question les évidences et proposer des perspectives "
            "que d'autres n'avaient pas envisagées."
        ),
        "love": (
            "En amour, tu recherches une relation fondée sur l'amitié, la liberté "
            "et la complicité intellectuelle. Tu as besoin d'être aimé sans être "
            "enfermé dans une identité ou un rôle fixe."
        ),
        "relationship_needs": (
            "Tu as besoin d'espace personnel, de confiance et d'un partenaire "
            "capable d'accepter ton indépendance sans interpréter chaque distance "
            "comme un manque d'attachement."
        ),
        "motivation": (
            "Tu es motivé par l'innovation, les projets collectifs et les idées "
            "capables de rendre un système plus intelligent ou plus libre."
        ),
        "work": (
            "Tu peux exceller dans la technologie, la recherche, la communication, "
            "les projets sociaux ou les environnements qui valorisent l'innovation "
            "et la pensée indépendante."
        ),
        "ambition": (
            "Ton ambition vise souvent à faire évoluer les règles plutôt qu'à "
            "simplement y réussir. Tu veux apporter une différence réelle et "
            "préserver ta liberté de pensée."
        ),
        "finances": (
            "Ton rapport à l'argent peut être détaché des conventions traditionnelles. "
            "Tu peux privilégier l'autonomie et les projets innovants, tout en "
            "ayant intérêt à conserver une base financière stable."
        ),
        "strengths": (
            "Originalité, indépendance, vision collective, ouverture d'esprit "
            "et capacité d'innovation constituent tes forces essentielles."
        ),
        "watchpoints": (
            "Le détachement, l'opposition systématique ou la difficulté à exprimer "
            "tes besoins affectifs peuvent créer une distance que tu ne souhaitais "
            "pas forcément."
        ),
        "balance": (
            "Ton équilibre nécessite une liberté réelle, des échanges stimulants "
            "et un cercle où ton originalité n'a pas besoin d'être justifiée."
        ),
        "growth": (
            "Ton potentiel s'affirme lorsque ta vision du collectif reste reliée "
            "à la réalité émotionnelle des individus. L'implication personnelle "
            "donne plus de portée à tes idées."
        ),
    },

    "pisces": {
        "identity": (
            "Ton énergie de Poissons repose sur la sensibilité, l'imagination "
            "et la capacité à percevoir ce qui échappe aux cadres habituels. "
            "Tu te construis en donnant une forme personnelle à ton intuition."
        ),
        "personality": (
            "Tu possèdes une personnalité réceptive, empathique et créative. "
            "Tu peux facilement comprendre plusieurs réalités à la fois et ressentir "
            "les ambiances avant même qu'elles soient exprimées."
        ),
        "emotional_world": (
            "Ton monde émotionnel est vaste, subtil et parfois difficile à délimiter. "
            "Tu peux absorber l'atmosphère environnante et avoir besoin de solitude "
            "pour distinguer ce que tu ressens réellement."
        ),
        "communication": (
            "Tu communiques volontiers par l'intuition, les images ou la sensibilité. "
            "Ta parole devient plus claire lorsque tu prends le temps de transformer "
            "tes impressions en besoins et en faits précis."
        ),
        "love": (
            "En amour, tu recherches une connexion profonde, tendre et inspirante. "
            "Tu peux beaucoup donner et idéaliser le lien, ce qui rend nécessaires "
            "des limites protectrices et une réciprocité réelle."
        ),
        "relationship_needs": (
            "Tu as besoin de douceur, d'empathie et d'un espace où ta sensibilité "
            "est accueillie sans être exploitée. Une relation équilibrée respecte "
            "tes rêves tout en restant ancrée dans des actes concrets."
        ),
        "motivation": (
            "Tu es motivé par l'inspiration, la création et la sensation de contribuer "
            "à quelque chose qui dépasse les intérêts purement matériels."
        ),
        "work": (
            "Tu peux exceller dans la création, l'accompagnement, l'imaginaire, "
            "le soin ou les projets qui demandent intuition et compréhension humaine."
        ),
        "ambition": (
            "Ton ambition est souvent liée au sens et à l'inspiration. Elle devient "
            "plus réalisable lorsque tes intuitions sont traduites en étapes claires "
            "et en engagements réguliers."
        ),
        "finances": (
            "Ton rapport à l'argent peut être influencé par l'émotion ou la générosité. "
            "Quelques règles concrètes et automatisées protègent tes ressources "
            "sans étouffer ton désir de partager."
        ),
        "strengths": (
            "Empathie, intuition, imagination, compassion et capacité créative "
            "constituent tes principales forces."
        ),
        "watchpoints": (
            "L'idéalisation, l'évitement ou la difficulté à poser des limites "
            "peuvent t'exposer à des déceptions ou à une fatigue émotionnelle."
        ),
        "balance": (
            "Ton équilibre passe par la création, le repos, des limites saines "
            "et des espaces où tu peux retrouver ton propre rythme intérieur."
        ),
        "growth": (
            "Ton potentiel se révèle lorsque ton intuition rencontre une structure. "
            "En donnant une forme concrète à ta sensibilité, tu peux transformer "
            "tes perceptions en véritable force de création et d'accompagnement."
        ),
    },
})


def build_identity_text(context):
    sign_name = context["sign_name"]
    element_label = context["sign_meta"]["element_label"]
    modality_label = context["sign_meta"]["modality_label"]
    language = context["language"]

    if language == "en":
        return (
            f"Your main zodiac sign is {sign_name}. "
            f"It belongs to the {element_label} element and "
            f"the {modality_label} modality."
        )

    return (
        f"Ton signe astrologique principal est {sign_name}. "
        f"Il appartient à l'élément {element_label} et "
        f"à la modalité {modality_label}."
    )


def build_birth_context_text(context):
    birth_date = context.get("birth_date")
    birth_time = context.get("birth_time")
    birth_time_known = context.get("birth_time_known")
    birth_place = context.get("birth_place")
    language = context["language"]

    if birth_date:
        if hasattr(birth_date, "strftime"):
            birth_date_text = birth_date.strftime("%d/%m/%Y")
        else:
            birth_date_text = str(birth_date)
    else:
        birth_date_text = None

    if birth_time_known and birth_time:
        if hasattr(birth_time, "strftime"):
            birth_time_text = birth_time.strftime("%H:%M")
        else:
            birth_time_text = str(birth_time)
    else:
        birth_time_text = None

    if language == "en":
        details = []

        if birth_date_text:
            details.append(f"📅 Birth date: {birth_date_text}")

        if birth_time_text:
            details.append(f"🕐 Birth time: {birth_time_text}")
        elif birth_time_known is False:
            details.append("🕐 Birth time: Unknown")

        if birth_place:
            details.append(f"📍 Birth place: {birth_place}")

        return "\n".join(details)

    details = []

    if birth_date_text:
        details.append(f"📅 Date de naissance : {birth_date_text}")

    if birth_time_text:
        details.append(f"🕐 Heure de naissance : {birth_time_text}")
    elif birth_time_known is False:
        details.append("🕐 Heure de naissance : Inconnue")

    if birth_place:
        details.append(f"📍 Lieu de naissance : {birth_place}")

    return "\n".join(details)


def build_french_summary(context, profile):
    sign_name = context["sign_name"]
    element_label = context["sign_meta"]["element_label"]
    modality_label = context["sign_meta"]["modality_label"]

    return (
        f"Ton profil de {sign_name} associe l'énergie de l'élément "
        f"{element_label} à une dynamique {modality_label.lower()}. "
        f"{profile['strengths']} "
        f"Ton évolution personnelle passe toutefois par une conscience "
        f"plus fine de ce point : {profile['watchpoints']} "
        f"Le cœur de ton parcours consiste à transformer tes qualités "
        f"naturelles en choix durables, libres et alignés."
    )


def generate_personal_profile(
    sign,
    language="fr",
    birth_date=None,
    birth_time=None,
    birth_time_known=None,
    birth_place=None,
):
    context = build_profile_context(
        sign=sign,
        language=language,
        birth_date=birth_date,
        birth_time=birth_time,
        birth_time_known=birth_time_known,
        birth_place=birth_place,
    )

    if language != "fr":
        raise ValueError(
            "English personal profiles are not available yet"
        )

    profile = SIGN_PROFILES_FR.get(
        context["sign_key"]
    )

    if not profile:
        raise ValueError(
            "Personal profile content is unavailable"
        )

    sections = []

    birth_context_text = build_birth_context_text(
        context
    )

    if birth_context_text:
        sections.append(
            "✨ PROFIL ASTROVIBE PERSONNEL\n\n"
            + birth_context_text
        )
    else:
        sections.append(
            "✨ PROFIL ASTROVIBE PERSONNEL"
        )

    sections.append(
        SECTION_TITLES["fr"]["identity"]
        + "\n\n"
        + build_identity_text(context)
        + "\n\n"
        + profile["identity"]
    )

    ordered_sections = (
        "personality",
        "emotional_world",
        "communication",
        "love",
        "relationship_needs",
        "motivation",
        "work",
        "ambition",
        "finances",
        "strengths",
        "watchpoints",
        "balance",
        "growth",
    )

    for section_key in ordered_sections:
        sections.append(
            SECTION_TITLES["fr"][section_key]
            + "\n\n"
            + profile[section_key]
        )

    sections.append(
        SECTION_TITLES["fr"]["summary"]
        + "\n\n"
        + build_french_summary(
            context,
            profile
        )
    )

    return "\n\n".join(sections)
