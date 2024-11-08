from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import time
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Cache simple en memoria
cache = {}

def fetch_url(url):
    """Fetch URL with caching."""
    if url in cache:
        return cache[url]
    try:
        result = requests.get(url, timeout=10)  # Timeout added for safety
        cache[url] = result
        return result
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def load_urls():
    """Load URLs from a JSON file."""
    with open('urls.json') as f:
        return json.load(f)

urls = load_urls()

def scrape_product_info(query, store_name):
    """Scrape product information from the specified store."""
    products = []
    store_urls = urls.get(store_name.lower(), [])

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(fetch_url, url): url for url in store_urls}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                result = future.result()
                if result is None:
                    continue

                soup = BeautifulSoup(result.text, 'html.parser')
                # Customize selectors based on the store
                if store_name.lower() == "carrefour":
                    name_tag = soup.find('span', class_='vtex-store-components-3-x-productBrand')
                    price_tag = soup.find('span', class_='valtech-carrefourar-product-price-0-x-currencyContainer')
                    image_tag = soup.find('img', class_='vtex-store-components-3-x-productImageTag')
                elif store_name.lower() == "dia":
                    name_tag = soup.find('span', class_='vtex-store-components-3-x-productBrand')
                    price_tag = soup.find('span', class_='vtex-product-price-1-x-sellingPriceValue')
                    image_tag = soup.find('img', class_='vtex-store-components-3-x-productImageTag')

                if name_tag and price_tag and image_tag:
                    name = name_tag.get_text(strip=True).lower()
                    price = price_tag.get_text(strip=True).replace('$', '').replace('.', '').replace(',', '.')
                    image_url = image_tag['src']

                    if query in name:
                        try:
                            price = float(price)
                        except ValueError:
                            price = 0.0
                        products.append({
                            "name": name,
                            "price": price,
                            "store": store_name.capitalize(),
                            "url": url,
                            "image": image_url
                        })
            except Exception as e:
                print(f"Error scraping {store_name} URL {url}: {e}")
    return products

@app.route('/search')
def search():
    """Search for products based on a query."""
    query = request.args.get('query', '').lower()
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    try:
        start_time = time.time()
        carrefour_products = scrape_product_info(query, "carrefour")
        dia_products = scrape_product_info(query, "dia")
        all_products = carrefour_products + dia_products
        all_products.sort(key=lambda x: x['price'])

        # Debugging output
        print(f"Total search time: {time.time() - start_time} seconds")

        return jsonify(all_products)
    except Exception as e:
        print(f"Error in search endpoint: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
