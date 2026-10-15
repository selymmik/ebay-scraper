
import argparse
import requests
import json
import time
import csv
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument('--search', required=True)
parser.add_argument('--pages-dir')
parser.add_argument('--csv', action='store_true')
args = parser.parse_args()

def get_text(listing, selector):
    tag = listing.select_one(selector)
    if tag is None:
        return None
    return tag.text

def extract_items(html):

    items = []      
    soup = BeautifulSoup(html, 'html.parser')
    listings = soup.select('.s-item')
        
    for listing in listings:
        item = {}
        item['name'] = get_text(listing, '.s-item__title')
        
        x1 = get_text(listing, '.s-item__price')
        if x1 is None: 
            item['price'] = None
        else:
            LowerPrice = x1.split(' to ')[0]
            digits = ''.join(c for c in LowerPrice if c.isdigit())
            item['price'] = int(digits)  

        item['status'] = get_text(listing, '.SECONDARY_INFO')

        x = get_text(listing, '.s-item__shipping')
        if x is None:
            item['shipping'] = None
        else:
            digits = ''.join(c for c in x if c.isdigit())
            if digits == '':
                item['shipping'] = 0
            else:
                item['shipping'] = int(digits)

        freeReturns = get_text(listing, '.s-item__free-returns')
        if freeReturns is None:
            item['free_returns'] = None
        else:
            if "Free returns" in freeReturns:
                item['free_returns'] = True
            else:
                item['free_returns'] = False

        y = get_text(listing, '.s-item__hotness')
        if y is None:
            item['items_sold'] = None
        else:
            digits = ''.join(c for c in y if c.isdigit())
            if digits == '':
                item['items_sold'] = 0
            else:
                item['items_sold'] = int(digits)    
        items.append(item)
    return items
            

all_items = []
for page in range (1,11):
    if args.pages_dir:
        path = f"{args.pages_dir}/page-{page}.html"
        with open(path, encoding='utf-8') as f:
            html = f.read()
    else: 
        url = f"https://www.ebay.com/sch/i.html?_nkw={args.search}&_pgn={page}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        print(response.raise_for_status())
        print(response.reason)
        print(response.ok)
        time.sleep(2)
        html = response.text
    all_items.extend(extract_items(html)) 
print(len(all_items))

if args.csv:
    filename1 = f"{args.search}.csv"
    with open(filename1, 'w', newline="", encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'price', 'status', 'shipping', 'free_returns', 'items_sold'])
        writer.writeheader()
        writer.writerows(all_items)
    print('Saved', filename1)
else:
    filename = f"{args.search}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(all_items, f, indent=2)
    print('Saved', filename)