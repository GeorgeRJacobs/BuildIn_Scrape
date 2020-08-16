import requests
from bs4 import BeautifulSoup
import urllib
import json
import pandas as pd
import functools
import os
from csv import DictReader

# Let's request the first page
page1 = requests.get('https://www.builtinchicago.org/companies?status=all')
page29 = requests.get('https://www.builtinchicago.org/companies?status=all&page=29')
urllib.parse.urlparse(page1.url)
# Page 1
soup = BeautifulSoup(page1.content, 'html.parser')

# We need to find:
# class = 'open-jobs'
job_hrefs = soup.find_all("div", {"class": "wrap-view-page"})
job_links = []
base_url = urllib.parse.urlparse(page1.url)
base_url.netloc
for job in job_hrefs:
    job_links.append(base_url.netloc + job.find('a')['href'])
job_links = [x.replace('/jobs', '') for x in job_links]
#


## Playing w/ page source
company = requests.get('https://www.builtinchicago.org/company/marketing-store')
url = company.url
company = BeautifulSoup(company.text, 'html.parser')
company_data = company.find_all('script')
for val in company_data:
    if val.string is None:
        continue
    if 'context' in val.string:
        data_we_want = val.string
        print(val.string)

data = json.loads(data_we_want)
data = data['@graph']


# Rewrite this a bit
def return_found_data(data):
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

t = {
    'Company': [data[0].get('name', '')],
    'Number of Employees': [data[0]],
    'Company URL': [data[0]['url']],
    "Physical Address": [data[0]['address']["streetAddress"]],
    'City': [data[0]['address']["addressLocality"]],
    'State': [data[0]['address']['addressRegion']],
    'ZIP': [data[0]['address']['postalCode']]
}

# Concatenating
files = os.listdir("scraped_data/")
files = [x for x in files if 'not' in x]
csvs = []
for f in files:
    fl = pd.read_csv('scraped_data/' + f)
    csvs.append(fl)

final_dta = pd.concat(csvs)
final_dta.to_csv('round_1_data_not_found.csv')

# Read the files
with open('round_1_data_not_found.csv', 'r') as read_obj:
    # pass the file object to DictReader() to get the DictReader object
    csv_dict_reader = DictReader(read_obj)
    # iterate over each line as a ordered dictionary
    for row in csv_dict_reader:
        # row variable is a dictionary that represents a row in csv
        print(row)

