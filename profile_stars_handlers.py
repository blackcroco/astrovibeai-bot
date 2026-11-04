# ============================================
# ASTROVIBE - TELEGRAM STARS HANDLERS
# ============================================

from telebot import types

from profile_stars_payment import (
    build_profile_invoice,
    validate_profile_pre_checkout,
    validate_profile_successful_payment,
    get_payment_success_text,
    get_payment_error_text,
)


PROFILE_PAYMENT_CALLBACK = (
    "unlock_profile_390"
)

PROFILE_PAYMENT_PAYLOAD_PREFIX = (
    "astrovibe_profile_v2:"
)


def send_profile_invoice(
    bot,
    call,
    language,
):
    bot.answer_callback_query(
        call.id
    )

    user_id = call.from_user.id

    invoice = build_profile_invoice(
        user_id=user_id,
        language=language,
    )

    prices = [
        types.LabeledPrice(
            label=item["label"],
            amount=item["amount"],
        )
        for item in invoice["prices"]
    ]

    bot.send_invoice(
        call.message.chat.id,
        title=invoice["title"],
        description=invoice["description"],
        invoice_payload=invoice["payload"],
        provider_token=invoice[
            "provider_token"
        ],
        currency=invoice["currency"],
        prices=prices,
        start_parameter=(
            "astrovibe-profile-v2"
        ),
    )


def is_profile_payment_payload(
    payload,
):
    return (
        isinstance(
            payload,
            str
        )
        and payload.startswith(
            PROFILE_PAYMENT_PAYLOAD_PREFIX
        )
    )


def process_profile_pre_checkout(
    bot,
    query,
):
    if not is_profile_payment_payload(
        query.invoice_payload
    ):
        return False

    result = validate_profile_pre_checkout(
        payload=query.invoice_payload,
        currency=query.currency,
        total_amount=query.total_amount,
        telegram_user_id=query.from_user.id,
    )

    if result["valid"]:
        bot.answer_pre_checkout_query(
            query.id,
            ok=True,
        )

        return True

    bot.answer_pre_checkout_query(
        query.id,
        ok=False,
        error_message=(
            "AstroVibe could not validate "
            "this payment."
        ),
    )

    return False


def process_profile_successful_payment(
    bot,
    message,
    language,
):
    payment = message.successful_payment

    if not is_profile_payment_payload(
        payment.invoice_payload
    ):
        return None

    result = (
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

    if not result["valid"]:
        bot.send_message(
            message.chat.id,
            get_payment_error_text(
                language
            ),
        )

        return result

    print(
        "ASTROVIBE PROFILE PAYMENT SUCCESS:",
        result[
            "telegram_payment_charge_id"
        ],
        result["user_id"],
        result["amount"],
        result["currency"],
    )

    bot.send_message(
        message.chat.id,
        get_payment_success_text(
            language
        ),
    )

    return result


def validate_stars_handlers_configuration():
    errors = []

    if (
        PROFILE_PAYMENT_CALLBACK
        != "unlock_profile_390"
    ):
        errors.append(
            "Invalid payment callback"
        )

    if (
        PROFILE_PAYMENT_PAYLOAD_PREFIX
        != "astrovibe_profile_v2:"
    ):
        errors.append(
            "Invalid payment payload prefix"
        )

    return {
        "valid": not errors,
        "errors": errors,
    }
