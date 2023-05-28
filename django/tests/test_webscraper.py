from unittest.mock import patch
from unittest.mock import MagicMock
import requests
import pytest

from webscraper import web_scraper
from tests.test_data.doggy import doggy


@pytest.mark.django_db()
def test_empty_db():
    """Test if creating local test db works"""


def test_get_mock():
    """Test if mock works"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"key": "value"}

    with patch("requests.get") as mock_get:
        mock_get.return_value = mock_response
        assert requests.get("https://google.com", timeout=5) == mock_response


def test_animal_page_mock():
    """Test if saved single animal page is parsed correctly"""
    mock_response = MagicMock()
    mock_response.status_code = 200

    # specify encoding to avoid warning
    mock_response.encoding = "utf-8"
    with open(doggy.MOCK_FILE, mode="r", encoding="utf-8") as mock_file:
        mock_response.text = mock_file.read()

    with patch("requests.get") as mock_get:
        mock_get.return_value = mock_response
        parsed_animal = web_scraper.parse_pet("https://google.com")
        assert parsed_animal == doggy.DATA


def test_animal_page_real():
    """
    Test if real animal page is parsed correctly
    and it hasn't changed substantially
    """
    parsed_animal = web_scraper.parse_pet(doggy.LINK)
    assert parsed_animal == doggy.DATA
