import requests
from bs4 import BeautifulSoup


# Let's request the first page
page1 = requests.get('https://www.builtinchicago.org/companies?status=all')
page1
# Page 1
soup = BeautifulSoup(page1.content, 'html.parser')

# We need to find:
# class = 'open-jobs'
job_hrefs = soup.find_all("div", {"class": "open-jobs"})
for job in job_hrefs:
    print(job.find('a')['href'])
#