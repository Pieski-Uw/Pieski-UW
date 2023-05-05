# file was previously in root directory of a project
# authors: MateuszWasilewski, Sulnek

import re
from bs4 import BeautifulSoup
import requests
import time
from multiprocessing import Process
import os
import signal
from webscraper.models import createPet, WebscrappingProcess, clearWebscrappingProcesses

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
        "name" : None,
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
    name = name_field.text.split(' ')[0]
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
            info["gender"] = indent.find("strong").text
        elif indent.text.startswith("Waga"):
            info["weight"] = int(indent.find("strong").text.split()[0])
        elif indent.text.startswith("Nr"):
            info["number"] = indent.find("strong").text
        elif indent.text.startswith("Status"):
            info["status"] = indent.find("strong").text
        elif indent.text.startswith("Przyjęty"):
            info["date_in"] = indent.find("strong").text
        elif indent.text.startswith("Wydany"):
            info["date_out"] = indent.find("strong").text
        elif indent.text.startswith("Znaleziony"):
            info["address_found"] = indent.find("strong").text
        elif indent.text.startswith("Boks"):
            info["box"] = indent.find("strong").text
        elif indent.text.startswith("Grupa"):
            info["group_name"] = indent.find("strong").text
            info["group_link"] = (
                indent.find("a").get("href") if indent.find("a") else None
            )
    return info


def __timed_get(href):
    """Performs get request with preset timeout, with a delay"""
    time.sleep(3) # added in order not to get banned from the server
    return requests.get(href, timeout=3)


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


def get_links_to_all_animal(href: str) -> set[str]:
    """Fetches links to subpages about animals all paged data
    Implementation is single threaded and very slow - will probably need fix in the future

    Usage example
    links = get_links_to_all_animal('https://napaluchu.waw.pl/zwierzeta/znalazly-dom')
    ...
    """
    result: set[str] = set()
    page_iter: int = 1
    while True:
        logs = open("webscrapper_log.txt" , "a" )
        logs.write(f"fetching from {page_iter}\n")
        logs.close()

        animals: list[str] = get_links_to_animals_from_page(
            f"{href}/?pet_page={page_iter}"
        )
        new_result = result | set(animals)
        if len(result) == len(new_result):
            break
        page_iter += 1
        result = new_result

    return result

def scrape():
    """Does full webscrapping and adds new data to database.
    Writes webscrapper progress in webscrapper_log.txt
    Note: DO NOT use outside start_webscrapping()

    Usage example
    scrape()
    ...
    """
    pet_links = get_links_to_all_animal('https://napaluchu.waw.pl/zwierzeta/znalazly-dom')
    it = 1
    for pet_link in pet_links:
        pet_info = parse_pet(pet_link)
        createPet(pet_info=pet_info, href=pet_link)
        logs = open("webscrapper_log.txt" , "a" )
        logs.write(f"Finished pet: {it}\n")
        logs.close()
        it += 1
    clearWebscrappingProcesses()

def kill_scrapping():
    """Kills process currently scrapping if there is one - if not
    does nothing.

    Usage example
    kill_scrapping()
    ...
    """
    try:
        proc = WebscrappingProcess.objects.get(working=True)
    except WebscrappingProcess.DoesNotExist:
        clearWebscrappingProcesses()
        return
    pid = proc.pid
    proc.delete()
    os.kill(pid, signal.SIGKILL)

    logs = open("webscrapper_log.txt" , "a" )
    logs.write("Webscrapping stopped\n")
    logs.close()

def start_scrapping():   
    """Starts (or restarts) the scrapping process

    Usage example
    start_scrapping()
    ...
    """
    kill_scrapping()
    if os.path.isfile("webscrapper_log.txt"):
        os.remove("webscrapper_log.txt")
    p = Process(target=scrape)
    p.daemon = True # detach a process
    p.start()
    WebscrappingProcess.objects.create(pid=p.pid, working=True)   

# print(parse_pet('https://napaluchu.waw.pl/pet/012300408/'))
# get_links_to_animals_from_page('https://napaluchu.waw.pl/zwierzeta/znalazly-dom/?pet_page=1')
# get_links_to_all_animal('https://napaluchu.waw.pl/zwierzeta/znalazly-dom')
