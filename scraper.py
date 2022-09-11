import requests
from bs4 import BeautifulSoup
import time

from Model.database import push_data_to_db
from Sheets.google_sheets import push_to_gsheets
from config import MAIN_URL, HEADERS


def get_all_urls(url: str, headers: dict) -> list:      # Generate a package of needed URLs
    try:
        r = requests.get(url=url, headers=headers)
        main_page = BeautifulSoup(r.text, "lxml")
        count = main_page.find(class_="resultsShowingCount-1707762110").text
        count = int(count.split('of')[1].split('result')[0].strip()) // 40 + 1
    except:
        count = 1
    print('Page count :', count)
    all_urls = [
        f'https://www.kijiji.ca/b-apartments-condos/city-of-toronto/page-{i}/c37l1700273' for i in range(1, count + 1)
    ]

    return all_urls
    

def parse(url: str, headers: dict) -> list:         # Scraping data from the page
    r = requests.get(url=url, headers=headers)
    page = BeautifulSoup(r.text, "lxml")
    aparts = page.find_all('div', class_='search-item')     # Get all the apartments on the page
    data = list()

    for apart in aparts:        # Get the necessary information from each apartment
        dct = dict()
        price = apart.find(class_='price').text.strip().replace(',', '')
        dct['title'] = apart.find(class_='title').text.strip()
        dct['price'] = price[1:] if price.startswith('$') else None
        dct['currency_type'] = price[0] if price.startswith('$') else None
        dct['location'] = apart.find(class_='location').find('span').text.strip()
        date = apart.find(class_='location').find('span', class_="date-posted").text.strip()
        dct['date'] = date.replace('/', '-') if len(date.split('/')) == 3 else time.strftime("%d/%m/%Y").replace('/', '-')
        dct['bedrooms'] = apart.find(class_='bedrooms').text.split()[1]
        dct['descr'] = apart.find(class_="description").text.split('...')[0].strip() + '...'
        try:
            dct['image_url'] = apart.find(class_='image').find('img')['data-src']
        except KeyError:
            dct['image_url'] = None
        data.append(dct)

    return data


def main():
    start = time.time()
    urls = get_all_urls(url=MAIN_URL, headers=HEADERS)      # Get URLs list
    res = []
    for url in urls:        # Parse all the page
        data = parse(url=url, headers=HEADERS)
        res.extend(data)

    duration = round(time.time() - start, 3)    # Duration in seconds
    push_data_to_db(res)  # Save data to db
    push_to_gsheets(res)  # Save data to Google Sheets

    print(f'Quantity of apartments: {len(res)}')
    print(f'Scraping duration: {duration} s')


if __name__ == '__main__':
    main()
