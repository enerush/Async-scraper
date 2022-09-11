# Google Sheets API has a limit of 500 requests per 100 seconds per project,
# and 100 requests per 100 seconds per user. Limits for reads and writes are tracked separately.

import gspread
import time
import os


sa = gspread.service_account(filename=f'{os.getcwd()}/Sheets/service_account.json')
sh = sa.open('Apartments')
wks = sh.worksheet('Data2')


def push_to_gsheets(data: list) -> None:
    wks.clear()
    wks.append_row(['Title', 'Price', 'Currency', 'City', 'Date', 'Bedrooms', 'INFO', 'Image_URL'])
    for item in data:
        header = []
        for k, v in item.items():
            header.append(v)
        time.sleep(1)
        wks.append_row(header)
    print('Saving data to the Google-Sheets was successful!')
