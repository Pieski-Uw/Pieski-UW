import re
from bs4 import BeautifulSoup
import requests

def parse_pet(href):
    html = requests.get(href)
    html_text = html.text
    soup = BeautifulSoup(html_text, 'lxml')
    details = soup.find('ul', class_ = 'petdetails')
    indents = details.find_all('li')
    #W poniższych zmiennych zapisze dane, None oznacza brak danych
    age = None
    breed = None
    gender = None
    weight = None
    number = None
    status = None
    date_in = None
    date_out = None
    box = None
    address_found = None
    group_link = None
    group_name = None
    for indent in indents:
        if (indent.text.startswith("W typie rasy")):
            breed = indent.find('strong').text
        elif (indent.text.startswith("Wiek")):
            age = indent.find('strong').text
        elif (indent.text.startswith("Płeć")):
            gender = indent.find('strong').text
        elif (indent.text.startswith("Waga")):
            weight = indent.find('strong').text
        elif (indent.text.startswith("Numer")):
            number = indent.find('strong').text
        elif (indent.text.startswith("Status")):
            status = indent.find('strong').text
        elif (indent.text.startswith("Przyjęty")):
            date_in = indent.find('strong').text
        elif (indent.text.startswith("Wydany")):
            date_out = indent.find('strong').text
        elif (indent.text.startswith("Znaleziony")):
            address_found = indent.find('strong').text
        elif (indent.text.startswith("Boks")):
            box = indent.find('strong').text
        elif (indent.text.startswith("Grupa")):
            group_name = indent.find('strong').text
            group_link = indent.find('a').get('href')
    #to be removed but may be useful in debug:
#     print(f'''
# Breed: {breed}
# Age: {age}
# Gender: {gender}
# Weight: {weight}
# Number: {number}
# Status: {status}
# date_in: {date_in}
# date_out: {date_out}
# address_found: {address_found}
# box: {box}
# group_name: {group_name}
# group_link: {group_link}
# ''')

def __timed_get(href):
    """Performs get request with preset timeout"""
    return requests.get(href, timeout=3)

def get_links_to_animals_from_page(href: str) -> list[str]:
    """
    Fetches links to subpages about animals from given href

    Usage example
    links = get_links_to_animals_from_page('https://napaluchu.waw.pl/zwierzeta/znalazly-dom/?pet_page=1')
    ...
    """
    html = __timed_get(href)
    soup = BeautifulSoup(html.text, 'lxml')
    html_links = soup.find_all('a', href=re.compile('/pet/'), text='dowiedz się więcej')

    result: list[str] = list(map(lambda tag: tag.get('href'), html_links))
    
    return result

def get_links_to_all_animal(href: str) -> set[str]:
    """ Fetches links to subpages about animals all paged data
    Implementation is single threaded and very slow - will probably need fix in the future

    Usage example
    links = get_links_to_all_animal('https://napaluchu.waw.pl/zwierzeta/znalazly-dom')
    ...
    """
    result: set[str] = set()
    page_iter: int = 1
    while True:
        print(f'fetching from {page_iter}')
        animals: list[str] = get_links_to_animals_from_page(f'{href}/?pet_page={page_iter}')
        new_result = result | set(animals)
        if len(result) == len(new_result):
            break
        page_iter += 1
        result = new_result

    return result

#parse_pet('https://napaluchu.waw.pl/pet/012300408/')
#get_links_to_animals_from_page('https://napaluchu.waw.pl/zwierzeta/znalazly-dom/?pet_page=1')
#get_links_to_all_animal('https://napaluchu.waw.pl/zwierzeta/znalazly-dom')