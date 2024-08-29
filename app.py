import requests
from bs4 import BeautifulSoup
import csv

# Amazon URL
url = "https://www.amazon.in/s?k=deals"

# Set the headers to mimic a browser visit
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
}

# Open a CSV file to store the data
with open("amazon_products.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Product Title", "Price", "ASIN"])

    for page in range(1, 6):  # Scrape the first 5 pages
        # Send a GET request to fetch the page content
        response = requests.get(f"{url}&page={page}", headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all product containers
        products = soup.find_all("div", {"data-component-type": "s-search-result"})

        for product in products:
            try:
                # Extract the product title
                title = product.h2.text.strip()

                # Extract the current price
                current_price = product.find("span", {"class": "a-price-whole"})
                if current_price:
                    current_price = current_price.text.replace(',', '').strip()
                else:
                    continue  # Skip the product if no price is found

                # Extract the product URL and ASIN
                product_url = "https://www.amazon.in" + product.h2.a["href"]
                asin = product_url.split('/dp/')[1].split('/')[0]

                # Write the product details to the CSV file
                writer.writerow([title, current_price, asin])

                # Print the product details (optional)
                print(f"Product: {title}")
                print(f"Price: ₹{current_price}")
                print(f"ASIN: {asin}\n")

            except Exception as e:
                # Handle any errors during extraction
                print(f"Error processing product: {e}")

print("Data collection complete. Check 'amazon_products.csv' for the results.")
