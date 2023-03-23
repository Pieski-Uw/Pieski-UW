from bs4 import BeautifulSoup
import requests


def parse_pet(href):
    html = requests.get(href)
    html_text = html.text
    soup = BeautifulSoup(html_text, 'lxml')
    details = soup.find('ul', class_='petdetails')
    indents = details.find_all('li')
    # W poniższym słowniku zapisze dane, None oznacza brak danych
    info = {
        "age": None,
        "breed": None,
        "gender": None,
        "weight": None,
        "number": None,
        "status": None,
        "date_in ": None,
        "date_out": None,
        "box": None,
        "address_found": None,
        "group_link": None,
        "group_name": None,
    }

    for indent in indents:
        if indent.text.startswith("W typie rasy"):
            info["breed"] = indent.find('strong').text if indent.find('strong') else None
        elif indent.text.startswith("Wiek"):
            info["age"] = indent.find('strong').text if indent.find('strong') else None
        elif indent.text.startswith("Płeć"):
            info["gender"] = indent.find('strong').text if indent.find('strong') else None
        elif indent.text.startswith("Waga"):
            info["weight"] = indent.find('strong').text if indent.find('strong') else None
        elif indent.text.startswith("Numer"):
            info["number"] = indent.find('strong').text if indent.find('strong') else None
        elif indent.text.startswith("Status"):
            info["status"] = indent.find('strong').text if indent.find('strong') else None
        elif indent.text.startswith("Przyjęty"):
            info["date_in"] = indent.find('strong').text if indent.find('strong') else None
        elif indent.text.startswith("Wydany"):
            info["date_out"] = indent.find('strong').text if indent.find('strong') else None
        elif indent.text.startswith("Znaleziony"):
            info["address_found"] = indent.find('strong').text if indent.find('strong') else None
        elif indent.text.startswith("Boks"):
            info["box"] = indent.find('strong').text if indent.find('strong') else None
        elif indent.text.startswith("Grupa"):
            info["group_name"] = indent.find('strong').text if indent.find('strong') else None
            info["group_link"] = indent.find('a').get('href') if indent.find('a') else None
    return info


# debugging print function
def print_pet_info(info):
    print(f'''
Breed: {info["breed"]}
Age: {info["age"]}
Gender: {info["gender"]}
Weight: {info["weight"]}
Number: {info["number"]}
Status: {info["status"]}
date_in: {info["date_in"]}
date_out: {info["date_out"]}
address_found: {info["address_found"]}
box: {info["box"]}
group_name: {info["group_name"]}
group_link: {info["group_link"]}
''')


# print_pet_info(parse_pet('https://napaluchu.waw.pl/pet/012300408/'))
