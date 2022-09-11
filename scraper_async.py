from bs4 import BeautifulSoup
import requests
import aiohttp

import asyncio
import time

from config import MAIN_URL, HEADERS
from Sheets.google_sheets import push_to_gsheets
from Model.database import push_data_to_db


async def get_page(session, url: str) -> str:  # Download the page
    async with session.get(url=url, headers=HEADERS, ssl=False) as r:
        assert r.status == 200      # Check response status
        return await r.text()


async def get_all(session, urls: list) -> tuple:      # Generate tasks
    tasks = []
    for url in urls:
        task = asyncio.create_task(get_page(session, url))     # Generate single task (get_page)
        tasks.append(task)
    result = await asyncio.gather(*tasks)      # Added all tasks
    return result


def get_all_urls() -> list:         # Generate a package of needed URLs
    r = requests.get(url=MAIN_URL, headers=HEADERS)
    assert r.status_code == 200     # Check response status
    try:
        html = BeautifulSoup(r.text, "lxml")
        count = html.find(class_="resultsShowingCount-1707762110").text
        count = int(count.split('of')[1].split('result')[0].strip()) // 40 + 1
    except:
        count = 1

    print('Page count:', count)

    urls = [
        f'https://www.kijiji.ca/b-apartments-condos/city-of-toronto/page-{i}/c37l1700273' for i in range(1, count + 1)
    ]
    return urls


def parse(data: list) -> list:  # Scraping data from the page
    res = list()
    for html in data:
        page = BeautifulSoup(html, 'lxml')
        aparts = page.find_all('div', class_='search-item')  # Get all the apartments on the page

        for apart in aparts:  # Get the necessary information from each apartment
            dct = dict()
            price = apart.find(class_='price').text.strip().replace(',', '')
            dct['title'] = apart.find(class_='title').text.strip()
            dct['price'] = price[1:] if price.startswith('$') else None
            dct['currency_type'] = price[0] if price.startswith('$') else None
            dct['location'] = apart.find(class_='location').find('span').text.strip()
            date = apart.find(class_='location').find('span', class_="date-posted").text.strip()
            dct['date'] = date.replace('/', '-') if len(date.split('/')) == 3 else time.strftime("%d/%m/%Y")
            try:
                dct['bedrooms'] = apart.find(class_='bedrooms').text.split()[1]
            except KeyError:
                dct['bedrooms'] = ''
            dct['descr'] = apart.find(class_="description").text.split('...')[0].strip() + '...'
            try:
                dct['image_url'] = apart.find(class_='image').find('img')['data-src']
            except KeyError:
                dct['image_url'] = None
            res.append(dct)

    return res


async def main(urls: list) -> tuple:
    async with aiohttp.ClientSession() as session:  # Create the session
        return await get_all(session=session, urls=urls)  # Download all pages


if __name__ == '__main__':
    start = time.time()
    urls = get_all_urls()   # Get all URLs
    data = asyncio.run(main(urls))      # Download all pages asynchronously
    res = parse(data)      # Parsing the received data
    duration = round(time.time() - start, 3)     # Duration in seconds

    push_data_to_db(res)     # Save data to db
    push_to_gsheets(res)     # Save data to Google Sheets

    print(f'Quantity of apartments: {len(res)}')
    print(f'Scraping complete! Duration: {duration} s')




