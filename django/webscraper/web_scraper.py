"""This module implements useful functions related to webscraping"""
# authors: MateuszWasilewski, Sulnek

import logging
import os
import re
import signal
import time
from multiprocessing import Process

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from webscraper.models import WebscrapingProcess, clear_webscraping_processes

from .tasks import create_pet

TIMED_GET_DELAY = 11
TIMED_GET_TIMEOUT = 3


# pylint: disable=too-many-branches
def parse_pet(href):
    """
    Returns information about a pet, from a website "href" in
    a dictionary. (value None if no information)

    usage example: parse_pet('https://napaluchu.waw.pl/pet/012300408/')
    """
    html = __timed_get(href)
    html_text = html.text
    soup = BeautifulSoup(html_text, "lxml")
    details = soup.find("ul", class_="petdetails")
    indents = details.find_all("li")
    name_field = soup.find("h2")
    # W poniższym słowniku zapisze dane, None oznacza brak danych
    info = {
        "name": None,
        "age": None,  # in months
        "breed": None,
        "gender": None,
        "weight": None,  # in kilograms
        "number": None,
        "status": None,
        "date_in": None,
        "date_out": None,
        "box": None,
        "address_found": None,
        "group_link": None,
        "group_name": None,
    }
    name = name_field.text.split(" ")[0]
    info["name"] = name

    for indent in indents:
        if not indent.find("strong"):  # site layout changed significantly
            pass
        if indent.text.startswith("W typie rasy"):
            info["breed"] = indent.find("strong").text
        elif indent.text.startswith("Wiek"):
            if indent.find("strong"):
                age_string = indent.find("strong").text
                num, unit = age_string.split()
                if unit.startswith("l"):
                    info["age"] = 12 * int(num)
                else:  # unit.startswith("m") - months
                    info["age"] = int(num)
        elif indent.text.startswith("Płeć"):
            info["gender"] = indent.find("strong").text.strip()
        elif indent.text.startswith("Waga"):
            info["weight"] = int(indent.find("strong").text.split()[0])
        elif indent.text.startswith("Nr"):
            info["number"] = indent.find("strong").text.strip()
        elif indent.text.startswith("Status"):
            info["status"] = indent.find("strong").text.strip()
        elif indent.text.startswith("Przyjęty"):
            info["date_in"] = indent.find("strong").text.strip()
        elif indent.text.startswith("Wydany"):
            info["date_out"] = indent.find("strong").text.strip()
        elif indent.text.startswith("Znaleziony"):
            info["address_found"] = indent.find("strong").text.strip()
        elif indent.text.startswith("Boks"):
            info["box"] = indent.find("strong").text.strip()
        elif indent.text.startswith("Grupa"):
            info["group_name"] = indent.find("strong").text.strip()
            info["group_link"] = (
                indent.find("a").get("href") if indent.find("a") else None
            )
    return info


def __timed_get(href):
    """Performs get request with preset timeout, with a delay"""
    time.sleep(TIMED_GET_DELAY)  # added in order not to get banned from the server
    try:
        return requests.get(
            href, timeout=TIMED_GET_TIMEOUT, headers={"User-Agent": UserAgent().random}
        )
    except requests.exceptions.Timeout:
        logging.warning("Request timed out")
        time.sleep(20)
        return requests.get(
            href, timeout=TIMED_GET_TIMEOUT, headers={"User-Agent": UserAgent().random}
        )


def get_links_to_animals_from_page(href: str) -> list[str]:
    """
    Fetches links to subpages about animals from given href

    Usage example
    links = get_links_to_animals_from_page(
        'https://napaluchu.waw.pl/zwierzeta/znalazly-dom/?pet_page=1'
        )
    ...
    """
    html = __timed_get(href)
    soup = BeautifulSoup(html.text, "lxml")
    html_links = soup.find_all("a", href=re.compile("/pet/"), text="dowiedz się więcej")

    result: list[str] = list(map(lambda tag: tag.get("href"), html_links))

    return result


def start_scraping(href: str):
    """Fetches links to subpages about animals all paged data
    and processes them one by one creating Pet objects
    Implementation is single threaded and very slow - will probably need fix in the future

    Usage example
    links = start_scraping('https://napaluchu.waw.pl/zwierzeta/znalazly-dom')
    ...
    """
    result: set[str] = set()
    page_iter: int = 1
    while True:
        logging.info("fetching from %s\n", f"{href}/?pet_page={page_iter}")

        animals: list[str] = get_links_to_animals_from_page(
            f"{href}/?pet_page={page_iter}"
        )
        new_result = result | set(animals)
        if len(result) == len(new_result):
            break

        pet_iter = 1
        for animal in set(animals) - result:
            pet_info = parse_pet("https://napaluchu.waw.pl" + animal)
            create_pet.delay(pet_info=pet_info, href=animal)
            logging.info(
                "Finished pet: %s, link: %s\n",
                str(page_iter) + ":" + str(pet_iter),
                animal,
            )
            pet_iter += 1

        page_iter += 1
        result = new_result


def scrape():
    """Does full webscraping and adds new data to database.
    Writes webscraper progress in webscraper_log.txt
    Note: DO NOT use outside start_webscraping()

    Usage example
    scrape()
    ...
    """
    start_scraping("https://napaluchu.waw.pl/zwierzeta/znalazly-dom")

    clear_webscraping_processes()


def kill_scrapping():
    """Kills process currently scrapping if there is one - else
    does nothing.

    Usage example
    kill_scrapping()
    ...
    """
    try:
        proc = WebscrapingProcess.objects.get(working=True)
    except WebscrapingProcess.DoesNotExist:
        clear_webscraping_processes()
        return
    pid = proc.pid
    proc.delete()
    try:
        os.kill(pid, signal.SIGKILL)
    except ProcessLookupError:
        logging.info("Webscraping stopped, process not found\n")

    logging.info("Webscraping stopped\n")


def start_scrapping():
    """Starts (or restarts if there is another one already working) the scrapping process

    Usage example
    start_scrapping()
    ...
    """
    if os.path.isfile("webscraper_log.txt"):
        os.remove("webscraper_log.txt")
    with open("webscraper_log.txt", "a", encoding="utf-8") as file:
        file.close()  # creating a file
    logging.basicConfig(
        filename="webscraper_log.txt",
        filemode="a",
        format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
        level=logging.DEBUG,
    )
    kill_scrapping()
    proc = Process(target=scrape)
    proc.daemon = True  # detach a process
    proc.start()
    WebscrapingProcess.objects.create(pid=proc.pid, working=True)


# print(parse_pet('https://napaluchu.waw.pl/pet/012300408/'))
# get_links_to_animals_from_page('https://napaluchu.waw.pl/zwierzeta/znalazly-dom/?pet_page=1')
# get_links_to_all_animal('https://napaluchu.waw.pl/zwierzeta/znalazly-dom')
