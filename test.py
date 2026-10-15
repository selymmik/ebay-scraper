
import argparse
import requests
from bs4 import BeautifulSoup


parser = argparse.ArgumentParser()
parser.add_argument('--search', required=True)
args = parser.parse_args()

all_items = []

for page in range (1,11):
    url = f"https://www.ebay.com/sch/i.html?_nkw={args.search}&_pgn={page}"
    html = requests.get(url).text
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    listings = soup.select('.s-card')
    
    for listing in listings:
        item = {}
        item['name'] = listing.select_one('.s-item__title').text
        x = listing.select_one('.s-item__price').text
        LowerPrice = x.split('to')[0]
        digits = ''.join(c for c in LowerPrice if c.isdigit())
        item['price'] = int(digits)
        item['status'] = listing.select_one('.SECONDARY_INFO').text
        shipping = listing.select_one('.s-item__shipping').text
        digits = ''.join(c for c in shipping if c.isdigit())
        if digits == '':
            item['shipping'] = 0
        else:
            item['shipping'] = int(digits)
        item['free_returns'] = listing.select_one('.s-item__free-returns').text
        item['items_sold'] = listing.select_one('.s-item__hotness').text
        
        all_items.append(item)


