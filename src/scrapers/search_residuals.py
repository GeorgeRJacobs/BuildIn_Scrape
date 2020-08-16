import requests
from bs4 import BeautifulSoup
import urllib
import re
import json
import time
import pandas as pd
import os
from csv import DictReader


class CrawlResiduals:
    def __init__(self):
        self.save_found = 'scraped_data/round_2_found.csv'
        self.files_to_scrape = 'round_1_data_not_found.csv'

    def return_found_data(self, data):
        name = ['?']
        num_employee = ['?']
        url = ['?']
        physical_address = ['?']
        city = ['?']
        state = ['?']
        zip = ['?']
        try:
            name = [data[0].get('name', '')]
        except:
            pass
        try:
            num_employee = [data[0].get('numberOfEmployees', '').get('name', '')]
        except:
            pass
        try:
            url = [data[0]['url']]
        except:
            pass

        try:
            physical_address = [data[0]['address']["streetAddress"]]
        except:
            pass

        try:
            city = [data[0]['address']["addressLocality"]]
        except:
            pass

        try:
            state = [data[0]['address']['addressRegion']]
        except:
            pass

        try:
            zip = [data[0]['address']['postalCode']]
        except:
            pass

        t = {
            'Company': name,
            'Number of Employees': num_employee,
            'Company URL': url,
            "Physical Address": physical_address,
            'City': city,
            'State': state,
            'ZIP': zip
        }

        return t

    def scrape_company_page(self, organization):
        """
        Takes in the company url page and scrapes the data we need from it.
        :param organization:
        :return:
        """
        try:
            company = requests.get(organization, timeout=5)
        except:
            return
        if company.status_code >= 400:
            return
        url = company.url
        company = BeautifulSoup(company.text, 'html.parser')
        # Find All script sections containing JSON
        company_data = company.find_all('script')
        # Find specific JSON we want
        data_we_want = None
        for val in company_data:
            # data_we_want = None
            if val.string is None:
                continue
            if '@context' in val.string and '@graph' in val.string:
                data_we_want = val.string
        if data_we_want is None:
            return
        # Create Dictionary Value
        print(f'Working: {url}')
        print(data_we_want)
        data = json.loads(data_we_want)
        data = data['@graph']
        data = self.return_found_data(data)
        # Write File to CSV
        # if file does not exist write header
        dta = pd.DataFrame(data)
        if not os.path.isfile(self.save_found):
            dta.to_csv(self.save_found, index=False)
        else:  # else it exists so append without writing the header
            dta.to_csv(self.save_found, mode='a', header=False, index=False)

    def crawl(self):
        """
        Crawl the remainder URLs
        :return:
        """
        # Read the files
        with open('round_1_data_not_found.csv', 'r') as read_obj:
            # pass the file object to DictReader() to get the DictReader object
            csv_dict_reader = DictReader(read_obj)
            # iterate over each line as a ordered dictionary
            for row in csv_dict_reader:
                # row variable is a dictionary that represents a row in csv
                self.scrape_company_page(row['url'])





if __name__ == "__main__":
    # os.system('rm scraped_data_round_1/*.csv')

    c = CrawlResiduals()
    c.crawl()

    # c.scrape_company_page('https://www.builtinchicago.org/company/marketing-store')
    # df = pd.read_csv('scraped_data_round_1/company_info.csv')
    # assert len(df) == 1
    # search = requests.get('https://www.builtinchicago.org/companies?status=all&page=14')
    # # Parse
    # search = BeautifulSoup(search, 'html.parser')
    # # Set max page
    # search.find_all('li', class_='pager__item')
