from bs4 import BeautifulSoup
import re
import requests
import time
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://www.flipkart.com/',
    }


def flipkartparser(url):
    time.sleep(2)
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    # }

    response = requests.get(url, headers=headers)

    # Debugging: Print response HTML
    print("Fetching URL:", url)

    soup = BeautifulSoup(response.text, 'html.parser')

    brand = soup.find('span', {'class': "mEh187"})
    name = soup.find('span', {'class': "VU-ZEz"})
    price = soup.find('div', {'class': "Nx9bqj CxhGGd"})
    rating = soup.find('div', {'class': "XQDdHH _1Quie7"})
    if not rating:
        rating = soup.find('div', {'class': "XQDdHH"})
    if not rating:
        rating = soup.find('div', {'class': "XQDdHH _6er70b"})

    # Debugging: Print extracted values
    print("Brand:", brand)
    print("Name:", name)
    print("Price:", price)
    print("Rating:", rating)
    # try:
    #     photo = soup.findall('div', {'class': "_0DkuPH"}).get('style')[21:-1]        #j9BzIm
    # except:
    #     photo = None

    photo_tag = soup.find('img', {'class': "_0DkuPH"})  # j9BzIm
    photo = photo_tag['src'] if photo_tag else "images/NA.jpg"
    print("photo:", photo)

    link = url
    output = [
        brand.text if brand else 'N/A',
        name.text if name else 'N/A',
        price.text if price else 'N/A',
        rating.text if rating else 'N/A',
        photo if photo else "images/NA.jpg",
        link
    ]

    return output

import time

def get_with_retry(url, headers, retries=3, delay=2):
    for _ in range(retries):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response
        time.sleep(delay)
    return None

from urllib.parse import quote
def getproductid(query):
    encoded_query = quote(query.lower())
    url = f"https://www.flipkart.com/search?q={encoded_query}"
    print("Searching your product at...", url, sep=" ")

    response = get_with_retry(url, headers)
    if not response:
        print("Failed to fetch the search page after multiple retries.")
        return []
    htmltext = response.text
    time.sleep(2)
    pattern = re.compile(r"/[/ 0-9 a-z -]+/p/[0-9a-z]{16,16}")  # flipkart product id
    List = re.findall(pattern, htmltext)

    List = list(set(List))

    return List


def Fetchfromflipkart(query):
    Id = getproductid(query)
    extracted_data = []
    ctr = 0
    for i in Id:
        ctr += 1

        url = "https://www.flipkart.com" + i
        print("Processing: " + url)
        extracted_data.append(flipkartparser(url))
        time.sleep(1)
        if (ctr == 5):
            break

    return extracted_data





# headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
#         'Accept-Language': 'en-US,en;q=0.9',
#         'Accept-Encoding': 'gzip, deflate, br',
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
#         'Referer': 'https://www.flipkart.com/',
#     }
#
# def flipkartparser(url):
#     """
#     Parses a Flipkart product page and extracts product details.
#     """
#     time.sleep(2)  # Delay to avoid overwhelming the server
#
#     response = requests.get(url, headers=headers)
#     if response.status_code != 200:
#         print(f"Failed to fetch the page. Status code: {response.status_code}")
#         return None
#
#     soup = BeautifulSoup(response.text, 'html.parser')
#     output = []
#
#     # Extract Brand
#     brand = soup.find('span', {'class': 'B_NuCI'})  # Primary class for brand
#     if not brand:
#         brand = soup.find('span', {'class': '_2J4LW6'})  # Fallback class for brand
#     output.append(brand.text.strip() if brand else 'N/A')
#
#     # Extract Product Name
#     name = soup.find('span', {'class': 'B_NuCI'})  # Primary class for name
#     if not name:
#         name = soup.find('h1', {'class': 'yhB1nd'})  # Fallback class for name
#     output.append(name.text.strip() if name else 'N/A')
#
#     # Extract Price
#     price = soup.find('div', {'class': '_30jeq3 _16Jk6d'})  # Primary class for price
#     if not price:
#         price = soup.find('div', {'class': '_1vC4OE _3qQ9m1'})  # Fallback class for price
#     output.append(price.text.strip() if price else 'N/A')
#
#     # Extract Rating
#     rating = soup.find('div', {'class': '_3LWZlK'})  # Primary class for rating
#     if not rating:
#         rating = soup.find('span', {'class': '_2_R_DZ'})  # Fallback class for rating
#     output.append(rating.text.strip() if rating else 'N/A')
#
#     # Extract Photo URL
#     photo = None
#     try:
#         photo = soup.find('img', {'class': '_396cs4 _2amPTt _3qGmMb'}).get('src')  # Primary class for photo
#     except:
#         pass
#     if not photo:
#         try:
#             photo = soup.find('img', {'class': '_2r_T1I _396QI4'}).get('src')  # Fallback class for photo
#         except:
#             pass
#     output.append(photo if photo else "images/NA.jpg")
#
#     # Add the product URL
#     output.append(url)
#
#     return output