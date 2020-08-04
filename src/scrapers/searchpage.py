import requests
from bs4 import BeautifulSoup
import urllib
import re


class SearchPage:
    def __init__(self, search_start_url):
        self.search_start_url = search_start_url
        self.resource_name = None
        self.current_max_page_value = None

    def get_pagination_code(self):
        """
        Grabs page code so we know how many pages we will need to request URLs for.
        The pagination code updates to always show 10 pages at once.
        :return: None
        """
        search = requests.get(self.search_start_url)
        # Parse
        search = BeautifulSoup(search.content, 'html.parser')
        # Set max page
        search = search.find_all('li', class_='pager__item')
        max_val = 0
        for page_number in search:
            num = re.findall('\d+', page_number.text.strip())
            if len(num) > 0:
                if int(num[0]) > max_val:
                    max_val = int(num[0])
        self.current_max_page_value = max_val
        print(f'Max Page value: {self.current_max_value_page}')



if __name__=="__main__":
    page = SearchPage('https://www.builtinchicago.org/companies?status=all')
    page.get_pagination_code()
    # search = requests.get('https://www.builtinchicago.org/companies?status=all&page=14')
    # # Parse
    # search = BeautifulSoup(search, 'html.parser')
    # # Set max page
    # search.find_all('li', class_='pager__item')