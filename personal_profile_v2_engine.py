from personal_profile_engine import (
    generate_personal_profile as generate_personal_profile_v1,
)

from natal_chart_engine import (
    calculate_natal_chart,
)

from natal_profile_interpreter import (
    interpret_natal_chart,
    format_natal_interpretation,
)


def generate_personal_profile_v2(
    sign,
    language="fr",
    birth_date=None,
    birth_time=None,
    birth_time_known=None,
    birth_place=None,
    birth_timezone=None,
    birth_latitude=None,
    birth_longitude=None,
):
    language = (
        language
        if language in ("fr", "en")
        else "fr"
    )

    base_profile = generate_personal_profile_v1(
        sign=sign,
        language=language,
        birth_date=birth_date,
        birth_time=birth_time,
        birth_time_known=birth_time_known,
        birth_place=birth_place,
    )

    natal_data_available = (
        birth_date is not None
        and bool(birth_place)
        and bool(birth_timezone)
        and birth_latitude is not None
        and birth_longitude is not None
    )

    if not natal_data_available:
        return base_profile

    try:
        natal_chart = calculate_natal_chart(
            birth_date=birth_date,
            birth_time=birth_time,
            birth_time_known=birth_time_known,
            birth_place=birth_place,
            birth_timezone=birth_timezone,
            birth_latitude=birth_latitude,
            birth_longitude=birth_longitude,
        )

        if not natal_chart.get("calculated"):
            return base_profile

        natal_interpretation = interpret_natal_chart(
            natal_chart,
            language=language,
        )

        if not natal_interpretation.get("available"):
            return base_profile

        natal_text = format_natal_interpretation(
            natal_interpretation,
            language=language,
        )

        if not natal_text:
            return base_profile

        if language == "en":
            separator_title = (
                "🌌 YOUR PERSONAL NATAL CHART"
            )
        else:
            separator_title = (
                "🌌 TON THÈME NATAL PERSONNALISÉ"
            )

        return (
            base_profile
            + "\n\n"
            + separator_title
            + "\n\n"
            + natal_text
        )

    except Exception as error:
        print(
            "AstroVibe natal profile fallback:",
            type(error).__name__,
            str(error),
        )

        return base_profile
