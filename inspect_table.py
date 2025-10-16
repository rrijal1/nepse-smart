#!/usr/bin/env python3
"""
Inspect ShareSansar table structure
"""

import requests
from bs4 import BeautifulSoup

def inspect_table():
    url = 'https://www.sharesansar.com/today-share-price'
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.content, 'lxml')

    table = soup.find('table', {'id': 'myTableCopy'})
    if table:
        headers = [th.get_text(strip=True) for th in table.find_all('th')]
        print('Table headers:')
        for i, header in enumerate(headers):
            print(f'{i}: "{header}"')

        # Check first row of data
        rows = table.find_all('tr')[1:2]  # Just first data row
        if rows:
            cols = rows[0].find_all(['td', 'th'])
            print('\nFirst row data:')
            for i, col in enumerate(cols):
                text = col.get_text(strip=True)
                print(f'{i}: "{text}"')

if __name__ == "__main__":
    inspect_table()