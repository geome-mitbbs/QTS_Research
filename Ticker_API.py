import urllib.request
from bs4 import BeautifulSoup

def scrape_list(site):
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(site, headers=hdr)
    page = urllib.request.urlopen(req)
    soup = BeautifulSoup(page, "html.parser")

    table = soup.find('table', {'class': 'wikitable sortable'})
    sector_tickers = dict()
    for row in table.findAll('tr'):
        col = row.findAll('td')
        if len(col) > 0:
            sector = str(col[3].string.strip()).lower().replace(' ', '_')
            ticker = str(col[0].string.strip())
            if sector not in sector_tickers:
                sector_tickers[sector] = list()
            sector_tickers[sector].append(ticker)
    return sector_tickers

def get_snp500_by_sector():
    sector_tickers = scrape_list("http://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    return sector_tickers

def get_snp500():
    by_sec = get_snp500_by_sector()
    all = []
    for key in by_sec:
        all += by_sec[key]
    return all

