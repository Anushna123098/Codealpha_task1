#CODEALPHA TAS
#scraping one page example
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Step 1: Target URL
url = "https://books.toscrape.com/catalogue/page-1.html"

# Step 2: Fetch the page content
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Step 3: Locate all book blocks
books = soup.find_all('article', class_='product_pod')

# Step 4: Extract data
titles, prices, ratings = [], [], []

for book in books:
    title = book.h3.a['title']
    price = book.find('p', class_='price_color').text
    rating = book.p['class'][1]  # The second class contains rating

    titles.append(title)
    prices.append(price)
    ratings.append(rating)

# Step 5: Create DataFrame
df = pd.DataFrame({
    'Title': titles,
    'Price': prices,
    'Rating': ratings
})

# Step 6: Save to CSV
df.to_csv('books_scraped.csv', index=False)

# Step 7: Show some results
print("✅ Data scraped and saved to CSV.")
print(df.head())

#analysis code
# Clean and convert price
df['Price'] = df['Price'].str.replace('£', '').astype(float)
# Summary stats
print("\n📊 Average Book Price:", df['Price'].mean())
print("\n📚 Book Count by Rating:")
print(df['Rating'].value_counts())
