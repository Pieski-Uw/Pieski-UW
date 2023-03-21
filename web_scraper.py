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



#parse_pet('https://napaluchu.waw.pl/pet/012300408/')
