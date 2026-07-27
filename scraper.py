import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, urljoin

BASE_URL = "https://mdcomputers.in/"


def search_products(search_term):
    url = f"{BASE_URL}?route=product/search&search={quote(search_term)}"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 Chrome/137.0 Safari/537.36"
        )
    }

    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    products = []

    for card in soup.select(".product-layout"):
        name_tag = card.select_one(".caption h4 a")
        price_tag = card.select_one(".price")
        image_tag = card.select_one("img")

        products.append({
            "name": name_tag.get_text(strip=True) if name_tag else "",
            "price": price_tag.get_text(" ", strip=True) if price_tag else "",
            "url": urljoin(BASE_URL, name_tag["href"]) if name_tag else "",
            "image": urljoin(BASE_URL, image_tag["src"]) if image_tag else "",
            "availability": "Out of Stock" if "out of stock" in card.get_text(" ", strip=True).lower() else "Available"
        })

    return products


if __name__ == "__main__":
    search_term = input("Enter search term: ")
    products = search_products(search_term)

    print(f"\nFound {len(products)} products:\n")

    for i, p in enumerate(products, 1):
        print(f"{i}. {p['name']}")
        print(f"   Price: {p['price']}")
        print(f"   Availability: {p['availability']}")
        print(f"   URL: {p['url']}")
        print(f"   Image: {p['image']}")
        print()
