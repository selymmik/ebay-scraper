# ebay-scraper

[Project Webpage](https://csci40.rtealwitter.com/projects/02_webscraping/project.html)

The Python file ebay-dl.py does multiple things. It first lets a user either scrape the live eBay website or point the program at a folder of saved HTML files. It then goes through the HTML code, pulls the relevant information about each product, and appends that information to one master list that includes all product entries. This repeats for each page of an eBay search result, up to 10 pages. For the live website, those entries relate only to the search term, but for the pre-downloaded HTML files the script only pulls whatever information is available on the pages, and that information is not specific to the entered search term (since it’s an offline process). The master list is then dumped into a JSON file that is created automatically in the project folder.

The three JSON files were generated from the artificial practice data because eBay limits web scraping on its servers. The exact commands are shown below. Input into a bash command line.

To scrape pre-downloaded ebay store page html files and output as JSON files:
```bash
    python ebay-dl.py --search "garden tools" --pages-dir practice-pages
    
    python ebay-dl.py --search "drill press" --pages-dir practice-pages

    python ebay-dl.py --search "claremont mckenna" --pages-dir practice-pages
```
The following outputs as CSV files instead of JSON: 
``` bash 
    python ebay-dl.py --search "garden tools" --pages-dir practice-pages --csv
    
    python ebay-dl.py --search "drill press" --pages-dir practice-pages --csv

    python ebay-dl.py --search "claremont mckenna" --pages-dir practice-pages --csv
```
To scrape live ebay store pages and output as either JSON (default) or CSV:
```bash
    python ebay-dl.py --search "steam deck"

    python ebay-dl.py --search "steam deck" --csv
```



This is the error that will likely occur if you attempt to scrape from ebay directly:
```bash 
Traceback (most recent call last):
  File "C:\Users\myles\OneDrive\! School\CMC\classes\comp sci\csci40\ebay-scraper\ebay-dl.py",line 83, in <module>
    print(response.raise_for_status())
          ~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "C:\Users\myles\OneDrive\! School\CMC\classes\comp sci\csci40\ebay-scraper\.venv\Lib\site-packages\requests\models.py", line 1167, in raise_for_status
    raise HTTPError(http_error_msg, response=self)
requests.exceptions.HTTPError: 403 Client Error: Forbidden for url: https://www.ebay.com/sch/i.html?_nkw=claremont%20mckenna&_pgn=1
```
