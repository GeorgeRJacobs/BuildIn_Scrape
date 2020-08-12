import requests
from bs4 import BeautifulSoup
import urllib
import re
import json
import time
import pandas as pd
import os


class Crawl:
    def __init__(self, search_start_url):
        self.save_missed = 'scraped_data/data_not_found.csv'
        self.save_found = 'scraped_data/company_info.csv'
        self.search_start_url = search_start_url
        self.resource_name = None
        self.current_max_page_value = 0
        self.current_page = 0
        self.base_url = urllib.parse.urlparse(search_start_url)

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
        print(f'Max Page value: {self.current_max_page_value}')

    def scrape_results_page(self):
        """
        After setting the pagination value, we need to actually grab the relevant company data. So that means grabbing
        The Hrefs.
        """
        if self.current_page == 0:
            page = requests.get('https://www.builtinchicago.org/companies?status=all')
            soup = BeautifulSoup(page.content, 'html.parser')
            job_hrefs = soup.find_all("div", {"class": "open-jobs"})
            job_links = []
            for job in job_hrefs:
                job_links.append(self.base_url.netloc + job.find('a')['href'])
            job_links = [x.replace('/jobs', '') for x in job_links]

            # Run Data Fetch
            for org in job_links:
                # To be nice
                time.sleep(2)
                if 'https://' not in org:
                    org = 'https://' + org
                if '/built' not in org:
                    self.scrape_company_page(org)

        else:
            pass

    def scrape_company_page(self, organization):
        """
        Takes in the company url page and scrapes the data we need from it.
        :param organization:
        :return:
        """
        company = requests.get(organization)
        url = company.url
        company = BeautifulSoup(company.text, 'html.parser')
        # Find All script sections containing JSON
        company_data = company.find_all('script')
        # Find specific JSON we want
        for val in company_data:
            data_we_want = None
            if val.string is None:
                continue
            if 'context' in val.string:
                data_we_want = val.string
        # Create Dictionary Value
        # try:
        print(f'Working: {url}')
        print(val.string)
        data = json.loads(data_we_want)
        data = data['@graph']
        data = {
            'Company': [data[0]['name']],
            'Number of Employees': [data[0]['numberOfEmployees']['name']],
            'Company URL': [data[0]['url']],
            'BuiltIn URL': url,
            "Physical Address": [data[0]['address']["streetAddress"]],
            'City': [data[0]['address']["addressLocality"]],
            'State': [data[0]['address']['addressRegion']],
            'ZIP': [data[0]['address']['postalCode']]
        }
        # Write File to CSV
        # if file does not exist write header
        dta = pd.DataFrame(data)
        if not os.path.isfile(self.save_found):
            dta.to_csv(self.save_found, index=False)
        else:  # else it exists so append without writing the header
            dta.to_csv(self.save_found, mode='a', header=False, index=False)
        # except:
        #     if not os.path.isfile(self.save_missed):
        #         pd.DataFrame({'url': [url]}).to_csv(self.save_missed, index=False)
        #     else:  # else it exists so append without writing the header
        #         pd.DataFrame({'url': [url]}).to_csv(self.save_missed, mode='a', header=False,
        #                                             index=False)


if __name__ == "__main__":
    os.system('rm scraped_data/*.csv')
    c = Crawl('https://www.builtinchicago.org/companies?status=all')
    c.scrape_results_page()
    # c.scrape_company_page('https://www.builtinchicago.org/company/marketing-store')
    # df = pd.read_csv('scraped_data/company_info.csv')
    # assert len(df) == 1
    # search = requests.get('https://www.builtinchicago.org/companies?status=all&page=14')
    # # Parse
    # search = BeautifulSoup(search, 'html.parser')
    # # Set max page
    # search.find_all('li', class_='pager__item')
