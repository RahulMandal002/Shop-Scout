from bs4 import BeautifulSoup
import re
import requests
import time


import time
import requests
from bs4 import BeautifulSoup

def amazonparser(url):
    # Delay to avoid overwhelming the server
    time.sleep(2)

    # Headers to mimic a real browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }

    # Send a GET request to the URL
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch the page. Status code: {response.status_code}")
        return None

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Initialize output list
    output = []

    # Extract Brand
    brand = soup.find('span', {'class': 'a-size-base po-break-word'})
    output.append(brand.text.strip() if brand else 'N/A')

    # Extract Product Name
    name = None
    try:
        name = soup.find('span', {'id': 'productTitle'})
        if name:
            name = name.text.strip()
    except:
        pass
    if not name:
        try:
            name = soup.find('img', {'id': 'landingImage'}).get('alt', '').strip()
        except:
            pass
    output.append(name if name else 'N/A')

    # Extract Price
    price = None
    try:
        price = soup.find('span', {'class': 'a-price-whole'})
        if price:
            price = price.text.strip()
    except:
        pass
    if not price:
        try:
            price = soup.find('span', {'id': 'priceblock_ourprice'}).text.strip()
        except:
            pass
    output.append(price if price else 'N/A')

    # Extract Rating
    rating = None
    try:
        rating = soup.find('span', {'class': 'a-icon-alt'})
        if rating:
            rating = rating.text.strip()
    except:
        pass
    output.append(rating if rating else 'N/A')

    # Extract Photo URL
    photo = None
    try:
        photo = soup.find('img', {'id': 'landingImage'}).get('src', '').strip()
    except:
        pass
    if not photo:
        try:
            photo = soup.find('img', {'id': 'landingImage'}).get('data-a-dynamic-image', '').split('"')[1]
        except:
            pass
    output.append(photo if photo else "images/NA.jpg")

    # Add the product URL
    output.append(url)

    return output





import time

def get_with_retry(url, headers, retries=3, delay=2):
    for _ in range(retries):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response
        time.sleep(delay)
    return None
import re
import requests
from urllib.parse import quote

def getproductid(query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://www.amazon.in/',
    }

    encoded_query = quote(query.lower())
    url = f"https://www.amazon.in/s?k={encoded_query}"
    print("Searching your product at...", url, sep=" ")

    response = get_with_retry(url, headers)
    if not response:
        print("Failed to fetch the search page after multiple retries.")
        return []
    htmltext = response.text
    pattern = re.compile(r"/[a-zA-Z0-9-]+/dp/[a-zA-Z0-9]{10}")  # Amazon product ID pattern
    List = re.findall(pattern, htmltext)
    List = list(set(List))  # Remove duplicates
    return List


def FetchfromAmazon(query):
    Id = getproductid(query)
    if not Id:
        print("No product IDs found.")
        return []

    extracted_data = []
    ctr = 0
    for i in Id:
        ctr += 1
        url = "http://www.amazon.in" + i
        print("Processing: " + url)
        extracted_data.append(amazonparser(url))
        if ctr == 5:  # Limit to 5 products
            break
        time.sleep(1)  # Add delay to avoid rate limiting
    return extracted_data





