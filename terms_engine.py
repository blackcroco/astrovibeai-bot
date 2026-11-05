# ==================================================
# ASTROVIBE - TERMS OF USE FR / EN
# ==================================================

TERMS_FR = """📜 Conditions d’utilisation — AstroVibe

En utilisant AstroVibe, tu acceptes les présentes conditions d’utilisation.

🔮 1. Nature du service

AstroVibe propose des contenus d’astrologie, notamment des horoscopes, des analyses de compatibilité, des profils astrologiques et des contenus Premium.

Ces contenus sont proposés à des fins de divertissement et de réflexion personnelle.

AstroVibe ne fournit pas de conseil médical, psychologique, juridique, financier ou professionnel. Les contenus astrologiques ne doivent pas remplacer l’avis d’un professionnel qualifié ni constituer l’unique base d’une décision importante.

✨ 2. Profil AstroVibe Personnel

Le Profil AstroVibe Personnel est un produit numérique vendu séparément.

Prix de lancement : 390 ⭐ Telegram Stars.

Il s’agit d’un achat unique.

Une fois le paiement validé, l’accès au Profil est associé au compte Telegram ayant effectué l’achat.

Le Profil Personnel est indépendant de l’abonnement AstroVibe Premium.

💎 3. AstroVibe Premium

AstroVibe Premium donne accès aux fonctionnalités Premium proposées par le bot.

Prix actuel : 199 ⭐ Telegram Stars tous les 30 jours.

Premium est un abonnement récurrent.

Telegram peut débiter automatiquement les Stars nécessaires à chaque nouvelle période tant que l’abonnement reste actif.

L’utilisateur est responsable de la gestion et de l’annulation de son abonnement depuis les outils proposés par Telegram.

L’arrêt de l’abonnement met fin aux renouvellements futurs. L’accès déjà payé peut rester disponible jusqu’à la fin de la période correspondante.

⭐ 4. Telegram Stars

Les produits numériques AstroVibe sont payés en Telegram Stars (XTR).

L’achat et l’utilisation des Telegram Stars sont également soumis aux conditions de Telegram et, le cas échéant, à celles du fournisseur utilisé pour acheter les Stars.

Le prix d’acquisition des Stars dans une devise réelle peut varier selon la plateforme, la région, les taxes et le prestataire de paiement.

💳 5. Paiements et problèmes d’achat

Après un paiement réussi, AstroVibe tente de débloquer automatiquement le produit ou l’accès correspondant.

En cas de paiement débité mais de contenu non débloqué, utilise :

/paysupport

Conserve si possible les informations de la transaction Telegram afin de faciliter la vérification.

Les demandes concernant l’achat initial de Telegram Stars peuvent dépendre de Telegram ou du fournisseur auprès duquel les Stars ont été achetées.

🚫 6. Utilisation abusive

Il est interdit de tenter de contourner les contrôles d’accès, de falsifier une transaction, d’exploiter volontairement une faille ou d’abuser des systèmes de points, de parrainage ou de paiement.

AstroVibe peut limiter l’accès à certaines fonctionnalités en cas d’utilisation abusive ou frauduleuse.

🛠 7. Disponibilité

AstroVibe est un service en évolution.

Certaines fonctionnalités peuvent être modifiées, corrigées, temporairement interrompues ou remplacées pour assurer la maintenance, la sécurité et l’amélioration du service.

Nous faisons notre possible pour maintenir le service disponible et préserver les accès légitimement acquis.

🔐 8. Données

AstroVibe peut traiter les informations nécessaires au fonctionnement du service, notamment l’identifiant Telegram, les préférences, les données astrologiques fournies par l’utilisateur et les informations techniques nécessaires à la gestion des achats et abonnements.

Une politique de confidentialité dédiée pourra fournir davantage d’informations sur ce traitement.

📩 9. Support

Pour un problème concernant un paiement AstroVibe :

/paysupport

📌 10. Évolution des conditions

Ces conditions peuvent évoluer avec AstroVibe, notamment lorsque des fonctionnalités, produits ou règles applicables évoluent.

La version accessible depuis /terms constitue la version actuellement proposée dans AstroVibe."""


TERMS_EN = """📜 Terms of Use — AstroVibe

By using AstroVibe, you agree to these Terms of Use.

🔮 1. Nature of the service

AstroVibe provides astrology-related content, including horoscopes, compatibility analyses, astrological profiles and Premium content.

This content is provided for entertainment and personal reflection purposes.

AstroVibe does not provide medical, psychological, legal, financial or professional advice. Astrological content should not replace advice from a qualified professional or be used as the sole basis for an important decision.

✨ 2. AstroVibe Personal Profile

The AstroVibe Personal Profile is a separate digital product.

Launch price: 390 ⭐ Telegram Stars.

It is a one-time purchase.

Once payment has been successfully validated, access to the Profile is associated with the Telegram account that made the purchase.

The Personal Profile is independent from the AstroVibe Premium subscription.

💎 3. AstroVibe Premium

AstroVibe Premium provides access to the Premium features offered by the bot.

Current price: 199 ⭐ Telegram Stars every 30 days.

Premium is a recurring subscription.

Telegram may automatically charge the required Stars for each new period while the subscription remains active.

Users are responsible for managing and cancelling their subscription using the tools provided by Telegram.

Cancelling the subscription stops future renewals. Access already paid for may remain available until the end of the corresponding subscription period.

⭐ 4. Telegram Stars

AstroVibe digital products are paid for using Telegram Stars (XTR).

The purchase and use of Telegram Stars are also subject to Telegram's terms and, where applicable, the terms of the provider used to purchase the Stars.

The real-currency cost of acquiring Stars may vary depending on the platform, region, taxes and payment provider.

💳 5. Payments and purchase issues

After a successful payment, AstroVibe attempts to automatically unlock the corresponding product or access.

If a payment was charged but the purchased content or access was not unlocked, use:

/paysupport

If possible, keep the Telegram transaction information available to help with verification.

Requests concerning the original purchase of Telegram Stars may depend on Telegram or the provider from which the Stars were purchased.

🚫 6. Abuse

Attempts to bypass access controls, falsify transactions, intentionally exploit vulnerabilities, or abuse points, referral or payment systems are prohibited.

AstroVibe may restrict access to certain features in cases of abusive or fraudulent use.

🛠 7. Availability

AstroVibe is an evolving service.

Features may be modified, corrected, temporarily interrupted or replaced for maintenance, security and service improvement purposes.

We aim to keep the service available and preserve legitimately acquired access.

🔐 8. Data

AstroVibe may process information necessary to operate the service, including Telegram identifiers, preferences, astrological information provided by users and technical information required to manage purchases and subscriptions.

A dedicated privacy policy may provide additional information about this processing.

📩 9. Support

For an AstroVibe payment issue:

/paysupport

📌 10. Changes to these terms

These terms may evolve with AstroVibe, including when features, products or applicable requirements change.

The version available through /terms is the version currently provided within AstroVibe."""


def get_terms(language="fr"):
    if language == "en":
        return TERMS_EN

    return TERMS_FR


def split_terms(text, limit=3900):
    if len(text) <= limit:
        return [text]

    chunks = []
    current = ""

    for paragraph in text.split("\n\n"):
        candidate = (
            paragraph
            if not current
            else current
            + "\n\n"
            + paragraph
        )

        if len(candidate) <= limit:
            current = candidate
            continue

        if current:
            chunks.append(current)

        current = paragraph

    if current:
        chunks.append(current)

    return chunks
