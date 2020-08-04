import requests

# Let's request the first page
page1 = requests.get('https://www.builtinchicago.org/companies?status=all')
page1
page1.text