# ============================================
# ASTROVIBE - BIRTH LOCATION ENGINE
# Résolution d'un lieu de naissance
# ============================================

import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


# ============================================
# CONFIGURATION
# ============================================

COUNTRIES_API_BASE_URL = (
    "https://countries.dev/cities"
)

LOCATION_USER_AGENT = (
    "AstroVibe/1.0"
)

DEFAULT_RESULT_LIMIT = 5
REQUEST_TIMEOUT_SECONDS = 10


# ============================================
# NETTOYAGE DES DONNÉES
# ============================================

def normalize_location_query(location_query):
    if not location_query:
        return ""

    return " ".join(
        str(location_query).strip().split()
    )


def normalize_country_code(country_code):
    if not country_code:
        return None

    normalized = str(
        country_code
    ).strip().upper()

    if len(normalized) != 2:
        return None

    return normalized


def safe_float(value):
    if value is None:
        return None

    try:
        return float(value)

    except (TypeError, ValueError):
        return None


def safe_int(value):
    if value is None:
        return 0

    try:
        return int(value)

    except (TypeError, ValueError):
        return 0


# ============================================
# FORMAT STANDARD D'UNE VILLE
# ============================================

def normalize_city_result(raw_city):
    if not isinstance(raw_city, dict):
        return None

    latitude = safe_float(
        raw_city.get("latitude")
    )

    longitude = safe_float(
        raw_city.get("longitude")
    )

    timezone = raw_city.get("timezone")
    city_name = raw_city.get("name")
    country_code = raw_city.get("countryCode")

    if not city_name:
        return None

    if latitude is None or longitude is None:
        return None

    if not timezone:
        return None

    country_code = (
        str(country_code).upper()
        if country_code
        else None
    )

    return {
        "geoname_id": raw_city.get("geonameId"),
        "name": str(city_name).strip(),
        "ascii_name": raw_city.get("asciiName"),
        "country_code": country_code,
        "admin1_code": raw_city.get("admin1Code"),
        "latitude": latitude,
        "longitude": longitude,
        "population": safe_int(
            raw_city.get("population")
        ),
        "timezone": str(timezone).strip(),
        "feature_code": raw_city.get("featureCode"),
    }


# ============================================
# APPEL DE L'API
# ============================================

def fetch_city_results(
    location_query,
    country_code=None,
    limit=DEFAULT_RESULT_LIMIT,
):
    clean_query = normalize_location_query(
        location_query
    )

    if len(clean_query) < 2:
        return {
            "status": "invalid_query",
            "query": clean_query,
            "results": [],
            "error": None,
        }

    clean_country_code = normalize_country_code(
        country_code
    )

    try:
        clean_limit = int(limit)

    except (TypeError, ValueError):
        clean_limit = DEFAULT_RESULT_LIMIT

    clean_limit = max(
        1,
        min(clean_limit, 10)
    )

    parameters = {
        "q": clean_query,
        "limit": clean_limit,
    }

    if clean_country_code:
        parameters["country"] = clean_country_code

    request_url = (
        COUNTRIES_API_BASE_URL
        + "?"
        + urlencode(parameters)
    )

    request = Request(
        request_url,
        headers={
            "Accept": "application/json",
            "User-Agent": LOCATION_USER_AGENT,
        },
        method="GET",
    )

    try:
        with urlopen(
            request,
            timeout=REQUEST_TIMEOUT_SECONDS
        ) as response:
            response_text = response.read().decode(
                "utf-8"
            )

        payload = json.loads(
            response_text
        )

    except HTTPError as error:
        if error.code == 404:
            return {
                "status": "not_found",
                "query": clean_query,
                "results": [],
                "error": None,
            }

        if error.code == 429:
            return {
                "status": "rate_limited",
                "query": clean_query,
                "results": [],
                "error": "HTTP 429",
            }

        return {
            "status": "api_error",
            "query": clean_query,
            "results": [],
            "error": f"HTTP {error.code}",
        }

    except URLError as error:
        return {
            "status": "network_error",
            "query": clean_query,
            "results": [],
            "error": str(error.reason),
        }

    except TimeoutError:
        return {
            "status": "timeout",
            "query": clean_query,
            "results": [],
            "error": "Request timeout",
        }

    except (
        json.JSONDecodeError,
        UnicodeDecodeError,
    ) as error:
        return {
            "status": "invalid_response",
            "query": clean_query,
            "results": [],
            "error": str(error),
        }

    except Exception as error:
        return {
            "status": "unexpected_error",
            "query": clean_query,
            "results": [],
            "error": str(error),
        }

    if not isinstance(payload, list):
        return {
            "status": "invalid_response",
            "query": clean_query,
            "results": [],
            "error": "Expected a JSON list",
        }

    normalized_results = []

    for raw_city in payload:
        city = normalize_city_result(
            raw_city
        )

        if city:
            normalized_results.append(
                city
            )

    normalized_results.sort(
        key=lambda city: city["population"],
        reverse=True,
    )

    if not normalized_results:
        return {
            "status": "not_found",
            "query": clean_query,
            "results": [],
            "error": None,
        }

    return {
        "status": "success",
        "query": clean_query,
        "results": normalized_results,
        "error": None,
    }


# ============================================
# DÉTECTION DES RÉSULTATS AMBIGUS
# ============================================

def is_exact_city_name(city, location_query):
    city_name = normalize_location_query(
        city.get("name")
    ).casefold()

    query_name = normalize_location_query(
        location_query
    ).casefold()

    return city_name == query_name


def select_exact_city_matches(
    results,
    location_query,
):
    exact_matches = [
        city
        for city in results
        if is_exact_city_name(
            city,
            location_query
        )
    ]

    if exact_matches:
        return exact_matches

    return results


def resolve_birth_location(
    location_query,
    country_code=None,
):
    search = fetch_city_results(
        location_query=location_query,
        country_code=country_code,
        limit=DEFAULT_RESULT_LIMIT,
    )

    if search["status"] != "success":
        return {
            "status": search["status"],
            "query": search["query"],
            "location": None,
            "choices": [],
            "error": search["error"],
        }

    candidates = select_exact_city_matches(
        search["results"],
        search["query"],
    )

    if len(candidates) == 1:
        return {
            "status": "resolved",
            "query": search["query"],
            "location": candidates[0],
            "choices": candidates,
            "error": None,
        }

    return {
        "status": "ambiguous",
        "query": search["query"],
        "location": None,
        "choices": candidates,
        "error": None,
    }


# ============================================
# FORMAT D'AFFICHAGE
# ============================================

def format_location_label(
    location,
    language="fr",
):
    if not location:
        return ""

    city_name = location.get(
        "name",
        ""
    )

    country_code = location.get(
        "country_code"
    )

    timezone = location.get(
        "timezone"
    )

    if country_code:
        base_label = (
            f"{city_name} ({country_code})"
        )
    else:
        base_label = city_name

    if timezone:
        if language == "en":
            return (
                f"{base_label} — Time zone: "
                f"{timezone}"
            )

        return (
            f"{base_label} — Fuseau : "
            f"{timezone}"
        )

    return base_label


def build_location_choices(
    locations,
    language="fr",
):
    return [
        {
            "index": index,
            "label": format_location_label(
                location,
                language
            ),
            "location": location,
        }
        for index, location in enumerate(
            locations,
            start=1,
        )
    ]


# ============================================
# DONNÉES PRÊTES POUR NEON
# ============================================

def location_to_birth_fields(location):
    if not location:
        return {
            "birth_place": None,
            "birth_timezone": None,
            "birth_latitude": None,
            "birth_longitude": None,
        }

    city_name = location.get("name")
    country_code = location.get(
        "country_code"
    )

    if city_name and country_code:
        birth_place = (
            f"{city_name}, {country_code}"
        )
    else:
        birth_place = city_name

    return {
        "birth_place": birth_place,
        "birth_timezone": location.get(
            "timezone"
        ),
        "birth_latitude": location.get(
            "latitude"
        ),
        "birth_longitude": location.get(
            "longitude"
        ),
    }
