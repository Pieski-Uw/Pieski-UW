from unittest.mock import patch
from unittest.mock import MagicMock
import requests
import pytest

from webscraper import web_scraper, models
from tests.test_data.doggy import doggy
from tests.test_data.list import lists


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


@pytest.mark.django_db()
def test_create_pet():
    """Test if creating pet works"""

    web_scraper.create_pet(doggy.DATA, doggy.LINK)
    assert len(models.Pet.objects.all()) == 1

    db_animal = models.Pet.objects.get(name=doggy.DATA["name"])
    assert db_animal.name == doggy.DATA["name"]
    assert db_animal.no == doggy.DATA["number"]
    assert db_animal.breed == doggy.DATA["breed"]
    assert db_animal.age == doggy.DATA["age"]
    assert db_animal.weight == doggy.DATA["weight"]
    assert db_animal.status == doggy.DATA["status"]
    assert db_animal.address_found == doggy.DATA["address_found"]
    assert db_animal.box == doggy.DATA["box"]
    assert db_animal.group_name == doggy.DATA["group_name"]
    assert db_animal.group_link == doggy.DATA["group_link"]
    assert db_animal.link == doggy.LINK


@pytest.mark.django_db()
def test_create_pet_twice():
    """Check if animal is inserted only once into DB"""

    web_scraper.create_pet(doggy.DATA, doggy.LINK)
    web_scraper.create_pet(doggy.DATA, doggy.LINK)
    assert len(models.Pet.objects.all()) == 1


def test_empty_list():
    """Test if parsing empty list of pets works"""

    mock_response = MagicMock()
    mock_response.status_code = 200

    # specify encoding to avoid warning
    mock_response.encoding = "utf-8"
    with open(lists.EMPTY_LIST_PATH, mode="r", encoding="utf-8") as mock_file:
        mock_response.text = mock_file.read()

    with patch("requests.get") as mock_get:
        mock_get.return_value = mock_response
        links = web_scraper.get_links_to_all_animal("https://google.com")
        assert len(links) == 0


def test_list():
    """Test if parsing not empty list of pets works"""

    mock_response = MagicMock()
    mock_response.status_code = 200

    # specify encoding to avoid warning
    mock_response.encoding = "utf-8"
    with open(lists.FULL_LIST_PATH, mode="r", encoding="utf-8") as mock_file:
        mock_response.text = mock_file.read()

    with patch("requests.get") as mock_get:
        mock_get.return_value = mock_response

        links = web_scraper.get_links_to_all_animal("https://google.com")
        assert len(links) == 15


def test_animal_page_real():
    """
    Test if real animal page is parsed correctly
    and it hasn't changed substantially
    """
    parsed_animal = web_scraper.parse_pet(doggy.LINK)
    assert parsed_animal == doggy.DATA
