"""
Vytvori seznam domen ceskych bank.
Odkazy jsou ze serveru https://www.banky.cz/ 
"""

import requests
from bs4 import BeautifulSoup as bs4
import re

url = "https://www.banky.cz"

def getBanks():
    r = requests.get(f"{url}/banky")
    if (r.ok):
        soup = bs4(r.content, "lxml")

        all_banks = soup.find_all(class_="InstituteItem")
        active_banks = [element for element in all_banks if "EndedItem" not in element.get("class", [])]
        links = [bank.find('a', href=True)['href'] for bank in active_banks]

    return links

def getLink(bank):
    r = requests.get(f"{url}{bank}")
    if r.ok:
        # print(bank)
        soup = bs4(r.content, "lxml")
        container = soup.find(class_="ParametersContainer")
        link = container.find("a", href=True)['href']
        return link

def cleanDomains():
    regex = r'https:\/\/([^\/\n]+)'
    with open('safeDomains.txt', 'w') as f:
        for l in getBanks():
            link = getLink(l)
            link = re.search(regex, link).groups(1)[0]
            f.write(f"{link}\n")

if __name__ == '__main__':
    cleanDomains()