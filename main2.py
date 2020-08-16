# Copy entire Directory to EC2
# scp -i ".ssh/aws_key_pair.pem" -r /Users/georgejacobs/PycharmProjects/BuiltIn_Scrape ubuntu@ec2-13-59-72-191.us-east-2.compute.amazonaws.com:/home/ubuntu/

from src.scrapers.search_residuals import CrawlResiduals

# Crawl
c = CrawlResiduals()
c.crawl()

