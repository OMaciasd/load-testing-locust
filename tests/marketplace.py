import logging

logger = logging.getLogger(__name__)


def get_market_offers(client, token):
    url = "$URL"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    params = {
        "page": 1,
        "per_page": 50,
        "operation": "buy"
    }

    response = client.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()

    logger.error(f"⚠️ Error obteniendo ofertas: {response.status_code}")
    return None
