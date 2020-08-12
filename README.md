## BuiltIn

### Game Plan
1. Start with this address: https://www.builtinchicago.org/companies?status=all
    + First, I noticed they have a pagination bar at the bottom. Hopefully, that means we can 
      page thru the datasource quite easily.  Just append the right number to the web page url and 
      away we go. 
    + Second, we will need to gather the links from the search results, store them, them step into them 
      to grab the data we need. 
    + Third, we may need to step into those websites to gather the right contact information. 
2. 

### Details: 
1. There are 3 things we need to manage.
    + The Search Page
        + Scrape the URL from the Search Page. 
    + The Company Page
        + Scrape: 
            + Company Name
            + Size 
            + Company Website
            + Location Data
    + Company Site Data
       + Potentially, we can grab the contact information from this website. 
2. We will need to develop 2 schemes to scrape the data we want. It appears for a subset of the companies
   there is not a context available. Instead, we will need to scrape the data from the JS in the page. 