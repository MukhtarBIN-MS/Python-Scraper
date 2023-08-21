from googlesearch import search
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from urllib.parse import urlparse


# Function to search for websites using Google search with location-based query
def search_websites(query, web_location, num_results):
    query = query + " " + web_location
    websites = []
    for url in search(query, num_results=num_results):
        websites.append(url)
    return websites


# Function to scrape business information from a website


def scrape_business_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract business name (website name)
    parsed_url = urlparse(url)
    website_name = parsed_url.netloc.replace("www.", "").split(".")[0]

    # Search for email and phone number patterns in the HTML
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    phone_pattern = r"\b(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})\b"

    email_matches = re.findall(email_pattern, str(soup))
    phone_matches = re.findall(phone_pattern, str(soup))

    # Extract up to two email addresses and two phone numbers
    email_list = list(set(email_matches[:2]))
    phone_list = ['-'.join([''.join(match) for match in phone_match]) for phone_match in phone_matches[:2]]

    # Search for phone numbers in <a href="tel:"> tags
    phone_elements = soup.find_all('a', href=lambda href: href and href.startswith('tel:'))

    # logo ingo
    log_list = []
    logo_info = soup.find_all('img', source=lambda source: source and source.startswith('img'))
    for lg in logo_info:
        logo = lg.get('source').replace('source:', '')
        if len(logo_info) < 2:
            log_list.append(logo_info)
        else:
            break
                   
    for element in phone_elements:
        phone_number = element.get('href').replace('tel:', '')
        if len(phone_list) < 2:
            phone_list.append(phone_number)
        else:
            break

    # Check if any email or phone number is found
    if email_list or phone_list:
        n_email = ', '.join(email_list) if email_list else ""
        n_phone = ', '.join(phone_list) if phone_list else ""
        return website_name, n_email, n_phone
    else:
        return website_name, "No contact found", ""


# Search query for furniture businesses
search_query = "logistics business"

# Location-based search query
location = "Texas"

# Number of websites to search and scrape
num_websites = 100

# Search for websites using Google search with location-based query
websites = search_websites(search_query, location, num_websites)

# print(websites)

# Create lists to store the scraped data
business_names = []
emails = []
phones = []

# Scrape business information from each website
# Scrape business information from each website
for website in websites:
    try:
        business_name, email, phone = scrape_business_info(website)
        business_names.append(business_name)
        emails.append(email)
        phones.append(phone)
        # print("Scraped:", website)
    except Exception as e:
        print("Error scraping website:", website)
        print("Error message:", str(e))

    print("Business Name:", business_name, 'Email:', email, 'Phone:', phone)

print("Business Name:", business_names, 'Email:', emails, 'Phone:', phones)
Create a DataFrame from the scraped data
data = {
    'Business name': business_names,
    'Email': emails,
    'Phone': phones
}
df = pd.DataFrame(data)
print(df)


# Generate the filename based on the search query
filename = f"{search_query.replace(' ', '_')}_business_information.xlsx"

# Save the DataFrame to an Excel file with the search query included in the filename
df.to_excel(filename, index=False)
