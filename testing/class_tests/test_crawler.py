import pandas as pd
import sys
sys.path.insert(0, "src/scrapers")
from searchpage import Crawl
import os

def test_pagination_code():
    c = Crawl('https://www.builtinchicago.org/companies?status=all')
    c.get_pagination_code()
    assert c.current_max_page_value == 9

def test_company_page_crawl():
    os.system('rm scraped_data/*.csv')
    c = Crawl('https://www.builtinchicago.org/companies?status=all')
    c.scrape_company_page('https://www.builtinchicago.org/company/marketing-store')
    df = pd.read_csv('scraped_data/company_info.csv')
    assert len(df) == 1

def test_scrape_results_page():
    pass

