import requests
from bs4 import BeautifulSoup
import urllib
import json
import pandas as pd


# Let's request the first page
page1 = requests.get('https://www.builtinchicago.org/companies?status=all')
urllib.parse.urlparse(page1.url)
# Page 1
soup = BeautifulSoup(page1.content, 'html.parser')

# We need to find:
# class = 'open-jobs'
job_hrefs = soup.find_all("div", {"class": "open-jobs"})
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
    if 'context' in val.string:
        data_we_want = val.string
        print(val.string)

data = json.loads(data_we_want)
data = data['@graph']
t = {
    'Company': [data[0]['name']],
    'Number of Employees': [data[0]['numberOfEmployees']['name']],
    'Company URL':  [data[0]['url']],
    "Physical Address": [data[0]['address']["streetAddress"]],
    'City': [data[0]['address']["addressLocality"]],
    'State': [data[0]['address']['addressRegion']],
    'ZIP': [data[0]['address']['postalCode']]
}

