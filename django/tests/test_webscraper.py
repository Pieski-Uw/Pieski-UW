"""Test for webscraper module"""

# pylint: disable=unused-argument

import requests
import pytest
import responses

from webscraper import web_scraper, models
from tests.test_data.animal import doggy, milka
from tests.test_data.list import lists


@pytest.fixture(name="remove_get_delay")
def fixture_remove_get_delay(mocker):
    """Remove delay from get function for tests"""
    return mocker.patch("webscraper.web_scraper.TIMED_GET_DELAY", 0)


def read_mock_file(file_path):
    """Read mock file"""
    with open(file_path, mode="r", encoding="utf-8") as mock_file:
        return mock_file.read()


def assert_animal_eq(db_animal: models.Pet, animal, link):
    """Checks field by field if animal in db is the same as animal_data"""
    assert db_animal.name == animal["name"]
    assert db_animal.no == animal["number"]
    assert db_animal.breed == animal["breed"]
    assert db_animal.age == animal["age"]
    assert db_animal.weight == animal["weight"]
    assert db_animal.status == animal["status"]
    assert db_animal.address_found == animal["address_found"]
    assert db_animal.box == animal["box"]
    assert db_animal.group_name == animal["group_name"]
    assert db_animal.group_link == animal["group_link"]
    assert db_animal.link == link


@pytest.mark.django_db()
def test_empty_db():
    """Test if creating local test db works"""
    assert len(models.Pet.objects.all()) == 0


@responses.activate
def test_get_mock(remove_get_delay):
    """Test if mock works"""
    responses.add(responses.GET, "https://google.com", body="{}", status=200)
    assert requests.get("https://google.com", timeout=5).json() == {}


@responses.activate
def test_animal_page_mock(remove_get_delay):
    """Test if saved single animal page is parsed correctly"""
    responses.add(
        responses.GET, doggy.LINK, body=read_mock_file(doggy.MOCK_FILE), status=200
    )
    parsed_animal = web_scraper.parse_pet(doggy.LINK)
    assert parsed_animal == doggy.DATA


@pytest.mark.django_db()
def test_create_pet():
    """Test if creating pet works"""

    web_scraper.create_pet(doggy.DATA, doggy.LINK)
    assert len(models.Pet.objects.all()) == 1

    db_animal = models.Pet.objects.get(name=doggy.DATA["name"])
    assert_animal_eq(db_animal, doggy.DATA, doggy.LINK)


@pytest.mark.django_db()
def test_create_pet_twice():
    """Check if animal is inserted only once into DB"""

    web_scraper.create_pet(doggy.DATA, doggy.LINK)
    web_scraper.create_pet(doggy.DATA, doggy.LINK)
    animals = models.Pet.objects.all()
    assert len(animals) == 1
    assert_animal_eq(animals[0], doggy.DATA, doggy.LINK)


@responses.activate
@pytest.mark.django_db()
def test_empty_list(remove_get_delay):
    """Test if parsing empty list of pets works"""
    responses.add(
        responses.GET,
        lists.FIRST_LIST_URL,
        body=read_mock_file(lists.EMPTY_LIST_PATH),
        status=200,
    )

    web_scraper.scrape()
    assert len(models.Pet.objects.all()) == 0


@responses.activate
@pytest.mark.django_db(transaction=True)
def test_list(remove_get_delay):
    """Test if parsing not empty list of pets works"""
    responses.add(
        responses.GET,
        lists.FIRST_LIST_URL,
        body=read_mock_file(lists.SIMPLE_LIST_PATH),
        status=200,
    )
    responses.add(
        responses.GET,
        lists.SECOND_LIST_URL,
        body=read_mock_file(lists.EMPTY_LIST_PATH),
        status=200,
    )
    responses.add(
        responses.GET, doggy.LINK, body=read_mock_file(doggy.MOCK_FILE), status=200
    )
    responses.add(
        responses.GET, milka.LINK, body=read_mock_file(milka.MOCK_FILE), status=200
    )

    web_scraper.scrape()
    animals = models.Pet.objects.all()
    assert len(animals) == 2
    animals.order_by("name")

    assert_animal_eq(animals.get(name=doggy.DATA["name"]), doggy.DATA, doggy.LINK)
    assert_animal_eq(animals.get(name=milka.DATA["name"]), milka.DATA, milka.LINK)


def test_animal_page_real(remove_get_delay):
    """
    Test if real animal page is parsed correctly
    and it hasn't changed substantially
    """
    parsed_animal = web_scraper.parse_pet(doggy.LINK)
    assert parsed_animal == doggy.DATA
