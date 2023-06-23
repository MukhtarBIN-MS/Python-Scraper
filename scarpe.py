import requests
from bs4 import BeautifulSoup

websites = [
    "www.johnscarpentry.com",
    "www.dallascarpentryservices.com",
]

for website in websites:
    url = "https://" + website  # Prepend "https://" to the website URL

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the business name from the URL
        business_name = website.replace("www.", "").replace(".com", "")

        # Extract the phone number if available
        phone_element = soup.find('a', href=lambda href: href and 'tel:' in href)
        phone_number = phone_element.get('href').replace('tel:', '') if phone_element else "N/A"

        # Extract the email if available
        email_element = soup.select_one('a[href^=mailto]')
        email = email_element.get('href').replace('mailto:', '') if email_element else "N/A"

        print("Website: ", website)
        print("Business Name: ", business_name)
        print("Phone Number: ", phone_number)
        print("Email: ", email)
        print("")

    except requests.exceptions.RequestException as e:
        print("An error occurred while scraping", website)
        print(e)
        print("")
