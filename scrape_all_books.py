import requests
from bs4 import BeautifulSoup
import pandas as pd

# Empty lists to hold data
all_titles = []
all_prices = []
all_ratings = []

# Loop through all 50 pages
for page in range(1, 51):
    print(f"Scraping Page {page}...")

    # Dynamic URL
    url = f"https://books.toscrape.com/catalogue/page-{page}.html"

    # Send request
    response = requests.get(url)

    # Parse with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all book containers
    books = soup.find_all('article', class_='product_pod')

    # Loop through each book
    for book in books:
        title = book.h3.a['title']
        price = book.find('p', class_='price_color').text
        rating = book.p['class'][1]  # 'One', 'Two', etc.

        all_titles.append(title)
        all_prices.append(price)
        all_ratings.append(rating)

# Clean price: remove £ and convert to float
all_prices = [float(p[1:]) for p in all_prices]

# Create DataFrame
df = pd.DataFrame({
    'Title': all_titles,
    'Price': all_prices,
    'Rating': all_ratings
})

# Save to CSV
df.to_csv('all_books.csv', index=False)

# Summary
print("\n✅ Scraped data from all 50 pages.")
print(f"Total books scraped: {len(df)}")
print("\n📊 Average Price:", df['Price'].mean())
print("\n📚 Book Count by Rating:")
print(df['Rating'].value_counts())
