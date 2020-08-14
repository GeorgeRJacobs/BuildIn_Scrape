from src.scrapers.searchpage import Crawl

# Run crawl on Built In Chicago
c = Crawl('https://www.builtinchicago.org/companies?status=all', 301)
c.current_page = 0
c.crawl()
