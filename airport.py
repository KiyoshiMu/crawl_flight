from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import os

def get_airports(keep_cur=True): -> None
    """
get a table for airports in china and their corresponding IATA codes,
save as a json file.
    """
    if keep_cur and os.path.isfile('airport.json'):
        return
    base_url = 'https://www.prokerala.com/travel/airports/china/'
    html = urlopen(base_url)
    bs = BeautifulSoup(html, 'html.parser')

    airports = bs.find_all('a', {'class':'airport-name'})
    iatas = bs.find_all('td', {'class':'tc td-width-60'})[::2]
    result = {airport.get_text():iata.get_text() for airport, iata in zip(airports, iatas)}
    with open('airport.json', 'w') as airport_table:
        json.dump(result, airport_table)
    

if __name__ == "__main__":
    get_airports()