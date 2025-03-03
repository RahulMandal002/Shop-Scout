import time
import requests
from bs4 import BeautifulSoup

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://www.snapdeal.com/',
    }

def snapdealparser(url):
    """
    Parses a Snapdeal product page and extracts product details.
    """
    time.sleep(2)  # Delay to avoid overwhelming the server

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch the page. Status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    output = []

    # Extract Brand
    brand = soup.find('a', {'class': 'product-brand'})
    output.append(brand.text.strip() if brand else 'N/A')

    # Extract Product Name
    name = soup.find('h1', {'class': 'pdp-e-i-head'})
    output.append(name.text.strip() if name else 'N/A')

    # Extract Price
    price = soup.find('span', {'class': 'payBlkBig'})
    if not price:
        price = soup.find('span', {'class': 'pdp-final-price'})  # Fallback for price
    output.append(price.text.strip() if price else 'N/A')

    # Extract Rating
    rating = soup.find('span', {'class': 'avrg-rating'})
    if not rating:
        rating = soup.find('span', {'class': 'pdp-e-i-ratings__rate'})  # Fallback for rating
    output.append(rating.text.strip() if rating else 'N/A')

    # Extract Photo URL
    photo = None
    try:
        photo = soup.find('img', {'class': 'cloudzoom'}).get('src')
    except:
        pass
    if not photo:
        try:
            photo = soup.find('img', {'class': 'pdpCloudZoom'}).get('src')
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
from urllib.parse import quote

def getproductid(query):
    encoded_query = quote(query.lower())
    url = f"https://www.snapdeal.com/search?keyword={encoded_query}"
    print("Searching your product at...", url, sep=" ")

    response = get_with_retry(url, headers)
    if not response:
        print("Failed to fetch the search page after multiple retries.")
        return []
    htmltext = response.text
    pattern = re.compile(r"/product/.*/\d{5,19}")  # Snapdeal product id
    List = re.findall(pattern, htmltext)
    List = list(set(List))  # Remove duplicates
    return List


def FetchfromSnapdeal(query):
    Id = getproductid(query)
    if not Id:
        print("No product IDs found.")
        return []

    extracted_data = []
    ctr = 0
    for i in Id:
        ctr += 1
        url = "http://www.snapdeal.com" + i
        print("Processing: " + url)
        extracted_data.append(snapdealparser(url))
        if ctr == 5:  # Limit to 5 products
            break
        time.sleep(1)  # Add delay to avoid rate limiting
    return extracted_data