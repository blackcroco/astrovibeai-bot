# ============================================
# ASTROVIBE - PROFILE PURCHASE DELIVERY
# Telegram Stars + Neon permanent ownership
# ============================================

from profile_purchase_engine import (
    has_purchased_profile,
    record_profile_purchase,
)

from profile_stars_handlers import (
    send_profile_invoice,
    process_profile_pre_checkout,
    is_profile_payment_payload,
)

from profile_stars_payment import (
    validate_profile_successful_payment,
    get_payment_success_text,
    get_payment_error_text,
)


def get_already_owned_text(
    language="fr",
):
    if language == "en":
        return (
            "✅ Your AstroVibe Personal Profile "
            "is already unlocked."
        )

    return (
        "✅ Ton Profil AstroVibe Personnel "
        "est déjà débloqué."
    )


def send_profile_invoice_if_not_owned(
    bot,
    call,
    language,
    connection_factory,
):
    user_id = call.from_user.id

    if has_purchased_profile(
        connection_factory,
        user_id,
    ):
        bot.answer_callback_query(
            call.id
        )

        bot.send_message(
            call.message.chat.id,
            get_already_owned_text(
                language
            ),
        )

        return {
            "invoice_sent": False,
            "already_owned": True,
        }

    send_profile_invoice(
        bot,
        call,
        language,
    )

    return {
        "invoice_sent": True,
        "already_owned": False,
    }


def process_profile_pre_checkout_with_ownership(
    bot,
    query,
    connection_factory,
):
    if not is_profile_payment_payload(
        query.invoice_payload
    ):
        return False

    if has_purchased_profile(
        connection_factory,
        query.from_user.id,
    ):
        bot.answer_pre_checkout_query(
            query.id,
            ok=False,
            error_message=(
                "This AstroVibe Profile "
                "is already unlocked."
            ),
        )

        return False

    return process_profile_pre_checkout(
        bot,
        query,
    )


def process_successful_profile_purchase(
    bot,
    message,
    language,
    connection_factory,
):
    payment = message.successful_payment

    if not is_profile_payment_payload(
        payment.invoice_payload
    ):
        return None

    validation = (
        validate_profile_successful_payment(
            payload=payment.invoice_payload,
            currency=payment.currency,
            total_amount=payment.total_amount,
            telegram_payment_charge_id=(
                payment.telegram_payment_charge_id
            ),
            telegram_user_id=(
                message.from_user.id
            ),
        )
    )

    if not validation["valid"]:
        bot.send_message(
            message.chat.id,
            get_payment_error_text(
                language
            ),
        )

        return {
            "valid": False,
            "recorded": False,
            "validation": validation,
        }

    purchase_result = record_profile_purchase(
        connection_factory=connection_factory,
        user_id=validation["user_id"],
        telegram_payment_charge_id=(
            validation[
                "telegram_payment_charge_id"
            ]
        ),
        amount=validation["amount"],
        currency=validation["currency"],
    )

    if (
        purchase_result["recorded"]
        or purchase_result["already_owned"]
        or purchase_result["duplicate_charge"]
    ):
        bot.send_message(
            message.chat.id,
            get_payment_success_text(
                language
            ),
        )

        return {
            "valid": True,
            "recorded": purchase_result[
                "recorded"
            ],
            "already_owned": purchase_result[
                "already_owned"
            ],
            "duplicate_charge": purchase_result[
                "duplicate_charge"
            ],
            "purchase": purchase_result[
                "purchase"
            ],
        }

    bot.send_message(
        message.chat.id,
        get_payment_error_text(
            language
        ),
    )

    return {
        "valid": True,
        "recorded": False,
        "already_owned": False,
        "duplicate_charge": False,
        "purchase": None,
    }
