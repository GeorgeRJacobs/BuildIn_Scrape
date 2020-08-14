# Copy entire Directory to EC2
# scp -i ".ssh/aws_key_pair.pem" -r /Users/georgejacobs/PycharmProjects/BuiltIn_Scrape ubuntu@ec2-13-59-72-191.us-east-2.compute.amazonaws.com:/home/ubuntu/
from src.scrapers.searchpage import Crawl
# Run crawl on Built In Chicago
list = [
    'https://www.builtinaustin.com/companies?status=all',
    'https://www.builtinnyc.com/companies?status=all',
    'https://www.builtinsf.com/companies?status=all',
    'https://www.builtinla.com/companies?status=all',
    'https://www.builtinseattle.com/companies?status=all',
    'https://www.builtinboston.com/companies?status=all',
    'https://www.builtincolorado.com/companies?status=all'
]
for area in list:
    c = Crawl(area, 300)
    c.current_page = 0
    c.scrape_results_page()
