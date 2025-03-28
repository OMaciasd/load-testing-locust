from unittest.mock import patch, MagicMock
import unittest


def test_token_renovation(mock_user):
    """Verifica que el token se renueva correctamente cuando expira"""
    with patch("your_module.get_token", return_value="new_token"):
        mock_user.renew_token()

        class TestMarketplace(unittest.TestCase):
            def test_token_renovation(self):
                self.assertEqual(mock_user.token, "new_token")


def test_fetch_market_offers_success(mock_user):
    """Simula una respuesta exitosa del marketplace"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"offers": ["item1", "item2"]}

    with patch("your_module.get_market_offers", return_value=mock_response):
        response = mock_user.fetch_market_offers()
        if response.status_code != 200:
            raise ValueError(
                f"Error: Código de estado inesperado {response.status_code}"
            )

        if response.json() != {"offers": ["item1", "item2"]}:
            raise ValueError(
                "Error: La respuesta no coincide con la esperada"
            )


def test_fetch_market_offers_unauthorized(mock_user):
    """Verifica que el token se renueva cuando la API devuelve 401"""
    mock_response_401 = MagicMock()
    mock_response_401.status_code = 401
