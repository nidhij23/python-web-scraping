import time
import csv
from urllib.parse import urljoin

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException


# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode

# Set up Chrome driver service
service = Service(ChromeDriverManager().install())

# Set up the Chrome driver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the URL
root_url = "https://signal.nfx.com"
url = urljoin(root_url, "/investor-lists/top-gaming-esports-seed-investors")
driver.get(url)

# Wait for the page to load
driver.implicitly_wait(10)

# Function to scroll and capture investors
def scroll_and_capture_investors():
    # Scroll through the page by clicking the "LOAD MORE INVESTORS" button
    count=0
    while True:
        count+=1
        try:
            print("loading more",count)
            load_more_button = driver.find_element(By.XPATH, '//button[text()="LOAD MORE INVESTORS"]')
            driver.execute_script("arguments[0].scrollIntoView();", load_more_button)
            load_more_button.click()
            time.sleep(2)  # Wait for the content to load
            
        except NoSuchElementException:
            break
        

# Scroll and capture investors
scroll_and_capture_investors()

# Get the page source
page_source = driver.page_source

# Close the driver
driver.quit()

# Create a BeautifulSoup object
soup = BeautifulSoup(page_source, 'html.parser')

# Find the container div with class "vc-search-card-grid"
container_div = soup.find('div', class_='vc-search-card-grid')

# Find all div tags with class "vc-search-card mb2" within the container div
investor_divs = container_div.find_all('div', class_='vc-search-card mb2')

# List to store the scraped data
investors = []

# Iterate over each investor div
for div in investor_divs:
    # Extract the name and URL from the <a> tag
    name_elem = div.find('a', class_='vc-search-card-name')
    name = name_elem.text.strip()
    url = urljoin(root_url, name_elem['href'])

    # Extract the company and company URL from the nested <a> tag
    company_elem = name_elem.find_next('a')
    company = company_elem.text.strip()
    company_url = urljoin(root_url, company_elem['href'])

    # Find the parent div with class "pr3"
    range_divs = div.find_all('div', class_=['pr3'])

    # Extract the sweet spot and range from the <span> tags
    sweet_spot = range_divs[0].find('span', class_='vc-search-card-value').text.strip()
    range_value = range_divs[0].find_all('span', class_='vc-search-card-value')[1].text.strip()

    # Create a dictionary object with the investor details
    investor = {
        'name': name,
        'URL': url,
        'company': company,
        'company_url': company_url,
        'sweet_spot': sweet_spot,
        'range': range_value,
    }

    # Add the investor to the list
    investors.append(investor)

# Print the scraped data
for investor in investors:
    print("Name:", investor['name'])
    print("URL:", investor['URL'])
    print("Company:", investor['company'])
    print("Company URL:", investor['company_url'])
    print("Sweet Spot:", investor['sweet_spot'])
    print("Range:", investor['range'])
    print()

print(len(investors))
filename = 'investors.csv'
fieldnames = ['name', 'URL', 'company', 'company_url', 'sweet_spot', 'range']

with open(filename, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(investors)

print("Data has been scraped and saved to", filename)
